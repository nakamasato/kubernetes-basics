# E2E on GitHub Actions

[`.github/workflows/e2e.yml`](../.github/workflows/e2e.yml) runs every lab against a kind cluster
on each pull request, once per tested Kubernetes version. What a lab is and how its output is
compared is in [labs.md](labs.md).

## Jobs

`versions` reads [`kubernetes-versions.json`](../kubernetes-versions.json):

- turns `kubernetes` into the matrix for `e2e`, and passes `kind` on as the kind release
- fails unless the root `README.md` lists exactly the same versions under
  `Tested Kubernetes versions:`

`e2e` runs once per version:

1. creates a kind cluster from `kindest/node:<version>` and installs kubectl of the same version,
   because kubectl only supports servers within one minor version of itself
2. runs `labs.py check` and `labs.py run` on every directory that has a `.lab/lab.yaml`

To add or drop a version, pick a kind release that ships a `kindest/node` image for every version
in the list (see its release notes), then follow
[Moving to new Kubernetes versions](labs.md#moving-to-new-kubernetes-versions).

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
