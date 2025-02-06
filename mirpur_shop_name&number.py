import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--incognito')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.117 Safari/537.36')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.google.com/')

driver.refresh()

search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('Laptopshop Near Mirpur')
time.sleep(1)
search_box.send_keys(Keys.RETURN)

re_captcha = driver.find_element(By.CLASS_NAME,'g-recaptcha')
action = ActionChains(driver)
time.sleep(1.5)
action.move_to_element(re_captcha).click().perform()

time.sleep(10)
map = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div[1]/div/div/div/a[1]').click()

height = driver.execute_script('return document.body.scrollHeight')
print(height)


scrollable_div = driver.find_element(By.CLASS_NAME, "m6QErb")  # Container class

for _ in range(34):  # Adjust the range for more scrolling
    ActionChains(driver).move_to_element(scrollable_div).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)  # Wait for new results to load

shops = driver.find_elements(By.CLASS_NAME, "qBF1Pd")
phones = driver.find_elements(By.CLASS_NAME, "UsdlK")

dict = {}
for i in range(len(phones)):

    dict[shops[i].text]=phones[i].text

print(dict)
time.sleep(20) 

driver.quit()