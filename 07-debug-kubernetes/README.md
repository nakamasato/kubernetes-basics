# Debug Kubernetes

## Prepare resources

```
kubectl apply -f .
```

## Practice `kubectl get` for `Pod` and `Node`

### label & selector


```
kubectl get po -A
kubectl get pod --selector run=nginx -A
```

<details>

```
kubectl get po -A
NAMESPACE     NAME                                     READY   STATUS             RESTARTS   AGE
default       nginx-1                                  0/1     ImagePullBackOff   0          2m58s
default       nginx-2                                  0/1     Pending            0          2m58s
default       nginx-3                                  1/1     Running            0          2m58s
kube-system   coredns-558bd4d5db-2h2mw                 1/1     Running            6          5d20h
kube-system   coredns-558bd4d5db-fzd8l                 1/1     Running            6          5d20h
kube-system   etcd-docker-desktop                      1/1     Running            6          5d20h
kube-system   kube-apiserver-docker-desktop            1/1     Running            6          5d20h
kube-system   kube-controller-manager-docker-desktop   1/1     Running            6          5d20h
kube-system   kube-proxy-klrcv                         1/1     Running            6          5d20h
kube-system   kube-scheduler-docker-desktop            1/1     Running            6          5d20h
kube-system   storage-provisioner                      1/1     Running            12         5d20h
kube-system   vpnkit-controller                        1/1     Running            274        5d20h
test          nginx-4                                  1/1     Running            0          2m58s
```

```
kubectl get pod --selector run=nginx -A
NAMESPACE   NAME      READY   STATUS         RESTARTS   AGE
default     nginx-1   0/1     ErrImagePull   0          119s
default     nginx-2   0/1     Pending        0          119s
default     nginx-3   1/1     Running        0          119s
test        nginx-4   1/1     Running        0          119s
```

</details>


```
kubectl get node
kubectl get node -l beta.kubernetes.io/arch=amd64
```

<details>

```
kubectl get node
NAME             STATUS   ROLES                  AGE     VERSION
docker-desktop   Ready    control-plane,master   5d20h   v1.21.2
```

```
kubectl get node -l beta.kubernetes.io/arch=amd64
NAME             STATUS   ROLES                  AGE     VERSION
docker-desktop   Ready    control-plane,master   5d20h   v1.21.2
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

### output

```
kubectl get pod -o wide
kubectl get node -o wide
```

```
kubectl get pod nginx-1 -o yaml
kubectl get node docker-desktop -o yaml
```

```
kubectl get pod nginx-1 -o json
kubectl get node docker-desktop -o json
```

```
kubectl get pod -o jsonpath='{.items[*].metadata.name}'
kubectl get node -o jsonpath='{.items[*].metadata.name}'
```

### namespace

- Specify a namespace

    ```
    kubectl get pod -n kube-system
    ```

- Check all namespaces

    ```
    kubectl get pod -A
    ```

## Practice Debugging


### Node

#### 1. How to check the status of all nodes in the cluster?

1. List all nodes in the cluster.

    ```
    kubectl get node
    ```

    <details><summary>result</summary>

    ```
    kubectl get node
    NAME             STATUS   ROLES                  AGE    VERSION
    docker-desktop   Ready    control-plane,master   4d2h   v1.21.2
    ```

    </details>

1. With `--selector` or `-l` if there are many nodes in the cluster.

    ```
    kubectl get node -l <key>=<value>
    ```


#### 2. On which node is Pod `nginx-1` running?

1. Check which node `nginx-1` Pod is running on.

    ```
    kubectl get pod nginx-1 -o wide
    ```

    <details><summary>result</summary>

    ```
    kubectl get pod nginx-1 -o wide
    NAME      READY   STATUS             RESTARTS   AGE   IP          NODE             NOMINATED NODE   READINESS GATES
    nginx-1   0/1     ImagePullBackOff   0          98s   10.1.0.31   docker-desktop   <none>           <none>
    ```

    </details>

#### 3. How to check all pods on a specific node?

1. Describe node `docker-desktop`.

    ```
    kubectl describe node docker-desktop
    ```

    <details><summary>result</summary>

    ```
    kubectl describe node docker-desktop
    Name:               docker-desktop
    Roles:              control-plane,master
    Labels:             beta.kubernetes.io/arch=amd64
                        beta.kubernetes.io/os=linux
                        kubernetes.io/arch=amd64
                        kubernetes.io/hostname=docker-desktop
                        kubernetes.io/os=linux
                        node-role.kubernetes.io/control-plane=
                        node-role.kubernetes.io/master=
                        node.kubernetes.io/exclude-from-external-load-balancers=
    Annotations:        kubeadm.alpha.kubernetes.io/cri-socket: /var/run/dockershim.sock
                        node.alpha.kubernetes.io/ttl: 0
                        volumes.kubernetes.io/controller-managed-attach-detach: true
    CreationTimestamp:  Sat, 28 Aug 2021 10:56:19 +0900
    Taints:             <none>
    Unschedulable:      false
    Lease:
      HolderIdentity:  docker-desktop
      AcquireTime:     <unset>
      RenewTime:       Wed, 01 Sep 2021 14:03:43 +0900
    Conditions:
      Type             Status  LastHeartbeatTime                 LastTransitionTime                    Reason                       Message
      ----             ------  -----------------                 ------------------                    ------                       -------
      MemoryPressure   False   Wed, 01 Sep 2021 14:03:36 +0900   Sat, 28 Aug 2021 10:56:15 +0900       KubeletHasSufficientMemory   kubelet has sufficient memory available
      DiskPressure     False   Wed, 01 Sep 2021 14:03:36 +0900   Sat, 28 Aug 2021 10:56:15 +0900       KubeletHasNoDiskPressure     kubelet has no disk pressure
      PIDPressure      False   Wed, 01 Sep 2021 14:03:36 +0900   Sat, 28 Aug 2021 10:56:15 +0900       KubeletHasSufficientPID      kubelet has sufficient PID available
      Ready            True    Wed, 01 Sep 2021 14:03:36 +0900   Sat, 28 Aug 2021 10:56:19 +0900       KubeletReady                 kubelet is posting ready status
    Addresses:
      InternalIP:  192.168.65.4
      Hostname:    docker-desktop
    Capacity:
      cpu:                8
      ephemeral-storage:  61255492Ki
      hugepages-1Gi:      0
      hugepages-2Mi:      0
      memory:             9172456Ki
      pods:               110
    Allocatable:
      cpu:                8
      ephemeral-storage:  56453061334
      hugepages-1Gi:      0
      hugepages-2Mi:      0
      memory:             9070056Ki
      pods:               110
    System Info:
      Machine ID:                 83fed71a-b8c8-4514-9ea5-80bdc2d0e75b
      System UUID:                58194c9d-0000-0000-b87b-b6103835f936
      Boot ID:                    a5c270ef-d474-4dc1-8451-1c1846b27b18
      Kernel Version:             5.10.25-linuxkit
      OS Image:                   Docker Desktop
      Operating System:           linux
      Architecture:               amd64
      Container Runtime Version:  docker://20.10.7
      Kubelet Version:            v1.21.2
      Kube-Proxy Version:         v1.21.2
    Non-terminated Pods:          (12 in total)
      Namespace                   Name                                      CPU Requests  CPU Limits  Memory     Requests  Memory Limits  Age
      ---------                   ----                                      ------------  ----------      ---------------  -------------  ---
      default                     nginx-1                                   0 (0%)        0 (0%)      0     (0%)           0 (0%)         164m
      default                     nginx-3                                   0 (0%)        0 (0%)      0     (0%)           0 (0%)         164m
      kube-system                 coredns-558bd4d5db-2h2mw                  100m (1%)     0 (0%)      70Mi     (0%)        170Mi (1%)     4d3h
      kube-system                 coredns-558bd4d5db-fzd8l                  100m (1%)     0 (0%)      70Mi     (0%)        170Mi (1%)     4d3h
      kube-system                 etcd-docker-desktop                       100m (1%)     0 (0%)      100Mi     (1%)       0 (0%)         4d3h
      kube-system                 kube-apiserver-docker-desktop             250m (3%)     0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 kube-controller-manager-docker-desktop    200m (2%)     0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 kube-proxy-klrcv                          0 (0%)        0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 kube-scheduler-docker-desktop             100m (1%)     0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 storage-provisioner                       0 (0%)        0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 vpnkit-controller                         0 (0%)        0 (0%)      0     (0%)           0 (0%)         4d3h
      test                        nginx-4                                   0 (0%)        0 (0%)      0     (0%)           0 (0%)         164m
    Allocated resources:
      (Total limits may be over 100 percent, i.e., overcommitted.)
      Resource           Requests    Limits
      --------           --------    ------
      cpu                850m (10%)  0 (0%)
      memory             240Mi (2%)  340Mi (3%)
      ephemeral-storage  0 (0%)      0 (0%)
      hugepages-1Gi      0 (0%)      0 (0%)
      hugepages-2Mi      0 (0%)      0 (0%)
    Events:              <none>
    ```

    </details>

    You can see the pods in `Non-terminated Pods` field:

    ```
    Non-terminated Pods:          (12 in total)
      Namespace                   Name                                      CPU Requests  CPU Limits  Memory     Requests  Memory Limits  Age
      ---------                   ----                                      ------------  ----------      ---------------  -------------  ---
      default                     nginx-1                                   0 (0%)        0 (0%)      0     (0%)           0 (0%)         164m
      default                     nginx-3                                   0 (0%)        0 (0%)      0     (0%)           0 (0%)         164m
      kube-system                 coredns-558bd4d5db-2h2mw                  100m (1%)     0 (0%)      70Mi     (0%)        170Mi (1%)     4d3h
      kube-system                 coredns-558bd4d5db-fzd8l                  100m (1%)     0 (0%)      70Mi     (0%)        170Mi (1%)     4d3h
      kube-system                 etcd-docker-desktop                       100m (1%)     0 (0%)      100Mi     (1%)       0 (0%)         4d3h
      kube-system                 kube-apiserver-docker-desktop             250m (3%)     0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 kube-controller-manager-docker-desktop    200m (2%)     0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 kube-proxy-klrcv                          0 (0%)        0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 kube-scheduler-docker-desktop             100m (1%)     0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 storage-provisioner                       0 (0%)        0 (0%)      0     (0%)           0 (0%)         4d3h
      kube-system                 vpnkit-controller                         0 (0%)        0 (0%)      0     (0%)           0 (0%)         4d3h
      test                        nginx-4                                   0 (0%)        0 (0%)      0     (0%)           0 (0%)         164m
    ```

### Pod
#### 1. Why isn't Pod `nginx-1` running?

##### 1. `kubectl describe pod`

1. Describe Pod `nginx-1`
    ```
    kubectl describe pod nginx-1
    ```
    <details><summary>result</summary>

    ```
    kubectl describe pod nginx-1
    Name:         nginx-1
    Namespace:    default
    Priority:     0
    Node:         docker-desktop/192.168.65.4
    Start Time:   Wed, 01 Sep 2021 11:18:49 +0900
    Labels:       run=nginx
    Annotations:  <none>
    Status:       Pending
    IP:           10.1.0.31
    IPs:
      IP:  10.1.0.31
    Containers:
      nginx:
        Container ID:
        Image:          wrong-nginx
        Image ID:
        Port:           <none>
        Host Port:      <none>
        State:          Waiting
          Reason:       ImagePullBackOff
        Ready:          False
        Restart Count:  0
        Environment:    <none>
        Mounts:
          /var/run/secrets/kubernetes.io/serviceaccount     from kube-api-access-xvznf (ro)
    Conditions:
      Type              Status
      Initialized       True
      Ready             False
      ContainersReady   False
      PodScheduled      True
    Volumes:
      kube-api-access-xvznf:
        Type:                    Projected (a volume     that contains injected data from multiple     sources)
        TokenExpirationSeconds:  3607
        ConfigMapName:           kube-root-ca.crt
        ConfigMapOptional:       <nil>
        DownwardAPI:             true
    QoS Class:                   BestEffort
    Node-Selectors:              <none>
    Tolerations:                 node.kubernetes.io/    not-ready:NoExecute op=Exists for 300s
                                 node.kubernetes.io/    unreachable:NoExecute     op=Exists for 300s
    Events:
      Type     Reason     Age                      From               Message
      ----     ------     ----                     ----               -------
      Normal   Scheduled  2m15s                    default-scheduler  Successfully assigned default/    nginx-1 to docker-desktop
      Normal   Pulling    35s (x4 over 2m15s)      kubelet            Pulling image "wrong-nginx"
      Warning  Failed     32s (x4 over 2m11s)      kubelet            Failed to pull image     "wrong-nginx": rpc error: code = Unknown desc =     Error response from daemon: pull access denied for     wrong-nginx, repository does not exist or may     require 'docker login': denied: requested access     to the resource is denied
      Warning  Failed     32s (x4 over 2m11s)      kubelet            Error: ErrImagePull
      Warning  Failed     18s (x6 over 2m10s)      kubelet            Error: ImagePullBackOff
      Normal   BackOff    4s (x7 over 2m10s)       kubelet            Back-off pulling image     "wrong-nginx"
    ```

    </details>

1. Check `Events` in the result.

    ```
      Normal   Pulling    35s (x4 over 2m15s)          kubelet            Pulling image "wrong-nginx"
      Warning  Failed     32s (x4 over 2m11s)          kubelet            Failed to pull image         "wrong-nginx": rpc error: code = Unknown desc     =     Error response from daemon: pull access     denied for     wrong-nginx, repository does not     exist or may     require 'docker login': denied:     requested access     to the resource is denied
      Warning  Failed     32s (x4 over 2m11s)          kubelet            Error: ErrImagePull
      Warning  Failed     18s (x6 over 2m10s)          kubelet            Error: ImagePullBackOff
      Normal   BackOff    4s (x7 over 2m10s)           kubelet            Back-off pulling image         "wrong-nginx"
    ```

    You can see `Error response from daemon: pull access     denied for     wrong-nginx, repository does not     exist or may     require 'docker login': denied:     requested access     to the resource is denied`

##### 2. `kubectl get pod` with `-o yaml` option

1. Get pod `nginx-1` with `-o yaml`. (Another way to check)

    ```
    kubectl get pod nginx-1 -o yaml
    ```

    <details><summary>result</summary>

    ```
    kubectl get pod nginx-1 -o yaml
    apiVersion: v1
    kind: Pod
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"creationTimestamp":null,"labels":    {"run":"nginx"},"name":"nginx-1","namespace":"default"},"spec":{"containers":[{"image":"wrong-nginx",    "name":"nginx","resources":{}}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always"},"status":{}}
      creationTimestamp: "2021-09-01T02:18:49Z"
      labels:
        run: nginx
      name: nginx-1
      namespace: default
      resourceVersion: "144889"
      uid: 5c475329-40e9-4a7b-bfd2-22bf6acb615f
    spec:
      containers:
      - image: wrong-nginx
        imagePullPolicy: Always
        name: nginx
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-xvznf
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: docker-desktop
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: default
      serviceAccountName: default
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - name: kube-api-access-xvznf
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2021-09-01T02:18:49Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2021-09-01T02:18:49Z"
        message: 'containers with unready status: [nginx]'
        reason: ContainersNotReady
        status: "False"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2021-09-01T02:18:49Z"
        message: 'containers with unready status: [nginx]'
        reason: ContainersNotReady
        status: "False"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2021-09-01T02:18:49Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - image: wrong-nginx
        imageID: ""
        lastState: {}
        name: nginx
        ready: false
        restartCount: 0
        started: false
        state:
          waiting:
            message: Back-off pulling image "wrong-nginx"
            reason: ImagePullBackOff
      hostIP: 192.168.65.4
      phase: Pending
      podIP: 10.1.0.31
      podIPs:
      - ip: 10.1.0.31
      qosClass: BestEffort
      startTime: "2021-09-01T02:18:49Z"
    ```

    </details>


1. Check `containerStatuses`.

    ```yaml
          containerStatuses:
          - image: wrong-nginx
            imageID: ""
            lastState: {}
            name: nginx
            ready: false
            restartCount: 0
            started: false
            state:
              waiting:
                message: Back-off pulling image "wrong-nginx"
                reason: ImagePullBackOff
    ```

    You can see `reason: ImagePullBackOff` and `message: Back-off pulling image "wrong-nginx"`


#### 2. Why isn't `nginx-2` running?

1. Describe the Pod.

    ```
    kubectl describe pod nginx-2
    ```

    <details><summary>result</summary>


    ```
    kubectl describe pod nginx-2
    Name:         nginx-2
    Namespace:    default
    Priority:     0
    Node:         <none>
    Labels:       run=nginx-2
    Annotations:  <none>
    Status:       Pending
    IP:
    IPs:          <none>
    Containers:
      nginx-2:
        Image:        nginx
        Port:         <none>
        Host Port:    <none>
        Environment:  <none>
        Mounts:
          /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-574ts (ro)
    Conditions:
      Type           Status
      PodScheduled   False
    Volumes:
      kube-api-access-574ts:
        Type:                    Projected (a volume that contains injected data from multiple sources)
        TokenExpirationSeconds:  3607
        ConfigMapName:           kube-root-ca.crt
        ConfigMapOptional:       <nil>
        DownwardAPI:             true
    QoS Class:                   BestEffort
    Node-Selectors:              nodeType=test
    Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
    Events:
      Type     Reason            Age                  From               Message
      ----     ------            ----                 ----               -------
      Warning  FailedScheduling  48s (x4 over 2m52s)  default-scheduler  0/1 nodes are available: 1 node    (s) didn't match Pod's node affinity/selector.
    ```

    </details>


    ```
    Events:
      Type     Reason            Age                  From               Message
      ----     ------            ----                 ----               -------
      Warning  FailedScheduling  48s (x4 over 2m52s)  default-scheduler  0/1 nodes are available: 1 node    (s) didn't match Pod's node affinity/selector.
    ```

    The pod chouldn't be scheduled:  `Warning  FailedScheduling  48s (x4 over 2m52s)  default-scheduler  0/1 nodes are available: 1 node    (s) didn't match Pod's node affinity/selector.`

    → `nginx-2` has `nodeSelector` with `nodeType: test`. There's no matched nodes in the cluster.

#### 3. How to check container logs of Pod `nginx-3`?

- Command: `kubectl logs <pod_name> <options>`
- Important Options:
    - `-f`, `--follow=false`: Specify if the logs should be streamed.
    - `--tail=-1`: Lines of recent log file to display. Defaults to -1 with no selector, showing all log lines otherwise 10, if a selector is provided.
    - `-c`, `--container=''`: Print the logs of this container


1. Check the logs of `nginx-3` Pod.

    ```
    kubectl logs nginx-3 -f --tail 20
    ```

1. Send some requests to the Pod.

    ```
    kubectl port-forward pod/nginx-3 8080:80
    ```

    Open http://localhost:8080 -> You can see the folloing log

    ```
    127.0.0.1 - - [01/Sep/2021:23:15:35 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36" "-"
    ```

    Open http://localhost:8080/aaaa -> You can see the folloing log

    ```
    2021/09/01 23:16:35 [error] 32#32: *3 open() "/usr/share/nginx/html/aaa" failed (2: No such file or directory), client: 127.0.0.1, server: localhost, request: "GET /aaa HTTP/1.1", host: "localhost:8080"
    127.0.0.1 - - [01/Sep/2021:23:16:35 +0000] "GET /aaa HTTP/1.1" 404 555 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36" "-"
    ```

### Service
#### 1. How to check if a service is available?

##### 1. Port-forward `nginx` service and check by sending request.

```
kubectl port-forward svc/nginx-1 8080:80
```

Open http://localhost:8080 on your browser or hit the localhost:8080 by a command e.g. `curl`

##### 2. Check `Endpoints` resource.


1. Get `Endpoints` resource

    ```
    kubectl get endpoints nginx-1
    ```

    <details><summary>result</summary>

    ```
    kubectl get endpoints nginx-1
    NAME      ENDPOINTS   AGE
    nginx-1   <none>      32s
    ```

    <details>

    Only available PodIp will be shown.

1. Describe `Endpoints` resource.

    ```
    kubectl describe endpoints nginx-1
    ```

    <details><summary>result</summary>

    ```
    kubectl describe endpoints nginx-1
    Name:         nginx-1
    Namespace:    default
    Labels:       run=nginx
    Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2021-09-01T23:37:01Z
    Subsets:
      Addresses:          10.1.0.53
      NotReadyAddresses:  10.1.0.52
      Ports:
        Name  Port  Protocol
        ----  ----  --------
        80    80    TCP

    Events:  <none>
    ```

    </details>

    - `Addresses:          10.1.0.53`: Pod ips for pods that are ready.
    - `NotReadyAddresses:  10.1.0.52`: Pod ips for pods that are not ready.

1. Check Pod Ips.

    ```
    kubectl get pod -o wide
    ```

    <details><summary>result</summary>

    ```
    kubectl get pod -o wide
    NAME      READY   STATUS         RESTARTS   AGE   IP          NODE             NOMINATED NODE   READINESS GATES
    nginx-1   0/1     ErrImagePull   0          74s   10.1.0.52   docker-desktop   <none>           <none>
    nginx-2   0/1     Pending        0          74s   <none>      <none>           <none>           <none>
    nginx-3   1/1     Running        0          74s   10.1.0.53   docker-desktop   <none>           <none>
    ```

    </details>

#### 2. Why is Service `nginx-2` unavailable?

1. Describe `Endpoints`

    ```
    kubectl describe ep nginx-2
    ```

    ```
    kubectl describe ep nginx-2
    Name:         nginx-2
    Namespace:    default
    Labels:       run=nginx
    Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2021-09-01T23:36:54Z
    Subsets:
    Events:  <none>
    ```

    There's no `Subsets` -> Should be no matching Pods.

1. Check `Service`'s `selector`

    ```
    kubectl get svc nginx-2 -o yaml
    ```

    <details><summary>result</summary>

    ```
    kubectl get svc nginx-2 -o yaml
    apiVersion: v1
    kind: Service
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"creationTimestamp":null,    "labels":{"run":"nginx"},"name":"nginx-2","namespace":"default"},"spec":{"ports":[{"name":"80",    "port":80,"protocol":"TCP","targetPort":80}],"selector":{"run":"nonexisting"},    "type":"ClusterIP"},"status":{"loadBalancer":{}}}
      creationTimestamp: "2021-09-01T23:36:54Z"
      labels:
        run: nginx
      name: nginx-2
      namespace: default
      resourceVersion: "182442"
      uid: b51378b1-c273-4004-b2d9-87c26d8e6a5a
    spec:
      clusterIP: 10.108.232.128
      clusterIPs:
      - 10.108.232.128
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - name: "80"
        port: 80
        protocol: TCP
        targetPort: 80
      selector:
        run: nonexisting
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
    ```

    </details>


    ```yaml
      selector:
        run: nonexisting
    ```

    There's no Pod with such a label.

    ```
    kubectl get po --show-labels
    NAME      READY   STATUS             RESTARTS   AGE   LABELS
    nginx-1   0/1     ImagePullBackOff   0          10m   run=nginx
    nginx-2   0/1     Pending            0          10m   run=nginx
    nginx-3   1/1     Running            0          10m   run=nginx
    ```

**Tips**:
1. Check if there's matching Pods.
1. Check if matched Pods are in `Running` state.
1. Check if `port` is correct.
## Summary

Commonly used `kubectl` commands for debugging:

1. `kubectl get pod -A`
1. `kubectl get pod <pod_name> -o wide`
1. `kubectl logs <pod_name> --tail=20 -f`
1. `kubectl port-forward svc/<service_name> <local_port>:<service_port>`
1. `kubectl get endpoints <service_name>`
1. `kubectl get node`
1. `kubectl describe node <node_name>`

For more details: [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
## Clean up

1. Clean up the resources:

    ```
    kubectl delete -f .
    ```
