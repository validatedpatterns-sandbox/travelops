# TravelOps Test Plan

[GitHub Repo](https://github.com/validatedpatterns-sandbox/travelops)

## PreRequisites

- Running OpenShift Cluster (3Node, 3x(n))
- Logged into cluster or exported KUBECONFIG


## Deployment

1. Copy the secrets template file to your home directory:

```shell
cp values-secret.yaml.template $HOME/values-secret-travelops.yaml
```

1. Run pattern.sh wrapper script

```shell
./pattern.sh make install
```

1. Get the route to the travel control portal

```shell
CONTROL=http://$(oc get route istio-ingressgateway -n istio-system -o jsonpath='{.spec.host}')
```

In the travel control dashboard, use the sliders to change the requests for each travel locale. We need this to generate traffic
between the different services in the service mesh.

1. Get the route to the kiali dashboard and log in using kubeadmin (or other credentialed user)

```shell
KIALI=https://$(oc get route kiali -n istio-system -o jsonpath=’{.spec.host}’
```

1. Use the kiali dashboard to verify the mTLS configuration and ensure that the travelops applications are configured in the mesh correctly:

Please use [kiali dashboard graphic](https://validatedpatterns.io/images/travelops/ossm-kiali-db-arrows.png) as a reference to what is presented on kiali dashboard
 
- A "lock" icon should be present in the upper right hand corner of the kiali dashboard
- Each application (travel-agency, travel-control and travel-portal) should also show a lock within their respective context boxes.
- Each application (travel-agency, travel-control and travel-portal) should have a green check mark next number of applications.

The kiali dashboard shows us that our travelops applications are configured correctly for mTLS and properly joined to the service mesh. 

## Conclusion:
This test plan confirms that the deployed configuration is working as expected.
