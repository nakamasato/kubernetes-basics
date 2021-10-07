# ConfigMap

1. Apply configmap and pods to set environment variables.

    ```
    kubectl apply -f configmap-env-var.yaml
    ```

    ```
    kubectl get pod
    ```

    -> `COMPLETED`

    ```
    kubectl logs test-pod
    ```

    -> `TEST_ENV=test`

    delete:

    ```
    kubectl delete -f configmap-env-var.yaml
    ```

1. Apply configmap and pods to read file set in configmap.

    ```
    kubectl apply -f configmap-file.yaml
    ```

    ```
    kubectl get pod
    ```

    ```
    kubectl exec -it test-pod sh
    ```

    inside the container:

    ```
    ls
    ls datadir
    cat datadir/data.csv
    ```

    you can read data.csv defined in configmap.

    delete:

    ```
    kubectl delete -f configmap-file.yaml
    ```
