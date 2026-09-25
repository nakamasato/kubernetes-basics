# Labs

Sections 04 to 07 are generated from a `.lab/lab.yaml` next to each `README.md`. That file holds
the prose, the commands and their recorded output, and it is the file to edit: the `README.md` is
written from it by [`scripts/labs.py`](../scripts/labs.py).

```
uv run scripts/labs.py render <dir>...   # lab.yaml -> README.md
uv run scripts/labs.py check  <dir>...   # is README.md up to date?
uv run scripts/labs.py run    <dir>...   # run the commands against the current context
uv run scripts/labs.py run --update ...  # replace the recorded output with what actually ran
```

## lab.yaml

| Key | Meaning |
| --- | --- |
| `blocks` | The README, top to bottom. Each is `md` (prose) or `exec` (commands) |
| `setup` / `teardown` | Commands run before and after the blocks by `run`. Not in the README |
| `env` | Shell variables the learner sets by hand, exported to every command |
| `mask` | Lab-specific values that change on every run (`pattern`, `as`) |

Each command in an `exec` block:

| Key | Meaning |
| --- | --- |
| `run` | The command |
| `output` | Recorded output. Rendered in the README and compared by `run` |
| `example` | Output rendered in the README but never compared, for output that depends on the host |
| `expect` | `success` (default), `failure` or `any` |
| `before` | Commands run first and kept out of the README, such as `kubectl wait` |
| `skip` | Do not run; the value says why |

## run

`run` executes `setup`, every command in `blocks`, then `teardown`, and reports each command as:

- `FAIL` — the exit code does not match `expect`
- `DRIFT` — the output does not match `output`
- `OK` / `SKIP`

Any `FAIL` or `DRIFT` makes the exit code 1.

Before comparing, both sides are masked: values that change on every run (ages, UIDs, IPs,
timestamps, resource versions, container IDs) and the lab's own `mask:`. What is stored stays as
it came out, so the README shows real values.

A `mask:` is only for values that differ between runs or clusters without changing what the
learner sees, such as generated names or the node's version string. A change in what `kubectl`
shows goes in `output_changes`.

## Kubernetes versions

[`kubernetes-versions.json`](../kubernetes-versions.json) lists the tested versions in
`kubernetes`. Every `output` is recorded on the first one; `--update` refuses to run against an
older server.

`output_changes` is the table of how the output of the older tested versions differs:

| `since` | `change` |
| --- | --- |
| v1.35 | kubectl describe prefixes an event message with the container it is about |
| v1.36 | A Pod's status reports resources |

Each entry has `new`, a regex for the text as it looks from `since` on, and `old`, the text before
`since` (empty when it did not exist; `\1` refers back to a group in `new`). A field that was added
or removed is a line in `new` with an empty `old`; a renamed field keeps its value with a group.

`run` reads the server version with `kubectl version`. When the server is older than `since`, the
recorded output is rewritten with that entry before comparing, so each version is compared against
what it actually prints. The actual output is never rewritten: when an older version does not
print what the table says, it is `DRIFT`.

## Moving to new Kubernetes versions

1. Update `kubernetes-versions.json` and the list in the root `README.md`
   ([how CI uses them](github-actions-e2e.md)).
2. Against a cluster of the first version, run `uv run scripts/labs.py run --update <dir>...`,
   then `render`, and review the diff. Leave out changes that are only ages or timestamps.
3. Run against the other versions. For each `DRIFT`, add an entry to `output_changes`.
