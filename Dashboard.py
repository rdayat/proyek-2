import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('all_data.csv')
    return data

data = load_data()

# Sidebar untuk filter data
st.sidebar.header("Filter")
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [pd.to_datetime(data['order_purchase_timestamp']).min(), pd.to_datetime(data['order_purchase_timestamp']).max()])

# Filter data berdasarkan rentang waktu
filtered_data = data[(pd.to_datetime(data['order_purchase_timestamp']) >= pd.to_datetime(date_range[0])) & (pd.to_datetime(data['order_purchase_timestamp']) <= pd.to_datetime(date_range[1]))]

# Header
st.title("Dashboard E-commerce Analysis")
st.write(f"Menampilkan data dari {date_range[0]} hingga {date_range[1]}.")

# 1. Tren Penjualan Selama Periode Waktu Tertentu
st.header("📊 Tren Penjualan E-commerce")

# Konversi ke datetime dan resampling data untuk tren harian
filtered_data['order_purchase_timestamp'] = pd.to_datetime(filtered_data['order_purchase_timestamp'])
filtered_data.set_index('order_purchase_timestamp', inplace=True)
daily_sales = filtered_data.resample('D').agg({'order_id': 'count', 'price': 'sum'}).reset_index()

# Line chart dengan lebih banyak informasi
st.line_chart(daily_sales.set_index('order_purchase_timestamp')[['price']], use_container_width=True)
st.write("Tren penjualan ini menunjukkan total pendapatan harian selama periode waktu yang dipilih.")

# Tambahkan insight tambahan
total_revenue = daily_sales['price'].sum()
st.metric("Total Pendapatan Selama Periode", f"Rp {total_revenue:,.2f}")

# 2. Produk yang Paling Banyak dan Sedikit Terjual
st.header("📦 Produk Terlaris dan Kurang Laku")

# Menghitung produk terlaris dan yang kurang laku
top_products = filtered_data.groupby('product_category_name_english')['order_id'].count().sort_values(ascending=False).reset_index()
top_products.columns = ['Kategori Produk', 'Total Pesanan']

# Produk Terlaris (Top 5)
st.subheader("Produk Terlaris")
st.bar_chart(top_products.head(5).set_index('Kategori Produk')['Total Pesanan'], use_container_width=True)
st.write(top_products.head(5))

# Produk Kurang Laku (Bottom 5)
st.subheader("Produk Kurang Laku")
st.bar_chart(top_products.tail(5).set_index('Kategori Produk')['Total Pesanan'], use_container_width=True)
st.write(top_products.tail(5))

# 3. Demografi Pelanggan
st.header("🌍 Demografi Pelanggan")

# Menghitung jumlah pelanggan berdasarkan negara bagian (state)
cust_demography = filtered_data.groupby('customer_state')['customer_id'].nunique().reset_index().sort_values(by='customer_id', ascending=False)
cust_demography.columns = ['Negara Bagian', 'Jumlah Pelanggan']

# Visualisasi Demografi (bar chart)
st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
st.bar_chart(cust_demography.set_index('Negara Bagian')['Jumlah Pelanggan'], use_container_width=True)
st.write("Grafik ini menunjukkan distribusi pelanggan berdasarkan negara bagian.")

# Insight tambahan
total_customers = cust_demography['Jumlah Pelanggan'].sum()
st.metric("Total Pelanggan Selama Periode", f"{total_customers} orang")

# Tambahkan interpretasi dan insight lebih mendalam
st.write("Pelanggan terbanyak berasal dari negara bagian dengan kode negara bagian tertinggi di grafik.")
