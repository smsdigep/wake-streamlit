from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import sys

STREAMLIT_URLS = [
    "https://estagio-sms.streamlit.app/",
    "https://sms-prof.streamlit.app/",
]

def wake_app(driver, url):
    print(f"Acessando {url}...")
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    try:
        button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(., 'Yes, get this app back up')]"
            ))
        )
        print(f"Botão encontrado em {url}. Clicando...")
        button.click()

        try:
            wait.until(
                EC.invisibility_of_element_located((
                    By.XPATH,
                    "//button[contains(., 'Yes, get this app back up')]"
                ))
            )
            print(f"App despertado com sucesso: {url}")
        except TimeoutException:
            print(f"Botão clicado, mas não sumiu em {url}")
            return False

    except TimeoutException:
        print(f"Sem botão em {url}. App já estava acordado.")
    
    return True

def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    ok = True
    try:
        for url in STREAMLIT_URLS:
            result = wake_app(driver, url)
            ok = ok and result
    except Exception as e:
        print(f"Erro inesperado: {e}")
        ok = False
    finally:
        driver.quit()

    if not ok:
        sys.exit(1)

if __name__ == "__main__":
    main()
