import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="class")
def driver():
    options = Options()

    # 🟢 Créer un profil Firefox pour HTTPS-Only
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.security.https_only_mode", True)
    profile.set_preference("dom.security.https_only_mode_pbm", True)  # navigation privée

    # ⚠️ Accepter les certificats auto-signés
    profile.set_preference("webdriver_accept_untrusted_certs", True)
    profile.set_preference("webdriver_assume_untrusted_issuer", False)

    # 🔹 Associer le profil aux options
    options.profile = profile

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def login(driver):
    driver.get("https://dev.nitacashhub.com/login")

    try:
        driver.find_element(By.ID, "username").send_keys("ALINA466")
        driver.find_element(By.NAME, "password").send_keys("11111111")
        driver.find_element(By.CLASS_NAME, "submit-btn").click()

        # Attente que l’URL contienne “index”
        WebDriverWait(driver, 20).until(
            EC.url_contains("index")
        )

        current_url = driver.current_url
        print("✅ Connexion réussie, URL actuelle :", current_url)

        # Vérifie que la connexion a réussi
        if "error" in current_url:
            pytest.fail("❌ Échec de la connexion : URL contient 'error'")

        yield True

    except Exception as e:
        pytest.fail(f"❌ Problème pendant le login : {str(e)}")
