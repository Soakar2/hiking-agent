import streamlit as st
import re

# Simple regex for email validation
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

st.title("🥾 AI Hiking Agent")
st.subheader("Get daily trail recommendations in your inbox.")

# Email Input Section
with st.form("signup_form", clear_on_submit=True):
    email = st.text_input("Enter your email to join the list:")
    submit_button = st.form_submit_button("Sign Me Up")

    if submit_button:
        if is_valid_email(email):
            # Save to a local file (CSV) for now
            with open("subscribers.csv", "a") as f:
                f.write(f"{email}\n")
            st.success(f"Dope! {email} has been added to the list.")
        else:
            st.error("Wait, that doesn't look like a real email address.")

st.info("We'll only email you when the weather is perfect for a hike.")