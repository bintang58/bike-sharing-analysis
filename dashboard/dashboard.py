import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style
sns.set(style="dark")

# Membaca dataset dari file CSV day_df & hour_df
day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")

# Menyiapkan function

def get_sum_daily_casual_df(df):
    sum_daily_casual_df = df.groupby(by="date")["casual"].sum().sort_values(ascending=False).reset_index()
    return sum_daily_casual_df

def get_sum_daily_registered_df(df):
    sum_daily_registered_df = df.groupby(by="date")["registered"].sum().sort_values(ascending=False).reset_index()
    return sum_daily_registered_df

def get_daily_rent_df(df):
    daily_rent_df = df.groupby(by="date")["count"].sum().sort_values(ascending=False).reset_index()
    return daily_rent_df

def get_season_df(df):
    season_df = df.groupby(by="season", observed=False)["count"].sum().sort_values(ascending=False).reset_index()
    return season_df

def get_sum_order_items_df(df):
    sum_order_items_df = df.groupby("hour")["count"].sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def get_spring_data_df(df):
    spring_data_df = df[df["season"] == "Spring"]
    return spring_data_df

def get_hourly_rentals_workingday(df):
    hourly_rentals_workingday = df.groupby(["hour", "workingday"])["count"].mean().unstack()
    return hourly_rentals_workingday

def get_rfm_df(df):
    rfm_df = df.groupby(by="day", as_index=False, observed=False).agg({
        "date": "max",
        "instant": "nunique",
        "count": "sum"
    })
    rfm_df.columns = ["day", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = day_df["date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df

datetime_columns = ["date"]
day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)

hour_df.sort_values(by="date", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

# Membuat komponen filter
min_date = day_df["date"].min()
max_date = day_df["date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("dashboard/logo.png")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu",min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df_day = day_df[(day_df["date"] >= str(start_date)) & 
                (day_df["date"] <= str(end_date))]

main_df_hour = hour_df[(hour_df["date"] >= str(start_date)) & 
                (hour_df["date"] <= str(end_date))]

daily_casual_df = get_sum_daily_casual_df(main_df_day)
daily_registered_df = get_sum_daily_registered_df(main_df_day)
daily_rent_df = get_daily_rent_df(main_df_day)
season_df = get_season_df(main_df_day)
spring_df = get_spring_data_df(main_df_day)
sum_order_items_df = get_sum_order_items_df(main_df_hour)
hourly_rentals_workingday = get_hourly_rentals_workingday(main_df_hour)
rfm_df = get_rfm_df(main_df_day)

# Header Bike Sharing
st.header("Bike Sharing Dashboard 🚲")

st.subheader("Daily Bike Sharing")

col1, col2, col3 = st.columns(3)

with col1:
    daily_casual_user = daily_casual_df["casual"].sum()
    st.metric("Casual User", value= daily_casual_user)

with col2:
    daily_registered_user = daily_registered_df["registered"].sum()
    st.metric("Registered User", value= daily_registered_user)
 
with col3:
    daily_rent_user = daily_rent_df["count"].sum()
    st.metric("Total User", value= daily_rent_user)

# Pertanyaan Analisis 3: Bagaimana strategi promosi yang dapat diterapkan pada musim dengan jumlah penyewaan sepeda yang rendah?
col1, col2 = st.columns(2)
# Kolom 1: Distribusi Temperature
with col1:
    st.subheader("Temperature Distribution in Spring")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(spring_df["temp"], bins=20, kde=True, ax=ax, color="blue")
    ax.set_xlabel("Temperature (Normalized)")
    st.pyplot(fig)

# Kolom 2: Distribusi Windspeed
with col2:
    st.subheader("Wind Speed Distribution in Spring")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(spring_df["windspeed"], bins=20, kde=True, ax=ax, color="red")
    ax.set_xlabel("Windspeed")
    st.pyplot(fig)

# Pertanyaan Analisis 4: Apakah perlu penyesuaian harga sewa berdasarkan pola peminjaman di jam-jam tertentu?
st.subheader("Comparison of Bicycle Loan Patterns between Weekdays and Weekends")
fig, ax = plt.subplots(figsize=(12, 6))  # Simpan figure dalam variabel

sns.lineplot(x=hourly_rentals_workingday.index, y=hourly_rentals_workingday["Weekdays"], marker="o", label="Weekdays", color="b", ax=ax)
sns.lineplot(x=hourly_rentals_workingday.index, y=hourly_rentals_workingday["Weekend"], marker="o", label="Weekend", color="r", ax=ax)

ax.set_xticks(range(0, 24))
ax.set_xlabel("Hours in a Day (AM-PM)")
ax.set_ylabel("Average Number of Borrowings")
ax.legend()

st.pyplot(fig)  # Tampilkan plot di Streamlit

# Pertanyaan Analisis 1: Pada musim apa jumlah penyewaan sepeda tertinggi?
st.subheader("Number of Bike Rentals by Season")
fig, ax = plt.subplots(figsize=(10, 5))

# Menentukan warna untuk bar chart
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#64B5F6"]

# Membuat grafik bar untuk jumlah penyewaan per musim
sns.barplot(y="count", x="season", data=season_df.sort_values(by="season", ascending=False), palette=colors, hue="season", legend=False, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12)

st.pyplot(fig)

# Pertanyaan Analisis 2: Pada jam berapa peminjaman sepeda mencapai jumlah tertinggi dan terendah?
st.subheader("Hours with the Highest and Lowest Bike Rentals")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Menentukan warna untuk grafik bar
colors1 = ["#D3D3D3", "#D3D3D3", "#64B5F6", "#D3D3D3", "#D3D3D3"]
colors2 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#64B5F6"]

# Membuat grafik bar untuk jam dengan penyewaan tertinggi
sns.barplot(x="hour", y="count", data=sum_order_items_df.head(5), palette=colors1, hue="hour", legend=False, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Hours with the Highest Bike Rentals", loc="center", fontsize=40)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)
 
# Membuat grafik bar untuk jam dengan penyewaan terendah
sns.barplot(x="hour", y="count", data=sum_order_items_df.sort_values(by="hour", ascending=True).head(5), palette=colors2, hue="hour", legend=False, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)",  fontsize=30)
ax[1].set_title("Hours with the Lowest Bike Rentals", loc="center", fontsize=40)
ax[1].tick_params(axis="y", labelsize=35)
ax[1].tick_params(axis="x", labelsize=30)
 
st.pyplot(fig)

#RFM Analysis (Recency, Frequency, Monetary)
st.subheader("Best Customer Based on RFM Parameters (day)")
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))

colors = ["#64B5F6"] * len(rfm_df["day"].unique())

# Recency: Menampilkan bar chart berdasarkan recency
sns.barplot(y="recency", x="day", data=rfm_df.sort_values(by="recency", ascending=True), palette=colors, hue="day", dodge=False, legend=False, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (day)", loc="center", fontsize=50)
ax[0].tick_params(axis="x", labelsize=30, rotation=45)
ax[0].tick_params(axis="y", labelsize=25)

# Frequency: Menampilkan bar chart berdasarkan frequency
sns.barplot(y="frequency", x="day", data=rfm_df.sort_values(by="frequency", ascending=False), palette=colors, hue="day", dodge=False, legend=False, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis="x", labelsize=30, rotation=45)
ax[1].tick_params(axis="y", labelsize=25)

# Monetary: Menampilkan bar chart berdasarkan monetary
sns.barplot(y="monetary", x="day", data=rfm_df.sort_values(by="monetary", ascending=False), palette=colors, hue="day", dodge=False, legend=False, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis="x", labelsize=30, rotation=45)
ax[2].tick_params(axis="y", labelsize=25)

st.pyplot(fig)
