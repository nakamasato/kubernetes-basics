# simple key-value pairs

```
kubectl create secret generic mysecret --from-literal=username=admin --from-literal=password=1f2d1e2e67df -o yaml --dry-run=client
```

# data.csv

```
echo -n 'name,age,email,password\nnaka,1,naka@example.com,j4gn43g4gr\ntanaka,2,tanaka@example.com,8j437fkw3v' | base64
bmFtZSxhZ2UsZW1haWwscGFzc3dvcmQKbmFrYSwxLG5ha2FAZXhhbXBsZS5jb20sajRnbjQzZzRncgp0YW5ha2EsMix0YW5ha2FAZXhhbXBsZS5jb20sOGo0Mzdma3czdg==
```

or

```
kubectl create secret generic mysecret --from-file=data.csv=data.csv -o yaml --dry-run=client
apiVersion: v1
data:
  data.csv: bmFtZSxhZ2UsZW1haWwscGFzc3dvcmQKbmFrYSwxLG5ha2FAZXhhbXBsZS5jb20sajRnbjQzZzRncgp0YW5ha2EsMix0YW5ha2FAZXhhbXBsZS5jb20sOGo0Mzdma3czdg==
kind: Secret
metadata:
  creationTimestamp: null
  name: mysecret
```
