source "${E2E_ROOT}/e2e/lib.sh"
k apply -f 05-kubernetes-resources/02-namespace/
for namespace in test team-a team-b; do
    k wait --for=jsonpath='{.status.phase}'=Active namespace/"$namespace" --timeout=30s
done
