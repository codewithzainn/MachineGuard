import streamlit as st
import os
import io
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from functions import (
    summary_stat_of_features,
    split_and_rename_X_summary,
    removing_redundant_features_columns,
    create_accumulator_condition_features,
    create_cooler_conditions_features,
    create_pump_leakage_features,
    convert_numpy_to_pandas
)


# ============================================================
# PAGE CONFIG (must be the first Streamlit command)
# ============================================================

st.set_page_config(
    page_title="MachineGuard | Predictive Maintenance",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

@st.cache_data
def load_model():

    # Project root directory
    base_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    artefact_path = os.path.join(
        base_path,
        "model_and_artefacts"
    )

    artefacts = {
        "model": "xgboost_model.pkl",
        "pca": "pca.pkl",
        "scaler": "scaler.pkl"
    }

    loaded = {}

    for key, filename in artefacts.items():

        file_path = os.path.join(
            artefact_path,
            filename
        )

        if not os.path.exists(file_path):

            raise FileNotFoundError(
                f"Missing artefact: {filename}\n"
                f"Expected location: {file_path}"
            )

        try:

            loaded[key] = joblib.load(file_path)

        except Exception as e:

            raise RuntimeError(
                f"Failed to load {filename}: {e}"
            )

    return (
        loaded["model"],
        loaded["pca"],
        loaded["scaler"]
    )


# Load model
model, pca, scaler = load_model()


# ============================================================
# CUSTOM CSS — MACHINEGUARD DARK INDUSTRIAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */
    .stApp {
        background-color: #0e1117;
        color: #e6e9ef;
    }

    section[data-testid="stSidebar"] {
        background-color: #12161f;
        border-right: 1px solid #232838;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #dfe4ee !important;
    }

    /* ---------- Header ---------- */
    .mg-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 24px;
        background: linear-gradient(180deg, #141926 0%, #10141d 100%);
        border: 1px solid #232838;
        border-radius: 12px;
        margin-bottom: 22px;
    }

    .mg-header-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .mg-logo {
        font-size: 30px;
        line-height: 1;
    }

    .mg-title {
        font-size: 24px;
        font-weight: 700;
        color: #f2f5fa;
        margin: 0;
        letter-spacing: 0.3px;
    }

    .mg-subtitle {
        font-size: 13.5px;
        color: #8b93a7;
        margin: 2px 0 0 0;
    }

    .mg-status-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 999px;
        background: rgba(34, 211, 238, 0.08);
        border: 1px solid rgba(34, 211, 238, 0.35);
        font-size: 12.5px;
        color: #67e8f9;
        font-weight: 600;
        white-space: nowrap;
    }

    .mg-status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22d3ee;
        box-shadow: 0 0 8px 2px rgba(34, 211, 238, 0.6);
    }

    /* ---------- Hero ---------- */
    .mg-hero {
        padding: 20px 24px;
        background: #12161f;
        border: 1px solid #232838;
        border-radius: 12px;
        margin-bottom: 24px;
    }

    .mg-hero-title {
        font-size: 18px;
        font-weight: 700;
        color: #f2f5fa;
        margin: 0 0 6px 0;
    }

    .mg-hero-text {
        font-size: 14px;
        color: #9aa2b6;
        margin: 0;
        line-height: 1.55;
    }

    /* ---------- Section headers ---------- */
    .mg-section-title {
        font-size: 16px;
        font-weight: 700;
        color: #f2f5fa;
        margin: 6px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ---------- Equipment status cards ---------- */
    .mg-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #232838;
        background: #12161f;
        text-align: center;
        margin-bottom: 10px;
    }

    .mg-card-healthy {
        border: 1px solid rgba(52, 211, 153, 0.4);
        background: rgba(52, 211, 153, 0.06);
    }

    .mg-card-maintenance {
        border: 1px solid rgba(248, 113, 113, 0.45);
        background: rgba(248, 113, 113, 0.07);
    }

    .mg-card-icon {
        font-size: 26px;
        margin-bottom: 6px;
    }

    .mg-card-name {
        font-size: 13.5px;
        color: #9aa2b6;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 4px;
    }

    .mg-card-status {
        font-size: 16px;
        font-weight: 700;
    }

    .mg-card-status-healthy {
        color: #34d399;
    }

    .mg-card-status-maintenance {
        color: #f87171;
    }

    /* ---------- Overall status banner ---------- */
    .mg-overall {
        padding: 20px 24px;
        border-radius: 12px;
        border: 1px solid #232838;
        margin: 8px 0 24px 0;
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .mg-overall-icon {
        font-size: 30px;
    }

    .mg-overall-title {
        font-size: 12.5px;
        color: #9aa2b6;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin: 0 0 2px 0;
    }

    .mg-overall-text {
        font-size: 16px;
        font-weight: 700;
        margin: 0;
    }

    .mg-overall-critical {
        background: rgba(248, 113, 113, 0.08);
        border-color: rgba(248, 113, 113, 0.4);
    }

    .mg-overall-warning {
        background: rgba(251, 191, 36, 0.08);
        border-color: rgba(251, 191, 36, 0.4);
    }

    .mg-overall-ok {
        background: rgba(52, 211, 153, 0.08);
        border-color: rgba(52, 211, 153, 0.4);
    }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        background: linear-gradient(180deg, #22d3ee 0%, #06b6d4 100%);
        color: #06131a;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.4em;
        font-size: 15px;
        letter-spacing: 0.2px;
        transition: opacity 0.15s ease-in-out;
    }

    div.stButton > button:hover {
        opacity: 0.88;
        color: #06131a;
    }

    /* ---------- Expanders / containers ---------- */
    div[data-testid="stExpander"] {
        background: #12161f;
        border: 1px solid #232838;
        border-radius: 10px;
    }

    hr {
        border-color: #232838 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="mg-header">
        <div class="mg-header-left">
            <div class="mg-logo">⚙️</div>
            <div>
                <p class="mg-title">MachineGuard</p>
                <p class="mg-subtitle">AI-Powered Predictive Maintenance</p>
            </div>
        </div>
        <div class="mg-status-pill">
            <div class="mg-status-dot"></div>
            System Monitoring Active
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO / INTRODUCTION
# ============================================================

st.markdown(
    """
    <div class="mg-hero">
        <p class="mg-hero-title">Predictive Maintenance Intelligence</p>
        <p class="mg-hero-text">
            Analyze hydraulic system sensor readings and identify equipment
            conditions before maintenance issues become critical. Enter the
            sensor readings in the sidebar, then run a maintenance analysis
            to see the predicted condition of the Cooler, Pump, and Accumulator.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR - SENSOR INPUTS
# ============================================================

st.sidebar.markdown("### 🧭 Sensor Inputs")
st.sidebar.write("Enter the current sensor readings below, organized by system.")

st.sidebar.markdown("---")

with st.sidebar.expander("🩸 Pressure Sensors", expanded=True):

    Pressure_1 = st.number_input(
        "Pressure_1 Reading",
        value=0.00,
        format="%.2f"
    )

    Pressure_2 = st.number_input(
        "Pressure_2 Reading",
        value=0.00,
        format="%.2f"
    )

    Pressure_3 = st.number_input(
        "Pressure_3 Reading",
        value=0.00,
        format="%.2f"
    )

    Pressure_4 = st.number_input(
        "Pressure_4 Reading",
        value=0.00,
        format="%.2f"
    )

    Pressure_5 = st.number_input(
        "Pressure_5 Reading",
        value=0.00,
        format="%.2f"
    )

    Pressure_6 = st.number_input(
        "Pressure_6 Reading",
        value=0.00,
        format="%.2f"
    )


with st.sidebar.expander("🌡️ Temperature Sensors"):

    Temperature_1 = st.number_input(
        "Temperature_1 Reading",
        value=0.00,
        format="%.2f"
    )

    Temperature_2 = st.number_input(
        "Temperature_2 Reading",
        value=0.00,
        format="%.2f"
    )

    Temperature_3 = st.number_input(
        "Temperature_3 Reading",
        value=0.00,
        format="%.2f"
    )

    Temperature_4 = st.number_input(
        "Temperature_4 Reading",
        value=0.00,
        format="%.2f"
    )


with st.sidebar.expander("💧 Flow Sensors"):

    Flow_sensor_1 = st.number_input(
        "Flow_sensor_1 Reading",
        value=0.00,
        format="%.2f"
    )

    Flow_sensor_2 = st.number_input(
        "Flow_sensor_2 Reading",
        value=0.00,
        format="%.2f"
    )


with st.sidebar.expander("❄️ Efficiency & Cooling"):

    Stable_efficiency = st.number_input(
        "Stable_efficiency Reading",
        value=0.00,
        format="%.2f"
    )

    Cooling_efficiency = st.number_input(
        "Cooling_efficiency Reading",
        value=0.00,
        format="%.2f"
    )

    Cooling_power = st.number_input(
        "Cooling_power Reading",
        value=0.00,
        format="%.2f"
    )

    Efficiency_power_signal = st.number_input(
        "Efficiency_power_signal Reading",
        value=0.00,
        format="%.2f"
    )


with st.sidebar.expander("📳 Vibration"):

    Vibration_sensor = st.number_input(
        "Vibration_sensor Reading",
        value=0.00,
        format="%.2f"
    )


st.sidebar.markdown("---")
st.sidebar.caption(
    "Once all readings are entered, click **Run Maintenance Analysis** "
    "in the main panel."
)


# ============================================================
# CREATE INPUT DATAFRAME
# ============================================================

input_data = pd.DataFrame({

    "pressure_readings_1": [Pressure_1],

    "pressure_readings_2": [Pressure_2],

    "pressure_readings_3": [Pressure_3],

    "pressure_readings_4": [Pressure_4],

    "pressure_readings_5": [Pressure_5],

    "pressure_readings_6": [Pressure_6],

    "temperature_readings_1": [Temperature_1],

    "temperature_readings_2": [Temperature_2],

    "temperature_readings_3": [Temperature_3],

    "temperature_readings_4": [Temperature_4],

    "flow_sensor_readings_1": [Flow_sensor_1],

    "flow_sensor_readings_2": [Flow_sensor_2],

    "stable_efficiency_readings_1": [Stable_efficiency],

    "cooling_efficiency_readings_1": [Cooling_efficiency],

    "cooling_power_readings_1": [Cooling_power],

    "vibration_sensor_readings_1": [Vibration_sensor],

    "efficiency_power_signal_readings_1": [
        Efficiency_power_signal
    ]

})


# ============================================================
# PREPROCESSING
# ============================================================

def process(input_data):

    # Summary statistics
    input_data = summary_stat_of_features(input_data)

    # Split and rename
    input_data = split_and_rename_X_summary(input_data)

    # Remove redundant columns
    input_data = removing_redundant_features_columns(
        input_data
    )

    # Feature engineering

    create_cooler_conditions_features(
        input_data
    )

    create_pump_leakage_features(
        input_data
    )

    create_accumulator_condition_features(
        input_data
    )

    # Check for infinite values (e.g. divide-by-zero in feature
    # engineering when sensor readings are left at their default
    # 0.00 values), then treat them the same way as missing values

    input_data = input_data.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Check missing values

    if input_data.isnull().sum().sum() > 0:

        st.warning(
            "⚠️ Some sensor readings produced missing or infinite "
            "values. These have been replaced with 0."
        )

        input_data = input_data.fillna(0)

    # Scaling

    X_scaled = scaler.transform(
        input_data
    )

    # PCA

    input_data = pca.transform(
        X_scaled
    )

    # Convert numpy to pandas

    input_data = convert_numpy_to_pandas(
        input_data
    )

    return input_data


# ============================================================
# PREDICTION
# ============================================================

def predict(input_data):

    prediction = model.predict(
        input_data
    )

    equipment_names = [
        "Cooler",
        "Pump",
        "Accumulator"
    ]

    condition_mapping = {
        0: "Healthy",
        1: "Needs Maintenance"
    }

    predicted_conditions = []

    for equipment, pred in zip(
        equipment_names,
        prediction[0]
    ):

        condition = condition_mapping.get(
            int(pred),
            "Unknown Condition"
        )

        predicted_conditions.append(
            f"{equipment}: {condition}"
        )

    return predicted_conditions


# ============================================================
# PLOT PREDICTIONS
# ============================================================

def plot_prediction(predicted_conditions):

    plt.style.use("dark_background")

    fig = plt.figure(
        figsize=(9, 3.4)
    )

    fig.patch.set_facecolor("#12161f")
    plt.gca().set_facecolor("#12161f")

    equipment_names = [
        "Cooler",
        "Pump",
        "Accumulator"
    ]

    stats = []

    for condition in predicted_conditions:

        if "Needs Maintenance" in condition:

            stats.append(
                "Needs Maintenance"
            )

        else:

            stats.append(
                "Healthy"
            )

    bars = plt.bar(
        equipment_names,
        [1, 1, 1],
        color=[
            "#f87171"
            if status == "Needs Maintenance"
            else "#34d399"
            for status in stats
        ]
    )

    plt.yticks([])

    plt.xticks(
        fontsize=12,
        fontweight="bold",
        color="#e6e9ef"
    )

    for spine in plt.gca().spines.values():

        spine.set_visible(False)

    for bar, status in zip(
        bars,
        stats
    ):

        plt.gca().text(
            bar.get_x()
            + bar.get_width() / 2,

            bar.get_height() - 0.4,

            status,

            ha="center",

            color="#0e1117" if status == "Healthy" else "white",

            fontweight="bold",

            fontsize=11
        )

    buf = io.BytesIO()

    fig.savefig(
        buf,
        format="png",
        transparent=True,
        dpi=200,
        bbox_inches="tight"
    )

    buf.seek(0)

    st.image(buf)

    plt.close(fig)


# ============================================================
# UI HELPER — EQUIPMENT STATUS CARD
# ============================================================

def render_equipment_card(equipment_name, status):

    is_healthy = "Needs Maintenance" not in status

    card_class = "mg-card-healthy" if is_healthy else "mg-card-maintenance"
    status_class = "mg-card-status-healthy" if is_healthy else "mg-card-status-maintenance"
    icon = "✅" if is_healthy else "🔴"
    status_text = "Healthy" if is_healthy else "Needs Maintenance"

    st.markdown(
        f"""
        <div class="mg-card {card_class}">
            <div class="mg-card-icon">{icon}</div>
            <div class="mg-card-name">{equipment_name}</div>
            <div class="mg-card-status {status_class}">{status_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RUN ANALYSIS BUTTON
# ============================================================

st.markdown(
    '<div class="mg-section-title">🚀 Maintenance Analysis</div>',
    unsafe_allow_html=True
)

run_analysis = st.button(
    "Run Maintenance Analysis"
)

if run_analysis:

    # --------------------------------------------------------
    # Process input
    # --------------------------------------------------------

    processed_data = process(
        input_data.copy()
    )

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    predicted_conditions = predict(
        processed_data
    )

    # --------------------------------------------------------
    # DISPLAY INDIVIDUAL PREDICTIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="mg-section-title">🔍 Equipment Health</div>',
        unsafe_allow_html=True
    )

    equipment_names = ["Cooler", "Pump", "Accumulator"]

    card_cols = st.columns(3)

    for col, equipment, condition in zip(
        card_cols,
        equipment_names,
        predicted_conditions
    ):

        with col:

            render_equipment_card(
                equipment,
                condition
            )

    # --------------------------------------------------------
    # Count maintenance requirements
    # --------------------------------------------------------

    num_maintenance_needed = sum(
        "Needs Maintenance" in condition
        for condition in predicted_conditions
    )

    # --------------------------------------------------------
    # System status
    # --------------------------------------------------------

    st.markdown(
        '<div class="mg-section-title">🛡️ System Health Overview</div>',
        unsafe_allow_html=True
    )

    if num_maintenance_needed == 3:

        system_status = "Immediate maintenance required!"
        overall_class = "mg-overall-critical"
        overall_icon = "🔴"

    elif num_maintenance_needed == 2:

        system_status = "Schedule maintenance soon."
        overall_class = "mg-overall-warning"
        overall_icon = "🟠"

    elif num_maintenance_needed == 1:

        system_status = "System manageable."
        overall_class = "mg-overall-warning"
        overall_icon = "🟡"

    else:

        system_status = "System is operating normally."
        overall_class = "mg-overall-ok"
        overall_icon = "🟢"

    st.markdown(
        f"""
        <div class="mg-overall {overall_class}">
            <div class="mg-overall-icon">{overall_icon}</div>
            <div>
                <p class="mg-overall-title">Overall System Status</p>
                <p class="mg-overall-text">{system_status}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Visualization
    # --------------------------------------------------------

    st.markdown(
        '<div class="mg-section-title">📊 Equipment Health Visualization</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        plot_prediction(
            predicted_conditions
        )

    # --------------------------------------------------------
    # PCA data
    # --------------------------------------------------------

    with st.expander("🔬 Technical Details / PCA Data"):

        st.write(
            "After preprocessing and scaling, the sensor readings are "
            "reduced to principal components before being passed to the "
            "trained model:"
        )

        st.write(
            processed_data
        )

else:

    st.info(
        "Enter sensor readings in the sidebar, then click "
        "**Run Maintenance Analysis** to generate a prediction."
    )


# ============================================================
# INPUT DATA
# ============================================================

st.markdown(
    '<div class="mg-section-title">📥 Submitted Sensor Data</div>',
    unsafe_allow_html=True
)

with st.expander("View Submitted Sensor Data"):

    st.markdown(
        """
        <span style='font-size:14px; color:#9aa2b6;'>
        After clicking <b>Run Maintenance Analysis</b>, this data is
        transformed into Principal Component Analysis (PCA) data before
        being passed to the model.
        </span>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        input_data
    )


# ============================================================
# ABOUT / TECHNICAL INFORMATION
# ============================================================

with st.expander("ℹ️ About / Technical Information"):

    st.write(
        """
        MachineGuard's underlying model was developed based on sensor
        readings from stable cycles of the **UCI Hydraulic Test Rig
        Dataset** for predictive maintenance.
        """
    )
