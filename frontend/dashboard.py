import os

import pandas as pd
import requests
import streamlit as st

API_URL = st.secrets.get(
    "API_URL",
    os.getenv("API_URL", "https://job-tracker-api-bp1l.onrender.com"),
)
st.set_page_config(
    page_title="Job Tracker",
    page_icon="💼",
    layout="wide",
)
st.caption(f"Connected API: {API_URL}")


def initialize_session_state():
    defaults = {
        "token": None,
        "logged_in": False,
        "email": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


def api_request(method, endpoint, **kwargs):
    try:
        return requests.request(
            method,
            f"{API_URL}{endpoint}",
            timeout=10,
            **kwargs,
        )
    except requests.RequestException:
        st.error(
            "Cannot connect to the API. Start FastAPI first with: "
            "`python -m uvicorn app.main:app --reload`"
        )
        return None


def login(email, password):
    response = api_request(
        "POST",
        "/users/login",
        data={
            "username": email,
            "password": password,
        },
    )

    if response is None:
        return

    if response.status_code == 200:
        st.session_state.token = response.json()["access_token"]
        st.session_state.email = email
        st.session_state.logged_in = True
        st.success("Login successful.")
        st.rerun()

    detail = response.json().get("detail", "Login failed")
    st.error(detail)
    return


def register(email, password):
    response = api_request(
        "POST",
        "/users/register",
        json={
            "email": email,
            "password": password,
        },
    )

    if response is None:
        return

    if response.status_code == 201:
        st.success("Account created. You can now log in.")
        return

    try:
        detail = response.json().get("detail", "Registration failed")
    except requests.exceptions.JSONDecodeError:
        detail = (
            f"Registration failed (HTTP {response.status_code}). "
            f"Server response: {response.text[:200]}"
        )

    st.error(detail)

def logout():
    st.session_state.token = None
    st.session_state.email = None
    st.session_state.logged_in = False
    st.rerun()


def fetch_applications():
    response = api_request(
        "GET",
        "/applications/",
        headers=get_headers(),
    )

    if response is None:
        return []

    if response.status_code == 401:
        st.error("Your session expired. Please log in again.")
        logout()

    if response.status_code != 200:
        st.error("Could not load applications.")
        return []

    return response.json()


def create_application(company, role, app_status, notes):
    response = api_request(
        "POST",
        "/applications/",
        headers=get_headers(),
        json={
            "company": company,
            "role": role,
            "status": app_status,
            "notes": notes or None,
        },
    )

    if response is None:
        return

    if response.status_code == 201:
        st.success("Job application added.")
        st.rerun()

    st.error(response.json().get("detail", "Could not add application."))


def update_status(application_id, new_status):
    response = api_request(
        "PATCH",
        f"/applications/{application_id}",
        headers=get_headers(),
        json={
            "status": new_status,
        },
    )

    if response is None:
        return

    if response.status_code == 200:
        st.success("Status updated.")
        st.rerun()

    st.error(response.json().get("detail", "Could not update application."))


def delete_application(application_id):
    response = api_request(
        "DELETE",
        f"/applications/{application_id}",
        headers=get_headers(),
    )

    if response is None:
        return

    if response.status_code == 200:
        st.success("Application deleted.")
        st.rerun()

    st.error(response.json().get("detail", "Could not delete application."))


def show_auth_page():
    st.title("💼 Job Tracker")
    st.caption("Track your job applications in one place.")
    st.caption(f"Connected API: {API_URL}")
    login_tab, register_tab = st.tabs(["Log in", "Create account"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )
            submitted = st.form_submit_button("Log in")

        if submitted:
            login(email, password)

    with register_tab:
        with st.form("register_form"):
            email = st.text_input("Email", key="register_email")
            password = st.text_input(
                "Password (minimum 8 characters)",
                type="password",
                key="register_password",
            )
            submitted = st.form_submit_button("Create account")

        if submitted:
            register(email, password)


def show_dashboard():
    st.sidebar.title("💼 Job Tracker")
    st.sidebar.write(f"Signed in as: `{st.session_state.email}`")

    if st.sidebar.button("Log out"):
        logout()

    st.title("Job Application Dashboard")
    st.caption("Manage your job search in one place.")

    applications = fetch_applications()

    if applications:
        dataframe = pd.DataFrame(applications)

        total = len(dataframe)
        applied = int((dataframe["status"] == "Applied").sum())
        interviews = int((dataframe["status"] == "Interview").sum())
        offers = int((dataframe["status"] == "Offer").sum())

        metric_1, metric_2, metric_3, metric_4 = st.columns(4)
        metric_1.metric("Total", total)
        metric_2.metric("Applied", applied)
        metric_3.metric("Interviews", interviews)
        metric_4.metric("Offers", offers)

        st.subheader("Application status overview")

        status_counts = (
            dataframe["status"]
            .value_counts()
            .reindex(
                ["Applied", "Interview", "Offer", "Rejected"],
                fill_value=0,
            )
        )

        st.bar_chart(status_counts)
    st.divider()

    left_column, right_column = st.columns([1, 2])

    with left_column:
        st.subheader("Add application")

        with st.form("create_application_form", clear_on_submit=True):
            company = st.text_input("Company")
            role = st.text_input("Role")
            app_status = st.selectbox(
                "Status",
                ["Applied", "Interview", "Offer", "Rejected"],
            )
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Add application")

        if submitted:
            if len(company.strip()) < 2 or len(role.strip()) < 2:
                st.error("Company and role must contain at least 2 characters.")
            else:
                create_application(
                    company.strip(),
                    role.strip(),
                    app_status,
                    notes.strip(),
                )

    with right_column:
        st.subheader("My applications")

        if not applications:
            st.info("No applications yet. Add your first one using the form.")
            return

        for application in applications:
            with st.expander(
                f'{application["company"]} — {application["role"]} '
                f'({application["status"]})'
            ):
                st.write(f'**Status:** {application["status"]}')

                if application.get("notes"):
                    st.write(f'**Notes:** {application["notes"]}')

                status_column, delete_column = st.columns([3, 1])

                with status_column:
                    new_status = st.selectbox(
                        "Change status",
                        ["Applied", "Interview", "Offer", "Rejected"],
                        index=[
                            "Applied",
                            "Interview",
                            "Offer",
                            "Rejected",
                        ].index(application["status"]),
                        key=f'status_{application["id"]}',
                    )

                    if st.button(
                        "Update status",
                        key=f'update_{application["id"]}',
                    ):
                        update_status(application["id"], new_status)

                with delete_column:
                    st.write("")
                    st.write("")
                    if st.button(
                        "Delete",
                        key=f'delete_{application["id"]}',
                        type="secondary",
                    ):
                        delete_application(application["id"])


initialize_session_state()

if st.session_state.logged_in:
    show_dashboard()
else:
    show_auth_page()

    