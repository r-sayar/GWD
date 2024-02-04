from selenium import webdriver
import csv
from selenium.webdriver.common.by import By

# Define the login data
username = "robin.sayar@grundwerk.digital"
password = "asöldkjfasdljfasd"

# Define the 2D array
data = [["https://www.northdata.de/Labor-+und+Reinraumtechnik+Arnsdorf+GmbH,+Arnsdorf/Amtsgericht+Dresden+HRB+37868", "Doreen Adler"]]

# Initialize the Selenium webdriver
driver = webdriver.Chrome()
driver.get("https://www.northdata.de/_login")

input("Press enter to continue")


'''
# Login to the website
email_input = driver.find_element_by_css_selector("input[type='email']")
email_input.send_keys(username)

password_input = driver.find_element_by_css_selector("input[type='password']")
password_input.send_keys(password)
submit_button = driver.find_element_by_css_selector("button[type='submit']")
submit_button.click()
'''
# Iterate over each element in the array
for element in data:
    print(element)
    link = element[0]
    name = element[1]
    
    # Open the link in the current tab
    driver.get(link)
    
   #try
    
    list_element = driver.find_element(By.CLASS_NAME, "network.ui.grey.segment")
    # should get by name instead of xpath
    parent_element = list_element.find_element(By.XPATH, "..")
    href = parent_element.get_attribute("href")
    # Get all hrefs in the list_element
    hrefs = [a.get_attribute("href") for a in list_element.find_elements(By.TAG_NAME, "a")]

    # Check if any href contains the first name or last name
    first_name = name.split()[0]
    last_name = name.split()[1]
    matching_href = None

    for href in hrefs:
        if first_name in href or last_name in href:
            matching_href = href
            break

    # Go to the link which contains the first or last name
    if matching_href:
        driver.get(matching_href)
    else:
        element.append("name not found")
        continue
    
    # Search for the element containing the birthdate
    vita_element = driver.find_element_by_class_name("vita.ui.grey.segment")
    vita_text = vita_element.text
    
    # Extract the birthdate from the vita text
    if "geb. am" in vita_text:
        birthdate = vita_text.split("geb. am")[1].strip().split()[0]
    else:
        birthdate = "-"
    
    # Add the birthdate as the third element of the element
    element.append(birthdate)
    #except:
     #   element.append("no match found")

# Save the results as a CSV file
with open("results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

# Close the webdriver
driver.quit()
