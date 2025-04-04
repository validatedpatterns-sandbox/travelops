import { test, expect } from '@playwright/test';

test.use({
  ignoreHTTPSErrors: true
});


test('travelops: test kiali dashboard and travel-agency graph', async ({ page }) => {
  // Log in to Openshift console
  await page.goto("<hub console url>");
  await page.getByLabel('Username *').fill('kubeadmin');
  await page.getByLabel('Password *').fill("<kubeadmin password>");
  await page.getByRole('button', { name: 'Log in' }).click();

  // Go to kiali console and check for expected text
  await page.goto("https://kiali-istio-system.apps.<hub cluster name>");
  await page.getByText('istio-systemControl plane').click();
  await page.getByText('travel-agency').click();
  await page.getByText('travel-control').click();
  await page.getByText('travel-portal').click();

  // Verify that mTLS is enabled (lock icon)
  await page.locator('[data-test="travel-agency-EXPAND"]').getByRole('img', { name: 'left' }).click();
  await page.locator('[data-test="travel-control-EXPAND"]').getByRole('img', { name: 'left' }).click();
  await page.locator('[data-test="travel-portal-EXPAND"]').getByRole('img', { name: 'left' }).click();

  // Go to kiali travel-agency graph
  await page.getByRole('link', { name: 'Graph' }).click();
  await page.locator('[data-test="namespace-dropdown"]').click();
  await page.locator('[id="namespace-list-item\\[travel-agency\\]"]').getByRole('checkbox').check();
  await page.locator('[id="namespace-list-item\\[travel-agency\\]"]').getByRole('checkbox').press('Escape');

  // Check for expected text/buttons
  await page.getByText('travel-agency').click();
  await page.getByRole('button', { name: 'Inbound' }).click();
  await page.getByRole('button', { name: 'Outbound' }).click();
  await page.getByRole('button', { name: 'Total' }).click();
  await page.getByText('HTTP (requests per second):').click();

  // Verify screenshot, accounting for date/time
  await expect(page).toHaveScreenshot({ maxDiffPixels: 500 });
});
