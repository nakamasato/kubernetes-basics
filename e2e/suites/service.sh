source "${E2E_ROOT}/e2e/lib.sh"
k apply -f 05-kubernetes-resources/07-service/
ready my-app your-app
assert_contains "$(http http://my-app)" 'Welcome to nginx!'
[[ "$(k get endpoints my-app -o jsonpath='{.subsets[*].addresses[*].targetRef.name}')" == my-app ]]
