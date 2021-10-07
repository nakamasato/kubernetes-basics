# Deployment

1. Create Deployment

    ```
    kubectl apply -f deployment.yaml
    ```

1. Check

    ```
    kubectl get deployment
    ```

    ```
    kubectl get replicaset
    ```

    ```
    kubectl get replicaset nginx-xxxx -o yaml
    ```

    - You can see the replicaset is created by `Deployment` in `ownerReferences` field.
    - You can also see `pod-template-hash`, which is added by `Deployment`.

    ```
    kubectl get pod
    ```

1. Change replicas

    1. Update `replicas: 2` in `deployment.yaml`

    1. Apply it

        ```
        kubectl apply deployment.yaml
        ```

        rollout isn't triggered as `replica` is not in the pod template.

1. Change image by command

    ```
    kubectl set image deployment/nginx nginx=nginx:1.15
    ```

    check:

    ```
    kubectl get rs
    ```

    You can see two replicasets; one is old one, the other is new one.

1. Change image by updating yaml file.

    1. Change `nginx:1.14` -> `nginx:1.15`  in deployment.yaml

    1. Apply it

        ```
        kubectl apply -f deployment.yaml
        ```
    1. You can check the replicasets

        ```
        kubectl get replicaset
        ```

        -> 3 replicasets

1. Rollback

    1. Check rollout history.

        ```
        kubectl rollout history deployment.v1.apps/nginx
        ```

    1. Roll back to the revision 2

        ```
        kubectl rollout undo deployment.v1.apps/nginx --to-revision=2
        ```

    1. Check replicaset

        ```
        kubectl get rs
        ```

        -> replicaset with `nginx:1.15` has running pods.

1. Delete the resources

    ```
    kubectl delete -f deployment.yaml
    ```
