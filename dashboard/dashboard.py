import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def wrapped_customer_id(customer_id):
    row_length = 8
    num_columns = len(customer_id) // row_length + 1  # Calculate the number of segments needed
    each_columns = [customer_id[i:i+row_length] for i in range(0, len(customer_id), row_length)]
    formatted_id = '\n'.join(each_columns)
    return formatted_id

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max", #mengambil tanggal order terakhir
        "order_id": "nunique",
        "price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_purchase_timestamp", "frequency", "monetary"]

    rfm_df["max_order_purchase_timestamp"] = rfm_df["max_order_purchase_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_purchase_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_purchase_timestamp", axis=1, inplace=True)

    return rfm_df


main_data_df = pd.read_csv("main_data.csv")

# Ubah tipe data yang perlu jadi datetime dan definisikan variabel baru min_date & max_date untuk dipakai di rfm analysis
datetime_columns = ["order_purchase_timestamp", "order_approved_at"]
main_data_df.sort_values(by="order_purchase_timestamp", inplace=True)
main_data_df.reset_index(inplace=True)

for column in datetime_columns:
    main_data_df[column] = pd.to_datetime(main_data_df[column])

min_date = main_data_df["order_purchase_timestamp"].min()
max_date = main_data_df["order_purchase_timestamp"].max()

# Definisikan data yang lain juga merupakan turunan dari main_data
yearly_orders_df = main_data_df.resample(rule='Y', on='order_purchase_timestamp').agg({
    "order_item_id": "sum",
    "price": "sum"
})
yearly_orders_df.index = yearly_orders_df.index.strftime('%Y')
yearly_orders_df = yearly_orders_df.reset_index()
yearly_orders_df.rename(columns={
    "order_item_id": "order_count",
    "price": "revenue"
}, inplace=True)

descending_category_df = main_data_df.groupby(by="product_category_name").order_item_id.count().sort_values(ascending=False).reset_index()

top5_state_selling = main_data_df.groupby(by="seller_state").order_id.count().sort_values(ascending=False).reset_index()

top5_state_buyers = main_data_df.groupby(by="customer_state").order_id.nunique().sort_values(ascending=False).reset_index()

price_to_qty = main_data_df.groupby(by="price").order_item_id.count()

sum_category_items_df = main_data_df.groupby(by="product_category_name").order_item_id.count().sort_values(ascending=False).reset_index()


with st.sidebar:
    
    st.image("https://emojiisland.com/cdn/shop/products/Praying_Emoji_ios10_020ec88e-ee33-496d-a95a-df23243cebf4_large.png?v=1571606092")

    st.subheader('Wilcent, swplayer8')

st.header('Belajar Analisis Data dengan Python :pray:')

st.subheader('Using E-Commerce Public Dataset')



col1, col2 = st.columns(2)

with col1:
    total_orders = main_data_df.order_id.nunique()
    st.metric("Total orders (2016-2018)", value=total_orders)

with col2:
    total_revenue = format_currency(main_data_df.price.sum(), "BRL", locale='es_BR') # using BRL, because product_category_name and state refers to Brazil
    st.metric("Total Revenue (2016-2018)", value=total_revenue)


st.subheader("Growth of Sales (2016-2018)")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

ax[0].plot(
    yearly_orders_df["order_purchase_timestamp"],
    yearly_orders_df["order_count"],
    marker='o',
    linewidth=3
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Number of Orders", loc="center", fontsize=30)
ax[0].tick_params(axis ='both', labelsize=15)
 
ax[1].plot(
    yearly_orders_df["order_purchase_timestamp"],
    yearly_orders_df["revenue"],
    marker='o',
    linewidth=3
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Revenue in Million", loc="center", fontsize=30)
ax[1].tick_params(axis ='both', labelsize=15)

st.pyplot(fig)




st.subheader("Best and Worst Performing Category by Quantity Sales (2016-2018)")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))


sns.barplot(x="order_item_id", y="product_category_name", data=sum_category_items_df.head(5), ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Category", loc="center", fontsize=30)
ax[0].tick_params(axis ='both', labelsize=15)

sns.barplot(x="order_item_id", y="product_category_name", data=sum_category_items_df.sort_values(by="order_item_id", ascending=True).head(5), ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Category", loc="center", fontsize=30)
ax[1].tick_params(axis='both', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(60, 30))

plt.plot(
    price_to_qty.index, 
    price_to_qty.values, 
    marker='o', 
    linestyle='-',
)

ax.set_ylabel("Quantity", fontsize=50)
ax.set_xlabel("Price", fontsize=50)
ax.set_title("Price-Quantity Trend", loc="center", fontsize=100)
ax.tick_params(axis='y', labelsize=50)
ax.tick_params(axis='x', labelsize=50)

st.pyplot(fig)


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(60, 30))

sns.barplot(
    x="order_item_id", 
    y="product_category_name", 
    data=descending_category_df.head(10), 
)
ax.set_ylabel("Product Category")
ax.set_xlabel("Quantity")
ax.set_title("Top 10 Category by Quantity", loc="center", fontsize=100)
ax.tick_params(axis='y', labelsize=50)
ax.tick_params(axis='x', labelsize=50)

st.pyplot(fig)


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

sns.barplot(y="seller_state", x="order_id", data=top5_state_selling.head(5), ax=ax[0])
ax[0].set_ylabel("Seller's State", fontsize=20)
ax[0].set_xlabel("Quantity", fontsize=20)
ax[0].set_title("Top 5 State by Selling Quantity", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=25)
ax[0].tick_params(axis='x', labelsize=25)

sns.barplot(y="customer_state", x="order_id", data=top5_state_buyers.head(5), ax=ax[1])
ax[1].set_ylabel("Buyer's State", fontsize=20)
ax[1].set_xlabel("Quantity", fontsize=20)
ax[1].set_title("Top 5 States by Purchasing Quantity", loc="center", fontsize=40)
ax[1].tick_params(axis='y', labelsize=25)
ax[1].tick_params(axis='x', labelsize=25)

st.pyplot(fig)







start_date, end_date = st.date_input(
        label='Timerange', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
)

main_df = main_data_df[(main_data_df["order_purchase_timestamp"] >= str(start_date)) & (main_data_df["order_purchase_timestamp"] <= str(end_date))]

rfm_df = create_rfm_df(main_df)


st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "BRL", locale='es_BR')
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(60, 30))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=6)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
ax[0].set_xticklabels([wrapped_customer_id(label.get_text()) for label in ax[0].get_xticklabels()])

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency",ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=6)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
ax[1].set_xticklabels([wrapped_customer_id(label.get_text()) for label in ax[1].get_xticklabels()])

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=6)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
ax[2].set_xticklabels([wrapped_customer_id(label.get_text()) for label in ax[2].get_xticklabels()])

st.pyplot(fig)



st.caption('Belajar Analisis Data dengan Python')