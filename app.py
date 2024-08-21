import streamlit as st
import requests
import time
import concurrent.futures

# List of applications with their URLs and names
applications = [
    {"url": "https://excel-assistant.streamlit.app/", "name": "Excel Bot"},
    {"url": "https://college-buddy-final.streamlit.app/", "name": "College Buddy Assistant"},
    {"url": "https://bentswoodworking-assistant.streamlit.app/", "name": "Bent's Woodworking Assistant"},
    {"url": "https://active-cyber.streamlit.app/", "name": "Active Cyber"},
    {"url": "https://gallo-buddy.streamlit.app/", "name": "Gallo Buddy"}
]

def wake_up_app(app):
    url = app['url']
    name = app['name']
    max_retries = 3
    delay = 2

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                if "Yes, get this app back up!" in response.text:
                    # App is sleeping, attempt to wake it up
                    wake_response = requests.get(url, params={"rerun": "true"}, timeout=15)
                    if wake_response.status_code == 200 and "Yes, get this app back up!" not in wake_response.text:
                        return "awakened"
                    else:
                        return "sleeping"
                else:
                    return "awake"
            else:
                return "error"
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1:
                return "error"
        
        time.sleep(delay)
        delay *= 2  # Exponential backoff

    return "error"

st.title("Streamlit App Awakener")

if 'app_states' not in st.session_state:
    st.session_state.app_states = {app['name']: 'unknown' for app in applications}

if 'loading' not in st.session_state:
    st.session_state.loading = {app['name']: False for app in applications}

def restart_app(app_name):
    st.session_state.loading[app_name] = True
    st.session_state.app_states[app_name] = 'unknown'
    st.experimental_rerun()

cols = st.columns(len(applications))

for i, app in enumerate(applications):
    with cols[i]:
        st.subheader(app['name'])
        
        if st.session_state.loading[app['name']]:
            status = wake_up_app(app)
            st.session_state.app_states[app['name']] = status
            st.session_state.loading[app['name']] = False

        if st.session_state.app_states[app['name']] == 'unknown':
            st.info("Status unknown")
        elif st.session_state.app_states[app['name']] == 'awake':
            st.success("Awake and running")
        elif st.session_state.app_states[app['name']] == 'awakened':
            st.success("Successfully awakened")
        elif st.session_state.app_states[app['name']] == 'sleeping':
            st.warning("Sleeping, wake-up failed")
        else:
            st.error("Error accessing app")

        st.markdown(f"[Open App]({app['url']})")
        
        if st.button(f"Restart {app['name']}", key=f"restart_{app['name']}"):
            restart_app(app['name'])

        if st.session_state.loading[app['name']]:
            st.write("Loading...")
            st.spinner()

if st.button("Restart All Apps"):
    for app in applications:
        st.session_state.loading[app['name']] = True
        st.session_state.app_states[app['name']] = 'unknown'
    st.experimental_rerun()

st.write("Click on individual 'Restart' buttons or 'Restart All Apps' to attempt waking up the applications.")
st.write("Note: If apps remain unresponsive, they might require manual intervention or be temporarily offline.")
