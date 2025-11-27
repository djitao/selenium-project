# helpers/select_ville_helpers.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def select_ville(driver, ville, timeout=10):
    """
    Sélectionne une ville dans un champ Select2 basé sur son libellé visible.

    :param driver: WebDriver Selenium
    :param ville: str, ex: "NIAMEY (NIGER 00227)"
    :param timeout: temps d'attente max (en secondes)
    """

    wait = WebDriverWait(driver, timeout)

    try:
        # 1. Ouvrir le champ Select2 (via l'élément d'affichage actuel)
        champ_ville = wait.until(EC.element_to_be_clickable(
            (By.ID, "select2-idSelectedVille-container")
        ))
        champ_ville.click()

        # 2. Saisir le nom de la ville dans le champ de recherche
        input_search = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "select2-search__field")
        ))
        input_search.clear()
        input_search.send_keys(ville)

        # 3. Attendre et cliquer sur la ville correspondante dans la liste déroulante
        option_ville = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//li[contains(text(), \"{ville}\")]")
        ))
        option_ville.click()

    except TimeoutException:
        driver.save_screenshot("erreur_select_ville.png")
        raise Exception(f"❌ Impossible de sélectionner la ville : {ville}")
