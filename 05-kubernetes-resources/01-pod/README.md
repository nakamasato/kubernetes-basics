# Pod

1. Create pod with yaml file.

    ```
    kubectl apply -f pod.yaml
    ```

1. Create pod with `kubectl run`

    ```
    kubectl run nginx --image=nginx
    ```

1. Check the pod created by `pod.yaml`

    ```
    kubectl get pod nginx-yaml -o yaml > nginx-yaml.yaml
    ```

1. Check the pod created by `kubectl run`

    ```
    kubectl get pod nginx -o yaml > nginx-kubectl-run.yaml
    ```

1. Compare them.

    - `kubectl apply` adds the `kubectl.kubernetes.io/last-applied-configuration` annotation.
    - `labels` appears in `kubectl run`.
    - The rest differs only in timestamps, hash values, resource versions and IPs.

    ```diff
    diff nginx-yaml.yaml nginx-kubectl-run.yaml
    4,6d3
    <   annotations:
    <     kubectl.kubernetes.io/last-applied-configuration: |
    <       {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"name":"nginx-yaml","namespace":"default"},"spec":{"containers":[{"image":"nginx","name":"nginx"}]}}
    9c6,8
    <   name: nginx-yaml
    ---
    >   labels:
    >     run: nginx
    >   name: nginx
    11,12c10,11
    <   resourceVersion: "1866"
    <   uid: 4c679147-42e5-4b18-b1e0-a5d12bf98dc4
    ---
    >   resourceVersion: "1873"
    >   uid: 548a3586-5517-42cd-a8ba-915735bd9b23
    23c22
    <       name: kube-api-access-zv854
    ---
    >       name: kube-api-access-6ttw7
    87c86
    <   - containerID: containerd://dc86531e10d411010e95f9d0ef830abca03829d6fb621e9f4a351f8fdecacf66
    ---
    >   - containerID: containerd://bfa8cb0fa7041046ffdcb9e22a9a0f6712843978182b1fb1dbb2f28b1f72f676
    114c113
    <   podIP: 10.244.0.7
    ---
    >   podIP: 10.244.0.8
    ```
