# MachineGuard — AI-Powered Predictive Maintenance

## Project Overview

**MachineGuard** is a machine-learning-based predictive maintenance system for **hydraulic equipment**.

The system analyzes sensor readings from a hydraulic test rig and uses an **XGBoost classification model** to assess the condition of three key components:

* **Cooler**
* **Pump**
* **Accumulator**

For each component, the system predicts whether it is:

* **Healthy**
* **Needs Maintenance**

MachineGuard provides an interactive **Streamlit web application** where sensor readings can be entered and the predicted equipment condition can be visualized.

---

## Features

* **Predictive Maintenance** — Detect potential maintenance requirements from hydraulic sensor readings.
* **XGBoost Classification** — Uses a trained XGBoost model for equipment-condition prediction.
* **Feature Engineering** — Creates equipment-specific features for the Cooler, Pump, and Accumulator.
* **PCA Dimensionality Reduction** — Reduces the dimensionality of the processed feature set.
* **Data Scaling** — Uses a trained StandardScaler before PCA and model prediction.
* **Interactive Streamlit Dashboard** — Provides a user-friendly interface for entering sensor readings.
* **Equipment-Level Predictions** — Displays the predicted condition of the Cooler, Pump, and Accumulator individually.
* **System Health Status** — Provides an overall maintenance status based on the equipment predictions.
* **Interactive Visualization** — Displays equipment conditions through a visual status chart.
* **Model Artifacts** — Includes the trained XGBoost model, scaler, and PCA artifacts required for prediction.
* **Database Scripts** — Includes PostgreSQL/PgAdmin SQL scripts for creating and managing the project database.

---

## Technology Stack

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-Learn**
* **XGBoost**
* **Joblib**
* **Matplotlib**
* **Streamlit**
* **PostgreSQL**
* **PgAdmin**
* **Jupyter Notebook**

---

## Project Structure

```text
MachineGuard/
│
├── assets/
│   ├── accumulator_condition.png
│   ├── cooler_condition.png
│   ├── pca_explained_variance.png
│   ├── pump_leakage.png
│   └── screenshots
│
├── data/
│   ├── synthetic_hydraulic_test_data.csv
│   ├── condition+monitoring+of+hydraulic+systems.zip
│   └── unzipped_data/
│
├── model_and_artefacts/
│   ├── model_metrics.txt
│   ├── pca.pkl
│   ├── scaler.pkl
│   └── xgboost_model.pkl
│
├── notebook/
│   └── Predictive_Maintenance_Classification.ipynb
│
├── python_and_deployment_scripts/
│   ├── functions.py
│   └── streamlit_deployment.py
│
├── sql_scripts/
│   ├── check_tables.sql
│   ├── create_indexes.sql
│   ├── create_tables.sql
│   └── optimize_query.sql
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/codewithzainn/MachineGuard.git
cd MachineGuard
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

The MachineGuard interface is built with **Streamlit**.

From the project root, run:

```bash
streamlit run python_and_deployment_scripts/streamlit_deployment.py
```

After starting Streamlit, open the local URL displayed in the terminal.

---

## How MachineGuard Works

The prediction pipeline follows these main stages:

```text
Sensor Readings
       ↓
Feature Engineering
       ↓
Feature Processing
       ↓
Data Scaling
       ↓
PCA Transformation
       ↓
XGBoost Model
       ↓
Equipment Predictions
       ↓
System Health Status
```

The application processes the entered hydraulic sensor readings using the same preprocessing and transformation pipeline associated with the trained model.

---

## Sensor Inputs

MachineGuard works with sensor measurements from the hydraulic test rig, including:

### Pressure Sensors

* Pressure 1
* Pressure 2
* Pressure 3
* Pressure 4
* Pressure 5
* Pressure 6

### Temperature Sensors

* Temperature 1
* Temperature 2
* Temperature 3
* Temperature 4

### Flow Sensors

* Flow Sensor 1
* Flow Sensor 2

### Efficiency and System Measurements

* Stable Efficiency
* Cooling Efficiency
* Cooling Power
* Vibration Sensor
* Efficiency Power Signal

---

## Feature Engineering

The preprocessing pipeline creates features used to evaluate equipment conditions, including:

* **Cooler Condition Features**
* **Pump Leakage Features**
* **Accumulator Condition Features**
* **Statistical Feature Summaries**
* **Redundant Feature Removal**

The resulting features are then scaled and transformed using the saved preprocessing artifacts.

---

## Machine Learning Model

### Algorithm

MachineGuard uses an **XGBoost Classifier** for equipment-condition prediction.

### Preprocessing

The prediction pipeline uses:

1. Feature engineering
2. Statistical feature processing
3. Redundant feature removal
4. Standard scaling
5. Principal Component Analysis (PCA)
6. XGBoost classification

### Prediction Labels

The equipment-condition predictions use:

```text
0 → Healthy
1 → Needs Maintenance
```

The application evaluates the condition of:

```text
Cooler
Pump
Accumulator
```

---

## Model Artifacts

The trained model and preprocessing components are stored in:

```text
model_and_artefacts/
```

### Included Artifacts

| File                | Purpose                          |
| ------------------- | -------------------------------- |
| `xgboost_model.pkl` | Trained XGBoost prediction model |
| `scaler.pkl`        | Saved feature scaler             |
| `pca.pkl`           | Saved PCA transformation         |
| `model_metrics.txt` | Model evaluation information     |

These artifacts allow the Streamlit application to perform predictions without retraining the model every time the application starts.

---

## Database

The project also contains PostgreSQL database scripts under:

```text
sql_scripts/
```

These scripts support database creation, table creation, indexing, and query optimization for the hydraulic-system dataset.

Available scripts include:

* `create_tables.sql`
* `create_indexes.sql`
* `check_tables.sql`
* `optimize_query.sql`

---

## Dataset

MachineGuard uses the **Condition Monitoring of Hydraulic Systems** dataset from the **UCI Machine Learning Repository**.

The dataset contains sensor measurements collected from a hydraulic test rig and provides information used for condition monitoring and predictive maintenance.

Dataset:

https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems

The dataset should be used according to the terms and conditions provided by the UCI Machine Learning Repository.

---

## Testing with New Sensor Data

The project includes:

```text
data/synthetic_hydraulic_test_data.csv
```

for testing the prediction workflow with sensor readings.

The Streamlit application also allows sensor values to be entered manually through the interface.

After entering the readings:

1. Enter the sensor values.
2. Run the prediction.
3. View the equipment-level predictions.
4. Review the overall system health status.
5. Inspect the visualization and processed prediction information.

---

## System Health Status

MachineGuard summarizes the individual equipment predictions to provide an overall system status.

The application distinguishes between different levels of maintenance requirement based on the number of components that require maintenance.

The individual equipment results remain visible so that the user can identify which component requires attention.

---

## Visualization

MachineGuard provides visual feedback for the predicted equipment conditions.

The application displays the status of:

```text
Cooler
Pump
Accumulator
```

and provides a visual representation of their predicted condition.

---

## Notebook

The machine-learning development and analysis work is available in:

```text
notebook/Predictive_Maintenance_Classification.ipynb
```

The notebook provides the development context behind the predictive-maintenance model and its preprocessing workflow.

---

## Project Purpose

MachineGuard demonstrates how machine learning can be applied to **industrial condition monitoring and predictive maintenance**.

The project combines:

* Sensor data
* Feature engineering
* Machine learning
* Dimensionality reduction
* Data preprocessing
* Database management
* Interactive visualization
* Streamlit deployment

into a single predictive-maintenance application for hydraulic systems.

---

## Future Improvements

Potential future improvements include:

* Incorporating additional real-world industrial datasets.
* Expanding the prediction workflow with time-series analysis.
* Improving failure prediction horizons.
* Adding additional equipment-condition indicators.
* Deploying the application to a cloud environment.

---

## Author

**Zain Ul Abideen**

GitHub: https://github.com/codewithzainn

---

## Acknowledgements

MachineGuard uses the **Condition Monitoring of Hydraulic Systems** dataset from the **UCI Machine Learning Repository**.

Special thanks to the UCI Machine Learning Repository and the dataset contributors for making the hydraulic-system data available for research and development.

---

## License

This project is intended for educational and research purposes.

The dataset used by MachineGuard is provided by the **UCI Machine Learning Repository** and remains subject to its respective terms and licensing conditions.

---

**MachineGuard — Built for Reliability, Efficiency, and Industrial AI Applications.**
