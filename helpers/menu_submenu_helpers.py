# helpers/menu_helpers.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def click_on_sidebar(driver, menu="Envois", sub="Effectuer un envoi", timeout=10):
    wait = WebDriverWait(driver, timeout)

    try:
        # 1. Cliquer sur le menu principal (span -> a)
        menu_element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//span[text()='{menu}']/parent::a")
        ))
        menu_element.click()

        # 2. Attendre que le sous-menu soit visible et cliquable
        submenu_element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//a[contains(normalize-space(), '{sub}')]")
        ))
        submenu_element.click()

    except TimeoutException:
        driver.save_screenshot("menu_click_error.png")
        raise Exception(f"❌ Menu '{menu}' ou sous-menu '{sub}' introuvable ou non cliquable.")
