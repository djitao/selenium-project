from selenium.webdriver import Keys


from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException



class Test_Etat_Nde:

    def test_navigation_envoi(self, driver, login):
        # Attendre que le menu apparaisse
        menu_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
        )

        # Click sur "Etats"
        gestion_op_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Etats']]"))
        )
        gestion_op_btn.click()
        time.sleep(3)
        # Attendre que le menu vertical soit présent
        menu_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
        )
        scroll_step = 200
        for _ in range(2):  # maximum 20 scrolls
            driver.execute_script("arguments[0].scrollTop += arguments[1];", menu_container, scroll_step)
            time.sleep(0.5)

            scroll_height = driver.execute_script("return arguments[0].scrollHeight", menu_container)
            scroll_top = driver.execute_script("return arguments[0].scrollTop", menu_container)
            client_height = driver.execute_script("return arguments[0].clientHeight", menu_container)

            if scroll_top + client_height >= scroll_height:
                break  # arrivé en bas

        time.sleep(2)

        # Click sur "etats NDE"
        gestion_envoi = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/coordinateur/etatPaiementSeen']"))
        )
        gestion_envoi.click()

        # Scroll progressif dans le div#app (limité à 20 itérations max pour éviter une boucle infinie)
        div_ap = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#app"))
        )

        scroll_step = 300
        for _ in range(20):  # maximum 20 scrolls
            driver.execute_script("arguments[0].scrollTop += arguments[1];", div_ap, scroll_step)
            time.sleep(0.5)

            scroll_height = driver.execute_script("return arguments[0].scrollHeight", div_ap)
            scroll_top = driver.execute_script("return arguments[0].scrollTop", div_ap)
            client_height = driver.execute_script("return arguments[0].clientHeight", div_ap)

            if scroll_top + client_height >= scroll_height:
                break  # arrivé en bas

        # Scroll horizontalement la table
        table_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.overflow-x-auto"))
        )
        driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth", table_container)
        time.sleep(3)


