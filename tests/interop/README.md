# Running tests

## Prerequisites

* Openshift cluster with travelops pattern installed
* kubeconfig file for Openshift cluster
* oc client installed at ~/oc_client/oc

## Steps

* create python3 venv, clone travelops repository
* export KUBECONFIG=\<path to hub kubeconfig file>
* export INFRA_PROVIDER=\<infra platform description>
* (optional) export WORKSPACE=\<dir to save test results to> (defaults to /tmp)
* cd travelops/tests/interop
* pip install -r requirements.txt
* ./run_tests.sh

## Results

* results .xml files will be placed at $WORKSPACE
* test logs will be placed at $WORKSPACE/.results/test_execution_logs/
* CI badge file will be placed at $WORKSPACE

## UI-based tests

* requires [Playwright](https://playwright.dev/docs/intro)Version 1.50.0 and dependencies
* requires included config (playwright.config.ts)
* edit travelops.spec.ts to add values for:
  * \<hub console url\>
  * \<kubeadmin password\>
  * \<hub cluster name\>
* "npx playwright test travelops.spec.ts" to execute
