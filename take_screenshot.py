import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="screenshot_ui.png")
        
        # Take screenshot of typing
        await page.fill("#q", "Hello, what can you do?")
        await page.click("#send")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="screenshot_chatting.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
