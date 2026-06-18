# BahaWatch PH 🌊

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-ff4b4b)
![SQLite](https://img.shields.io/badge/Database-SQLite-003b57)
![Folium](https://img.shields.io/badge/Maps-Folium-green)
![Pandas](https://img.shields.io/badge/Dashboard-Pandas-150458)
![Status](https://img.shields.io/badge/Status-MVP-orange)
![License](https://img.shields.io/badge/License-Not%20specified-lightgrey)

BahaWatch PH is a Python web application for crowdsourced flood reporting in the Philippines. It helps community members submit flood reports and gives NGOs a simple live map and dashboard for monitoring flood conditions, urgent needs, and report status.

The app is built with Streamlit, Folium, SQLite, and Pandas. It is intentionally lightweight so it can run locally with a single command and store reports in a local SQLite database.

## Features ✨

- 📝 Submit flood reports with latitude and longitude.
- 🗺️ Choose a location by typing coordinates or clicking on an interactive map.
- 📍 Record location name, flood level, road condition, urgent needs, and notes.
- 🌐 View all submitted reports on a Folium map centered on Metro Manila.
- 🚦 Color-code map markers by flood level.
- 📊 Review reports in an NGO dashboard table.
- 🔎 Filter reports by flood level, road condition, verification status, and urgent needs.
- ✅ Mark reports as verified or resolved.
- ⏱️ Show report age in hours and label older reports as possibly outdated or expired.
- 📤 Export filtered dashboard results as a CSV file.

## Tech Stack 🧰

- 🐍 Python
- 🎈 Streamlit
- 🗺️ Folium
- 🧩 streamlit-folium
- 🗄️ SQLite
- 🐼 Pandas

## Project Structure 📁

```text
flood-info-crowdsourcing-app/
|
|-- app.py
|-- database.py
|-- models.py
|-- services.py
|-- report_view.py
|-- map_view.py
|-- dashboard_view.py
|-- requirements.txt
|-- README.md
|
`-- data/
    `-- flood_reports.db
```

## Module Overview 🧱

- `app.py` is the main Streamlit entry point. It initializes the database and routes users to the selected sidebar page.
- `models.py` defines the `FloodReport` dataclass used across the app.
- `database.py` manages the SQLite connection, table creation, report inserts, report loading, and status updates.
- `services.py` contains validation and business logic, including report submission, marker colors, dataframe conversion, and report age calculations.
- `report_view.py` renders the public flood report form.
- `map_view.py` renders the live Folium flood map.
- `dashboard_view.py` renders the NGO dashboard, filters, CSV export, and report status actions.

## Report Fields 📋

Each flood report stores:

- Report ID
- Created timestamp
- Latitude
- Longitude
- Location name
- Flood level
- Road condition
- Urgent needs
- Notes
- Verification status
- Confirmations count

## Flood Levels 🌧️

The app supports these flood level values:

- `ankle_deep`
- `knee_deep`
- `waist_deep`
- `chest_deep`
- `not_passable`

Map marker colors are based on flood level:

- `ankle_deep`: green
- `knee_deep`: orange
- `waist_deep`: red
- `chest_deep`: dark red
- `not_passable`: black

If a report is submitted as `not_passable`, the app automatically stores its road condition as `blocked`.

## Road Conditions 🚧

The app supports these road condition values:

- `passable`
- `difficult`
- `blocked`
- `strong_current`

## Urgent Needs 🆘

The app supports these urgent needs values:

- `food`
- `water`
- `rescue`
- `medicine`
- `shelter`
- `none`

## Report Status ✅

Reports start with a verification status of `unverified`.

NGO or admin users can update reports to:

- `verified`
- `resolved`

The dashboard also calculates report freshness:

- `active`: up to 6 hours old
- `possibly outdated`: older than 6 hours
- `expired`: older than 12 hours

## Installation ⚙️

Create and activate a virtual environment if desired:

```bash
python -m venv .venv
```

On Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App ▶️

Start the Streamlit app with:

```bash
streamlit run app.py
```

Streamlit will open the app in your browser. If it does not open automatically, use the local URL shown in the terminal.

## How to Use 🧭

### Submit a Flood Report 📝

1. Open the sidebar.
2. Select `Report Flood`.
3. Choose a location input method:
   - `Type coordinates`
   - `Select on map`
4. Fill in the flood level, road condition, urgent needs, and any notes.
5. Click `Submit Report`.

### View the Live Flood Map 🗺️

1. Open the sidebar.
2. Select `Live Flood Map`.
3. Click report markers to see details such as location, flood level, needs, status, timestamp, and notes.

### Use the NGO Dashboard 📊

1. Open the sidebar.
2. Select `NGO Dashboard`.
3. Filter reports by flood level, road condition, verification status, or urgent needs.
4. Download the filtered table as CSV.
5. Enter a report ID to mark a report as verified or resolved.

## Database 🗄️

The app uses SQLite and stores data in:

```text
data/flood_reports.db
```

The database table is created automatically when the app starts. No separate migration step is required for this MVP.

## Acceptance Criteria ✅

- A user can submit a flood report.
- A user can select a report location manually or from a map.
- Reports are saved in SQLite.
- Reports appear on the live map.
- The NGO dashboard displays all reports.
- Dashboard filters work.
- Reports can be marked as verified or resolved.
- Reports can be exported as CSV.

## Notes 📝

This is an MVP designed for clarity and simplicity. It does not include authentication, user accounts, deployment configuration, or a public report confirmation workflow yet.
