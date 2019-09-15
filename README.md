
```bash
kubectl apply -f guestbook_manifest.yaml
kubectl create namespace test1ns

kubectl apply -f watcher_manifest.yaml

# get Guestbook IP
kubectl get svc frontend | awk 'END{print $4}'

# check in browser Guestbook page
kubectl create namespace test3ns

# wait a minute and check again
```