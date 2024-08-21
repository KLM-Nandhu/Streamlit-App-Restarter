import streamlit as st
import requests
import time

# List of applications with their URLs and names
applications = [
    {"url": "https://excel-assistant.streamlit.app/", "name": "Excel Bot"},
    {"url": "https://college-buddy-final.streamlit.app/", "name": "College Buddy Assistant"},
    {"url": "https://bentswoodworking-assistant.streamlit.app/", "name": "Bent's Woodworking Assistant"},
    {"url": "https://active-cyber.streamlit.app/", "name": "Active Cyber"},
    {"url": "https://gallo-buddy.streamlit.app/", "name": "Gallo Buddy"}
]

def wake_up_app(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

st.title("Streamlit App Restarter")

if st.button("GET-UP KLM you ready for the war"):
    for app in applications:
        st.write(f"Waking up {app['name']}...")
        if wake_up_app(app['url']):
            st.success(f"{app['name']} is now awake!")
            st.markdown(f"[Open {app['name']}]({app['url']})")
        else:
            st.error(f"Failed to wake up {app['name']}. Please try again later.")
        time.sleep(2)  # Add a small delay between each app restart attempt

st.write("Click the button above to wake up all applications.")
