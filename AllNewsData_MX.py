import json

# Path of the original JSON file
input_file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/1 Titulares/AllNewsData.json"

# Paths for the new JSON files
output_file_mx = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/2 Limitantes/AllNewsData_MX.json"

# Load the original JSON file
with open(input_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter the data for MX only
data_mx = [item for item in data if item.get('country') == 'MX']

# Save the filtered data to new JSON files
with open(output_file_mx, 'w', encoding='utf-8') as f:
    json.dump(data_mx, f, ensure_ascii=False, indent=4)

print("JSON files created successfully!")