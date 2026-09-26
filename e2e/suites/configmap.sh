source "${E2E_ROOT}/e2e/lib.sh"
k apply -f 05-kubernetes-resources/05-configmap/configmap-env-var.yml
completed test-pod
assert_contains "$(k logs test-pod)" 'TEST_ENV=test'
k delete pod test-pod --wait=true
k apply -f 05-kubernetes-resources/05-configmap/configmap-file.yml
ready test-pod
[[ "$(k exec test-pod -- cat /datadir/data.csv)" == "$(k get cm test-file -o jsonpath='{.data.data\.csv}')" ]]
