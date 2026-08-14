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
NAMESPACE            NAME                                            READY   STATUS         RESTARTS   AGE
default              nginx-1                                         0/1     ErrImagePull   0          6s
default              nginx-2                                         0/1     Pending        0          6s
default              nginx-3                                         1/1     Running        0          6s
kube-system          coredns-674b8bbfcf-dtms5                        1/1     Running        0          67m
kube-system          coredns-674b8bbfcf-mlj6k                        1/1     Running        0          67m
kube-system          etcd-desktop-control-plane                      1/1     Running        0          67m
kube-system          kindnet-n4fjq                                   1/1     Running        0          67m
kube-system          kube-apiserver-desktop-control-plane            1/1     Running        0          67m
kube-system          kube-controller-manager-desktop-control-plane   1/1     Running        0          67m
kube-system          kube-proxy-zls4t                                1/1     Running        0          67m
kube-system          kube-scheduler-desktop-control-plane            1/1     Running        0          67m
local-path-storage   local-path-provisioner-7dc846544d-c2gl7         1/1     Running        0          67m
test                 nginx-4                                         1/1     Running        0          6s
```

```
kubectl get pod --selector run=nginx -A
NAMESPACE   NAME      READY   STATUS         RESTARTS   AGE
default     nginx-1   0/1     ErrImagePull   0          6s
default     nginx-2   0/1     Pending        0          6s
default     nginx-3   1/1     Running        0          6s
test        nginx-4   1/1     Running        0          6s
```

</details>

```
kubectl get node
kubectl get node -l kubernetes.io/arch=amd64
```

<details>

```
kubectl get node
NAME                    STATUS   ROLES           AGE   VERSION
desktop-control-plane   Ready    control-plane   67m   v1.33.1
```

```
kubectl get node -l kubernetes.io/arch=amd64
No resources found
```

</details>

arm mac

```
kubectl get node
kubectl get node -l kubernetes.io/arch=arm64
```

<details>

```
kubectl get node
NAME                    STATUS   ROLES           AGE   VERSION
desktop-control-plane   Ready    control-plane   67m   v1.33.1
```

```
kubectl get node -l kubernetes.io/arch=arm64
NAME                    STATUS   ROLES           AGE   VERSION
desktop-control-plane   Ready    control-plane   67m   v1.33.1
```

</details>

```
kubectl get po --show-labels
kubectl get node --show-labels
```

<details>

```
kubectl get po --show-labels
NAME      READY   STATUS         RESTARTS   AGE   LABELS
nginx-1   0/1     ErrImagePull   0          6s    run=nginx
nginx-2   0/1     Pending        0          6s    run=nginx
nginx-3   1/1     Running        0          6s    run=nginx
```

```
kubectl get node --show-labels
NAME                    STATUS   ROLES           AGE   VERSION   LABELS
desktop-control-plane   Ready    control-plane   67m   v1.33.1   beta.kubernetes.io/arch=arm64,beta.kubernetes.io/os=linux,kubernetes.io/arch=arm64,kubernetes.io/hostname=desktop-control-plane,kubernetes.io/os=linux,node-role.kubernetes.io/control-plane=
```

</details>

### output

```
kubectl get pod -o wide
kubectl get node -o wide
```

```
kubectl get pod nginx-1 -o yaml
kubectl get node desktop-control-plane -o yaml
```

```
kubectl get pod nginx-1 -o json
kubectl get node desktop-control-plane -o json
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

    <details>

    ```
    kubectl get node
    NAME                    STATUS   ROLES           AGE   VERSION
    desktop-control-plane   Ready    control-plane   67m   v1.33.1
    ```

    </details>

1. With `--selector` or `-l` if there are many nodes in the cluster.

    ```
    kubectl get node -l <key>=<value>
    ```

#### 2. On which node is Pod `nginx-1` running?

1. Check which node `nginx-1` Pod is running on.

    <details>

    ```
    kubectl get pod nginx-1 -o wide
    NAME      READY   STATUS         RESTARTS   AGE   IP            NODE                    NOMINATED NODE   READINESS GATES
    nginx-1   0/1     ErrImagePull   0          7s    10.244.0.72   desktop-control-plane   <none>           <none>
    ```

    </details>

#### 3. How to check all pods on a specific node?

1. Describe node `desktop-control-plane`.

    <details>

    ```
    kubectl describe node desktop-control-plane
    Name:               desktop-control-plane
    Roles:              control-plane
    Labels:             beta.kubernetes.io/arch=arm64
                        beta.kubernetes.io/os=linux
                        kubernetes.io/arch=arm64
                        kubernetes.io/hostname=desktop-control-plane
                        kubernetes.io/os=linux
                        node-role.kubernetes.io/control-plane=
    Annotations:        kubeadm.alpha.kubernetes.io/cri-socket: unix:///run/containerd/containerd.sock
                        node.alpha.kubernetes.io/ttl: 0
                        volumes.kubernetes.io/controller-managed-attach-detach: true
    CreationTimestamp:  Fri, 14 Aug 2026 23:23:45 +0900
    Taints:             <none>
    Unschedulable:      false
    Lease:
      HolderIdentity:  desktop-control-plane
      AcquireTime:     <unset>
      RenewTime:       Sat, 15 Aug 2026 00:30:56 +0900
    Conditions:
      Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
      ----             ------  -----------------                 ------------------                ------                       -------
      MemoryPressure   False   Sat, 15 Aug 2026 00:30:45 +0900   Fri, 14 Aug 2026 23:23:42 +0900   KubeletHasSufficientMemory   kubelet has sufficient memory available
      DiskPressure     False   Sat, 15 Aug 2026 00:30:45 +0900   Fri, 14 Aug 2026 23:23:42 +0900   KubeletHasNoDiskPressure     kubelet has no disk pressure
      PIDPressure      False   Sat, 15 Aug 2026 00:30:45 +0900   Fri, 14 Aug 2026 23:23:42 +0900   KubeletHasSufficientPID      kubelet has sufficient PID available
      Ready            True    Sat, 15 Aug 2026 00:30:45 +0900   Fri, 14 Aug 2026 23:24:04 +0900   KubeletReady                 kubelet is posting ready status
    Addresses:
      InternalIP:  172.18.0.3
      Hostname:    desktop-control-plane
    Capacity:
      cpu:                8
      ephemeral-storage:  474095688Ki
      hugepages-1Gi:      0
      hugepages-2Mi:      0
      hugepages-32Mi:     0
      hugepages-64Ki:     0
      memory:             8025700Ki
      pods:               110
    Allocatable:
      cpu:                8
      ephemeral-storage:  474095688Ki
      hugepages-1Gi:      0
      hugepages-2Mi:      0
      hugepages-32Mi:     0
      hugepages-64Ki:     0
      memory:             8025700Ki
      pods:               110
    System Info:
      Machine ID:                 de7a8bf9bda64c91a09b4ef9930ae150
      System UUID:                de7a8bf9bda64c91a09b4ef9930ae150
      Boot ID:                    e4b83f9a-ff7a-4f1e-a834-05a5268a9ed2
      Kernel Version:             6.10.14-linuxkit
      OS Image:                   Debian GNU/Linux 12 (bookworm)
      Operating System:           linux
      Architecture:               arm64
      Container Runtime Version:  containerd://2.1.1
      Kubelet Version:            v1.33.1
      Kube-Proxy Version:
    PodCIDR:                      10.244.0.0/24
    PodCIDRs:                     10.244.0.0/24
    ProviderID:                   kind://docker/desktop/desktop-control-plane
    Non-terminated Pods:          (12 in total)
      Namespace                   Name                                             CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
      ---------                   ----                                             ------------  ----------  ---------------  -------------  ---
      default                     nginx-1                                          0 (0%)        0 (0%)      0 (0%)           0 (0%)         7s
      default                     nginx-3                                          0 (0%)        0 (0%)      0 (0%)           0 (0%)         7s
      kube-system                 coredns-674b8bbfcf-dtms5                         100m (1%)     0 (0%)      70Mi (0%)        170Mi (2%)     67m
      kube-system                 coredns-674b8bbfcf-mlj6k                         100m (1%)     0 (0%)      70Mi (0%)        170Mi (2%)     67m
      kube-system                 etcd-desktop-control-plane                       100m (1%)     0 (0%)      100Mi (1%)       0 (0%)         67m
      kube-system                 kindnet-n4fjq                                    100m (1%)     100m (1%)   50Mi (0%)        50Mi (0%)      67m
      kube-system                 kube-apiserver-desktop-control-plane             250m (3%)     0 (0%)      0 (0%)           0 (0%)         67m
      kube-system                 kube-controller-manager-desktop-control-plane    200m (2%)     0 (0%)      0 (0%)           0 (0%)         67m
      kube-system                 kube-proxy-zls4t                                 0 (0%)        0 (0%)      0 (0%)           0 (0%)         67m
      kube-system                 kube-scheduler-desktop-control-plane             100m (1%)     0 (0%)      0 (0%)           0 (0%)         67m
      local-path-storage          local-path-provisioner-7dc846544d-c2gl7          0 (0%)        0 (0%)      0 (0%)           0 (0%)         67m
      test                        nginx-4                                          0 (0%)        0 (0%)      0 (0%)           0 (0%)         7s
    Allocated resources:
      (Total limits may be over 100 percent, i.e., overcommitted.)
      Resource           Requests    Limits
      --------           --------    ------
      cpu                950m (11%)  100m (1%)
      memory             290Mi (3%)  390Mi (4%)
      ephemeral-storage  0 (0%)      0 (0%)
      hugepages-1Gi      0 (0%)      0 (0%)
      hugepages-2Mi      0 (0%)      0 (0%)
      hugepages-32Mi     0 (0%)      0 (0%)
      hugepages-64Ki     0 (0%)      0 (0%)
    Events:              <none>
    ```

    </details>

    You can see the pods in `Non-terminated Pods` field:

    ```
    Non-terminated Pods:          (12 in total)
      Namespace                   Name                                             CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
      ---------                   ----                                             ------------  ----------  ---------------  -------------  ---
      default                     nginx-1                                          0 (0%)        0 (0%)      0 (0%)           0 (0%)         2m5s
      default                     nginx-3                                          0 (0%)        0 (0%)      0 (0%)           0 (0%)         2m5s
      kube-system                 coredns-674b8bbfcf-dtms5                         100m (1%)     0 (0%)      70Mi (0%)        170Mi (2%)     57m
      kube-system                 coredns-674b8bbfcf-mlj6k                         100m (1%)     0 (0%)      70Mi (0%)        170Mi (2%)     57m
      kube-system                 etcd-desktop-control-plane                       100m (1%)     0 (0%)      100Mi (1%)       0 (0%)         57m
      kube-system                 kindnet-n4fjq                                    100m (1%)     100m (1%)   50Mi (0%)        50Mi (0%)      57m
      kube-system                 kube-apiserver-desktop-control-plane             250m (3%)     0 (0%)      0 (0%)           0 (0%)         57m
      kube-system                 kube-controller-manager-desktop-control-plane    200m (2%)     0 (0%)      0 (0%)           0 (0%)         57m
      kube-system                 kube-proxy-zls4t                                 0 (0%)        0 (0%)      0 (0%)           0 (0%)         57m
      kube-system                 kube-scheduler-desktop-control-plane             100m (1%)     0 (0%)      0 (0%)           0 (0%)         57m
      local-path-storage          local-path-provisioner-7dc846544d-c2gl7          0 (0%)        0 (0%)      0 (0%)           0 (0%)         57m
      test                        nginx-4                                          0 (0%)        0 (0%)      0 (0%)           0 (0%)         2m5s
    ```

### Pod
#### 1. Why isn't Pod `nginx-1` running?

##### 1. `kubectl describe pod`

1. Describe Pod `nginx-1`

    <details>

    ```
    kubectl describe pod nginx-1
    Name:             nginx-1
    Namespace:        default
    Priority:         0
    Service Account:  default
    Node:             desktop-control-plane/172.18.0.3
    Start Time:       Sat, 15 Aug 2026 00:30:50 +0900
    Labels:           run=nginx
    Annotations:      <none>
    Status:           Pending
    IP:               10.244.0.72
    IPs:
      IP:  10.244.0.72
    Containers:
      nginx:
        Container ID:
        Image:          wrong-nginx
        Image ID:
        Port:           <none>
        Host Port:      <none>
        State:          Waiting
          Reason:       ErrImagePull
        Ready:          False
        Restart Count:  0
        Environment:    <none>
        Mounts:
          /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-hpgjv (ro)
    Conditions:
      Type                        Status
      PodReadyToStartContainers   True
      Initialized                 True
      Ready                       False
      ContainersReady             False
      PodScheduled                True
    Volumes:
      kube-api-access-hpgjv:
        Type:                    Projected (a volume that contains injected data from multiple sources)
        TokenExpirationSeconds:  3607
        ConfigMapName:           kube-root-ca.crt
        Optional:                false
        DownwardAPI:             true
    QoS Class:                   BestEffort
    Node-Selectors:              <none>
    Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
    Events:
      Type     Reason     Age   From               Message
      ----     ------     ----  ----               -------
      Normal   Scheduled  7s    default-scheduler  Successfully assigned default/nginx-1 to desktop-control-plane
      Normal   Pulling    7s    kubelet            Pulling image "wrong-nginx"
      Warning  Failed     4s    kubelet            Failed to pull image "wrong-nginx": failed to pull and unpack image "docker.io/library/wrong-nginx:latest": failed to resolve reference "docker.io/library/wrong-nginx:latest": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
      Warning  Failed     4s    kubelet            Error: ErrImagePull
      Normal   BackOff    3s    kubelet            Back-off pulling image "wrong-nginx"
      Warning  Failed     3s    kubelet            Error: ImagePullBackOff
    ```

    </details>

1. Check `Events` in the result.

    ```
    Events:
      Type     Reason     Age                 From               Message
      ----     ------     ----                ----               -------
      Normal   Scheduled  2m5s                default-scheduler  Successfully assigned default/nginx-1 to desktop-control-plane
      Normal   Pulling    24s (x4 over 2m4s)  kubelet            Pulling image "wrong-nginx"
      Warning  Failed     22s (x4 over 2m2s)  kubelet            Failed to pull image "wrong-nginx": failed to pull and unpack image "docker.io/library/wrong-nginx:latest": failed to resolve reference "docker.io/library/wrong-nginx:latest": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
      Warning  Failed     22s (x4 over 2m2s)  kubelet            Error: ErrImagePull
      Normal   BackOff    10s (x6 over 2m1s)  kubelet            Back-off pulling image "wrong-nginx"
      Warning  Failed     10s (x6 over 2m1s)  kubelet            Error: ImagePullBackOff
    ```

    You can see `pull access denied, repository does not exist or may require authorization`

##### 2. `kubectl get pod` with `-o yaml` option

1. Get pod `nginx-1` with `-o yaml`. (Another way to check)

    <details>

    ```
    kubectl get pod nginx-1 -o yaml
    apiVersion: v1
    kind: Pod
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"creationTimestamp":null,"labels":{"run":"nginx"},"name":"nginx-1","namespace":"default"},"spec":{"containers":[{"image":"wrong-nginx","name":"nginx","resources":{}}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always"},"status":{}}
      creationTimestamp: "2026-08-14T15:30:50Z"
      generation: 1
      labels:
        run: nginx
      name: nginx-1
      namespace: default
      resourceVersion: "8033"
      uid: 63b3b6ed-a423-4523-8e32-714a360cb057
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
          name: kube-api-access-hpgjv
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: desktop-control-plane
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
      - name: kube-api-access-hpgjv
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
        lastTransitionTime: "2026-08-14T15:30:54Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2026-08-14T15:30:50Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2026-08-14T15:30:50Z"
        message: 'containers with unready status: [nginx]'
        reason: ContainersNotReady
        status: "False"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2026-08-14T15:30:50Z"
        message: 'containers with unready status: [nginx]'
        reason: ContainersNotReady
        status: "False"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2026-08-14T15:30:50Z"
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
            message: 'failed to pull and unpack image "docker.io/library/wrong-nginx:latest":
              failed to resolve reference "docker.io/library/wrong-nginx:latest": pull
              access denied, repository does not exist or may require authorization: server
              message: insufficient_scope: authorization failed'
            reason: ErrImagePull
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-hpgjv
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 172.18.0.3
      hostIPs:
      - ip: 172.18.0.3
      phase: Pending
      podIP: 10.244.0.72
      podIPs:
      - ip: 10.244.0.72
      qosClass: BestEffort
      startTime: "2026-08-14T15:30:50Z"
    ```

    </details>

    You can see `reason: ImagePullBackOff` and `message: Back-off pulling image "wrong-nginx"`

#### 2. Why isn't `nginx-2` running?

1. Describe the Pod.

    <details>

    ```
    kubectl describe pod nginx-2
    Name:             nginx-2
    Namespace:        default
    Priority:         0
    Service Account:  default
    Node:             <none>
    Labels:           run=nginx
    Annotations:      <none>
    Status:           Pending
    IP:
    IPs:              <none>
    Containers:
      nginx:
        Image:        nginx
        Port:         <none>
        Host Port:    <none>
        Environment:  <none>
        Mounts:
          /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-pwbzp (ro)
    Conditions:
      Type           Status
      PodScheduled   False
    Volumes:
      kube-api-access-pwbzp:
        Type:                    Projected (a volume that contains injected data from multiple sources)
        TokenExpirationSeconds:  3607
        ConfigMapName:           kube-root-ca.crt
        Optional:                false
        DownwardAPI:             true
    QoS Class:                   BestEffort
    Node-Selectors:              nodeType=test
    Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
    Events:
      Type     Reason            Age   From               Message
      ----     ------            ----  ----               -------
      Warning  FailedScheduling  7s    default-scheduler  0/1 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
    ```

    </details>

    ```
    Events:
      Type     Reason            Age   From               Message
      ----     ------            ----  ----               -------
      Warning  FailedScheduling  2m5s  default-scheduler  0/1 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
    ```

    The pod couldn't be scheduled: `0/1 nodes are available: 1 node(s) didn't match Pod's node affinity/selector.`

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

    Open http://localhost:8080 -> You can see the following log

    ```
    127.0.0.1 - - [01/Sep/2021:23:15:35 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36" "-"
    ```

    Open http://localhost:8080/aaaa -> You can see the following log

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

##### 2. Check `EndpointSlice` resource.

1. Get `EndpointSlice` resource

    <details>

    ```
    kubectl get endpointslice -l kubernetes.io/service-name=nginx-1
    NAME            ADDRESSTYPE   PORTS   ENDPOINTS                 AGE
    nginx-1-2vhb2   IPv4          80      10.244.0.73,10.244.0.72   7s
    ```

    </details>

    Only ready and not-ready Pod IPs backing the Service are shown.

1. Describe `EndpointSlice` resource.

    <details>

    ```
    kubectl describe endpointslice -l kubernetes.io/service-name=nginx-1
    Name:         nginx-1-2vhb2
    Namespace:    default
    Labels:       endpointslice.kubernetes.io/managed-by=endpointslice-controller.k8s.io
                  kubernetes.io/service-name=nginx-1
                  run=nginx
    Annotations:  <none>
    AddressType:  IPv4
    Ports:
      Name  Port  Protocol
      ----  ----  --------
      80    80    TCP
    Endpoints:
      - Addresses:  10.244.0.73
        Conditions:
          Ready:    true
        Hostname:   <unset>
        TargetRef:  Pod/nginx-3
        NodeName:   desktop-control-plane
        Zone:       <unset>
      - Addresses:  10.244.0.72
        Conditions:
          Ready:    false
        Hostname:   <unset>
        TargetRef:  Pod/nginx-1
        NodeName:   desktop-control-plane
        Zone:       <unset>
    Events:         <none>
    ```

    </details>

    - `Conditions.Ready: true`: the Pod behind that address is ready to receive traffic.
    - `Conditions.Ready: false`: the Pod is registered but not ready.
    - `TargetRef` tells you which Pod each address belongs to.

1. Check Pod Ips.

    <details>

    ```
    kubectl get pod -o wide
    NAME      READY   STATUS         RESTARTS   AGE   IP            NODE                    NOMINATED NODE   READINESS GATES
    nginx-1   0/1     ErrImagePull   0          7s    10.244.0.72   desktop-control-plane   <none>           <none>
    nginx-2   0/1     Pending        0          7s    <none>        <none>                  <none>           <none>
    nginx-3   1/1     Running        0          7s    10.244.0.73   desktop-control-plane   <none>           <none>
    ```

    </details>

#### 2. Why is Service `nginx-2` unavailable?

1. Describe `EndpointSlice`

    ```
    kubectl describe endpointslice -l kubernetes.io/service-name=nginx-2
    Name:         nginx-2-r8fsm
    Namespace:    default
    Labels:       endpointslice.kubernetes.io/managed-by=endpointslice-controller.k8s.io
                  kubernetes.io/service-name=nginx-2
                  run=nginx
    Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2026-08-14T15:30:50Z
    AddressType:  IPv4
    Ports: <unset>
    Endpoints: <none>
    Events:  <none>
    ```

    There's no `Endpoints` -> Should be no matching Pods.

1. Check `Service`'s `selector`

    <details>

    ```
    kubectl get svc nginx-2 -o yaml
    apiVersion: v1
    kind: Service
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"creationTimestamp":null,"labels":{"run":"nginx"},"name":"nginx-2","namespace":"default"},"spec":{"ports":[{"name":"80","port":80,"protocol":"TCP","targetPort":80}],"selector":{"run":"nonexisting"},"type":"ClusterIP"},"status":{"loadBalancer":{}}}
      creationTimestamp: "2026-08-14T15:30:50Z"
      labels:
        run: nginx
      name: nginx-2
      namespace: default
      resourceVersion: "8013"
      uid: f7bf8ca1-3f62-4b71-82b5-74d5628b8504
    spec:
      clusterIP: 10.96.202.236
      clusterIPs:
      - 10.96.202.236
      internalTrafficPolicy: Cluster
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
    NAME      READY   STATUS         RESTARTS   AGE   LABELS
    nginx-1   0/1     ErrImagePull   0          7s    run=nginx
    nginx-2   0/1     Pending        0          7s    run=nginx
    nginx-3   1/1     Running        0          7s    run=nginx
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
1. `kubectl get endpointslice -l kubernetes.io/service-name=<service_name>`
1. `kubectl get node`
1. `kubectl describe node <node_name>`

For more details: [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
## Clean up

1. Clean up the resources:

    ```
    kubectl delete -f .
    ```
