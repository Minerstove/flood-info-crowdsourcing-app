import html

import folium
import streamlit as st
from streamlit_folium import st_folium

import database
import services


METRO_MANILA_CENTER = [14.5995, 120.9842]


def render() -> None:
    st.title("Live Flood Map")
    st.caption("Crowdsourced flood reports around Metro Manila.")

    reports = database.get_reports()
    flood_map = folium.Map(location=METRO_MANILA_CENTER, zoom_start=11)

    for report in reports:
        folium.Marker(
            location=[report.latitude, report.longitude],
            popup=folium.Popup(_build_popup(report), max_width=320),
            tooltip=report.location_name or f"Report #{report.id}",
            icon=folium.Icon(
                color=services.get_marker_color(report.flood_level),
                icon="info-sign",
            ),
        ).add_to(flood_map)

    st_folium(flood_map, width=1200, height=620)


def _build_popup(report) -> str:
    location_name = html.escape(report.location_name or "Unnamed location")
    notes = html.escape(report.notes or "No notes")
    needs = html.escape(report.needs or "none")

    return f"""
    <strong>{location_name}</strong><br>
    Flood level: {html.escape(report.flood_level)}<br>
    Road condition: {html.escape(report.road_condition)}<br>
    Needs: {needs}<br>
    Verification: {html.escape(report.verification_status)}<br>
    Confirmations: {report.confirmations}<br>
    Created: {html.escape(report.created_at)}<br>
    Notes: {notes}
    """
