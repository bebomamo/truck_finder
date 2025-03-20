import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
    
def main():
    # URLs of the websites to scrape
    DAT = "https://one.dat.com/search-trucks-ow"
    Turvo = "https://app.turvo.com/#/auth/login"
    Turvo_shipments = "https://app.turvo.com/#/UI9IynZ9/shipments-categories/list"
    # Instantiation of basic options
    options = Options()
    options.add_argument("--window-size=1920,1080")

    # DAT_Driver login and preparation for truckfinder
    # DAT_driver = Chrome(options=options)
    # DAT_driver.get(DAT)
    # time.sleep(3)
    # # Actions after website has been accessed
    # # Using XPATH to more easily specify web elements 
    # user_email = DAT_driver.find_element(By.XPATH, "//*[@id='mat-input-1']")
    # password = DAT_driver.find_element(By.XPATH, "//*[@id='mat-input-0']")
    # if (not user_email.is_selected()):
    #     print("Username/Email Selected")
    #     user_email.click()
    # user_email.send_keys("xyz@gmail.com")
    # if (not password.is_selected()):
    #     print("Password Selected")
    #     password.click()
    # password.send_keys("westchester")
    # # ... do the rest of the login stuff and ultimately navigate to the truck locator ...
    # time.sleep(5)
    # DAT_driver.minimize_window()


    # Turvo login ########################################################################
    turvo_driver = Chrome(options=options)
    turvo_driver.get(Turvo)
    time.sleep(3)
    EMAIL_KEY = 0
    PASSWORD_KEY = 1
    SIGN_IN_BUTTON_KEY = 2
    curr = 0
    turvo_email = turvo_driver.find_element(By.CLASS_NAME, "form-group")
    turvo_pass = turvo_driver.find_element(By.CLASS_NAME, "form-group")
    turvo_sign_in_button = turvo_driver.find_element(By.CLASS_NAME, "form-group")
    forms = turvo_driver.find_elements(By.CLASS_NAME, "form-group")
    for form in forms:
        if curr == EMAIL_KEY:
            turvo_email = form.find_element(By.TAG_NAME, "input")
        if curr == PASSWORD_KEY:
            turvo_pass = form.find_element(By.TAG_NAME, "input")
        if curr == SIGN_IN_BUTTON_KEY:
            turvo_sign_in_button = form.find_element(By.TAG_NAME, "button")
        curr = curr + 1
    if (not turvo_email.is_selected()):
        print("Username/Email Selected")
        turvo_email.click()
    turvo_email.send_keys("USERNAME") #need to replace username with an actual username
    if (not turvo_pass.is_selected()):
        print("Password Selected")
        turvo_pass.click()
    turvo_pass.send_keys("PASSWORD") # same for password
    turvo_sign_in_button.click()
    time.sleep(5)
    ######################################################################################

    # Scrape Shipment orders #############################################################
    turvo_driver.get(Turvo_shipments)
    time.sleep(5)
    cur_shipment_elements = turvo_driver.find_elements(By.CLASS_NAME, "item-title")
    shipment_elements = [] #instantiate shipment elements list and dump first set of elements
    for element in cur_shipment_elements:
        shipment_elements.append(element.text)
    print(str(len(cur_shipment_elements)))

    #Find Count of Routes(elements)
    COUNT_KEY = 38
    curr = 0
    num_elements = turvo_driver.find_element(By.TAG_NAME, "span")
    count_elements = turvo_driver.find_elements(By.TAG_NAME, "span")
    for count in count_elements:
        if(curr == COUNT_KEY):
            num_elements = count
        curr+=1
    stop = len(num_elements.text)
    res = (num_elements.text)[:stop-10]
    results = int(res)

    # Begin Scrolling
    go_to = cur_shipment_elements[len(cur_shipment_elements)-11]
    print(go_to.text)
    ActionChains(turvo_driver).move_to_element(go_to).perform()
    # scroll_origin = ScrollOrigin.from_element(go_to,0,-50)
    # ActionChains(turvo_driver).scroll_from_origin(scroll_origin, 0, 800).perform() #Scroll in Widget window
    time.sleep(5)

    #Scroll Loop (update shipment elements, regrab bottom element to scroll from, repeat)
    while(len(shipment_elements) <= results):
        cur_shipment_elements = turvo_driver.find_elements(By.CLASS_NAME, "item-title")
        print(str(len(cur_shipment_elements)))
        time.sleep(1)
        for element in cur_shipment_elements:
            shipment_elements.append(element.text) #line sometimes causes StaleElementExceptiop (TO FIX)
        #Scroll again
        go_to = cur_shipment_elements[len(cur_shipment_elements)-11]
        print(go_to.text)
        ActionChains(turvo_driver).move_to_element(go_to).perform()

    # START_LOCATION = 4
    # DESTINATION = 5
    # JUMP_COUNT = 10
    count = 0
    current_element = ""
    for element in shipment_elements:
        if(count%10 == 0):
            print(current_element)
            current_element = ""
        else:
            current_element += element
        count+=1
        # if count%JUMP_COUNT == START_LOCATION:
        #     current_element+=element
        # elif count%JUMP_COUNT == DESTINATION:
        #     current_element+=" ------> "+element
        #     print(current_element)
        #     current_element = ""
        # count+=1




    print("Completed Run\n element count= "+str(len(shipment_elements)))
    input()


    # Send an HTTP GET request to the website
    # response = requests.get(url)

    # Parse the HTML code using BeautifulSoup
    # soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the relevant information from the HTML code (first searching by tag then by classes)

    ### Testing With DAT ONE ###
    # DAT_driver.quit()
    turvo_driver.quit()
    ############################

    return



if __name__ == "__main__":
    main()