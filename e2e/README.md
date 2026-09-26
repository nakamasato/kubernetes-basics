# kind E2E

Docker, kind v0.29.0+, kubectl, Python 3, and Bash are required. No Python packages are needed.

```bash
python3 e2e/run.py --list
python3 e2e/run.py service       # one target
python3 e2e/run.py pod service   # several targets
python3 e2e/run.py               # all targets, sequentially
KIND_NODE_IMAGE=kindest/node:v1.36.1 python3 e2e/run.py deployment
python3 e2e/run.py --select origin/master  # JSON targets changed since merge-base
```

Each target gets a uniquely named, disposable kind cluster and temporary kubeconfig.
Every kubectl invocation supplies both `--context` and `--kubeconfig`. Creation,
diagnostics, and deletion use the temporary kubeconfig; your existing kubeconfig
and current-context are never updated. The cluster is deleted even after failure.
Failure diagnostics are saved under `e2e-artifacts/` and uploaded by CI.

The default Kubernetes image is `kindest/node:v1.33.1`; override `KIND_NODE_IMAGE`
to check a Kubernetes upgrade. Application images come from the checked-out YAML.

PR CI selects suites by changed chapter/subchapter, including deleted and renamed
files. Changes to a suite select only that suite; shared runner/workflow changes
select all suites. Unrelated changes skip cluster creation. The manual workflow
runs all suites. Use `e2e-result` as the stable required check for branch protection.

The core suites cover HTTP through Services, ReplicaSet adoption/replacement,
Deployment readiness, ConfigMap/Secret environment and mounted-file contents,
and expected failures plus repairs in the debugging exercises. The exported
`01-pod/nginx-*.yaml` files are illustrative command output, not deployable input.
EKS setup requires AWS and is outside this local kind test scope.
