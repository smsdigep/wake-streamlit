from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

STREAMLIT_URL = "https://estagio-sms.streamlit.app/" 

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(STREAMLIT_URL)
        print(f"Acessando {STREAMLIT_URL}...")

        wait = WebDriverWait(driver, 15)
        try:
            button = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(text(),'Yes, get this app back up')]"
                ))
            )
            print("Botão de despertar encontrado. Clicando...")
            button.click()
            print("App despertado com sucesso ✅")

        except TimeoutException:
            print("App já estava acordado ✅")

    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
