import json
import pandas as pd
from datetime import datetime

# Paths to the input files
json_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/Averages.json"
excel_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/2. Bases de Datos/Mnotics & Prices.xlsx"

# Load JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Load the Excel sheet
df = pd.read_excel(excel_file_path, sheet_name="Prices", header=None)

# Extract tickers from the second row starting at the second column
tickers = df.iloc[3, 1:].dropna().tolist()

# Map tickers to their columns for opening and closing prices
ticker_to_columns = {tickers[i]: (2 * i + 1, 2 * i + 2) for i in range(len(tickers))}

# Extract dates from the first column starting at the seventh row
df_dates = pd.to_datetime(df.iloc[6:, 0], format='%d/%m/%Y').dt.strftime('%Y-%m-%d').tolist()

# Extract prices data starting from row 7 and columns associated with each ticker
prices_data = df.iloc[6:, 1:].values

# Function to find the index of a date in the Excel dates list
def find_date_index(date_str):
    try:
        return df_dates.index(date_str)
    except ValueError:
        return None

# Iterate over each data point in the JSON data
for data_point in data:
    # Get the ticker and date information from the data point
    ticker_BB = data_point.get('ticker_BB')
    date_str = data_point.get('date')
    timeframe = data_point.get('timeframe')

    # Check if the ticker is present in the Excel file
    if ticker_BB in ticker_to_columns:
        # Get the columns for the ticker
        open_col, close_col = ticker_to_columns[ticker_BB]
        
        # Find the row corresponding to the date
        date_index = find_date_index(date_str)

        if date_index is not None:
            # Assign values based on the timeframe conditions
            if timeframe in ["00:00:00 to 07:29:59", "00:00:00 to 08:29:59"]:
                # Use the opening and closing prices of the specified date
                px_open = prices_data[date_index, open_col - 1]
                px_last = prices_data[date_index, close_col - 1]
            elif timeframe in ["08:30:00 to 14:59:59", "07:30:00 to 13:59:59"]:
                # Use the closing price of the specified date as px_open
                px_open = prices_data[date_index, close_col - 1]
                # Use the opening price of the next date as px_last
                if date_index + 1 < len(prices_data):
                    px_last = prices_data[date_index + 1, open_col - 1]
                else:
                    # If there is no next date, set px_last to None
                    px_last = None
            elif timeframe in ["14:00:00 to 23:59:59", "15:00:00 to 23:59:59"]:
                # Use the opening and closing prices of the next date
                if date_index + 1 < len(prices_data):
                    px_open = prices_data[date_index + 1, open_col - 1]
                    px_last = prices_data[date_index + 1, close_col - 1]
                else:
                    # If there is no next date, set px_open and px_last to None
                    px_open = None
                    px_last = None

            # Convert px_open and px_last to floats if they are not None
            if px_open is not None and px_last is not None:
                try:
                    px_open = float(px_open)
                    px_last = float(px_last)
                    # Add the prices to the data point
                    data_point['px_open'] = px_open
                    data_point['px_last'] = px_last
                    # Calculate the price return
                    data_point['price_return'] = round(100 * ((px_last - px_open) / px_open), 4)
                except ValueError:
                    # Handle cases where conversion to float fails
                    data_point['px_open'] = None
                    data_point['px_last'] = None
                    data_point['price_return'] = None

# Save the modified JSON data to a new file
output_json_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/Averages&Returns.json"
with open(output_json_path, 'w') as output_file:
    json.dump(data, output_file, indent=4)

print(f"Modified JSON data saved to {output_json_path}")