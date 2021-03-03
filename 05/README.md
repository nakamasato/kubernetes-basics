# 05 Set Environment Variables with ConfigMap

## Prerequisite

Namespace is set.

```
namespace=<yourname>
```

```
kubectl create ns $namespace
```

## Practice ConfigMap

1. Create `ConfigMap`

    ```
    kubectl create configmap test-configmap --from-literal=username=testuser --from-literal=hostname=test.com
    ```

1. Check the created `ConfigMap`

    ```
    kubectl get configmap test-configmap -o yaml
    ```

    <details>

    ```
    apiVersion: v1
    data:
      hostname: test.com
      username: testuser
    kind: ConfigMap
    metadata:
      creationTimestamp: "2021-03-02T22:39:14Z"
      managedFields:
      - apiVersion: v1
        fieldsType: FieldsV1
        fieldsV1:
          f:data:
            .: {}
            f:hostname: {}
            f:username: {}
        manager: kubectl-create
        operation: Update
        time: "2021-03-02T22:39:14Z"
      name: test-configmap
      namespace: default
      resourceVersion: "8026947"
      selfLink: /api/v1/namespaces/default/configmaps/test-configmap
      uid: 22068908-bbfa-4a61-9292-45ed30294609
    ```

    </details>

1. Delete

    ```
    kubectl delete configmap test-configmap
    ```

## Run Nginx with custom index.html

1. Apply `ConfigMap` and `Deployment`

    ```
    kubectl apply -f nginx-configmap.yaml,nginx-deployment.yaml,nginx-service.yaml -n $namespace
    ```

1. Check

    port forward

    ```
    kubectl -n $namespace port-forward service/nginx 8080:80
    ```

    Open http://localhost:8080 -> You'll see "My Page" in the page.
