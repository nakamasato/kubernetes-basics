# Kubernetes Basics

1. Introduction
1. Kubernetes Overview
1. [Kubernetes Environment Setup](03-environment-setup)
1. [kubectl](04-kubectl)
1. [Kubernetes Resources](05-kubernetes-resources)
    1. [Pod](05-kubernetes-resources/01-pod)
    1. [Namespace](05-kubernetes-resources/02-namespace)
    1. [ReplicaSet](05-kubernetes-resources/03-replicaset)
    1. [Deployment](05-kubernetes-resources/04-deployment)
    1. [ConfigMap](05-kubernetes-resources/05-configmap)
    1. [Secret](05-kubernetes-resources/06-secret)
    1. [Service](05-kubernetes-resources/07-service)
1. [Run a simple app in Kubernetes](06-run-simple-application-in-kubernetes)
1. [Debug Kubernetes](07-debug-kubernetes)
1. [EKS setup](08-setup-eks-cluster)
1. [CI/CD](09-cicd)

## Keeping the exercises runnable

Sections 04 to 07 are generated from a `.lab/lab.yaml` next to each
`README.md`. That file holds the prose, the commands and the recorded
output, and it is the file to edit — the `README.md` is written from it.

```
uv run scripts/labs.py render <dir>...   # lab.yaml -> README.md
uv run scripts/labs.py check  <dir>...   # is README.md up to date?
uv run scripts/labs.py run    <dir>...   # run the commands against the current context
uv run scripts/labs.py run --update ...  # replace the recorded output with what actually ran
```

`run` compares each command's exit code and output against what the
README claims. Values that change on every run (timestamps, UIDs,
resource versions, container IDs, IP addresses, ages) are masked before
comparing; what gets stored stays as it came out, so the README shows
real values.

When a new Kubernetes release changes what the commands print, run with
`--update` and review the diff.
