source "${E2E_ROOT}/e2e/lib.sh"
k apply -f 05-kubernetes-resources/04-deployment/deployment.yaml
rollout nginx
[[ "$(k get deploy nginx -o jsonpath='{.status.readyReplicas}')" == 2 ]]
k expose deployment nginx --port=80
assert_contains "$(http http://nginx)" 'Welcome to nginx!'
