import streamlit as st
import pandas as pd
from scipy.stats import pearsonr
import os

# Function to load data from a given folder
def load_data(folder):
    data = pd.DataFrame()
    for file in os.listdir(folder):
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder, file)
            df = pd.read_excel(file_path)
            data = pd.concat([data, df], ignore_index=True)
    return data

# Function to calculate correlation
def calculate_correlation(portfolio, hedge_data):
    correlation_results = {}
    for stock in portfolio.columns:
        if stock != 'Date':
            correlation, _ = pearsonr(portfolio[stock], hedge_data[stock])
            correlation_results[stock] = correlation
    return correlation_results

# Function to display the app
def main():
    st.title("Stock Portfolio Hedging App")

    # Load stock data from stockfolder
    stock_folder = "stockfolder"
    stock_data = load_data(stock_folder)

    # Display available stocks for selection
    st.sidebar.header("Select Stocks for Portfolio")
    selected_stocks = st.sidebar.multiselect("Select stocks for your portfolio", stock_data.columns[1:])

    # Create portfolio dataframe
    portfolio = stock_data[['Date'] + selected_stocks]

    # Load hedge data from hedgefolder
    hedge_folder = "hedgefolder"
    hedge_data = load_data(hedge_folder)

    # Calculate correlation and display results
    st.header("Correlation with Hedge Stocks")
    st.write("Correlation Scores:")
    
    if len(selected_stocks) > 0:
        correlation_results = calculate_correlation(portfolio, hedge_data)
        
        for stock, correlation in correlation_results.items():
            st.write(f"{stock} : {correlation:.2f}")
    else:
        st.warning("Please select at least one stock for your portfolio.")

if __name__ == "__main__":
    main()
