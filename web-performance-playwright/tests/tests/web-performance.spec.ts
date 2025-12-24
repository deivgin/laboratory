import { test, expect } from "@playwright/test";

test("largest contentful paint", async ({ page }) => {
  const entries: PerformanceEntryList = [];

  await page.goto("http://localhost:3000");

  await expect(
    page.getByRole("heading", { name: "Web performance test" })
  ).toBeVisible();

  await page.evaluate(() => {
    entries.push(...performance.getEntries());
  });

  console.log(entries);
});
