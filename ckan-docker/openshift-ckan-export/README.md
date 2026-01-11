# CKAN on OpenShift

This directory contains everything you need to deploy CKAN (and its companion services) into an OpenShift project, using YAML manifests exported from an existing cluster, cleaned up, and ready to apply.

---

## 1. Prerequisites

- **OpenShift CLI** (`oc`) installed  
- An existing OpenShift project/namespace (e.g. `buspark-test-v2-dev`)  
- `yq` (v4.x) installed (if you ever need to tweak or re-clean the manifests)  
- CKAN image (/ckan/Dockerfile.dev) is already built and pushed to Quay:  
  ```bash
  quay.io/buspark_test/spark-ckan:latest
  ```

### Logging into OpenShift

You’ll need to authenticate your `oc` CLI with your OpenShift project before running any commands locally:

1. Log into your [OpenShift Web Console](https://console-openshift-console.example.com/) (replace with your cluster URL).  
2. Switch to your target project/namespace (e.g. `buspark-test-v2-dev`).  
3. In the top-right corner, click your user menu → **Copy Login Command**.  
4. This will open a page showing a login command with a token, for example:  
   ```bash
   oc login --token=sha256~XXXXXX --server=https://api.cluster-name:6443
   ```  
5. Run that command in your terminal. This authenticates your local `oc` session with the correct project and permissions.  

Once logged in, all subsequent `oc` commands will run against your selected project.

## 2. Deployment steps

### 1. Select your project

```bash
oc project buspark-test-v2-dev
```

### 2. (Optional) Clean out any old resources

```bash
oc delete all --all
oc delete pvc --all
```

### 3. Apply the cleaned manifests


```bash
cd ckan-docker/openshift-ckan-export
for f in clean-*.yaml; do
  oc apply -f "$f"
done
```

### 4. Verify PVCs bound

```bash
oc get pvc
```

### 5. Wait for all Deployments

```bash
oc rollout status deployment/ckan-dev
oc rollout status deployment/db
oc rollout status deployment/datapusher
oc rollout status deployment/redis
oc rollout status deployment/solr
oc rollout status deployment/nginx
```

### 6. Check pod health & logs

```bash
oc get pods
oc logs -f deployment/ckan-dev
```


### 7. Expose & test the HTTP route

```bash
oc expose svc/nginx --name=ckan-nginx
oc patch route ckan-nginx -p '{"spec":{"to":{"kind":"Service","name":"nginx"},"port":{"targetPort":81}}}'

ROUTE_HOST=$(oc get route ckan-nginx -o jsonpath='{.spec.host}')
curl -I "http://$ROUTE_HOST"
```