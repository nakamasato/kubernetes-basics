# Debug

## Prepare

1. Prepare the resources

    ```
    kubectl apply -f .
    ```

## Check Pods

1. Practice `kubectl get` for `Pod` and `Node`

    1. labels

        ```
        kubectl get pod --selector run=nginx
        kubectl get node -l beta.kubernetes.io/arch=amd64
        ```

        <details>

        ```
        kubectl get pod --selector run=nginx
        NAME      READY   STATUS             RESTARTS   AGE
        nginx-1   0/1     ImagePullBackOff   0          35m
        nginx-2   0/1     Pending            0          35m
        nginx-3   1/1     Running            0          35m
        ```

        ```
        kubectl get node -l beta.kubernetes.io/arch=amd64
        NAME             STATUS   ROLES    AGE   VERSION
        docker-desktop   Ready    master   79d   v1.16.6-beta.0
        ```

        </details>

        ```
        kubectl get po --show-labels
        kubectl get node --show-labels
        ```

        <details>

        ```
        kubectl get po --show-labels
        NAME      READY   STATUS             RESTARTS   AGE   LABELS
        nginx-1   0/1     ImagePullBackOff   0          36m   run=nginx
        nginx-2   0/1     Pending            0          36m   run=nginx
        nginx-3   1/1     Running            0          36m   run=nginx
        ```

        ```
        kubectl get node --show-labels
        NAME             STATUS   ROLES    AGE   VERSION          LABELS
        docker-desktop   Ready    master   79d   v1.16.6-beta.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=docker-desktop,kubernetes.io/os=linux,node-role.kubernetes.io/master=
        ```

        </details>


    1. output

        ```
        kubectl get pod -o yaml
        kubectl get node -o yaml
        ```

        ```
        kubectl get pod -o wide
        kubectl get node -o wide
        ```

        ```
        kubectl get pod -o json
        kubectl get node -o json
        ```

        ```
        kubectl get pod -o jsonpath='{.items[*].metadata.name}'
        kubectl get node -o jsonpath='{.items[*].metadata.name}'
        ```

    1. namespace

        ```
        kubectl get pod -n kube-system
        ```

        ```
        kubectl get pod -A
        ```

1. Check the status of all pods in the cluster.

    ```
    kubectl get pod -A
    ```

    <details>

    ```
    kubectl get po -A
    NAMESPACE     NAME                                     READY   STATUS             RESTARTS   AGE
    default       nginx-1                                  0/1     ImagePullBackOff   0          32m
    default       nginx-2                                  0/1     Pending            0          32m
    default       nginx-3                                  1/1     Running            0          32m
    kube-system   coredns-777fb94669-bvm4d                 1/1     Running            3          79d
    kube-system   coredns-777fb94669-pxv9j                 1/1     Running            3          79d
    kube-system   etcd-docker-desktop                      1/1     Running            6          79d
    kube-system   kube-apiserver-docker-desktop            1/1     Running            17         79d
    kube-system   kube-controller-manager-docker-desktop   1/1     Running            3          79d
    kube-system   kube-proxy-l6rx5                         1/1     Running            3          79d
    kube-system   kube-scheduler-docker-desktop            1/1     Running            19         79d
    kube-system   storage-provisioner                      1/1     Running            42         79d
    kube-system   vpnkit-controller                        1/1     Running            3          79d
    test          nginx-4                                  1/1     Running            0          32m
    ```

    </details>

1. Check which node `nginx-1` Pod is running on.

    ```
    kubectl get pod nginx-1 -o wide
    ```

1. Check the reason for `nginx-1` not running.

    ```
    kubectl describe pod nginx-1
    ```

1. Check the logs of `nginx-3` Pod.

    ```
    kubectl logs nginx-3 -f --tail 20
    ```

1. Check if `nginx` Service is available.

    ```
    kubectl port-forward svc/nginx 8080:80
    ```

    -> Open http://localhost:8080 on your browser.

    ```
    kubectl get endpoints nginx
    ```

1. Check all the node in the cluster

    ```
    kubectl get node
    ```

1. Check all the pods running on `docker-desktop`

    ```
    kubectl describe node docker-desktop
    ```

## Prepare

1. Clean up the resources:

    ```
    kubectl delete -f .
    ```
