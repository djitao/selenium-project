from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from helpers.menu_submenu_helpers import click_on_sidebar
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException





class Test_Historique_Versement_Partenaire:

    def test_navigation_envoi(self, driver, login):
        # 1️⃣ Attendre que le menu apparaisse
        menu_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
        )

        # Scroll du menu principal pour révéler tous les items
        scroll_step = 200
        for _ in range(10):  # maximum 10 scrolls
            driver.execute_script("arguments[0].scrollTop += arguments[1];", menu_container, scroll_step)
            time.sleep(0.2)

            scroll_height = driver.execute_script("return arguments[0].scrollHeight", menu_container)
            scroll_top = driver.execute_script("return arguments[0].scrollTop", menu_container)
            client_height = driver.execute_script("return arguments[0].clientHeight", menu_container)

            if scroll_top + client_height >= scroll_height:
                break  # atteint le bas

        time.sleep(0.5)

        # 2️⃣ Click sur "Partenaires"
        gestion_op_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Partenaires']]"))
        )
        gestion_op_btn.click()
        time.sleep(1)

        # 3️⃣ Click sur "Historique de versement partenaire"
        # Attendre que l'élément soit visible
        gestion_envoi = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/historiqueVersementChef']"))
        )

        # Scroller jusqu'à l'élément et cliquer via JS
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", gestion_envoi)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", gestion_envoi)

        # 4️⃣ Attendre que le conteneur principal soit present
        div_app = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#app"))
        )

        # 5️⃣ Scroll complet de div#app de manière robuste
        scroll_step = 20
        max_attempts_no_change = 5
        no_change_count = 0
        previous_scroll_top = -1

        while True:
            try:
                # Récupérer l'élément à chaque itération pour éviter StaleElementReference
                div_app = driver.find_element(By.CSS_SELECTOR, "div#app")
                driver.execute_script("arguments[0].scrollTop += arguments[1];", div_app, scroll_step)
                time.sleep(0.3)

                scroll_top = driver.execute_script("return arguments[0].scrollTop;", div_app)
                scroll_height = driver.execute_script("return arguments[0].scrollHeight;", div_app)
                client_height = driver.execute_script("return arguments[0].clientHeight;", div_app)

                # Si plus aucun changement ou atteint le bas, arrêter
                if scroll_top == previous_scroll_top:
                    no_change_count += 1
                    if no_change_count >= max_attempts_no_change:
                        break
                else:
                    no_change_count = 0

                if scroll_top + client_height >= scroll_height:
                    break

                previous_scroll_top = scroll_top

            except StaleElementReferenceException:
                # Récupérer l'élément à nouveau et continuer
                time.sleep(0.01)
                continue
        time.sleep(3)