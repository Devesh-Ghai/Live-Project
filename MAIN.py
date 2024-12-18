import pandas as pd
import streamlit as st
import Preprocessor

df = pd.read_csv("data.csv")

#creating time feature
df=Preprocessor.fetch_time_features(df)

# Title for Dashboard
st.title("Sales Analytics Dashboard")

# Side bar for filters
st.sidebar.title("Filters")

# Filters
selected_year = Preprocessor.multiselect("Select Year", df['Financial_Year'].unique())
selected_retailer = Preprocessor.multiselect("Select Retailer", df['Retailer'].unique())
selected_company = Preprocessor.multiselect("Select Company", df['Company'].unique())
selected_month = Preprocessor.multiselect("Select Financial Month", df['Financial_Month'].unique())


filtered_df= df[(df['Financial_Year'].isin(selected_year)) &
                (df['Retailer'].isin(selected_retailer)) &
                (df['Company'].isin(selected_company)) &
                (df['Financial_Month'].isin(selected_month))]
               

# KPI's - Key Performance indicators, 
# Create columns to displays KPIs
col1, col2 , col3 , col4 = st.columns(4)

#total_sales
with col1:
    st.metric(label = 'Total Sales', value =f'₹{int(filtered_df["Amount"].sum())}')

#total_margin
with col2:
    st.metric(label = 'Total Margin', value =f'₹{int(filtered_df["Margin"].sum())}')

#total_transaction
with col3:
    st.metric(label = 'Total Transaction', value =len(filtered_df))

#Margin_%
with col4:
    st.metric(label = 'Margin Percentage', value =f'{int((filtered_df["Margin"].sum())*100/(filtered_df["Amount"].sum()))}%')
    
#Visualization for month to month sales

yearly_sales=(df[['Financial_Year','Financial_Month','Amount']]
              .groupby(['Financial_Year','Financial_Month'])
              .sum()
              .reset_index()
              .pivot(index = 'Financial_Month',columns='Financial_Year',values='Amount'))
              
st.line_chart(yearly_sales, x_label="Financial_Month",y_label = "Total Sales")

# Visualize Retail Count by Revenue %
col5, col6 = st.columns(2)

with col5:
    st.title("Retailer count by Revenue %")
    retailer_count = Preprocessor.fetch_top_revenue_retailers(filtered_df)
    retailer_count.set_index("percentage revenue", inplace=True)
    st.bar_chart(retailer_count, x_label = "percentage revenue", y_label = "retailer_count")


with col6:
    st.title("Company count by Revenue %")
    retailer_count = Preprocessor.fetch_top_revenue_companies(filtered_df)
    retailer_count.set_index("percentage revenue", inplace=True)
    st.bar_chart(retailer_count, x_label = "percentage revenue", y_label = "company_count")