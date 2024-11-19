import json
import re

# Load the JSON file
json_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/Responses3.5&4.json"

with open(json_file_path, 'r') as file:
    data = json.load(file)

# Map "YES," "NO," and "UNKNOWN" to corresponding scores
score_mapping = {"YES": 1, "NO": -1, "UNKNOWN": 0}

# Update each data point with the "chatgpt_score" key
for item in data:
    response = item.get("chatgpt3.5_response", "UNKNOWN").strip().upper()

    # Use regular expression to capture the response category
    match = re.match(r'^(YES|NO|UNKNOWN)', response)
    score_key = match.group(1) if match else "UNKNOWN"

    score = score_mapping.get(score_key, 0)
    item["chatgpt3.5_score"] = score

# Update each data point with the "chatgpt_score" key
for item in data:
    response = item.get("chatgpt4_response", "UNKNOWN").strip().upper()

    # Use regular expression to capture the response category
    match = re.match(r'^(YES|NO|UNKNOWN)', response)
    score_key = match.group(1) if match else "UNKNOWN"

    score = score_mapping.get(score_key, 0)
    item["chatgpt4_score"] = score

# Save the updated data back to the JSON file
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)