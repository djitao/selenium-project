from pygments.lexer import default
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



class Test_Rapport_Decaissement:

    def test_navigation_vers_les_etats(self, driver, login):
        # Attendre que le menu apparaisse
        menu_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
        )
        scroll_step = 250
        for _ in range(2):  # maximum 20 scrolls
            driver.execute_script("arguments[0].scrollTop += arguments[1];", menu_container, scroll_step)
            time.sleep(0.5)

            scroll_height = driver.execute_script("return arguments[0].scrollHeight", menu_container)
            scroll_top = driver.execute_script("return arguments[0].scrollTop", menu_container)
            client_height = driver.execute_script("return arguments[0].clientHeight", menu_container)

            if scroll_top + client_height >= scroll_height:
                break  # arrivé en bas

        time.sleep(2)

        # Click sur "Rapport"
        etat_op_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Rapports']]"))
        )
        etat_op_btn.click()
        # Attendre que le menu vertical soit présent
        menu_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
        )
        scroll_step = 250
        for _ in range(1):  # maximum 20 scrolls
            driver.execute_script("arguments[0].scrollTop += arguments[1];", menu_container, scroll_step)
            time.sleep(0.5)

            scroll_height = driver.execute_script("return arguments[0].scrollHeight", menu_container)
            scroll_top = driver.execute_script("return arguments[0].scrollTop", menu_container)
            client_height = driver.execute_script("return arguments[0].clientHeight", menu_container)

            if scroll_top + client_height >= scroll_height:
                break  # arrivé en bas

        time.sleep(2)

        # Click sur "decaissement
        etat_profil_marchand = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/coordinateur/decaissementEnAttente']"))
        )
        etat_profil_marchand.click()
        time.sleep(3)
        # Scroll progressif dans le div#app (limité à 20 itérations max pour éviter une boucle infinie)
        div_app = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#app"))
        )

        scroll_step = 300
        for _ in range(20):  # maximum 20 scrolls
            driver.execute_script("arguments[0].scrollTop += arguments[1];", div_app, scroll_step)
            time.sleep(0.5)

            scroll_height = driver.execute_script("return arguments[0].scrollHeight", div_app)
            scroll_top = driver.execute_script("return arguments[0].scrollTop", div_app)
            client_height = driver.execute_script("return arguments[0].clientHeight", div_app)

            if scroll_top + client_height >= scroll_height:
                break  # arrivé en bas

        time.sleep(2)
        # Scroll horizontalement la table
        table_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.overflow-x-auto"))
        )
        driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth", table_container)
        time.sleep(3)
