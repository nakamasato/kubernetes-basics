source "${E2E_ROOT}/e2e/lib.sh"
k apply -f 07-debug-kubernetes/
ready nginx-3
ready -n test nginx-4
k wait --for=jsonpath='{.status.conditions[?(@.type=="PodScheduled")].reason}'=Unschedulable pod/nginx-2 --timeout=60s
k wait --for=jsonpath='{.status.containerStatuses[0].state.waiting.reason}'=ImagePullBackOff pod/nginx-1 --timeout=180s
assert_contains "$(http http://nginx-1)" 'Welcome to nginx!'
[[ -z "$(k get endpoints nginx-2 -o jsonpath='{.subsets[*].addresses[*].ip}')" ]]
# Repair only the disposable cluster, preserving the intentional broken examples.
k set image pod/nginx-1 nginx=nginx
k label nodes --all nodeType=test
ready nginx-1 nginx-2
k patch service nginx-2 --type=merge -p='{"spec":{"selector":{"run":"nginx"}}}'
assert_contains "$(http http://nginx-2)" 'Welcome to nginx!'
