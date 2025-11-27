def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", element)