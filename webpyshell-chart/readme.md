## Helm install
This helm script installs the WebShell within a kubernetes cluster.

```bash
helm install webpyshell . -n shells --create-namespace
```

```bash
kubectl get secret webpyshell-tls -n istio-ingress
kubectl get gateway,virtualservice -n shells
```

```bash
helm upgrade webpyshell . -n shells 
```

```bash
helm uninstall webpyshell -n shells
```
