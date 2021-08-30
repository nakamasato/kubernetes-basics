# Deploy Simple Application in Kubernetes

## Diagram
1. Application
    ![](diagram.drawio.svg)
1. Kubernetes Objects
    ![](kubernetes-object.drawio.svg)


## Create your namespace

1. Set your name to `namespace` variable.

    ```
    namespace=<yourname>
    ```
1. Create your namespace.
    ```
    kubectl create namespace $namespace
    ```

    - [ ] Check your namespace exists

        ```
        kubectl get ns $namespace
        NAME   STATUS   AGE
        naka   Active   71m
        ```

## Create MySQL (Deployment and Service)

Notice: `StatefulSet` is more preferable resource to manage database applications, but just for simplicity `Deployment` is used for MySQL here.

1. Create Deployment for MySQL.

    ```
    kubectl apply -f mysql-deployment.yaml
    ```

    <details><summary>how to create the yaml easily</summary>

    ```
    kubectl create deploy mysql --image=mysql:5.7 --dry-run=client -o yaml > mysql-deployment.yaml
    ```

    </details>

    - [ ] Check `Deployment` in your namespace

        ```
        kubectl get deploy -n $namespace
        ```

    - [ ] Check `ReplicaSet` in your namespace

        ```
        kubectl describe replicaset -n $namespace
        ```

        <details><summary>result</summary>


        </details>

    - [ ] Check `Pod` in your namespace

        ```
        kubectl get pods -n $namespace
        ```

    - [ ] Check if you can connect to MySQL with `kubectl exec`

        ```
        kubectl exec -it mysql-xxxx mysql -uroot -ppassword
        ```

1. Create Service for MySQL.

    1. Create `Service`.

        ```
        kubectl create mysql-service.yaml -n $namespace
        ```

        <details><summary>how to create the yaml easily</summary>

        ```
        kubectl create service clusterip mysql --tcp=3306 --dry-run=client --output yaml > mysql-service.yaml
        ```

        </details>

        - [ ] Check the created `Service`

            ```
            kubectl get service -n $namespace
            ```


## Create sample application (Deployment, ConfigMap, Secret)

Sample application: https://github.com/nakamasato/fastapi-sample

1. Create `Deployment` yaml.

    - [ ] Set container image to `ghcr.io/nakamasato/fastapi-sample:v1.0`.
    - [ ] Set environment variables `MYSQL_HOST`, `MYSQL_DATABASE`, and `MYSQL_USER` with `ConfigMap`.
    - [ ] Set environment variable `MYSQL_PASSWORD` with `Secret`.

1. Create `ConfigMap` yaml.

    1. Prepare `env.txt`.

        ```
        MYSQL_HOST=mysql
        MYSQL_DATABASE=test_db
        MYSQL_USER=sample_app
        ```
    1. Create yaml from `env.txt`.
        ```
        kubectl create cm sample-app --from-env-file=env.txt --dry-run=client -o yaml > sample-app-configmap.yaml
        ```

1. Create `Secret` yaml.

    ```
    kubectl create secret generic sample-app --from-literal=MYSQL_PASSWORD=password --dry-run=client -o yaml > sample-app-secret.yaml
    ```

1. Apply `Deployment`, `ConfigMap`, and `Secret`.

    ```
    kubectl apply -f sample-app-deployment.yaml,sample-app-configmap.yaml,sample-app-secret.yaml
    ```

    - [ ] Check `Deployment` in your namespace

        ```
        kubectl get deploy -n $namespace
        ```

    - [ ] Check `Pod` in your namespace

        ```
        kubectl get pods -n $namespace
        ```

    - [ ] Check `ConfigMap` in your namespace

        ```
        kubectl get cm -n $namespace
        ```

    - [ ] Check `Secret` in your namespace

        ```
        kubectl get secret -n $namespace
        ```

1. Apply `Service`.

    ```
    kubectl apply -f sample-app-service.yaml
    ```

    - [ ] Check the created `Service`

        ```
        kubectl get service -n $namespace
        ```

## Clean up resources

```
kubectl delete -f nginx-deployment-1.14.2.yaml -n $namespace
kubectl delete -f nginx-service.yaml -n $namespace
kubectl delete ns $namespace
```
