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

## Create nginx with imperative command (命令型)

1. Create nginx

    ```
    kubectl create deployment nginx --image nginx --namespace $namespace
    ```

    - [ ] Check deployment exists in your namespace

        ```
        kubectl get deploy -n $namespace
        NAME    READY   UP-TO-DATE   AVAILABLE   AGE
        nginx   1/1     1            1           71m
        ```

1. Delete nginx

    ```
    kubectl delete deployment nginx -n $namespace
    ```

    - [ ] Check everything is cleaned up

        ```
        kubectl get all -n $namespace
        ```

## Create nginx in a declerative way (宣言型)

Create a kubernetes manifest file (with 2 replicas)

```
kubectl create deployment nginx --image nginx:1.14.2 --replicas=2 --dry-run=client --output yaml > nginx-deployment-1.14.2.yaml
```

```
kubectl apply -f nginx-deployment-1.14.2.yaml -n $namespace
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
            Image:        nginx:1.14.2
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
kubectl diff -f nginx-deployment-1.15.12.yaml -n $namespace
```

<details>

```diff
diff -u -N /var/folders/nb/qvtm13kn74l5s366lg1mzfjc0000gn/T/LIVE-624793422/apps.v1.Deployment.naka.nginx /var/folders/nb/qvtm13kn74l5s366lg1mzfjc0000gn/T/MERGED-277639253/apps.v1.Deployment.naka.nginx
--- /var/folders/nb/qvtm13kn74l5s366lg1mzfjc0000gn/T/LIVE-624793422/apps.v1.Deployment.naka.nginx       2021-03-02 07:43:31.000000000 +0900
+++ /var/folders/nb/qvtm13kn74l5s366lg1mzfjc0000gn/T/MERGED-277639253/apps.v1.Deployment.naka.nginx     2021-03-02 07:43:31.000000000 +0900
@@ -6,7 +6,7 @@
     kubectl.kubernetes.io/last-applied-configuration: |
       {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"creationTimestamp":null,"labels":{"app":"nginx"},"name":"nginx","namespace":"naka"},"spec":{"replicas":2,"selector":{"matchLabels":{"app":"nginx"}},"strategy":{},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx"}},"spec":{"containers":[{"image":"nginx:1.14.2","name":"nginx","resources":{}}]}}},"status":{}}
   creationTimestamp: "2021-03-01T22:43:19Z"
-  generation: 1
+  generation: 2
   labels:
     app: nginx
   managedFields:
@@ -15,6 +15,39 @@
     fieldsV1:
       f:metadata:
         f:annotations:
+          f:deployment.kubernetes.io/revision: {}
+      f:status:
+        f:availableReplicas: {}
+        f:conditions:
+          .: {}
+          k:{"type":"Available"}:
+            .: {}
+            f:lastTransitionTime: {}
+            f:lastUpdateTime: {}
+            f:message: {}
+            f:reason: {}
+            f:status: {}
+            f:type: {}
+          k:{"type":"Progressing"}:
+            .: {}
+            f:lastTransitionTime: {}
+            f:lastUpdateTime: {}
+            f:message: {}
+            f:reason: {}
+            f:status: {}
+            f:type: {}
+        f:observedGeneration: {}
+        f:readyReplicas: {}
+        f:replicas: {}
+        f:updatedReplicas: {}
+    manager: kube-controller-manager
+    operation: Update
+    time: "2021-03-01T22:43:22Z"
+  - apiVersion: apps/v1
+    fieldsType: FieldsV1
+    fieldsV1:
+      f:metadata:
+        f:annotations:
           .: {}
           f:kubectl.kubernetes.io/last-applied-configuration: {}
         f:labels:
@@ -56,40 +89,7 @@
             f:terminationGracePeriodSeconds: {}
     manager: kubectl-client-side-apply
     operation: Update
-    time: "2021-03-01T22:43:19Z"
-  - apiVersion: apps/v1
-    fieldsType: FieldsV1
-    fieldsV1:
-      f:metadata:
-        f:annotations:
-          f:deployment.kubernetes.io/revision: {}
-      f:status:
-        f:availableReplicas: {}
-        f:conditions:
-          .: {}
-          k:{"type":"Available"}:
-            .: {}
-            f:lastTransitionTime: {}
-            f:lastUpdateTime: {}
-            f:message: {}
-            f:reason: {}
-            f:status: {}
-            f:type: {}
-          k:{"type":"Progressing"}:
-            .: {}
-            f:lastTransitionTime: {}
-            f:lastUpdateTime: {}
-            f:message: {}
-            f:reason: {}
-            f:status: {}
-            f:type: {}
-        f:observedGeneration: {}
-        f:readyReplicas: {}
-        f:replicas: {}
-        f:updatedReplicas: {}
-    manager: kube-controller-manager
-    operation: Update
-    time: "2021-03-01T22:43:22Z"
+    time: "2021-03-01T22:43:31Z"
   name: nginx
   namespace: naka
   resourceVersion: "7878112"
@@ -114,7 +114,7 @@
         app: nginx
     spec:
       containers:
-      - image: nginx:1.14.2
+      - image: nginx:1.15.12
         imagePullPolicy: IfNotPresent
         name: nginx
         resources: {}
```

</details>

Apply

```
kubectl apply -f nginx-deployment-1.15.12.yaml -n $namespace
```

- [ ] Check the new image

    ```
    kubectl get po -n $namespace -o jsonpath='{.items[*].spec.containers[].image}'
    nginx:1.15.12 nginx:1.15.12
    ```

- [ ] Check all resources

    ```
    kubectl get all -n $namespace
    ```

    <details>

    ```
    NAME                        READY   STATUS    RESTARTS   AGE
    pod/nginx-fcb5599cb-c82k9   1/1     Running   0          13s
    pod/nginx-fcb5599cb-l7hfg   1/1     Running   0          8s

    NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
    service/nginx   ClusterIP   10.110.182.156   <none>        80/TCP    29s

    NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/nginx   2/2     2            2           36s

    NAME                               DESIRED   CURRENT   READY   AGE
    replicaset.apps/nginx-6799fc88d8   0         0         0       36s
    replicaset.apps/nginx-75d64795db   0         0         0       20s
    replicaset.apps/nginx-fcb5599cb    2         2         2       13s
    ```

    </details>

## Clean up resources

```
kubectl delete -f nginx-deployment-1.14.2.yaml -n $namespace
kubectl delete -f nginx-service.yaml -n $namespace
kubectl delete ns $namespace
```
