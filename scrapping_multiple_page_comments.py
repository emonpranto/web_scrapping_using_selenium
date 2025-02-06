import os 
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.113 Safari/537.36')

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

driver.get('''https://www.daraz.com.bd/products/xiaomi-wi-fi-n300-i355981644-s1751281598.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253A%253Bnid%253A355981644%253Bsrc%253
           ALazadaMainSrp%253Brn%253A2309313217285312ad59e5fbd39d22ca%253Bregion%253Abd%253Bsku%253A355981644_BD%253Bprice%253A1250%253Bclient%253Adesktop%253Bsupplier_id%25
           3A5406%253Bbiz_source%253Ahp_categories%253Bslot%253A11%253Butlog_bucket_id%253A470687%253Basc_category_id%253A128%253Bitem_id%253A355981644%253Bsku_id%253A175128
           1598%253Bshop_id%253A5411%253BtemplateInfo%253A&freeshipping=0&fs_ab=1&fuse_fs=&lang=en&location=Dhaka&price=1.25E%203&priceCompare=skuId%3A1751281598%3Bsource%3A
           lazada-search-voucher%3Bsn%3A2309313217285312ad59e5fbd39d22ca%3BoriginPrice%3A125000%3BdisplayPrice%3A125000%3BsinglePromotionId%3A50000028020001%3BsingleToolCode
           %3ApromPrice%3BvoucherPricePlugin%3A0%3Btimestamp%3A1738151008260&ratingscore=4.544642857142857&request_id=2309313217285312ad59e5fbd39d22ca&review=112&sale=715&se
           arch=1&source=search&spm=a2a0e.searchlistcategory.list.11&stock=1''')

rating = driver.find_element(By.XPATH, '//*[@id="module_product_review_star_1"]/div/a[1]').text
no_comment = re.findall(r'\d+',rating)[0]

page_no = round(int(no_comment)/5)

height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
    time.sleep(0.2)

    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height==height:
        break
    height=new_height

def wait_for_button_clickable(xpath, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )


def click_button(xpath):
    try:
        wait_for_button_clickable(xpath)
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(1)  
    except Exception as e:
        print(f"Error clicking button: {e}")


comments = []

def comment_extraction():
    content = driver.find_elements(By.CLASS_NAME,'content')
    for comment in content:
        comments.append(comment.text)

try:
    for i in range(1,page_no+1):
        page_no_local= 0
        if i ==1 :
            comment_extraction()
        elif i>4 and i<page_no :
            page_no_local=4
            button=f'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[{str(page_no_local)}]'
            click_button(button)
            time.sleep(1)
            comment_extraction()
        
            
        elif i==page_no:
            page_no_local=5
            button= f'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[{str(page_no_local)}]'
            click_button(button)
            time.sleep(1)
            comment_extraction()
            
        else:
            page_no_local=i
            button= f'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[{str(page_no_local)}]'
            click_button(button)
            time.sleep(1)
            comment_extraction()

        
    print('Comment extraction successfully done.')

except Exception as e:
    print(f"There is an exception on executing this code is: {e}")
print(comments)
print(len(comments))






driver.quit()