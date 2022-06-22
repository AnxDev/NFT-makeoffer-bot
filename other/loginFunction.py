def log_in(driver, site):
    global password, secret_phrase
    driver.switch_to.window(driver.window_handles[0])
    driver.minimize_window()
    phrase = secret_phrase.lower().split()
    wait_for_element(driver, By.XPATH, "//button [@role='button']")
    nextbutton = driver.find_element_by_class_name("btn--rounded")
    nextbutton.click()
    
    time.sleep(1)
    wait_for_element(driver, By.CLASS_NAME, "btn--rounded")
    driver.find_elements_by_class_name("btn--rounded")[0].click()
    wait_for_element(driver, By.CLASS_NAME, "btn-primary")
    driver.find_element_by_class_name("btn-primary").click()
    wait_for_element(driver, By.ID, "password")
    passwordfield = driver.find_element_by_id("password")
    #phrasefield = driver.find_element_by_id("import-srp__srp-word-0")
    confirmpasswordfield = driver.find_element_by_id("confirm-password")
    for i in range(len(phrase)):
        driver.find_element_by_id(f"import-srp__srp-word-{i}").send_keys(phrase[i])
    passwordfield.send_keys(password)
    confirmpasswordfield.send_keys(password)
    
    driver.find_element_by_id("create-new-vault__terms-checkbox").click()
    confirmpasswordfield.send_keys(key.ENTER)
    
    driver.get("https://opensea.io/login?referrer=%2Faccount")
    numberofwindows = len(driver.window_handles)
    
    wait_for_element(driver, By.CLASS_NAME, "elements__StyledListItem-sc-197zmwo-0")
    open_metamask(driver, numberofwindows)
    
    
    
    

    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("password").send_keys(key.ENTER)
    
    wait_for_element(driver, By.CLASS_NAME, "box")
    driver.find_elements_by_class_name("box")[3].click()
    wait_for_element(driver, By.CLASS_NAME, "btn-secondary")
    driver.find_element_by_class_name("btn-secondary").click()
    driver.get("https://opensea.io/login?referrer=%2Faccount")
    
    driver.find_elements_by_class_name("elements__StyledListItem-sc-197zmwo-0")[0].click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[3])
    print(driver.current_url)
    wait_for_element(driver, By.CLASS_NAME, "btn-primary")
    driver.find_element_by_class_name("btn-primary").click()
    wait_for_element(driver, By.CLASS_NAME, "btn-primary")
    driver.find_element_by_class_name("btn-primary").click()
    driver.switch_to.window(driver.window_handles[0])
    try:
        driver.get(site + "?search[sortAscending]=true&search[sortBy]=CREATED_DATE")
    except:
        print("Il driver di google non è aggiornato alla tua versione, elimina il file chromedriver.exe e sostituiscilo con la tua versione che puoi scaricare su: https://chromedriver.chromium.org/downloads\nPoi riavvia il programma.")