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



class Test_Envoi_Dargent:

    def test_navigation_envoi(self, driver, login):
        # Attendre que le menu apparaisse
        menu_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
        )

        # Click sur "Gestion des opérations"
        gestion_op_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Gestion des opérations']]"))
        )
        gestion_op_btn.click()

        # Click sur "Gestion des envois"
        gestion_envoi = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/coordinateur/gestionEnvois']"))
        )
        gestion_envoi.click()

        # Localiser le bouton et scroller dessus
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(normalize-space(), 'Numéro Destinataire')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

        # Attendre l’input
        input_numero_dest = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "numeroDestId"))
        )
        time.sleep(3)
        input_numero_dest.send_keys("92803406")
        time.sleep(3)

        driver.find_element(By.ID, "destBtnId").click()
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
        time.sleep(3)
        # Scroll horizontalement la table (lent et progressif)
        table_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.overflow-x-auto"))
        )

        scroll_step = 150
        for _ in range(30):
            driver.execute_script("arguments[0].scrollLeft += arguments[1];", table_container, scroll_step)
            time.sleep(0.2)
            current = driver.execute_script("return arguments[0].scrollLeft;", table_container)
            max_scroll = driver.execute_script("return arguments[0].scrollWidth;", table_container)
            if current >= max_scroll:
                break

        # Trouver toutes les icônes d'édition dans la table
        icons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//table//i[contains(@class,'fa-pen-to-square')]")
            )
        )

        if not icons:
            raise Exception("❌ Aucune icône d'édition trouvée dans la table")

        # Prendre la première icône trouvée
        edit_icon = icons[0]
        # Scroll automatique vers l'icône
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", edit_icon)
        time.sleep(1)

        # Essayer clic normal
        try:
            edit_icon.click()
        except:
            # sinon clic JS
            driver.execute_script("arguments[0].click();", edit_icon)