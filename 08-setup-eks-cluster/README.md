# Set up an AWS EKS (Elastic Kubernetes Service) cluster

## Setup methods

- [eksctl](https://eksctl.io) <- We use `eksctl` here.
- [Terraform](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest)
- AWS Console
- CloudFormation

## Preparation

1. Install `aws`. (reference: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html) (For Mac OS)

    1. Download pkg file: https://awscli.amazonaws.com/AWSCLIV2.pkg
    1. Click the downloaded file. It'll start installation steps and follow them.
    1. Check

        Installed location:

        ```
        which aws
        ```

        Expected: `/usr/local/bin/aws`

        Installed version:

        ```
        aws --version
        ```

        Expected: `aws-cli/2.1.30 Python/3.8.8 Darwin/20.3.0 exe/x86_64 prompt/off` <- might be different. Depends on when you install.

1. Create `eks-setup-user` IAM user on console. (If you already have IAM user, you can skip this step.)

    1. Log in to your AWS account with root user. https://console.aws.amazon.com/iam/home?region=ap-northeast-1#/home
    1. Open [IAM page](https://console.aws.amazon.com/iam/home?region=ap-northeast-1#/home)
    1. "Add user" and write "eks-setup-user" as a username.
    1. Click "Attach policies directly" and grant "AdministratorAccess"
    1. Click the create user "eks-setup-user" and open "Security Credentials" tab.
    1. Click "Create access key", choose "Command Line Interface (CLI)", and then create it.
    1. Click “Create User” and download the `credentials.csv` (You cannot give this credentials to anyone.)


1. Set up `aws` cli with the created IAM user.

    ```
    aws configure --profile eks-setup-user
    ```

    You'll be asked to fill out the following info

    ```
    AWS Access Key ID [None]: <YOUR ACCESS KEY> <- you can get it from credentials.tsv
    AWS Secret Access Key [None]: <YOUR SECRET ACCESS KEY>  <- you can get it from credentials.tsv
    Default region name [None]: ap-northeast-1
    Default output format [None]:
    ```

1. Install `eksctl`. (Reference: https://github.com/weaveworks/eksctl#installation)

    ```
    curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
    sudo mv /tmp/eksctl /usr/local/bin
    ```

    ```
    eksctl version
    0.137.0
    ```

## Create an EKS cluster (It would take around 20 mins)

```
eksctl create cluster --name test-cluster --region ap-northeast-1 --profile eks-setup-user
```

<details>

```
2023-04-22 07:20:20 [ℹ]  eksctl version 0.137.0
2023-04-22 07:20:20 [ℹ]  using region ap-northeast-1
2023-04-22 07:20:20 [ℹ]  setting availability zones to [ap-northeast-1c ap-northeast-1a ap-northeast-1d]
2023-04-22 07:20:20 [ℹ]  subnets for ap-northeast-1c - public:192.168.0.0/19 private:192.168.96.0/19
2023-04-22 07:20:20 [ℹ]  subnets for ap-northeast-1a - public:192.168.32.0/19 private:192.168.128.0/19
2023-04-22 07:20:20 [ℹ]  subnets for ap-northeast-1d - public:192.168.64.0/19 private:192.168.160.0/19
2023-04-22 07:20:20 [ℹ]  nodegroup "ng-30993b22" will use "" [AmazonLinux2/1.25]
2023-04-22 07:20:20 [ℹ]  using Kubernetes version 1.25
2023-04-22 07:20:20 [ℹ]  creating EKS cluster "test-cluster" in "ap-northeast-1" region with managed nodes
2023-04-22 07:20:20 [ℹ]  will create 2 separate CloudFormation stacks for cluster itself and the initial managed nodegroup
2023-04-22 07:20:20 [ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=ap-northeast-1 --cluster=test-cluster'
2023-04-22 07:20:20 [ℹ]  Kubernetes API endpoint access will use default of {publicAccess=true, privateAccess=false} for cluster "test-cluster" in "ap-northeast-1"
2023-04-22 07:20:20 [ℹ]  CloudWatch logging will not be enabled for cluster "test-cluster" in "ap-northeast-1"
2023-04-22 07:20:20 [ℹ]  you can enable it with 'eksctl utils update-cluster-logging --enable-types={SPECIFY-YOUR-LOG-TYPES-HERE (e.g. all)} --region=ap-northeast-1 --cluster=test-cluster'
2023-04-22 07:20:20 [ℹ]
2 sequential tasks: { create cluster control plane "test-cluster",
    2 sequential sub-tasks: {
        wait for control plane to become ready,
        create managed nodegroup "ng-30993b22",
    }
}
2023-04-22 07:20:20 [ℹ]  building cluster stack "eksctl-test-cluster-cluster"
2023-04-22 07:20:21 [ℹ]  deploying stack "eksctl-test-cluster-cluster"
2023-04-22 07:20:51 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:21:21 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:22:21 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:23:21 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:24:21 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:25:21 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:26:22 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:27:22 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:28:22 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:29:22 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:30:22 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:31:22 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-cluster"
2023-04-22 07:33:24 [ℹ]  building managed nodegroup stack "eksctl-test-cluster-nodegroup-ng-30993b22"
2023-04-22 07:33:24 [ℹ]  deploying stack "eksctl-test-cluster-nodegroup-ng-30993b22"
2023-04-22 07:33:24 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-nodegroup-ng-30993b22"
2023-04-22 07:33:54 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-nodegroup-ng-30993b22"
2023-04-22 07:34:41 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-nodegroup-ng-30993b22"
2023-04-22 07:35:20 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-nodegroup-ng-30993b22"
2023-04-22 07:36:07 [ℹ]  waiting for CloudFormation stack "eksctl-test-cluster-nodegroup-ng-30993b22"
2023-04-22 07:36:07 [ℹ]  waiting for the control plane to become ready
2023-04-22 07:36:07 [✔]  saved kubeconfig as "/Users/m.naka/.kube/config"
2023-04-22 07:36:07 [ℹ]  no tasks
2023-04-22 07:36:07 [✔]  all EKS cluster resources for "test-cluster" have been created
2023-04-22 07:36:08 [ℹ]  nodegroup "ng-30993b22" has 2 node(s)
2023-04-22 07:36:08 [ℹ]  node "ip-192-168-42-202.ap-northeast-1.compute.internal" is ready
2023-04-22 07:36:08 [ℹ]  node "ip-192-168-95-169.ap-northeast-1.compute.internal" is ready
2023-04-22 07:36:08 [ℹ]  waiting for at least 2 node(s) to become ready in "ng-30993b22"
2023-04-22 07:36:08 [ℹ]  nodegroup "ng-30993b22" has 2 node(s)
2023-04-22 07:36:08 [ℹ]  node "ip-192-168-42-202.ap-northeast-1.compute.internal" is ready
2023-04-22 07:36:08 [ℹ]  node "ip-192-168-95-169.ap-northeast-1.compute.internal" is ready
2023-04-22 07:36:10 [ℹ]  kubectl command should work with "/Users/m.naka/.kube/config", try 'kubectl get nodes'
2023-04-22 07:36:10 [✔]  EKS cluster "test-cluster" in "ap-northeast-1" region is ready
```

</details>


## Set up kubeconfig

```
aws eks update-kubeconfig --name test-cluster --profile setup-eks-user
```

You can check the created eks cluster `test-cluster` is configured in `~/.kube/config`.

You can also check the connected cluster with the following command:

```
kubectl cluster-info
```

<details>

```
Kubernetes control plane is running at https://xxxxxx.yl4.ap-northeast-1.eks.amazonaws.com
CoreDNS is running at https://xxxxx.yl4.ap-northeast-1.eks.amazonaws.com/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

</details>


## Check

1. Check `Node`

    ```
    kubectl get nodes
    NAME                                                STATUS   ROLES    AGE     VERSION
    ip-192-168-42-202.ap-northeast-1.compute.internal   Ready    <none>   8m27s   v1.25.7-eks-a59e1f0
    ip-192-168-95-169.ap-northeast-1.compute.internal   Ready    <none>   8m27s   v1.25.7-eks-a59e1f0
    ```

1. Deploy and check nginx `Pod`

    ```
    ± kubectl run nginx --image=nginx
    pod/nginx created
    ```

    ```
    ± kubectl get pod

    NAME    READY   STATUS    RESTARTS   AGE
    nginx   1/1     Running   0          8s
    ```

## Clean up

1. Destroy cluster

    ```
    eksctl delete cluster --name test-cluster --region ap-northeast-1 --profile eks-setup-user
    ```

1. Remove `[eks-setup-user]` credentials from `~/.aws/credentials` and `~/.aws/config`
1. Log in to [AWS console](https://console.aws.amazon.com/iam/home?region=ap-northeast-1#/users) with the root user and remove `eks-setup-user` IAM user from console.


## References

- [Quickstart Amazon EKS](https://github.com/aws-quickstart/quickstart-amazon-eks)

## Checked versions

`eksctl`:
1. 0.40.0
1. 0.66.0
1. 0.137.0
