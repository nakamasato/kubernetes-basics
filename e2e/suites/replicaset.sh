source "${E2E_ROOT}/e2e/lib.sh"
k apply -f 05-kubernetes-resources/03-replicaset/pod.yaml
k apply -f 05-kubernetes-resources/03-replicaset/replicaset.yaml
k wait --for=jsonpath='{.status.readyReplicas}'=2 rs/nginx --timeout=180s
[[ "$(k get pod nginx -o jsonpath='{.metadata.ownerReferences[0].kind}')" == ReplicaSet ]]
k delete pod nginx --wait=true
k wait --for=jsonpath='{.status.readyReplicas}'=2 rs/nginx --timeout=180s
[[ "$(k get pods -l app=nginx -o name | wc -l | tr -d ' ')" == 2 ]]
