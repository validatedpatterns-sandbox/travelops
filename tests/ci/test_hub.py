import pytest
from validatedpatterns_tests.interop import application, components, subscription

from .helpers import assert_url_reachable, gateway_url, route_url


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_subscription_status_hub(openshift_dyn_client):
    expected_subs = {
        "openshift-gitops-operator": ["openshift-gitops-operator"],
        "advanced-cluster-management": ["open-cluster-management"],
        "multicluster-engine": ["multicluster-engine"],
    }
    subscription.assert_subscription_status(openshift_dyn_client, expected_subs)


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_SPOKECONFIG"],
    indirect=True,
)
def test_subscription_status_spoke(openshift_dyn_client):
    expected_subs = {
        "openshift-gitops-operator": ["openshift-gitops-operator"],
    }

    subscription.assert_subscription_status(openshift_dyn_client, expected_subs)


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG", "VP_SPOKECONFIG"],
    indirect=True,
)
def test_site_reachable(openshift_dyn_client):

    components.assert_site_reachable(openshift_dyn_client)


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_pod_status_hub(openshift_dyn_client):
    projects = [
        "patterns-operator",
        "open-cluster-management",
        "open-cluster-management-hub",
        "vp-gitops",
        "vault",
        "hello-world",
        "config-demo",
        "external-secrets",
    ]

    components.assert_pod_status(openshift_dyn_client, projects, skip_check=[])


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_SPOKECONFIG"],
    indirect=True,
)
def test_pod_status_spoke(openshift_dyn_client):
    projects = [
        "open-cluster-management-agent",
        "open-cluster-management-agent-addon",
        "vp-gitops",
        "hello-world",
        "config-demo",
        "external-secrets",
    ]

    components.assert_pod_status(openshift_dyn_client, projects, skip_check=[])


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_managed_clusters(openshift_dyn_client):
    components.assert_managed_clusters(openshift_dyn_client, ["group-one"])


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG", "VP_SPOKECONFIG"],
    indirect=True,
)
def test_argocd_reachable(openshift_dyn_client):
    components.assert_argocd_reachable(openshift_dyn_client)


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG", "VP_SPOKECONFIG"],
    indirect=True,
)
def test_argocd_applications_health(openshift_dyn_client):
    projects = ["vp-gitops", "multicloud-gitops-hub"]

    application.assert_argocd_applications(openshift_dyn_client, projects)


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
