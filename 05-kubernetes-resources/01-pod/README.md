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

    - Mostly different in `CreationTimestamp` and hash values.
    - `labels` appears in `kubectl-run`

    ```diff
    diff nginx-yaml.yaml nginx-kubectl-run.yaml
    4,5c4,7
    <   creationTimestamp: "2021-08-10T23:10:55Z"
    <   name: nginx-yaml
    ---
    >   creationTimestamp: "2021-08-10T23:12:34Z"
    >   labels:
    >     run: nginx
    >   name: nginx
    7,8c9,10
    <   resourceVersion: "74084"
    <   uid: 3bc02c8e-fe9a-4d5b-b816-8e58377e5e2b
    ---
    >   resourceVersion: "74214"
    >   uid: a492f636-535a-4117-80a0-9abc4af15345
    19c21
    <       name: kube-api-access-p8rlz
    ---
    >       name: kube-api-access-6vfnl
    42c44
    <   - name: kube-api-access-p8rlz
    ---
    >   - name: kube-api-access-6vfnl
    63c65
    <     lastTransitionTime: "2021-08-10T23:10:55Z"
    ---
    >     lastTransitionTime: "2021-08-10T23:12:34Z"
    67c69
    <     lastTransitionTime: "2021-08-10T23:10:59Z"
    ---
    >     lastTransitionTime: "2021-08-10T23:12:38Z"
    71c73
    <     lastTransitionTime: "2021-08-10T23:10:59Z"
    ---
    >     lastTransitionTime: "2021-08-10T23:12:38Z"
    75c77
    <     lastTransitionTime: "2021-08-10T23:10:55Z"
    ---
    >     lastTransitionTime: "2021-08-10T23:12:34Z"
    79c81
    <   - containerID: docker://7dc65e0a60261002faa0847c565bb9d8d515aebc77ff31b7b8d1e5714757992c
    ---
    >   - containerID: docker://b49d81708345a54f1218fdba81070cbdab16619299de1160eaec6968af884ffb
    89c91
    <         startedAt: "2021-08-10T23:10:59Z"
    ---
    >         startedAt: "2021-08-10T23:12:37Z"
    92c94
    <   podIP: 10.1.0.6
    ---
    >   podIP: 10.1.0.7
    94c96
    <   - ip: 10.1.0.6
    ---
    >   - ip: 10.1.0.7
    96c98
    <   startTime: "2021-08-10T23:10:55Z"
    ---
    >   startTime: "2021-08-10T23:12:34Z"
    ```
