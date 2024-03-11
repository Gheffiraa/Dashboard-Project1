#Import Library
import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from plotly.offline import iplot, init_notebook_mode
from PIL import Image
import os

#Data Wrangling
#Gathering Data
path = os.path.dirname(__file__)
data_aoti = pd.read_csv(path + "\..\data\PRSA_Data_Aotizhongxin_20130301-20170228.csv")
data_changping = pd.read_csv(path + "\..\data\PRSA_Data_Changping_20130301-20170228.csv")
data_dingling = pd.read_csv(path + "\..\data\PRSA_Data_Dingling_20130301-20170228.csv")
data_dongsi = pd.read_csv(path + "\..\data\PRSA_Data_Dongsi_20130301-20170228.csv")
data_guanyuan = pd.read_csv(path + "\..\data\PRSA_Data_Guanyuan_20130301-20170228.csv")
data_gucheng = pd.read_csv(path + "\..\data\PRSA_Data_Gucheng_20130301-20170228.csv")
data_huairou = pd.read_csv(path + "\..\data\PRSA_Data_Huairou_20130301-20170228.csv")
data_nongzha = pd.read_csv(path + "\..\data\PRSA_Data_Nongzhanguan_20130301-20170228.csv")
data_shunyi = pd.read_csv(path + "\..\data\PRSA_Data_Shunyi_20130301-20170228.csv")
data_tiantan = pd.read_csv(path + "\..\data\PRSA_Data_Tiantan_20130301-20170228.csv")
data_wanliu = pd.read_csv(path + "\..\data\PRSA_Data_Wanliu_20130301-20170228.csv")
data_wanshou = pd.read_csv(path + "\..\data\PRSA_Data_Wanshouxigong_20130301-20170228.csv")
#Assesing Data
data = [data_aoti, data_changping, data_dingling, data_dongsi, data_guanyuan, data_gucheng, data_huairou, data_nongzha, data_shunyi, data_tiantan, data_wanliu, data_wanshou]
data = pd.concat(data)
data1 = data.copy()

#Cleaning Data

#Handling missing values
#Fill the missing values with the median value
for column in data1.columns[5:11]:  # Loop through column 5 until 10'
    data1[column] = data1.groupby('station')[column].transform(lambda x: x.fillna(x.median()))
#Handling missing values
#Fill the missing values with the mean value
for column in data1.columns[11:15]:  # Loop through column 11 until 14'
    data1[column] = data1.groupby('station')[column].transform(lambda x: x.fillna(x.mean()))
#Handling missing values by filling it with mode
data1['wd'] = data1['wd'].fillna(data1['wd'].mode()[0])
#Handling missing value by filling it with mean
mean_WSPM = data1['WSPM'].mean()
data1['WSPM'] = data1['WSPM'].fillna(mean_WSPM)


#Exploratory Data Analysis (EDA)
#make datetime variable
a = "2016-04-15T04:08:03.000+0000"
b = "Apr 15, 2016, 4:08:03 AM"

a = datetime.strptime(a, '%Y-%m-%dT%H:%M:%S.%f%z')
b = datetime.strptime(b, '%b %d, %Y, %I:%M:%S %p')
b = b.replace(tzinfo=a.tzinfo)

cols=["year","month","day","hour"]
data1['datetime'] = data1[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")

data1['datetime'] = pd.to_datetime(data1['datetime'], format = "%Y-%m-%d-%H")
#Resampling the time series data based on days
data1 = data1.set_index('datetime')
daily_resampled_data = data1.resample('D').sum() #D indicates days

#reset the index so the datetime is no longer an index and it'll be a column 
data1_reindex = data1.reset_index()

#Create sidebar
min_date = data1_reindex['datetime'].min()
max_date = data1_reindex['datetime'].max()
 
with st.sidebar:
    # Menambahkan image
    img = Image.open(path + '/image.jpeg')   
    st.image(img)
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Range', min_value = min_date, max_value = max_date, value=[min_date, max_date]
    )

main_data = data1_reindex[(data1_reindex['datetime'] >= str(start_date)) &  (data1_reindex['datetime'] <= str(end_date))]

st.header('Beijing\'s Air Quality Dashboard :sparkles:')

st.subheader('Daily Trend of Pollutant Concentration')

### Choosing the statio and pollutant

station_name = st.selectbox(
    label="Select station",
    options=('Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong')
)

pollutant = st.selectbox(
    label="Select Pollutant",
    options=('PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3')
)

#Daily Trend
fig, ax = plt.subplots(figsize = (10,4))

ax = sns.lineplot(data = main_data[main_data['station']== station_name], x = 'datetime', y = pollutant)

plt.xlabel('Datetime',fontsize=14)
plt.ylabel(f'{pollutant} Average Concentration',fontsize=14)
plt.title(f'Daily trend in the hourly recorded {pollutant} concentration in the air in {station_name}',fontsize=14)
st.pyplot(fig)

#Top Polluted Stations
st.subheader(f'Top Polluted Stations by {pollutant} from {str(start_date)} to {str(end_date)}')
main_data_sorted = main_data.groupby('station')[pollutant].mean().sort_values(ascending=False).reset_index()
 
fig2, ax2 = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ['#728FCE', '#BCC6CC', "#BCC6CC", "#BCC6CC", "#BCC6CC"]
 
sns.barplot(x=pollutant, y='station', data=main_data_sorted.head(5), palette=colors, ax=ax2[0])
ax2[0].set_ylabel(None)
ax2[0].set_xlabel(f'Average Concentration of {pollutant}', fontsize=30)
ax2[0].set_title("Most Polluted Stations", loc="center", fontsize=50)
ax2[0].tick_params(axis='y', labelsize=35)
ax2[0].tick_params(axis='x', labelsize=30)

sns.barplot(x=pollutant, y='station', data=main_data_sorted.sort_values(by=pollutant, ascending=True).head(5), palette=colors, ax=ax2[1])
ax2[1].set_ylabel(None)
ax2[1].set_xlabel(f'Average Concentration of {pollutant}', fontsize=30)
ax2[1].invert_xaxis()
ax2[1].yaxis.set_label_position("right")
ax2[1].yaxis.tick_right()
ax2[1].set_title("Least Polluted Stations", loc="center", fontsize=50)
ax2[1].tick_params(axis='y', labelsize=35)
ax2[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig2)





