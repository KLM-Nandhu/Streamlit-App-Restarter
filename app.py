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

def wake_up_app(url, max_retries=3, timeout=20):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            st.write(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(5)  # Wait 5 seconds before retrying
    return False

st.title("Streamlit App Restarter")

if st.button("GET-UP KLM you ready for the war"):
    for app in applications:
        st.write(f"Waking up {app['name']}...")
        if wake_up_app(app['url']):
            st.success(f"{app['name']} is now awake!")
            st.markdown(f"[Open {app['name']}]({app['url']})")
        else:
            st.error(f"Failed to wake up {app['name']} after multiple attempts. Please try manually.")
        time.sleep(5)  # Increased delay between app wake-up attempts
    
    # Attempt to refresh the page after all wake-up attempts
    st.experimental_rerun()

st.write("Click the button above to wake up all applications.")

# Display all app links, regardless of wake-up status
st.subheader("All Application Links:")
for app in applications:
    st.markdown(f"[{app['name']}]({app['url']})")

# Add some information about potential limitations
st.info("""
Note: The ability to wake up apps may be limited by their hosting setup. 
If an app doesn't wake up automatically, you may need to click its link and wake it up manually.
""")
