import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# List of applications with their URLs and names
applications = [
    {"url": "https://excel-assistant.streamlit.app/", "name": "Excel Bot"},
    {"url": "https://college-buddy-final.streamlit.app/", "name": "College Buddy Assistant"},
    {"url": "https://bentswoodworking-assistant.streamlit.app/", "name": "Bent's Woodworking Assistant"},
    {"url": "https://active-cyber.streamlit.app/", "name": "Active Cyber"},
    {"url": "https://gallo-buddy.streamlit.app/", "name": "Gallo Buddy"}
]

def wake_up_app(driver, app):
    url = app['url']
    name = app['name']
    
    try:
        driver.get(url)
        # Wait for the "Yes, get this app back up!" button to appear
        wake_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Yes, get this app back up!')]"))
        )
        wake_button.click()
        
        # Wait for the app to load (you might need to adjust this based on the specific app)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        return f"{name} is now awake!"
    except TimeoutException:
        return f"{name} is already awake or couldn't be awakened."

st.title("Streamlit App Awakener")

if st.button("GET-UP KLM you ready for the war"):
    # Setup Selenium WebDriver using webdriver_manager
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    for app in applications:
        status = wake_up_app(driver, app)
        if "awake" in status:
            st.success(status)
            st.markdown(f"[Open {app['name']}]({app['url']})")
        else:
            st.warning(status)
        time.sleep(2)  # Add a small delay between each app awakening attempt
    
    driver.quit()

st.write("Click the button above to wake up all applications.")
