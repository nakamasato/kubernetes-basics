# Service


1. Apply pods

    ```
    kubectl apply -f pod-my-app.yaml
    kubectl apply -f pod-your-app.yaml
    ```

1. Show labels

    ```
    kubectl get po --show-labels
    ```

1. Filter pods by label

    ```
    kubectl get po --selector app=MyApp
    kubectl get po --selector app=YourApp
    ```

1. Create service.


    ```
    kubectl apply -f service-my-service.yaml
    ```

    ```
    kubectl get service
    ```

    Check Endpoints

    ```
    kubectl get endpoints
    ```

    You can see IP address with port `80`.

    This IP is the IP address of pod `my-app`

    ```
    kubectl get pod --selector app=MyApp -o wide
    ```

1. Access to the service

    port-forward:

    ```
    kubectl port-forward svc/my-app 8080:80
    ```

    logs

    ```
    kubectl logs my-app -f
    ```

    Open [localhost:8080]() on your browser.

    -> You can see the nginx page.

1. Delete resources.

    ```
    kubectl delete -f .
    ```
