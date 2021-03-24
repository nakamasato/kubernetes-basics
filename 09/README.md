# CI/CD

## ArgoCD

## Setup

1. Install ArgoCD (Version v1.8.7)

    ```
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v1.8.7/manifests/install.yaml
    ```

1. Check
    ```
    kubectl get pod -n argocd
    NAME                                 READY   STATUS    RESTARTS   AGE
    argocd-application-controller-0      1/1     Running   0          90s
    argocd-dex-server-567b48df49-svbsg   1/1     Running   0          91s
    argocd-redis-6fb68d9df5-mxxrj        1/1     Running   0          91s
    argocd-repo-server-6dcbd9cb-8gkjq    1/1     Running   0          91s
    argocd-server-69678b4f65-zl98p       1/1     Running   0          91s
    ```

1. Expose port

    Either of the following methods:

    1. Port forward the service (port: 30080)

        ```
        kubectl -n argocd port-forward service/argocd-server 30080:80
        ```

    1. Create `Service` with `NodePort` type (port: 30080)

        ```
        kubectl apply -f argocd-install/argocd-server-node-port.yaml -n argocd
        ```

1. Login

    Open https://localhost:30080, click on `Advanced` and `Proceed to localhost (unsafe)` (this is ok because we're connecting to the argocd running in our local computer)

    - username: `admin`
    - password: pod name for argocd-server (can be got by `kubectl get po -n argocd | grep argocd-server | awk '{print $1}'`)

    <img src="argocd.png" width="400"/>

## Deploy an application using ArgoCD

1. Create `AppProject`
    ```
    kubectl apply -f argocd-appproject-test.yaml
    ```
1. Create `Application`


    ```
    kubectl apply -f argocd-application-test.yaml
    ```

## Clean up

1. Delete ArgoCD `Application` and `AppProject`.

    ```
    kubectl delete -f argocd-application-test.yaml
    kubectl delete -f argocd-appproject-test.yaml
    ```

1. Uninstall ArgoCD and delete the `argocd` namespace.

    ```
    kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v1.8.7/manifests/install.yaml
    kubectl delete ns argocd
    ```
