# 06 Set environment specific configuration with Secrets

## Prerequisite

Namespace is set.

```
namespace=<yourname>
```

```
kubectl create ns $namespace
```

## Practice Secret

1. Create `Secret`

    ```
    kubectl create secret generic test-secret --from-literal=username=testuser --from-literal=password=12345
    ```

1. Check the created `ConfigMap`

    ```
    kubectl get secret test-secret -o yaml
    ```

    <details>

    ```
    apiVersion: v1
    data:
      password: MTIzNDU=
      username: dGVzdHVzZXI=
    kind: Secret
    metadata:
      creationTimestamp: "2021-03-03T21:54:38Z"
      managedFields:
      - apiVersion: v1
        fieldsType: FieldsV1
        fieldsV1:
          f:data:
            .: {}
            f:password: {}
            f:username: {}
          f:type: {}
        manager: kubectl-create
        operation: Update
        time: "2021-03-03T21:54:38Z"
      name: test-secret
      namespace: default
      resourceVersion: "8171263"
      selfLink: /api/v1/namespaces/default/secrets/test-secret
      uid: 7b7dd748-dae5-4ef8-8cc3-7a961e8a5cde
    type: Opaque
    ```

    </details>

1. Get original value (decode)

    ```
    echo -n 'MTIzNDU=' | base64 --decode # password
    12345
    ```

    ```
    echo -n 'dGVzdHVzZXI=' | base64 --decode # username
    testuser
    ```

1. Delete

    ```
    kubectl delete secret test-secret
    ```

## Nginx with basic auth

1. Prepare `ConfigMap` `nginx-configmap.yaml`

    `default.conf` is added to the ConfigMap that we used last time.

    ```
      default.conf: |
        server {
            listen       80;
            server_name  localhost;

            location / {
                root   /usr/share/nginx/html;
                index  index.html index.htm;
                auth_basic "Restricted";
                auth_basic_user_file /etc/nginx/.htpasswd;
            }

            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   /usr/share/nginx/html;
            }

        }
    ```

1. Prepare `Secret` for basic auth

    ```
    htpasswd -nb username password
    username:$apr1$bdO42eI1$Ep4R2CT7luFEycP6l2AW41
    ```

    ```
    echo -n 'username:$apr1$bdO42eI1$Ep4R2CT7luFEycP6l2AW41' | base64
    dXNlcm5hbWU6JGFwcjEkYmRPNDJlSTEkRXA0UjJDVDdsdUZFeWNQNmwyQVc0MQ==
    ```

    https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/#creating-a-password-file

1. Prepare `Deployment` to mount `ConfigMap` and `Secret`

    1. Define both `ConfigMap` and `Secret` as volume

        ```
              volumes:
                - name: config
                  configMap:
                    name: nginx
                    items:
                      - key: index.html
                        path: index.html
                      - key: default.conf
                        path: default.conf
                - name: secret
                  secret:
                    secretName: nginx
                    items:
                      - key: .htpasswd
                        path: .htpasswd
        ```

    1. Mount the volume from the `nginx` container


        ```
                  volumeMounts:
                    - mountPath: /usr/share/nginx/html/index.html
                      name: config
                      subPath: index.html
                    - mountPath: /etc/nginx/conf.d/default.conf
                      name: config
                      subPath: default.conf
                    - mountPath: /etc/nginx/.htpasswd
                      name: secret
                      subPath: .htpasswd
        ```

1. Apply

    ```
    kubectl apply -f nginx-deployment.yaml,nginx-configmap.yaml,nginx-secret.yaml,nginx-service.yaml -n $namespace
    ```

1. Check

    port forward

    ```
    kubectl -n $namespace port-forward service/nginx 8080:80
    ```

    Open http://localhost:8080 -> You'll be asked to input username and password.
