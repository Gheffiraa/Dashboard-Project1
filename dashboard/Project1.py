import streamlit as st 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.title('Average Concentration of PM2.5 Pollutant :sparkles:')
path = os.path.dirname(__file__)
full_path = path + '/data1.csv'
data1 = pd.read_csv(full_path)

fig, ax = plt.subplots(figsize = (15, 7))

ax = sns.barplot(data = data1, x='station', y='PM2.5', dodge = False, ax = ax, palette = 'turbo')
ax.set_title('Average PM2.5 concentration Grouped by Station (Hourly Recorded)',fontsize=16)
ax.set_xlabel('Station')
ax.set_ylabel('PM 2.5 Average Concentration')
st.pyplot(fig)

wind = data1[['wd','PM2.5']].groupby('wd').median()
fig2, ax2 = plt.subplots(figsize = (15, 7))
# plot
ax2 = sns.barplot(data = wind, x = 'wd', y = 'PM2.5', palette = 'turbo')
ax2.set_title('Average PM2.5 concentration in Dongsi Air Grouped by Wind Direction (Hourly Recorded)',fontsize=16)
ax2.set_xlabel('Wind Direction')
ax2.set_ylabel('PM2.5 Concentration')
st.pyplot(fig2)