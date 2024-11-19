import json
from collections import defaultdict
from datetime import datetime, timedelta

# Load the data from the original JSON file
input_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/Responses3.5&4.json"
with open(input_path, 'r') as file:
    data = json.load(file)

# Create a dictionary to store averages for each time frame
averages_dict = defaultdict(lambda: defaultdict(lambda: {"chatgpt3.5_scores": [], "chatgpt4_scores": []}))

# Define date ranges and associated time frames
date_ranges = [
    (datetime.strptime("2021-10-01", "%Y-%m-%d"), datetime.strptime("2021-10-31", "%Y-%m-%d")),
    (datetime.strptime("2021-11-06", "%Y-%m-%d"), datetime.strptime("2022-03-13", "%Y-%m-%d")),
    (datetime.strptime("2022-04-02", "%Y-%m-%d"), datetime.strptime("2022-10-30", "%Y-%m-%d")),
    (datetime.strptime("2022-11-05", "%Y-%m-%d"), datetime.strptime("2023-03-12", "%Y-%m-%d")),
    (datetime.strptime("2023-11-04", "%Y-%m-%d"), datetime.strptime("2023-12-31", "%Y-%m-%d"))
]

# Define time frames
time_frames = {
    "00:00:00 to 08:29:59": (datetime.strptime("00:00:00", "%H:%M:%S").time(), datetime.strptime("08:29:59", "%H:%M:%S").time()),
    "08:30:00 to 14:59:59": (datetime.strptime("08:30:00", "%H:%M:%S").time(), datetime.strptime("14:59:59", "%H:%M:%S").time()),
    "15:00:00 to 23:59:59": (datetime.strptime("15:00:00", "%H:%M:%S").time(), datetime.strptime("23:59:59", "%H:%M:%S").time())
}

# Default time frames
default_time_frames = {
    "00:00:00 to 07:29:59": (datetime.strptime("00:00:00", "%H:%M:%S").time(), datetime.strptime("07:29:59", "%H:%M:%S").time()),
    "07:30:00 to 13:59:59": (datetime.strptime("07:30:00", "%H:%M:%S").time(), datetime.strptime("13:59:59", "%H:%M:%S").time()),
    "14:00:00 to 23:59:59": (datetime.strptime("14:00:00", "%H:%M:%S").time(), datetime.strptime("23:59:59", "%H:%M:%S").time())
}

# Iterate through data points
for entry in data:
    # Parse datetime
    entry_datetime = datetime.strptime(entry["datetime"], "%Y-%m-%d %H:%M:%S")
    entry_date = entry_datetime.date()

    # Determine the applicable time frames based on the date
    in_range = False
    for start_date, end_date in date_ranges:
        if start_date <= entry_datetime <= end_date:
            time_frames_to_use = time_frames
            in_range = True
            break
    
    if not in_range:
        time_frames_to_use = default_time_frames

    # Determine the time frame for the entry
    entry_time = entry_datetime.time()
    for timeframe_key, (start_time, end_time) in time_frames_to_use.items():
        if start_time <= entry_time <= end_time:
            timeframe_key_to_use = timeframe_key
            break

    # Add the chatgpt3.5_score and chatgpt4_score to the corresponding company, date, and timeframe in the averages_dict
    averages_dict[(entry["ticker"], entry["ticker_BB"], entry["company_name"], entry["full_company_name"], entry_date)][timeframe_key_to_use]["chatgpt3.5_scores"].append(entry.get("chatgpt3.5_score", 0.0))
    averages_dict[(entry["ticker"], entry["ticker_BB"], entry["company_name"], entry["full_company_name"], entry_date)][timeframe_key_to_use]["chatgpt4_scores"].append(entry.get("chatgpt4_score", 0.0))

# Calculate averages for each time frame and create a new data structure
result_data = []
for key, timeframes in averages_dict.items():
    for timeframe, scores_dict in timeframes.items():
        # Calculate average for chatgpt3.5 and chatgpt4 scores
        chatgpt3_5_avg = round(sum(scores_dict["chatgpt3.5_scores"]) / len(scores_dict["chatgpt3.5_scores"]) if scores_dict["chatgpt3.5_scores"] else 0.0, 4)
        chatgpt4_avg = round(sum(scores_dict["chatgpt4_scores"]) / len(scores_dict["chatgpt4_scores"]) if scores_dict["chatgpt4_scores"] else 0.0, 4)
        
        result_data.append({
            "ticker": key[0],
            "ticker_BB": key[1],
            "company_name": key[2],
            "full_company_name": key[3],
            "date": key[4].strftime('%Y-%m-%d'),
            "timeframe": timeframe,
            "chatgpt3.5_average": chatgpt3_5_avg,
            "chatgpt4_average": chatgpt4_avg
        })

# Save the result to a new JSON file
output_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/Averages.json"
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(result_data, output_file, ensure_ascii=False, indent=4)

print("Averages for both chatgpt3.5 and chatgpt4 calculated and saved to:", output_path)