import { test, expect } from "@playwright/test";

test("has title", async ({ page }) => {
  await page.goto("http://localhost:3000");

  await expect(
    page.getByRole("heading", { name: "Web performance test" })
  ).toBeVisible();
});

test("has items", async ({ page }) => {
  await page.goto("http://localhost:3000");

  await expect(page.getByRole("listitem").first()).toBeVisible();
});
