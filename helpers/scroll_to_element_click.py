# helpers/ui_helpers.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scroll_and_click(driver, button_text, timeout=10):
    """
    Scrolle jusqu’à un bouton contenant `button_text` et clique dessus.

    Args:
        driver: Instance WebDriver
        button_text: Le texte visible du bouton (ex: "Envoyer")
        timeout: Temps d’attente maximum (en secondes)
    """
    wait = WebDriverWait(driver, timeout)

    try:
        # 1. Attendre que le bouton soit dans le DOM (présent)
        xpath = f"//button[contains(normalize-space(), '{button_text}')]"
        bouton = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        # 2. Scroller jusqu’à lui
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", bouton)

        # 3. Attendre qu’il soit cliquable puis cliquer
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    except Exception as e:
        driver.save_screenshot("scroll_and_click_error.png")
        raise Exception(f"❌ Impossible de cliquer sur le bouton '{button_text}' : {e}")
