# E2E on GitHub Actions

[`.github/workflows/e2e.yml`](../.github/workflows/e2e.yml) runs every `.lab/lab.yaml` against a
real cluster on each pull request.

## What it runs

For every directory that has a `.lab/lab.yaml`:

1. `uv run scripts/labs.py check` — the committed `README.md` matches what `lab.yaml` renders.
2. `uv run scripts/labs.py run` — runs `setup`, then each command in `blocks`, then `teardown`,
   and compares every command with what `lab.yaml` records:
    - the exit code against `expect` (success by default) — a mismatch is `FAIL`
    - the output against `output`, after masking volatile values (ages, UIDs, IPs, timestamps,
      and the lab's own `mask:` entries) — a mismatch is `DRIFT`
    - `example` is rendered in the README but never compared
    - `skip` is not run

Any `FAIL` or `DRIFT` fails the job.

## Kubernetes versions

[`kubernetes-versions.json`](../kubernetes-versions.json) is the single source:

- `kind` — the kind release used to create the cluster
- `kubernetes` — the tested versions. The first entry is the one the outputs are recorded on
- `output_changes` — how the output differs between the tested versions

The `versions` job turns `kubernetes` into the job matrix. Each job uses the same version for the
`kindest/node` image and for kubectl, because kubectl only supports servers within one minor
version of itself. The job also fails unless the root `README.md` lists exactly the same versions
under `Tested Kubernetes versions:`.

### Output that changes between versions

Every `output` in `lab.yaml` is what the first version prints. `output_changes` is the table of
what changed since the older tested versions:

| `since` | `change` |
| --- | --- |
| v1.35 | kubectl describe prefixes an event message with the container it is about |
| v1.36 | A Pod's status reports resources |

Each entry also has `new`, a regex for the text as it looks from `since` on, and `old`, what the
text looked like before (empty when it did not exist; `\1` refers back to a group in `new`). When
`labs.py run` finds the server older than `since`, it rewrites the recorded output with the entry
before comparing, so each version is compared against the output it actually prints. The actual
output is never rewritten: if an older version does not print what the table says, it is `DRIFT`.

A lab's `mask:` is only for values that change on every run or cluster, such as generated names
or the node's version string. A change in what `kubectl` shows belongs in `output_changes`.

### Changing the versions

1. Pick a kind release that ships a `kindest/node` image for each version (see its release notes),
   and update `kubernetes-versions.json` and the list in `README.md`.
2. Record the outputs on the first version with `uv run scripts/labs.py run --update <dir>...`
   and review the diff. Keep changes that are only ages or timestamps out of the commit.
   `--update` refuses to run against an older server.
3. For drift that remains on the other versions, add an entry to `output_changes`.

## Matching Docker Desktop

The recorded outputs come from Docker Desktop's Kubernetes (kind mode) on Apple Silicon. The
workflow reproduces the parts that show up in the outputs:

| Docker Desktop | Workflow |
| --- | --- |
| arm64 node | `runs-on: ubuntu-24.04-arm` |
| node `desktop-control-plane` | kind `cluster_name: desktop` |
| context `docker-desktop` | `kubectl config rename-context kind-desktop docker-desktop` |
| macOS `base64` (no line wrapping) | a `base64` wrapper that runs GNU `base64 -w0` |

Output that depends on the host (CPU, memory, kernel and node events in `kubectl describe node`)
is recorded as `example`, not `output`.

## Why not a macOS runner

kind runs each Kubernetes node as a Docker container, and Docker needs a Linux kernel.

On a Mac, Docker Desktop starts a lightweight Linux VM with Apple's Virtualization.framework and
runs Docker inside it:

```
Mac (macOS) -> Linux VM (Docker Desktop) -> kind node containers
```

A GitHub-hosted macOS runner is itself a VM on a physical Mac, so Docker would need a VM inside a
VM (nested virtualization):

```
Mac -> macOS VM (runner) -> Linux VM (Docker)  <- cannot be created -> kind
```

GitHub's arm64 macOS runners do not support nested virtualization, so neither Docker Desktop nor
colima can start and there is no kind cluster.

A Linux runner already runs a Linux kernel, so Docker runs directly and kind works:

```
Linux runner -> Docker -> kind node containers
```

`ubuntu-24.04-arm` also matches the arm64 Linux that Docker Desktop runs on Apple Silicon.
