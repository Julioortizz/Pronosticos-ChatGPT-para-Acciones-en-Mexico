import requests
import json
import pandas as pd

# Your API key for NewsCatcher
api_key = 'HG9VCNxm5MlbCnUmSfYveuHhppJ4jRnknq23GMjL2Uk'
from_date = '2021-10-01'
to_date = '2023-12-31'
excel_file_path = '/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/2. Bases de Datos/Mnotics & Prices.xlsx'

# Read Excel file
df = pd.read_excel(excel_file_path, sheet_name='Mnotics')

# Dictionary to store grouped data by company
grouped_data = {}

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    ticker = row['Ticker s/ Serie']
    ticker_BB = row['Ticker']
    company_name = row['Company Name s/ SA de CV']
    full_company_name = row['Company Name']

    # Define languages to search in
    languages = ['en', 'es']

    for lang in languages:
        # Set up the API request parameters for ticker
        params_ticker = {
            'q': f'"{ticker}"',
            'lang': lang,
            'search_in': 'title',
            'from': from_date,
            'to': to_date,
            'sort_by': 'date',
            'page_size': 100
        }

        # Set up the API request parameters for company name
        params_company = {
            'q': f'"{company_name}"',
            'lang': lang,
            'search_in': 'title',
            'from': from_date,
            'to': to_date,
            'sort_by': 'date',
            'page_size': 100
        }

        headers = {
            'x-api-key': api_key
        }

        # Make the API request for ticker
        response_ticker = requests.get('https://api.newscatcherapi.com/v2/search', params=params_ticker, headers=headers)
        data_ticker = response_ticker.json()
        articles_ticker = data_ticker.get('articles', [])

        # Make the API request for company name
        response_company = requests.get('https://api.newscatcherapi.com/v2/search', params=params_company, headers=headers)
        data_company = response_company.json()
        articles_company = data_company.get('articles', [])

        # Combine the results from both queries
        articles = articles_ticker + articles_company

        # Extract and store title, date, hour, country, and source of publication
        for article in articles:
            title = article.get('title', 'N/A')
            published_at = article.get('published_date', 'N/A')
            rank = article.get('rank', 'N/A')
            country = article.get('country', 'N/A')
            source = article.get('clean_url', 'N/A')

            if published_at != 'N/A':
                date_time = published_at.split(' ')
                date = date_time[0]
                hour = date_time[1] if len(date_time) > 1 else 'N/A'
            else:
                date = 'N/A'
                hour = 'N/A'

            article_data = {
                'title': title,
                'date': date,
                'hour': hour,
                'source': source,
                'rank': rank,
                'country': country,
                'ticker': ticker,
                'ticker_BB': ticker_BB,
                'company_name': company_name,
                'full_company_name': full_company_name,
                'language': lang  # Store the language of the article
            }

            # Group data by full_company_name
            if full_company_name not in grouped_data:
                grouped_data[full_company_name] = []
            grouped_data[full_company_name].append(article_data)

# List to store sorted and grouped data
sorted_all_data = []

# Sort each group by date and hour in descending order, then combine
for company, articles in grouped_data.items():
    articles.sort(key=lambda x: (x['date'], x['hour']), reverse=True)
    sorted_all_data.extend(articles)

# Save the sorted and grouped data to a single JSON file
output_file_path = '/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/1 Titulares/AllNewsData.json'
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(sorted_all_data, file, ensure_ascii=False, indent=4)

# Print the number of data points
print(f"Number of data points: {len(sorted_all_data)}")