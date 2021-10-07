# Secret

## Environment variables


1. apply

    ```
    kubectl apply -f secret-env-var.yaml
    ```

1. check with logs

    ```
    kubectl logs test-pod
    ```

    -> you can see `username=admin` and `password=xxx` in the environment variables.

1. Delete

    ```
    kubectl delete -f secret-env-var.yaml
    ```
## Mount file

data.csv

```csv
name,age,email,password
naka,1,naka@example.com,j4gn43g4gr
tanaka,2,tanaka@example.com,8j437fkw3v
```

1. Encode `data.csv`

    ```
    echo -n 'name,age,email,password
    naka,1,naka@example.com,j4gn43g4gr
    tanaka,2,tanaka@example.com,8j437fkw3v' | base64
    bmFtZSxhZ2UsZW1haWwscGFzc3dvcmQKbmFrYSwxLG5ha2FAZXhhbXBsZS5jb20sajRnbjQzZzRncgp0YW5ha2EsMix0YW5ha2FAZXhhbXBsZS5jb20sOGo0Mzdma3czdg==
    ```

    or

    ```
    kubectl create secret generic mysecret --from-file=data.csv=data.csv -o yaml --dry-run=client
    apiVersion: v1
    data:
      data.csv: bmFtZSxhZ2UsZW1haWwscGFzc3dvcmQKbmFrYSwxLG5ha2FAZXhhbXBsZS5jb20sajRnbjQzZzRncgp0YW5ha2EsMix0YW5ha2FAZXhhbXBsZS5jb20sOGo0Mzdma3czdg==
    kind: Secret
    metadata:
      creationTimestamp: null
      name: mysecret
    ```

1. Apply

    ```
    kubectl apply -f secret-file.yaml
    ```

1. Check

    ```
    kubectl exec -it test-pod sh
    ```

    inside the container


    ```
    ls
    ls datadir
    cat datadir/data.csv
    ```

1. Delete

    ```
    kubectl delete -f secret-file.yaml
    ```

## Others

Create secret with `--from-literal`
```
kubectl create secret generic mysecret --from-literal=username=admin --from-literal=password=1f2d1e2e67df -o yaml --dry-run=client
```
