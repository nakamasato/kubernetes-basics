# kubectl

## Install

https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/

## Check Kubernetes in Docker Desktop

Please check [03-environment-setup](../03-environment-setup)

## Commonly used commands

1. Check current context

    ```
    kubectl config current-context
    docker-desktop
    ```

1. Check pods in `default` namespace.

    ```
    kubectl get pods
    ```

1. Run nginx pod in default namespace.

    ```
    kubectl run nginx --image=nginx
    ```

1. Delete the nginx pod.

    ```
    kubectl delete pod nginx
    pod "nginx" deleted from default namespace
    ```

## Create and delete resources

`create` and `delete` take two forms.

- `kubectl create|delete -f FILENAME` — write what you want in a file and pass the file
- `kubectl create|delete TYPE NAME [flags]` — name the resource on the command line

### From a file

[pod-test.yaml](pod-test.yaml) describes one Pod. What each field means is covered in the
next lecture.

1. Create

    ```
    kubectl create -f pod-test.yaml
    pod/pod-test created
    ```

1. Check. `-f` takes the same file, so you do not have to name the Pod.

    ```
    kubectl get pod
    NAME       READY   STATUS    RESTARTS   AGE
    pod-test   1/1     Running   0          4s
    ```

    ```
    kubectl get -f pod-test.yaml
    NAME       READY   STATUS    RESTARTS   AGE
    pod-test   1/1     Running   0          5s
    ```

1. Delete

    ```
    kubectl delete -f pod-test.yaml
    pod "pod-test" deleted from default namespace
    ```

    ```
    kubectl get pod
    No resources found in default namespace.
    ```

### From the command line

1. Create

    ```
    kubectl create namespace test-ns
    namespace/test-ns created
    ```

1. Check. `ns` is the short name for `namespace`.

    ```
    kubectl get ns test-ns
    NAME      STATUS   AGE
    test-ns   Active   0s
    ```

1. Delete

    ```
    kubectl delete namespace test-ns
    namespace "test-ns" deleted
    ```

`kubectl create -h` lists what you can create this way — `configmap`, `deployment`,
`namespace`, `secret`, `service` and a dozen more. Anything not on that list needs a file.

```
kubectl create -h
```

### Build a manifest with `--dry-run`

`--dry-run=client` stops before the request reaches the API server. Combined with `-o yaml`
it prints the manifest the command would have sent, which makes a good starting point.

```
kubectl create namespace test-ns --dry-run=client -o yaml
apiVersion: v1
kind: Namespace
metadata:
  name: test-ns
spec: {}
status: {}
```

Redirect it to a file and edit from there.

```
kubectl create namespace test-ns --dry-run=client -o yaml > test-ns.yaml
```

## Reference

- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
