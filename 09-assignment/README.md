# ArgoCD assignment

## Prerequisite

- ArgoCD is already installed. (If not, please go back to [09](../09/README.md) and install it and confirm you can open the ArgoCD UI.)

##

1. Create your own Git repository.
1. Create `argocd-test/nginx-deployment.yaml`. (You can copy the file from this repo.)
1. Add `argocd-test/nginx-deployment.yaml`, commit, and push to your repository.
1. Create ArgoCD Application yaml file. (name: argocd-final-assignment, project: default, namespace: default, source: <your git repository>, revision: master, path: argocd-test) [argocd-final-assignment.yaml]()
1. Apply ArgoCD Application by `kubectl apply -f argocd-final-assignment.yaml`
1. Check application is running on ArgoCD UI.
1. Change `argocd-test/nginx-deployment.yaml` to `replicas: 3`
1. Check argocd-final-assignment has 3 pods on ArgoCD UI.
