from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_if_present(driver, xpath, timeout=15):
    try:
        # Vérifie que l'élément est dans le DOM (présent mais pas forcément visible)
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        element.click()
        return True
    except:
        print(f"❌ Élément non trouvé : {xpath}")
        return False
