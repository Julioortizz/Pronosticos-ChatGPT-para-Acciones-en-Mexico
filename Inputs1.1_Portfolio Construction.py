import pandas as pd
import json
from datetime import datetime

# Load the JSON file
json_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/4 Regresion/Averages&Returns.json"
output_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/5 Portafolios/Inputs_Portfolios.xlsx"

with open(json_file_path, 'r') as f:
    data = json.load(f)

# Prepare to collect date, timeframe, and ticker information
date_timeframes = {}
tickers = set()

for entry in data:
    date_str = entry.get('date')
    timeframe = entry.get('timeframe')
    ticker_bb = entry.get('ticker_BB')
    
    if date_str and timeframe and ticker_bb:
        # Collect unique tickers
        tickers.add(ticker_bb)
        
        # Collect timeframes for each date
        if date_str not in date_timeframes:
            date_timeframes[date_str] = set()
        date_timeframes[date_str].add(timeframe)

# Sort dates in ascending order
sorted_dates = sorted(date_timeframes.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'))

# Prepare final data for dates and timeframes (flattened to avoid nested lists)
final_data = []
for date in sorted_dates:
    final_data.append(date)  # Add the original date format (YYYY-MM-DD) as a string, not as a list
    for timeframe in sorted(date_timeframes[date]):  # Sort timeframes
        final_data.append(timeframe)  # Add timeframes as strings, not as a list

# Create a DataFrame for the dates and timeframes (with no nesting)
df_dates_timeframes = pd.DataFrame(final_data, columns=['Dates and Timeframes'])

# Sort tickers
sorted_tickers = sorted(tickers)

# Create empty DataFrames for each sheet (including the new one for 'price_return')
df_chatgpt3_5 = pd.DataFrame(columns=['Dates and Timeframes'] + sorted_tickers)
df_chatgpt4 = pd.DataFrame(columns=['Dates and Timeframes'] + sorted_tickers)
df_px_open = pd.DataFrame(columns=['Dates and Timeframes'] + sorted_tickers)
df_px_last = pd.DataFrame(columns=['Dates and Timeframes'] + sorted_tickers)
df_price_return = pd.DataFrame(columns=['Dates and Timeframes'] + sorted_tickers)  # New sheet for 'price_return'

# Fill the first column (dates and timeframes)
df_chatgpt3_5['Dates and Timeframes'] = final_data
df_chatgpt4['Dates and Timeframes'] = final_data
df_px_open['Dates and Timeframes'] = final_data
df_px_last['Dates and Timeframes'] = final_data
df_price_return['Dates and Timeframes'] = final_data  # Populate 'price_return' sheet

# Write each DataFrame to separate sheets in the Excel file
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    df_chatgpt3_5.to_excel(writer, index=False, startrow=0, sheet_name='ChatGPT 3.5')
    df_chatgpt4.to_excel(writer, index=False, startrow=0, sheet_name='ChatGPT 4')
    df_px_open.to_excel(writer, index=False, startrow=0, sheet_name='px_open')
    df_px_last.to_excel(writer, index=False, startrow=0, sheet_name='px_last')
    df_price_return.to_excel(writer, index=False, startrow=0, sheet_name='price_return')  # Write the new sheet

print(f"Excel file '{output_file_path}' created successfully.")