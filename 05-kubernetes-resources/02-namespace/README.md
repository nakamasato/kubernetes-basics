# Namespace


1. Create and delete namespace with yaml file.

    Create:

    ```
    kubectl apply -f namespace-test.yaml
    ```

    Check:

    ```
    kubectl get namespace
    ```

    Delete:

    ```
    kubectl delete -f namespace-test.yaml
    ```

1. Create and delete namespace with only command.

    ```
    kubectl create namespace test-with-kubectl-create
    ```

    ```
    kubectl delete ns test-with-kubectl-create
    ```

1. Create yaml file for namespace `team-a` and `team-b`.

    1. `team-a`: Create manually by filling `apiVersion`, `kind`, and `metadata`.

    1. `team-b`: Create with `kubectl create` command

    ```
    kubectl create ns team-b --dry-run=client -o yaml > ns-team-b.yaml
    ```

1. Create namespaces

    ```
    kubectl apply -f ns-team-a.yaml,ns-team-b.yaml
    ```

1. Check namespaces

    ```
    kubectl get ns
    ```

1. Create pod in `team-a`

    ```
    kubectl run nginx --image=nginx -n team-a
    ```

    check:

    ```
    kubectl get pod
    ```

    ```
    kubectl get pod -n team-a
    ```

1. Create pod with the same name in `team-a`

    ```
    kubectl run nginx --image=nginx -n team-a
    ```

    -> Will fail with an error: `Error from server (AlreadyExists): pods "nginx" already exists`

1. Create pod with the same name in `team-b`

    ```
    kubectl run nginx --image=nginx -n team-b
    ```

1. Check pods in all namespaces

    ```
    kubectl get pod --all-namespaces
    ```

1. Delete namespace `team-a`

    ```
    kubectl delete ns team-a
    ```

    -> the pod in namespace `team-a` is also deleted.

    ```
    kubectl get pod --all-namespaces
    ```

1. Delete namespace `team-b`

    ```
    kubectl delete ns team-b
    ```

    ```
    kubectl get pod --all-namespaces
    ```

    Everything is deleted.
