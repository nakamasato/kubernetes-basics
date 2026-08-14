#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["ruamel.yaml>=0.18"]
# ///
"""lab.yaml を正として README.md を生成し、実行列をクラスタ上で検証する。

    labs.py render <dir>...   lab.yaml から README.md を書き出す
    labs.py check  <dir>...   生成結果が README.md と一致するか確かめる
    labs.py run    <dir>...   実行列をクラスタで流す
    labs.py run --update ...  実測した出力を lab.yaml に書き戻す
"""

import argparse
import difflib
import os
import re
import subprocess
import sys
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

INDENT = "    "
TIMEOUT = 120

# 実行のたびに変わる値。比較の前に両側を潰さないと差分がノイズで埋まり、
# 本当に見たいバージョン差分が読めなくなる。保存する値は生のまま。
VOLATILE = [
    (re.compile(r"\bkube-api-access-[a-z0-9]{5}\b"), "kube-api-access-<RAND>"),
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"), "<UID>"),
    (re.compile(r"\b(?:docker|containerd|cri-o)://[0-9a-f]{64}"), "<CONTAINER_ID>"),
    (re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"), "<TIMESTAMP>"),
    # kubectl describe は ISO ではなく RFC 1123 で出す
    (
        re.compile(
            r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{1,2} \w{3} \d{4} \d{2}:\d{2}:\d{2} [+-]\d{4}"
        ),
        "<TIMESTAMP>",
    ),
    (re.compile(r"\b[0-9a-f]{1,4}(?::[0-9a-f]{0,4}){3,7}\b"), "<IP>"),
    (re.compile(r'(?<=resourceVersion: ")\d+'), "<RV>"),
    (re.compile(r"\b(?:10|172|192)\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "<IP>"),
    (re.compile(r"\b\d+[smhd](?:\d+[smhd])?\b"), "<AGE>"),
    (re.compile(r"^\d+(?:,\d+)?[acd]\d+(?:,\d+)?$", re.M), "<DIFF_RANGE>"),
    # 引けないイメージの Pod は2つの状態を行き来する。文字数が違うので
    # 揃えないと kubectl get の表の列幅が毎回ずれる
    (re.compile(r"\b(?:ErrImagePull|ImagePullBackOff)\b"), "<PULL_ERROR>"),
    # 行頭のインデントは意味を持つので残し、行中の桁揃えだけ潰す
    (re.compile(r"(?<=\S) {2,}"), " "),
]


def normalize(text, extra=()):
    for pattern, repl in list(extra) + VOLATILE:
        text = pattern.sub(repl, text)
    return "\n".join(line.rstrip() for line in text.strip().split("\n"))


def lab_masks(lab):
    """lab.yaml の mask:。汎用ルールでは判別できない、その演習だけの揮発値。"""
    return [(re.compile(m["pattern"]), m["as"]) for m in lab.get("mask") or []]


# --- render ---------------------------------------------------------------


def fence(body, lang="", indent=""):
    lines = [f"{indent}```{lang}"]
    for line in body.rstrip("\n").split("\n"):
        lines.append(f"{indent}{line}" if line else "")
    lines.append(f"{indent}```")
    return "\n".join(lines)


def indent_block(text, indent):
    return "\n".join(
        f"{indent}{line}" if line else "" for line in text.rstrip("\n").split("\n")
    )


def render_exec(ex):
    listed = ex.get("list", True)
    indent = INDENT * ex.get("level", 1) if listed else ""
    combined = ex.get("style") == "combined"
    lang = ex.get("lang", "")
    commands = ex.get("commands") or []
    parts = []

    if ex.get("desc"):
        outer = INDENT * (ex.get("level", 1) - 1) if listed else ""
        marker = ex.get("marker", "1.")
        parts.append(f"{outer}{marker} {ex['desc']}" if listed else ex["desc"])
    if ex.get("note"):
        parts.append(indent_block(ex["note"], indent))

    if commands and not combined:
        parts.append(fence("\n".join(c["run"] for c in commands), lang, indent))

    shown = [(c, c.get("output") or c.get("example")) for c in commands]
    shown = [(c, body) for c, body in shown if body]
    if shown:
        blocks = "\n\n".join(
            fence(f"{c['run']}\n{body.rstrip()}", lang, indent) for c, body in shown
        )
        if ex.get("details", not combined):
            parts.append(f"{indent}<details>\n\n{blocks}\n\n{indent}</details>")
        else:
            parts.append(blocks)

    return "\n\n".join(parts)


def render(lab):
    parts = []
    for block in lab["blocks"]:
        if "md" in block:
            parts.append(indent_block(block["md"], INDENT * block.get("level", 0)))
        else:
            parts.append(render_exec(block["exec"]))
    return "\n\n".join(parts) + "\n"


# --- run ------------------------------------------------------------------


def shell(cmd, cwd, env=None):
    try:
        proc = subprocess.run(
            ["bash", "-o", "pipefail", "-c", cmd],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            env={**os.environ, **(env or {})},
        )
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {TIMEOUT}s"
    merged = proc.stdout + proc.stderr
    # 表出力の行末空白を落とす。YAML のリテラルブロックが使えなくなるため
    body = "\n".join(line.rstrip() for line in merged.rstrip("\n").split("\n"))
    return proc.returncode, body


def code_ok(expect, code):
    if expect == "failure":
        return code != 0
    if expect == "any":
        return True
    return code == 0


def run_lab(path, lab, update):
    findings = []
    # 受講者が手で設定するシェル変数。コマンドごとにプロセスが分かれるので
    # export で引き継ぐ
    env = {k: str(v) for k, v in (lab.get("env") or {}).items()}
    masks = lab_masks(lab)
    for cmd in lab.get("setup", []):
        shell(cmd, path, env)
    try:
        for block in lab["blocks"]:
            ex = block.get("exec")
            if not ex:
                continue
            for command in ex.get("commands") or []:
                if command.get("skip"):
                    findings.append(
                        {
                            "run": command["run"],
                            "code": "-",
                            "status": "SKIP",
                            "actual": command["skip"],
                        }
                    )
                    continue
                # README には出さず、受講者が手でやっていること (起動を待つ、
                # マニフェストを書き換える) を自動実行側で埋める
                for prep in command.get("before") or []:
                    shell(prep, path, env)
                code, actual = shell(command["run"], path, env)
                expect = command.get("expect", "success")
                entry = {"run": command["run"], "code": code, "actual": actual}
                if not code_ok(expect, code):
                    entry["status"] = "FAIL"
                elif command.get("output") and normalize(command["output"], masks) != normalize(
                    actual, masks
                ):
                    entry["status"] = "DRIFT"
                    entry["diff"] = "".join(
                        difflib.unified_diff(
                            (normalize(command["output"], masks) + "\n").splitlines(True),
                            (normalize(actual, masks) + "\n").splitlines(True),
                            "expected",
                            "actual",
                            lineterm="\n",
                        )
                    )
                else:
                    entry["status"] = "OK"
                findings.append(entry)
                if update and command.get("output") is not None:
                    command["output"] = LiteralScalarString(actual + "\n" if actual else "")
    finally:
        for cmd in lab.get("teardown", []):
            shell(cmd, path, env)
    return findings


# --- cli ------------------------------------------------------------------


def yaml_io():
    io = YAML()
    io.preserve_quotes = True
    io.width = 10**6
    io.indent(mapping=2, sequence=4, offset=2)
    return io


# kubectl apply -f <dir> は非再帰なので、サブディレクトリに置けば
# 教材の演習で lab.yaml がマニフェストとして読まれることがない
def lab_path(path):
    return path / ".lab" / "lab.yaml"


def load(path):
    return yaml_io().load(lab_path(path))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["render", "check", "run"])
    parser.add_argument("dirs", nargs="+", type=Path)
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    failed = False
    for path in args.dirs:
        lab = load(path)
        readme = path / "README.md"

        if args.command == "render":
            readme.write_text(render(lab))
            print(f"wrote {readme}")

        elif args.command == "check":
            want = render(lab)
            have = readme.read_text() if readme.exists() else ""
            if want == have:
                print(f"ok   {readme}")
            else:
                failed = True
                print(f"diff {readme}")
                sys.stdout.writelines(
                    difflib.unified_diff(
                        have.splitlines(True), want.splitlines(True), "README.md", "lab.yaml"
                    )
                )

        elif args.command == "run":
            print(f"=== {path} ===")
            for entry in run_lab(path, lab, args.update):
                if entry["status"] in ("FAIL", "DRIFT"):
                    failed = True
                print(f"{entry['status']:5} ({entry['code']}) {entry['run']}")
                if entry["status"] == "SKIP":
                    print(f"{INDENT}{entry['actual']}")
                elif entry["status"] == "FAIL":
                    print(indent_block(entry["actual"], INDENT))
                elif entry["status"] == "DRIFT":
                    print(indent_block(entry["diff"], INDENT))
            if args.update:
                yaml_io().dump(lab, lab_path(path))
                print(f"updated {lab_path(path)}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
