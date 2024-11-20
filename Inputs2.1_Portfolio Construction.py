import pandas as pd
import json
from datetime import datetime

# Load the JSON file
json_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/4 Regresion/Filtered&ModifiedAverages&Returns_MX.json"
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Load the Excel file
excel_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/5 Portafolios/Inputs_Portfolios.xlsx"
xls = pd.ExcelFile(excel_file_path)

# Read the first sheet into a DataFrame
df = pd.read_excel(xls, sheet_name='ChatGPT 3.5')

for entry in data:
    date_str = entry.get('date')  # Get the date from the JSON
    timeframe = entry.get('timeframe')  # Get the timeframe from the JSON
    ticker_bb = entry.get('ticker_BB')  # Get the ticker from the JSON
    chatgpt3_5 = entry.get('chatgpt3.5_average')  # Get the chatgpt average
    chatgpt4 = entry.get('chatgpt4_average')  # Get the chatgpt average
    px_open = entry.get('px_open')  # Get the px_open value
    px_last = entry.get('px_last')  # Get the px_last value
    price_return = entry.get('price_return') #Get the price_return

    if date_str and timeframe and ticker_bb:

        # Locate the date in the first column
        date_row = df[df.iloc[:, 0] == date_str].index
        if not date_row.empty:
            date_index = date_row[0]  # Get the first row index for the matching date
            
            # Check only the rows immediately below this date for the timeframe (up to 3 rows below)
            timeframe_row_range = df.iloc[date_index+1:date_index+4]  # Check the next 3 rows
            timeframe_index = timeframe_row_range[timeframe_row_range.iloc[:, 0] == timeframe].index
            
            if not timeframe_index.empty:
                time_index = timeframe_index[0]  # Get the first row index for the matching timeframe
                
                # Locate the column associated with the ticker
                ticker_columns = df.columns[df.iloc[0] == ticker_bb].tolist()
                if ticker_columns:
                    ticker_column = ticker_columns[0]  # Get the first column index for the matching ticker
                   
                    # Get the column index of the ticker
                    ticker_column_index = df.columns.get_loc(ticker_column)  # Get the index of the ticker column

                    # Populate the corresponding cells
                    df.at[time_index, df.columns[ticker_column_index]] = chatgpt3_5  # Score ChatGPT

# Save the modified DataFrame back to the Excel file
with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, index=False, sheet_name='ChatGPT 3.5')

print(f"Excel file '{excel_file_path}' updated successfully.")
