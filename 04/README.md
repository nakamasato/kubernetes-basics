# 04 Deploy simple application


## Create your namespace

```
namespace=<yourname>
```

```
kubectl create namespace $namespace
```

## Create nginx with imperative command (in `default` namespace) (命令型)

```
kubectl create deployment nginx-deployment --image nginx
```

```
kubectl get deployment nginx-deployment
```

## Create nginx in a declerative way (宣言型) (in your own namespace)

Create a kubernetes manifest file (with 2 replicas)

```
kubectl create deployment nginx-deployment --image nginx --replicas=2 --dry-run=client --output yaml > nginx-deployment.yaml
```

```
kubectl apply -f nginx-deployment.yaml -n $namespace
```

Check `Deployment` in your namespace

```
kubectl get deployment -n $namespace
```

Check all resources in your namespace

```
kubectl get all -n $namespace
```

```
kubectl describe rs -n $namespace
```

## Create service for nginx

```
kubectl create service nginx-service --dry-run=client --output=yaml > nginx-service.yaml
```
