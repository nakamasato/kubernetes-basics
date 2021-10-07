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

## Reference

- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
