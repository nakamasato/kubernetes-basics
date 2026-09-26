source "${E2E_ROOT}/e2e/lib.sh"
# nginx-*.yaml are captured kubectl output for comparison, not input manifests.
k apply -f 05-kubernetes-resources/01-pod/pod.yaml
ready nginx-yaml
assert_contains "$(k exec nginx-yaml -- curl -fsS http://localhost)" 'Welcome to nginx!'
