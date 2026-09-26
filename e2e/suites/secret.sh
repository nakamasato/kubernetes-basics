source "${E2E_ROOT}/e2e/lib.sh"
k apply -f 05-kubernetes-resources/06-secret/secret-env-var.yaml
completed test-pod
assert_contains "$(k logs test-pod)" 'username=admin'
k delete pod test-pod --wait=true
k apply -f 05-kubernetes-resources/06-secret/secret-string-data.yaml
[[ "$(k get secret mysecret -o jsonpath='{.data.username}')" == YWRtaW4= ]]
k apply -f 05-kubernetes-resources/06-secret/secret-file.yml
ready test-pod
[[ "$(k exec test-pod -- cat /datadir/data.csv)" == "$(k get secret mysecret -o jsonpath='{.data.data\.csv}' | base64 --decode)" ]]
