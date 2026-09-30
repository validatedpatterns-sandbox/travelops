import pytest
from validatedpatterns_tests.interop import components, subscription

from .helpers import assert_url_reachable, gateway_url, route_url


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_subscription_status(openshift_dyn_client):
    expected_subs = {
        "openshift-gitops-operator": ["openshift-gitops-operator"],
        "tempo-product": ["openshift-tempo-operator"],
        "cluster-observability-operator": ["openshift-cluster-observability-operator"],
        "opentelemetry-product": ["openshift-opentelemetry-operator"],
    }

    subscription.assert_subscription_status(openshift_dyn_client, expected_subs)


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_site_reachable_hub(openshift_dyn_client):
    components.assert_site_reachable(openshift_dyn_client)


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_argocd_reachable(openshift_dyn_client):
    components.assert_argocd_reachable(openshift_dyn_client)


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_pod_status(openshift_dyn_client):
    projects = [
        "patterns-operator",
        "vp-gitops",
        "vault",
        "golang-external-secrets",
        "vp-s4-storage",
        "travel-agency",
        "travel-control",
        "travel-portal",
        "openshift-tempo-operator",
        "openshift-opentelemetry-operator",
        "openshift-cluster-observability-operator",
    ]
    components.assert_pod_status(openshift_dyn_client, projects, skip_check=[])


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_console_route(openshift_dyn_client):
    url = route_url(openshift_dyn_client, "openshift-console", "console")
    assert_url_reachable(url)


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_kiali_route(openshift_dyn_client):
    url = route_url(openshift_dyn_client, "istio-system", "kiali")
    assert_url_reachable(url)


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_travel_control_gateway(openshift_dyn_client):
    url = gateway_url(
        openshift_dyn_client, "travel-control", "travel-control-gateway"
    )
    assert_url_reachable(url)
