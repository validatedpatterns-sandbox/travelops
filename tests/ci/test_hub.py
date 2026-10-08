import os

import pytest
from playwright.sync_api import sync_playwright
from validatedpatterns_tests.interop import components, subscription

from .helpers import (
    assert_url_reachable,
    gateway_url,
    kubeadmin_password,
    route_url,
)


def _results_dir():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".results")
    os.makedirs(path, exist_ok=True)
    return path


def _openshift_login(page, url, password):
    page.goto(url)
    page.get_by_label("Username *").fill("kubeadmin")
    page.get_by_label("Password *").fill(password)
    page.get_by_role("button", name="Log in").click()


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
        "external-secrets",
        "external-secrets-operator",
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


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_travel_control_dashboard(openshift_dyn_client):
    console_url = route_url(openshift_dyn_client, "openshift-console", "console")
    dashboard_url = gateway_url(
        openshift_dyn_client, "travel-control", "travel-control-gateway"
    )
    password = kubeadmin_password()
    results_dir = _results_dir()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        context.set_default_timeout(120_000)
        page = context.new_page()
        try:
            _openshift_login(page, console_url, password)
            page.goto(dashboard_url)
            page.locator('[id="travels\\.uk_ratio"]').fill("98")
            page.locator('[id="travels\\.uk_device_mobile"]').fill("5")
            page.locator('[id="travels\\.uk_user_registered"]').fill("89")
            page.locator('[id="travels\\.uk_travel_t3"]').fill("71")
            page.locator('[id="viaggi\\.it_ratio"]').fill("0")
            page.locator('[id="viaggi\\.it_device_mobile"]').fill("100")
            page.locator('[id="viaggi\\.it_user_registered"]').fill("99")
            page.locator('[id="viaggi\\.it_travel_t2"]').fill("80")
            page.locator('[id="voyages\\.fr_ratio"]').fill("51")
            page.locator('[id="voyages\\.fr_travel_t1"]').fill("59")
            page.screenshot(
                path=os.path.join(results_dir, "travel_control_dashboard.png"),
                full_page=True,
            )
        finally:
            context.close()
            browser.close()


@pytest.mark.parametrize(
    "openshift_dyn_client",
    ["VP_HUBCONFIG"],
    indirect=True,
)
def test_kiali_traffic_graph(openshift_dyn_client):
    kiali_url = route_url(openshift_dyn_client, "istio-system", "kiali")
    password = kubeadmin_password()
    results_dir = _results_dir()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        context.set_default_timeout(120_000)
        page = context.new_page()
        try:
            _openshift_login(page, kiali_url, password)
            page.get_by_role("link", name="Traffic Graph").click()
            page.locator('[data-test="namespace-dropdown"]').click()
            page.locator('[id="namespace-list-item\\[travel-agency\\]"]').get_by_role(
                "checkbox"
            ).check()
            page.locator('[id="namespace-list-item\\[travel-control\\]"]').get_by_role(
                "checkbox"
            ).check()
            page.locator('[id="namespace-list-item\\[travel-portal\\]"]').get_by_role(
                "checkbox"
            ).check()
            page.locator('[data-test="namespace-dropdown"]').click()
            page.wait_for_timeout(5000)
            page.screenshot(
                path=os.path.join(results_dir, "kiali_traffic_graph.png"),
                full_page=True,
            )
        finally:
            context.close()
            browser.close()
