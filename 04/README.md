# 04 Deploy simple application


## Create your namespace

```
namespace=<yourname>
```

```
kubectl create namespace $namespace
```

- [ ] Check your namespace exists

    ```
    kubectl get ns $namespace
    NAME   STATUS   AGE
    naka   Active   71m
    ```

## Create nginx with imperative command (in `default` namespace) (命令型)

```
kubectl create deployment nginx --image nginx
```

```
kubectl get deployment nginx
```

- [ ] Check deployment exists in `default` namespace

    ```
    kubectl get deploy -n default
    NAME    READY   UP-TO-DATE   AVAILABLE   AGE
    nginx   1/1     1            1           71m
    ```

## Create nginx in a declerative way (宣言型) (in your own namespace)

Create a kubernetes manifest file (with 2 replicas)

```
kubectl create deployment nginx --image nginx --replicas=2 --dry-run=client --output yaml > nginx-deployment.yaml
```

```
kubectl apply -f nginx-deployment.yaml -n $namespace
```

Check `Deployment` in your namespace

```
kubectl get deployment -n $namespace
```

- [ ] Check all resources in your namespace

    ```
    kubectl get all -n $namespace
    ```

    - [ ] 2 `Pod`s
    - [ ] 1 `Deployment`
    - [ ] 1 `ReplicaSet`

    <details><summary>Result</summary>

        kubectl get all -n $namespace
        NAME                         READY   STATUS    RESTARTS   AGE
        pod/nginx-6799fc88d8-cgrf2   1/1     Running   0          11s
        pod/nginx-6799fc88d8-mp7j8   1/1     Running   0          11s

        NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
        deployment.apps/nginx   2/2     2            2           11s

        NAME                               DESIRED   CURRENT   READY   AGE
        replicaset.apps/nginx-6799fc88d8   2         2         2       11s

    </details>

- [ ] Check `ReplicaSet` in your namespace

    ```
    kubectl describe replicaset -n $namespace
    ```

    <details><summary>result</summary>

        Name:           nginx-6799fc88d8
        Namespace:      naka
        Selector:       app=nginx,pod-template-hash=6799fc88d8
        Labels:         app=nginx
                        pod-template-hash=6799fc88d8
        Annotations:    deployment.kubernetes.io/desired-replicas: 2
                        deployment.kubernetes.io/max-replicas: 3
                        deployment.kubernetes.io/revision: 1
        Controlled By:  Deployment/nginx
        Replicas:       2 current / 2 desired
        Pods Status:    2 Running / 0 Waiting / 0 Succeeded / 0 Failed
        Pod Template:
        Labels:  app=nginx
                pod-template-hash=6799fc88d8
        Containers:
        nginx:
            Image:        nginx
            Port:         <none>
            Host Port:    <none>
            Environment:  <none>
            Mounts:       <none>
        Volumes:        <none>
        Events:
        Type    Reason            Age   From                   Message
        ----    ------            ----  ----                   -------
        Normal  SuccessfulCreate  4m    replicaset-controller  Created pod: nginx-6799fc88d8-cgrf2
        Normal  SuccessfulCreate  4m    replicaset-controller  Created pod: nginx-6799fc88d8-mp7j8

    </details>

- [ ] Check `Pod` in your namespace

    ```
    kubectl get pods -n $namespace
    NAME                     READY   STATUS    RESTARTS   AGE
    nginx-6799fc88d8-cgrf2   1/1     Running   0          3m43s
    nginx-6799fc88d8-mp7j8   1/1     Running   0          3m43s
    ```


## Create service for nginx

Create yaml file

```
kubectl create service clusterip nginx --tcp=80:80 --dry-run=client --output yaml > nginx-service.yaml
```

Apply `Service`

```
kubectl apply -f nginx-service.yaml -n $namespace
```

- [ ] Check the created `Service`

    ```
    kubectl get service -n $namespace
    NAME    TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
    nginx   ClusterIP   10.109.93.6   <none>        80/TCP    6s
    ```

Port forward to access to the service from localhost

```
kubectl -n $namespace port-forward service/nginx 8080:80
```

- [ ] Check access to nginx

    - Open http://localhost:8080
    - `curl http://localhost:8080`

        <details>

        ```html
        <!DOCTYPE html>
        <html>
        <head>
        <title>Welcome to nginx!</title>
        <style>
            body {
                width: 35em;
                margin: 0 auto;
                font-family: Tahoma, Verdana, Arial, sans-serif;
            }
        </style>
        </head>
        <body>
        <h1>Welcome to nginx!</h1>
        <p>If you see this page, the nginx web server is successfully installed and
        working. Further configuration is required.</p>

        <p>For online documentation and support please refer to
        <a href="http://nginx.org/">nginx.org</a>.<br/>
        Commercial support is available at
        <a href="http://nginx.com/">nginx.com</a>.</p>

        <p><em>Thank you for using nginx.</em></p>
        </body>
        </html>
        ```

        </details>

## Set nginx image to `1.14.2` (Preparation)

```
kubectl apply -f nginx-deployment-1.14.2.yaml -n $namespace
```

- [ ] Check the image version

```
kubectl get pod -n $namespace -o yaml | grep image:
              f:image: {}
    - image: nginx:1.14.2
      image: nginx:1.14.2
              f:image: {}
    - image: nginx:1.14.2
      image: nginx:1.14.2
```

## Change image from `1.14.2` to `1.15.12`

Check the current image of pods

```
kubectl get pod -n $namespace -o jsonpath='{.items[*].spec.containers[].image}'
```

Check the diff between `nginx-deployment-1.14.2.yaml` and `nginx-deployment-1.15.12.yaml`

```
diff nginx-deployment-1.14.2.yaml nginx-deployment-1.15.12.yaml
<       - image: nginx:1.14.2
---
>       - image: nginx:1.15.12
```

Check the diff with `kubectl`

```
```
