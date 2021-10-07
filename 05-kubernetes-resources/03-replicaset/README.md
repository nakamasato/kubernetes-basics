# ReplicaSet

1. Apply replicaset

    ```
    kubectl apply -f replicaset.yaml
    ```
1. Check replicaset and pod

    ```
    kubectl get replicaset
    ```

    ```
    kubectl get pod
    ```

1. Scale replicaset to replica=3

    ```
    kubectl scale rs/nginx --replicas=3
    ```

    `rs`: `replicaset`

    ```
    kubectl get pods
    ```

    -> 3 pods

1. Apply yaml file (replica: 2) again

    ```
    kubectl apply -f replicaset.yaml
    ```

    check pods:
    ```
    kubectl get pods
    ```

    -> 2 pods

1. Confirm replicaset keeps the required number of pods running all the time.

    Keep watching the number of pods

    ```
    watch kubectl get pod
    ```

    Delete a pod

    ```
    kubectl delete po <pod name>
    ```

    ReplicaSet automatically add a new pod

1. Delete all the resources

    ```
    kubectl delete -f replicaset.yaml
    ```
