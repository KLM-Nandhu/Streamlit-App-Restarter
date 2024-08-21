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
                        return f"{name} has been successfully awakened!"
                    else:
                        return f"{name} is still sleeping. Manual wake-up may be required."
                else:
                    return f"{name} is already awake and running!"
            else:
                return f"Failed to access {name}. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return f"Error accessing {name}: {str(e)}"
        
        time.sleep(delay)
        delay *= 2  # Exponential backoff

    return f"Failed to wake up {name} after {max_retries} attempts. Manual intervention may be needed."

st.title("Streamlit App Awakener")

if 'awakening_in_progress' not in st.session_state:
    st.session_state.awakening_in_progress = False

if 'results' not in st.session_state:
    st.session_state.results = []

if st.button("GET-UP KLM you ready for the war", disabled=st.session_state.awakening_in_progress):
    st.session_state.awakening_in_progress = True
    st.session_state.results = []
    
    progress_bar = st.progress(0)
    status_message = st.empty()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_app = {executor.submit(wake_up_app, app): app for app in applications}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_app)):
            app = future_to_app[future]
            result = future.result()
            st.session_state.results.append(result)
            status_message.text(f"Processing: {app['name']}")
            progress_bar.progress((i + 1) / len(applications))
            time.sleep(1)  # Short delay for visual feedback

    st.session_state.awakening_in_progress = False
    status_message.empty()
    st.experimental_rerun()

if st.session_state.results:
    st.subheader("Wake-up Results:")
    for result in st.session_state.results:
        if "successfully awakened" in result or "already awake" in result:
            st.success(result)
        elif "still sleeping" in result or "Failed to wake up" in result:
            st.warning(result)
        else:
            st.error(result)

    st.subheader("Application Links:")
    for app in applications:
        st.markdown(f"[{app['name']}]({app['url']})")

st.write("Click the button above to attempt waking up all applications.")
