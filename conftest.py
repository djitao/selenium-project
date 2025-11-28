import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="class")
def driver():
    options = Options()

    # 🔥 Mode headless obligatoire pour Jenkins
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    # 🟢 Création du profil Firefox
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.security.https_only_mode", True)
    profile.set_preference("dom.security.https_only_mode_pbm", True)
    profile.set_preference("webdriver_accept_untrusted_certs", True)
    profile.set_preference("webdriver_assume_untrusted_issuer", False)

    options.profile = profile

    # 🔧 Service Geckodriver (pour Jenkins)
    service = Service(executable_path="drivers/geckodriver.exe")

    # 🚀 Démarrer Firefox headless
    driver = webdriver.Firefox(service=service, options=options)

    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def login(driver):

    driver.get("https://dev.nitacashhub.com/login")

    try:
        driver.find_element(By.ID, "username").send_keys("ALINA466")
        driver.find_element(By.NAME, "password").send_keys("11111111")
        driver.find_element(By.CLASS_NAME, "submit-btn").click()

        # Attente jusqu'à la redirection vers "index"
        WebDriverWait(driver, 20).until(
            EC.url_contains("index")
        )

        current_url = driver.current_url
        print("✅ Connexion réussie, URL actuelle :", current_url)

        if "error" in current_url.lower():
            pytest.fail("❌ Échec de la connexion : URL contient 'error'")

        yield True

    except Exception as e:
        pytest.fail(f"❌ Problème pendant le login : {str(e)}")
