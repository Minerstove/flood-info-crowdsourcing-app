import folium
import streamlit as st
from streamlit_folium import st_folium

import services


METRO_MANILA_CENTER = [14.5995, 120.9842]

FLOOD_LEVELS = [
    "ankle_deep",
    "knee_deep",
    "waist_deep",
    "chest_deep",
    "not_passable",
]

ROAD_CONDITIONS = [
    "passable",
    "difficult",
    "blocked",
    "strong_current",
]

NEEDS_OPTIONS = [
    "food",
    "water",
    "rescue",
    "medicine",
    "shelter",
    "none",
]


def render() -> None:
    st.title("Report Flood")
    st.caption("Submit a field report for communities and NGO response teams.")

    location_method = st.radio(
        "Location input method",
        ("Type coordinates", "Select on map"),
        horizontal=True,
    )

    selected_latitude = None
    selected_longitude = None

    if location_method == "Select on map":
        selected_latitude, selected_longitude = _render_location_picker()

    with st.form("flood_report_form", clear_on_submit=True):
        if location_method == "Type coordinates":
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", format="%.6f", value=None)
            with col2:
                longitude = st.number_input("Longitude", format="%.6f", value=None)
        else:
            latitude = selected_latitude
            longitude = selected_longitude
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(
                    "Selected latitude",
                    value=_format_coordinate(latitude),
                    disabled=True,
                )
            with col2:
                st.text_input(
                    "Selected longitude",
                    value=_format_coordinate(longitude),
                    disabled=True,
                )

        location_name = st.text_input("Location name")

        col3, col4 = st.columns(2)
        with col3:
            flood_level = st.selectbox(
                "Flood level",
                options=[""] + FLOOD_LEVELS,
                format_func=lambda value: "Select flood level" if value == "" else value,
            )
        with col4:
            road_condition = st.selectbox(
                "Road condition",
                options=[""] + ROAD_CONDITIONS,
                format_func=lambda value: "Select road condition" if value == "" else value,
            )

        needs = st.multiselect("Urgent needs", NEEDS_OPTIONS, default=["none"])
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Submit Report")

    if submitted:
        try:
            report_id = services.submit_flood_report(
                {
                    "latitude": latitude,
                    "longitude": longitude,
                    "location_name": location_name,
                    "flood_level": flood_level,
                    "road_condition": road_condition,
                    "needs": needs,
                    "notes": notes,
                }
            )
            st.success(f"Flood report submitted. Report ID: {report_id}")
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Could not submit report: {exc}")


def _render_location_picker() -> tuple[float | None, float | None]:
    st.info("Click the map to choose the flood report location.")

    latitude = st.session_state.get("selected_report_latitude")
    longitude = st.session_state.get("selected_report_longitude")
    map_center = (
        [latitude, longitude]
        if latitude is not None and longitude is not None
        else METRO_MANILA_CENTER
    )

    picker_map = folium.Map(location=map_center, zoom_start=12)
    if latitude is not None and longitude is not None:
        folium.Marker(
            location=[latitude, longitude],
            tooltip="Selected report location",
            icon=folium.Icon(color="blue", icon="map-marker"),
        ).add_to(picker_map)

    map_data = st_folium(picker_map, width=1200, height=420, key="report_location_map")
    last_clicked = map_data.get("last_clicked") if map_data else None

    if last_clicked:
        latitude = float(last_clicked["lat"])
        longitude = float(last_clicked["lng"])
        st.session_state.selected_report_latitude = latitude
        st.session_state.selected_report_longitude = longitude
        st.success(f"Selected location: {latitude:.6f}, {longitude:.6f}")
    elif latitude is not None and longitude is not None:
        st.success(f"Selected location: {latitude:.6f}, {longitude:.6f}")

    return latitude, longitude


def _format_coordinate(value: float | None) -> str:
    if value is None:
        return "No map location selected yet"
    return f"{value:.6f}"
