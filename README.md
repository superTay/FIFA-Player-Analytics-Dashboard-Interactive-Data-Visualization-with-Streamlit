<!-- 🔹 Static Badges -->

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Data%20Viz-239120?logo=plotly&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML%20Model-F7931E?logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=flat)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Streamlit%20Cloud-orange)

# ⚽ FIFA Player Analytics Dashboard

An interactive and modular **Streamlit dashboard** for exploring, visualizing, and predicting FIFA player statistics.  
This project showcases advanced skills in **data visualization, caching, state management, and AI model integration**, following professional engineering standards and a clean modular architecture.

---

## 🌟 Overview

This dashboard allows users to:

- Load and clean FIFA player data from local or remote sources.
- Explore the dataset through **interactive filters and Plotly visualizations**.
- Analyze trends in player performance, value, and potential.
- Predict player potential using a **pre-trained Machine Learning model**.

Built with a focus on:

- **Modular Streamlit architecture**
- **Optimized caching and session state management**
- **Professional UI/UX principles**
- **Deployment-ready structure**

---

## 🧩 Project Structure

proyecto_fifa/
│
├── app.py # Main Streamlit app controller
│
├── modules/ # Modularized page components
│ ├── page_intro.py # Page 1 - Data loading & cleaning
│ ├── page_data_viz.py # Page 2 - Data visualization & filters
│ └── page_model_inference.py # Page 3 - Predictive model inference
│
├── assets/
│ ├── dataset_description.html # HTML dataset dictionary (from Kaggle)
│ └── model_fifa.pkl # Pre-trained model (generated locally)
│
├── data/
│ └── players_21.csv # Local FIFA dataset
│
├── create_dummy_model.py # Script to train and save a regression model
├── requirements.txt # Dependencies for reproducibility
└── README.md # Project documentation

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

````bash
git clone https://github.com/superTay/fifa-player-analytics.git
cd fifa-player-analytics


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/superTay/fifa-player-analytics.git
cd fifa-player-analytics

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Generate the model (if not already created)
python create_dummy_model.py

4️⃣ Run the Streamlit app
streamlit run app.py

🧠 Architecture & Functionality

🏁 Page 1 — Introduction

Loads and cleans the dataset with @st.cache_data.

Displays sample data and metadata using st.expander.

Shows dataset dictionary embedded via HTML.

Initializes st.session_state['df'] for global access.

📊 Page 2 — Data Visualization

Includes interactive filters (multiselects, sliders).

Uses @st.cache_data for unique value caching.

Stores filtered DataFrame in st.session_state['df_fil'].

Generates responsive Plotly charts (scatter, histogram, box, bar).

Displays results dynamically based on user filters.

🤖 Page 3 — Predictive Model

Loads a pre-trained regression model (LinearRegression) via joblib.

Allows users to input player attributes (age, overall, value_eur, etc.).

Predicts future potential rating interactively.

Uses @st.cache_resource for efficient model loading.

💾 Caching & State Management

Purpose	Implementation
Dataset caching	@st.cache_data
Model caching	@st.cache_resource
Session control	st.session_state['df'], st.session_state['df_fil']
Filtering	Persistent across interactions
Performance	Optimized data loading and resource reuse

🎨 UI/UX Principles

Dark theme aesthetic for data visualization.

Clear visual hierarchy with emoji section titles.

Sidebar-based navigation for intuitive flow.

Use of st.expander, st.columns, and st.form for a clean layout.

Responsive design for desktop and wide-screen displays.

📈 Tech Stack

Area	Technology
Frontend	Streamlit

Data	Pandas, NumPy
Visualization	Plotly Express
Machine Learning	Scikit-learn (Linear Regression)
Model Handling	Joblib
Deployment	Streamlit Cloud / Render / Docker-ready

🧮 Model Overview

A lightweight Linear Regression model trained with:

y ~ overall + age + value_eur


Predicts a player’s potential rating (potential).

Demonstrates clean separation between training (in create_dummy_model.py) and inference (in page_model_inference.py).

Cached and reusable for future sessions.

🚀 Future Enhancements

Replace dummy model with an advanced Random Forest or XGBoost.

Integrate real-time data via an API (e.g. sofifa.com).

Add KPIs (average overall, mean market value, etc.).

Extend the model for player clustering or similarity search.

Include authentication for personalized dashboards.

🧠 Key Learning Outcomes

This project demonstrates proficiency in:

🧩 Streamlit architecture design (multi-page modularization)

⚙️ Session state & caching optimization

🎨 Data visualization and UI/UX

🧠 Model inference integration

🧾 Professional software documentation & Git version control

🧑‍💻 Author

Christian Marzal Della Rovere
🎓 Full Stack AI Developer (in progress)
🌐 LinkedIn
 • GitHub

🏷️ GitHub Topics

#streamlit #data-visualization #machine-learning #fifa21
#dashboard #ai #python #fullstack

⭐ If you find this project useful, consider giving it a star on GitHub — it helps others discover it and supports the project’s visibility!
````
