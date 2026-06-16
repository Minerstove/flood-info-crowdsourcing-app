import streamlit as st

import database
import dashboard_view
import map_view
import report_view


def main() -> None:
    st.set_page_config(page_title="BahaWatch PH", layout="wide")
    database.create_table()

    st.sidebar.title("BahaWatch PH")
    selected_page = st.sidebar.radio(
        "Navigation",
        ("Live Flood Map", "Report Flood", "NGO Dashboard"),
    )

    if selected_page == "Live Flood Map":
        map_view.render()
    elif selected_page == "Report Flood":
        report_view.render()
    elif selected_page == "NGO Dashboard":
        dashboard_view.render()


if __name__ == "__main__":
    main()
