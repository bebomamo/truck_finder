import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
    
def main():
    # URL of the website to scrape
    url = "https://tboi.com/repentance"

    # Send an HTTP GET request to the website
    response = requests.get(url)

    # Parse the HTML code using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the relevant information from the HTML code (first searching by tag then by classes)

    ### FINDING A SPECIFIC TAG SECTION, USEFUL FOR CHECKING IF FIELDS UPDATED ###
    tag = soup.find("body").find("div", {"class":"repentanceitems-container"}).find("li", {"data-tid":"172"})

    print(tag)
    ##############################################################################

    ### USER INPUT, FINDING TEXT, FINDS PARENT OF THE SPECIFIED TEXT, EXTRACTS A SPECIFIC TAG FIELD ###
    item_name = input("Input an items exact name:\n")

    item = soup.find(string=item_name)

    item_parent = (item.parent).parent

    item_info = item_parent.find("p", {"class":"pickup"})

    print(item_info.string)
    ####################################################################################################

    return



if __name__ == "__main__":
    main()