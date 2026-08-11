import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            record_video_dir=".",
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_timeout(2000)
        
        # Upload the PDF
        pdf_path = r"C:\Users\Vishwajit\OneDrive\Documents\Vishwajit Tidke Resume.pdf"
        await page.set_input_files("#fileInput", pdf_path)
        await page.click("#uploadBtn")
        
        # Wait for upload success
        await page.wait_for_selector("text=Document indexed!", timeout=30000)
        
        # Take UI screenshot after upload so it shows the file attached
        await page.screenshot(path="screenshot_ui.png")
        
        # Ask questions
        questions = [
            "What are Vishwajit's key educational qualifications?",
            "Where is Vishwajit currently located right now in real-time?",
            "What programming languages and frameworks does Vishwajit know?",
            "Did Vishwajit work on any projects that utilized Docker?"
        ]
        
        for q in questions:
            await page.fill("#q", q)
            await page.click("#send")
            # Wait a few seconds for Gemini to respond and typing animation to finish
            await page.wait_for_timeout(4000)
            
        # Take final screenshot showing all chat
        await page.screenshot(path="screenshot_chatting.png")
        
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
