import shap
import numpy as np
import streamlit as st

from matplotlib import pyplot as plt
from pyarrow import parquet as pq
from catboost import CatBoostClassifier

# Load data into session state if not already present
if 'sample_dataframe' not in st.session_state:
    st.session_state['sample_dataframe'] = pq.read_table('./artifacts/demo_data.pq').to_pandas()

# Use sample instead of head to get a randomized patient list
if 'patient_list' not in st.session_state:
    st.session_state['patient_list'] = set(st.session_state['sample_dataframe']['patient_nbr'].sample(100))

# Title
st.title('Readmission Risk')
#st.set_option('deprecation.showPyplotGlobalUse', False)

# Patient selection
option = st.selectbox('Select a patient ID', st.session_state['patient_list'])

# Load model function
def load_model():
    model = CatBoostClassifier()
    model.load_model('artifacts/scoring_model.cbm')
    return model

# Get patient features and score
def get_features(pt_id, model, df):
    dataframe = df[df['patient_nbr'] == pt_id][model.feature_names_].copy()
    features = dataframe.to_dict(orient='records')[0]
    score = model.predict_proba(dataframe)[0][1]
    return features, score, dataframe

# Display score style
def get_style(score):
    color = "Red" if score > 0.5 else "Green"
    return f'<p style="font-family:Georgia; color:{color}; font-size: 30px;"> % {str(np.round(score*100,2))}</p>'

# Get SHAP explainer
def get_explainer():
    model = load_model()
    return shap.TreeExplainer(model, feature_perturbation="tree_path_dependent")

# Compute SHAP values
def get_shap_values(requested_data):
    explainer = get_explainer()
    return explainer(requested_data)

# Generate waterfall plot
def get_waterfall_plot(shap_values):
    plt.figure(figsize=(10, 10))
    fig = shap.plots.waterfall(shap_values[0], max_display=10)
    return fig

# Load model and get initial data
modelx = load_model()
features, score, dfx = get_features(option, modelx, st.session_state['sample_dataframe'])

# Age slider implementation
age = st.slider("Adjust Age", 15, 100, int(dfx['age'].values[0]))
dfx['age'] = age
features['age'] = age
score = modelx.predict_proba(dfx)[0][1]

# Get SHAP values and graph
graph = get_waterfall_plot(get_shap_values(dfx))

# Display updated risk score
st.header('Risk for the patient')
col1, col2, col3 = st.columns(3)
col2.write(score)
col2.markdown(get_style(score), unsafe_allow_html=True)

# Button to display raw features
if st.button("Show Raw Features"):
    st.write(features)

# Display SHAP waterfall plot
st.header('Main drivers of the decision')
st.pyplot(graph)