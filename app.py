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
                        return f"{name} was sleeping and has been successfully awakened!"
                    else:
                        return f"{name} is sleeping, but wake-up attempt was unsuccessful. Status: {wake_response.status_code}"
                else:
                    return f"{name} is already awake and running!"
            else:
                return f"Failed to access {name}. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return f"Error accessing {name}: {str(e)}"
        
        time.sleep(delay)
        delay *= 2  # Exponential backoff

    return f"Failed to wake up {name} after {max_retries} attempts. The app might be offline or require manual intervention."

st.title("Streamlit App Awakener")

if st.button("GET-UP KLM"):
    progress_bar = st.progress(0)
    status_placeholders = [st.empty() for _ in applications]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_app = {executor.submit(wake_up_app, app): app for app in applications}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_app)):
            app = future_to_app[future]
            result = future.result()
            status_placeholders[i].write(result)
            if "successfully awakened" in result or "already awake" in result:
                status_placeholders[i].success(f"[Open {app['name']}]({app['url']})")
            else:
                status_placeholders[i].warning(result)
            progress_bar.progress((i + 1) / len(applications))

    st.success("All wake-up attempts completed!")

st.write("Click the button above to attempt waking up all applications.")
st.write("Note: If apps remain unresponsive, they might require manual intervention or be temporarily offline.")
