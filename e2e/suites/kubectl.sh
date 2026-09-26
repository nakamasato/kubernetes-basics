source "${E2E_ROOT}/e2e/lib.sh"
k apply -f 04-kubectl/test-ns.yaml
k apply -n test-ns -f 04-kubectl/pod-test.yaml
ready -n test-ns pod-test
assert_contains "$(k exec -n test-ns pod-test -- curl -fsS http://localhost)" 'Welcome to nginx!'
