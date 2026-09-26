#!/usr/bin/env python3
"""Run isolated kind suites, or select suites from a Git diff (stdlib only)."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "kubectl": ["04-kubectl/"],
    "pod": ["05-kubernetes-resources/01-pod/"],
    "namespace": ["05-kubernetes-resources/02-namespace/"],
    "replicaset": ["05-kubernetes-resources/03-replicaset/"],
    "deployment": ["05-kubernetes-resources/04-deployment/"],
    "configmap": ["05-kubernetes-resources/05-configmap/"],
    "secret": ["05-kubernetes-resources/06-secret/"],
    "service": ["05-kubernetes-resources/07-service/"],
    "debug": ["07-debug-kubernetes/"],
}


def select(paths):
    selected = set()
    for path in paths:
        if path == ".github/workflows/e2e.yml" or (
            path.startswith("e2e/") and not path.startswith("e2e/suites/")
        ):
            return list(TARGETS)
        for target, prefixes in TARGETS.items():
            if path == f"e2e/suites/{target}.sh" or any(
                path.startswith(prefix) for prefix in prefixes
            ):
                selected.add(target)
    return [target for target in TARGETS if target in selected]


def run(target):
    name = f"kb-e2e-{target}-{uuid.uuid4().hex[:8]}"
    artifacts = Path(os.environ.get("E2E_ARTIFACTS", ROOT / "e2e-artifacts")) / name
    artifacts.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="kb-e2e-") as temporary:
        env = os.environ.copy()
        # Never load or merge the user's kubeconfig, including during kind cleanup.
        env["KUBECONFIG"] = str(Path(temporary) / "config")
        env["E2E_CONTEXT"] = f"kind-{name}"
        env["E2E_ROOT"] = str(ROOT)
        env["E2E_ARTIFACTS"] = str(artifacts)
        print(f"Running {target}: {name}", flush=True)
        try:
            subprocess.run([
                "kind", "create", "cluster", "--name", name,
                "--kubeconfig", env["KUBECONFIG"], "--wait", "120s",
                "--image", env.get("KIND_NODE_IMAGE", "kindest/node:v1.33.1"),
            ], env=env, check=True, timeout=360)
            subprocess.run(["bash", str(ROOT / f"e2e/suites/{target}.sh")],
                           cwd=ROOT, env=env, check=True, timeout=900)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            subprocess.run(["kind", "export", "logs", "--name", name, str(artifacts)],
                           env=env, check=False, timeout=90)
            raise
        finally:
            subprocess.run(["kind", "delete", "cluster", "--name", name,
                            "--kubeconfig", env["KUBECONFIG"]],
                           env=env, check=True, timeout=120)
    print(f"PASS: {target}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="*", help="suite names (default: all)")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--select", metavar="BASE", help="print JSON suites changed since merge-base")
    args = parser.parse_args()
    if args.list:
        print("\n".join(TARGETS))
    elif args.select:
        paths = subprocess.check_output([
            "git", "diff", "--name-only", "--no-renames", "-z", f"{args.select}...HEAD",
        ], cwd=ROOT).decode().split("\0")
        print(json.dumps(select(paths)))
    else:
        for target in args.targets:
            if target not in TARGETS:
                parser.error(f"unknown suite: {target}")
        for target in args.targets or TARGETS:
            run(target)


if __name__ == "__main__":
    main()
