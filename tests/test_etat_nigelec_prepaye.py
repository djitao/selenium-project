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



class Test_Etat_Nigelec_prepaye:

    def test_navigation_etat_nigelec_prepaye(self, driver, login):
        wait = WebDriverWait(driver, 30)

        # 1️⃣ Attendre le menu VISIBLE
        menu = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "nav-links"))
        )

        # 2️⃣ Cliquer sur "Etats" de manière robuste l
        etats_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Etats']/ancestor::a")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", etats_btn)
        etats_btn.click()

        # 3️⃣ Cliquer sur "Etats Nigelec Prépayé"
        nigelec_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href,'etatPaiementNigelecPrepaye')]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", nigelec_btn)
        nigelec_btn.click()

        # 4️⃣ ASSERT — vérifier qu’on est sur la bonne page
        wait.until(EC.url_contains("etatPaiementNigelecPrepaye"))

        # 5️⃣ Attendre la table (preuve que la page est chargée)
        table_container = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.overflow-x-auto")
            )
        )

        # 6️⃣ Scroll horizontal (SAFE)
        driver.execute_script(
            "arguments[0].scrollLeft = arguments[0].scrollWidth",
            table_container
        )

        # 7️⃣ ASSERT FINAL (OBLIGATOIRE)
        assert "Nigelec" in driver.page_source
