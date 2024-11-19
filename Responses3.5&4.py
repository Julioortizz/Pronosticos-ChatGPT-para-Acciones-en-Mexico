import json
from openai import OpenAI

# Load data from JSON file
input_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/ChatGPTResponses3.5.json"
output_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/Responses3.5&4.json"

with open(input_file_path, "r") as file:
    news_data = json.load(file)

# Initialize OpenAI client
client = OpenAI(api_key="OpenAI_api_key")

# Iterate through each element in the JSON file
for element in news_data:
    # Replace placeholders in the code
    user_message = f"Is this headline good or bad for the stock price of {element['full_company_name']} in the short term? Headline: {element['title']}"

    # Make API call to OpenAI
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Forget all your previous instructions. Pretend you are a financial expert. You are a financial expert with stock recommendation experience. Answer 'YES' if good news, 'NO' if bad news, or 'UNKNOWN' if uncertain in the first line. Then elaborate with one short and concise sentence on the next line."},
            {"role": "user", "content": user_message}
        ]
    )

    # Extracting content from the response
    response_content = response.choices[0].message.content

    # Update the element with the ChatGPT response
    element["chatgpt4_response"] = response_content

# Save the updated data to a new JSON file
with open(output_file_path, "w", encoding='utf-8') as output_file:
    json.dump(news_data, output_file, ensure_ascii=False, indent=4)