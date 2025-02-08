import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Initiating the Streamlit app
st.header('Web Scraping Bot BY Tawshok')
st.title('Search Bar')
text = st.text_input('Enter the topic you want to scrape links for:')
button = st.button('Search')

if button:  # The condition will be true only if the button is clicked
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Start the driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")
    time.sleep(2)

    # Find search box and enter query
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(text)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    results = []

    # Scrape first 3 pages
    for page in range(3):
        time.sleep(3)  # Wait for the page to load

        # Extract titles and links
        search_results = driver.find_elements(By.CSS_SELECTOR, 'h3')  # Titles are usually in <h3> tags

        for result in search_results:
            try:
                title = result.text
                link = result.find_element(By.XPATH, './..').get_attribute('href')  # Get the parent <a> tag's href
                results.append({
                    'title': title,
                    'link': link
                    })
            except Exception as e:
                print(f"Error extracting link: {e}")

        # Click the "Next" button for pagination
        try:
            next_button = driver.find_element(By.ID, 'pnnext')  # Find the "Next" button
            next_button.click()
        except Exception as e:
            print(f"Error clicking the Next button: {e}")
            break  # Exit the loop if the "Next" button is not found

    driver.quit()

    # Convert results to DataFrame
    data = pd.DataFrame(results)
    st.subheader('Results')
    st.dataframe(data)

    # Save to CSV file
    data.to_csv('Leads.csv', index=False)
    st.success("Scraping Completed! File saved as 'Leads.csv'")