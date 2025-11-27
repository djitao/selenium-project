from selenium.webdriver import Keys

from helpers.click_button_text import click_button_by_text
from helpers.presence_of_element_to_click import click_if_present
from helpers.select_ville_helper import select_ville
from helpers.scroll_helper import scroll_to_element
from helpers.element_utils import wait_for_element
from helpers.menu_submenu_helpers import click_on_sidebar
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException



class Test_Agence:

    def test_navigation_envoi(self, driver, login):
        # Attendre que le menu apparaisse
        menu_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
        )

        # Click sur "Agence"
        gestion_op_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Agences']]"))
        )
        gestion_op_btn.click()
        time.sleep(2)

        # Click sur "agence submenu"
        gestion_envoi = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By. XPATH, "//a[@href='/coordinateur/agences']"))
        )
        gestion_envoi.click()

        # Attendre que le conteneur principal soit présent
        div_app = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#app"))
        )

        previous_height = 0
        max_wait_same_height = 5  # nombre d'itérations sans changement avant d'arrêter
        no_change_count = 0
        scroll_step = 500

        while True:
            # Faire défiler vers le bas
            driver.execute_script("arguments[0].scrollTop += arguments[1];", div_app, scroll_step)
            time.sleep(0.5)

            # Vérifier la position et la hauteur du scroll
            scroll_top = driver.execute_script("return arguments[0].scrollTop;", div_app)
            scroll_height = driver.execute_script("return arguments[0].scrollHeight;", div_app)
            client_height = driver.execute_script("return arguments[0].clientHeight;", div_app)

            # Si on est en bas, on arrête
            if scroll_top + client_height >= scroll_height:
                print("✅ Arrivé en bas du conteneur.")
                break

            # Si la hauteur ne change plus (page figée), on arrête après X tentatives
            if scroll_height == previous_height:
                no_change_count += 1
                if no_change_count >= max_wait_same_height:
                    print("⚠️ Aucun nouveau contenu détecté après plusieurs scrolls.")
                    break
            else:
                no_change_count = 0

            previous_height = scroll_height

        # Scroll horizontalement la table
        table_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-body.p-4.overflow-x-auto"))
        )
        driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth", table_container)
        time.sleep(3)



