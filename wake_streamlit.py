import asyncio
from playwright.async_api import async_playwright

STREAMLIT_URLS = [
    "https://estagio-sms.streamlit.app/",
    "https://sms-prof.streamlit.app/",
]

WAKE_TEXT = "Yes, get this app back up!"

async def wake_app(page, url):
    print(f"Acessando {url}")
    await page.goto(url, wait_until="domcontentloaded", timeout=120000)
    await page.wait_for_timeout(5000)

    wake_button = page.get_by_role("button", name=WAKE_TEXT)

    if await wake_button.count() > 0:
        print(f"Botão de wake encontrado em {url}. Clicando...")
        await wake_button.click()
        await page.wait_for_timeout(60000)
        print(f"Wake solicitado para {url}")
    else:
        print(f"App já aparenta estar acordado em {url}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for url in STREAMLIT_URLS:
            try:
                await wake_app(page, url)
            except Exception as e:
                print(f"Erro em {url}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
