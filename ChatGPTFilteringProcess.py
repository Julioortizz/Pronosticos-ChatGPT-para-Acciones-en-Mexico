import json
from openai import OpenAI

# File paths
input_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/AllNewsData_MX.json"
output_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/FilteredAllNewsData_MX.json"

# Load data from JSON file
with open(input_file_path, "r") as file:
    news_data = json.load(file)

# Initialize OpenAI client
client = OpenAI()

# Function to determine if two headlines are about the same event using OpenAI
def are_headlines_same_event(headline1, headline2, company_name, date):
    user_message = f"Compare these two headlines related to {company_name} on {date} and tell me if they describe the same event:\n1. {headline1}\n2. {headline2}\nAnswer 'YES' if they describe the same event or 'NO' if they are different."
    
    # Make API call to OpenAI using gpt-4-turbo
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that compares news headlines to determine if they talk about the same event."},
            {"role": "user", "content": user_message}
        ]
    )
    
    # Extract response content
    response_content = response.choices[0].message.content.strip().upper()
    
    # Return True if the response is 'YES', otherwise False
    return response_content == "YES"

# Filter the news data
filtered_news_data = []
seen_headlines = set()  # Track processed headlines to avoid duplicates

# Group headlines by company (ignoring specific dates for initial grouping)
grouped_data = {}
for element in news_data:
    company = element["company_name"]
    if company not in grouped_data:
        grouped_data[company] = []
    grouped_data[company].append(element)

# Compare headlines in pairs within each company group
for company, headlines in grouped_data.items():
    # Sort headlines by date and hour to process them chronologically
    sorted_headlines = sorted(headlines, key=lambda x: (x["date"], x["hour"]))
    
    # Track last added headline for each date to ensure at least one headline per day is preserved
    last_added_by_date = {}

    for i in range(len(sorted_headlines)):
        headline_i = sorted_headlines[i]
        headline_date = headline_i["date"]

        if headline_i["title"] in seen_headlines:
            continue  # Skip if already processed
        
        keep_headline = True
        for j in range(i + 1, len(sorted_headlines)):
            headline_j = sorted_headlines[j]
            
            # If headlines are from different days, ensure at least one is kept per day
            if headline_j["date"] != headline_date:
                if headline_date not in last_added_by_date:
                    last_added_by_date[headline_date] = headline_i  # Keep at least one per day
                continue  # Move to next comparison

            # Use OpenAI to check if they are about the same event
            if are_headlines_same_event(headline_i["title"], headline_j["title"], company, headline_date):
                # If they are the same event, mark the later headline as seen
                keep_headline = True
                seen_headlines.add(headline_j["title"])
            else:
                # Otherwise, keep both headlines
                continue
        
        # If the current headline should be kept, add it to the filtered list
        if keep_headline:
            filtered_news_data.append(headline_i)
            seen_headlines.add(headline_i["title"])
            last_added_by_date[headline_date] = headline_i  # Update last added for the date

# Save the filtered data to a new JSON file
with open(output_file_path, "w", encoding='utf-8') as output_file:
    json.dump(filtered_news_data, output_file, ensure_ascii=False, indent=4)

print("Filtering process completed. Filtered data saved to:", output_file_path)