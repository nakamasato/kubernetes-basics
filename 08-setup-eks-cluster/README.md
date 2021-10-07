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
    1. Check "Programmatic access"
    1. Grant "AdministratorAccess"
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
    0.40.0
    ```

## Create an EKS cluster (It would take around 20 mins)

```
eksctl create cluster --name test-cluster --region ap-northeast-1 --profile eks-setup-user
```

## Check

1. Check `Node`

    ```
    kubectl get nodes
    NAME                                                STATUS   ROLES    AGE     VERSION
    ip-192-168-32-253.ap-northeast-1.compute.internal   Ready    <none>   9m12s   v1.18.9-eks-d1db3c
    ip-192-168-67-143.ap-northeast-1.compute.internal   Ready    <none>   9m12s   v1.18.9-eks-d1db3c
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
