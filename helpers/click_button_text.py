from selenium.webdriver.common.by import By


def click_button_by_text(driver, button_text):
    xpath = f"//button[contains(normalize-space(), '{button_text}')]"
    driver.find_element(By.XPATH, xpath).click()
