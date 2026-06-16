import pandas as pd
import streamlit as st

import database
import services


def render() -> None:
    st.title("NGO Dashboard")
    st.caption("Review, filter, export, and update submitted flood reports.")

    reports = database.get_reports()
    df = services.reports_to_dataframe(reports)

    if df.empty:
        st.info("No flood reports have been submitted yet.")
        return

    filtered_df = _apply_filters(df)
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv_data,
        file_name="bahawatch_ph_reports.csv",
        mime="text/csv",
    )

    _render_admin_actions(df)


def _apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("Filters")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        flood_levels = st.multiselect(
            "Flood level",
            sorted(df["flood_level"].dropna().unique()),
        )
    with col2:
        road_conditions = st.multiselect(
            "Road condition",
            sorted(df["road_condition"].dropna().unique()),
        )
    with col3:
        verification_statuses = st.multiselect(
            "Verification status",
            sorted(df["verification_status"].dropna().unique()),
        )
    with col4:
        needs = st.multiselect(
            "Urgent needs",
            _unique_needs(df),
        )

    filtered_df = df.copy()
    if flood_levels:
        filtered_df = filtered_df[filtered_df["flood_level"].isin(flood_levels)]
    if road_conditions:
        filtered_df = filtered_df[filtered_df["road_condition"].isin(road_conditions)]
    if verification_statuses:
        filtered_df = filtered_df[
            filtered_df["verification_status"].isin(verification_statuses)
        ]
    if needs:
        filtered_df = filtered_df[
            filtered_df["needs"].fillna("").apply(
                lambda value: any(need in _split_needs(value) for need in needs)
            )
        ]

    return filtered_df


def _render_admin_actions(df: pd.DataFrame) -> None:
    st.subheader("Update Report Status")

    report_id = st.number_input(
        "Report ID",
        min_value=1,
        step=1,
        value=int(df["id"].min()),
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Mark as Verified"):
            database.verify_report(int(report_id))
            st.success(f"Report #{report_id} marked as verified.")
            st.rerun()
    with col2:
        if st.button("Mark as Resolved"):
            database.resolve_report(int(report_id))
            st.success(f"Report #{report_id} marked as resolved.")
            st.rerun()


def _unique_needs(df: pd.DataFrame) -> list[str]:
    needs = set()
    for value in df["needs"].fillna(""):
        needs.update(_split_needs(value))
    return sorted(needs)


def _split_needs(value: str) -> list[str]:
    return [need.strip() for need in value.split(",") if need.strip()]
