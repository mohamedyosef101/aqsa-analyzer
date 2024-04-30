import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
sns.set()

st.markdown('''
# **The Analyzer**
Here you can analyze your startup data (sales, finance, etc.)
''')

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    data = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

hero = st.container()
topRow = st.container()
midRow = st.container()
footer = st.container()

# ========= Functions ============
if data is not None:
    # read the file with pandas
    data = pd.read_csv(data)

    with hero:
        column_options = []
        for col in data.columns:
            if data[col].unique().shape[0] < 10:
                column_options.append(col)
        target = st.selectbox("Choose a target column", column_options, index=None)

    if target is not None:

        def classify_columns(df):
            # Initialize empty lists for each category
            continuous_cols = []
            categorical_cols = []
            non_useful_cols = []

            # Iterate through columns
            for col in df.columns:
                if df[col].unique().shape[0] == df.shape[0]:
                    non_useful_cols.append(col)
                    
                elif df[col].unique().shape[0] < 20:
                    categorical_cols.append(col)
                    
                elif np.issubdtype(df[col].dtype, np.number):
                    continuous_cols.append(col)
                    
                else: 
                    non_useful_cols.append(col)

            # Return the results as a dictionary
            return continuous_cols, categorical_cols, non_useful_cols

        features = data.drop(target, axis=1)
        classify_columns(features)
        cont_cols = classify_columns(features)[0]
        cat_cols = classify_columns(features)[1]
        non_use = classify_columns(features)[2]

        # topRow
        with topRow:
            st.markdown('### Target Analysis...')
            counts = data[target].value_counts()
            counts
            trans_counts = []
            trans_labels = data[target].unique()
            for i, count in enumerate(counts):
                trans_counts.append(counts[i])

            # Create the pie chart
            plt.figure(figsize=(4,4))
            plt.pie(trans_counts, labels=trans_labels, autopct="%1.2f%%", colors=['lightcoral', 'darkcyan', 'green', 'red', 'blue', 'gray'])
            st.pyplot(plt.gcf())



            st.markdown('### Categorical Variables Analysis...')
            fig = plt.figure(figsize=(10, 5*len(cat_cols)))
            for i, col in enumerate(cat_cols):
                ax=fig.add_subplot(len(cat_cols), 1, i+1)
                sns.countplot(data=data, x=col, axes=ax, hue=target, palette='Greens')
                plt.title(f"{col} Analysis", fontsize=24)
                ax.set(xlabel=None, ylabel=None)
                
            fig.tight_layout()
            st.pyplot(plt.gcf())

            st.divider()

        with midRow:
            st.markdown('### Continuous Variables Analysis...')
            fig = plt.figure(figsize=(5, 4*len(cont_cols)))
            for i, col in enumerate(cont_cols):
                ax=fig.add_subplot(len(cont_cols), 1, i+1)
                sns.kdeplot(data=data, x=col, axes=ax, hue=target, fill=True, palette=['lightcoral', 'darkcyan', 'blue', 'red', 'gray', 'orange', 'yellow'])
                ax.set_title(f"{col} Distribution")
                ax.set(xlabel=None, ylabel=None)
                
            fig.tight_layout()
            st.pyplot(plt.gcf())
