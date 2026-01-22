# EcoTrack: Intelligent Air Quality Analytics Engine 🌍

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**EcoTrack** is a data-driven environmental monitoring solution designed to aggregate, store, and analyze real-time Air Quality Index (AQI) metrics. By integrating with global telemetry APIs, the system provides actionable health insights and visual trend analysis to aid in environmental decision-making.

This project demonstrates core competencies in **Backend Development**, **Database Management**, and **Data Visualization**.

---

## ⚡ Key Technical Features

* **📡 Real-Time Telemetry Integration**
    * Connects to the **WAQI (World Air Quality Index) REST API** to fetch live particulate matter (PM2.5/PM10) data with low latency.
    * Handles JSON response parsing and error management for high reliability.

* **💾 Robust Data Persistence**
    * Implements a normalized **MySQL** database schema to archive historical environmental data.
    * Prevents data redundancy through intelligent duplicate checking before insertion.

* **📊 Dynamic Data Visualization**
    * Utilizes **Matplotlib** to generate comparative line graphs, enabling longitudinal analysis of pollution trends across multiple cities.

* **🏥 Automated Health Heuristics**
    * Algorithmic categorization of AQI levels (0-500) into standardized health impact groups (e.g., "Good," "Hazardous") based on EPA standards.

* **📂 ETL (Extract, Transform, Load) Capability**
    * Built-in export module to serialize database records into **CSV/Excel** formats for external reporting and downstream analysis.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|:----------|:-----------|:------------|
| **Core Logic** | Python 3.13 | Main application logic and orchestration. |
| **Database** | MySQL 8.0 | Relational database for historical data storage. |
| **API** | WAQI API | External source for real-time environmental data. |
| **Visualization** | Matplotlib | Library for generating trend analysis graphs. |
| **Networking** | Requests | HTTP library for API communication. |

---

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.x installed
* MySQL Server running locally
* Internet connection for API access

### 1. Clone the Repository

```bash
git clone https://github.com/Prakhar0206/EcoTrack-AQI-Monitoring.git
cd EcoTrack-AQI-Monitoring
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Initialization

Launch your MySQL command line and execute the following to create the required database. The application will handle table creation automatically.

```sql
CREATE DATABASE aqi_project;
```

### 4. Configuration

Open `main.py` and update the security credentials section:

```python
# Security Credentials
password = 'YOUR_MYSQL_PASSWORD'
api_token = 'YOUR_WAQI_API_TOKEN'
```

### 5. Execution

```bash
python main.py
```

---

## 🔮 Future Scope

* [ ] GUI Implementation (Tkinter/PyQt) for enhanced user experience.
* [ ] Machine Learning integration for predictive AQI forecasting.
* [ ] Cloud Database Deployment (AWS RDS) for remote accessibility.

---

## 👥 Author

**Prakhar Aggarwal** - Lead Developer - [GitHub Profile](https://github.com/Prakhar0206)

---

## 📄 License

Licensed under the MIT License.
