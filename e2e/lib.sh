#!/usr/bin/env bash
set -euo pipefail

: "${E2E_CONTEXT:?Run through python3 e2e/run.py}"
: "${KUBECONFIG:?An isolated kubeconfig is required}"
[[ "$E2E_CONTEXT" == kind-kb-e2e-* ]]

k() {
    kubectl --context "$E2E_CONTEXT" --kubeconfig "$KUBECONFIG" --request-timeout=30s "$@"
}

diagnostics() {
    local status=$?
    if (( status != 0 )); then
        k get pods -A -o wide > "$E2E_ARTIFACTS/pods.txt" 2>&1 || true
        k get events -A --sort-by=.metadata.creationTimestamp > "$E2E_ARTIFACTS/events.txt" 2>&1 || true
        k describe pods -A > "$E2E_ARTIFACTS/describe.txt" 2>&1 || true
    fi
    return "$status"
}
trap diagnostics EXIT

ready() { k wait --for=condition=Ready pod "$@" --timeout=180s; }
rollout() { k rollout status deployment/"$1" "${@:2}" --timeout=240s; }
completed() { k wait --for=jsonpath='{.status.phase}'=Succeeded pod/"$1" --timeout=180s; }
assert_contains() { grep -F -- "$2" <<< "$1"; }

http() {
    k run "probe-$RANDOM" --image=busybox:1.37.0 --restart=Never --attach --rm \
        --pod-running-timeout=180s --command -- wget -q -T 15 -O - "$1"
}
