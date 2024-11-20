import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

# Load the JSON data
file_path = "/Users/Julioortiz/Documents/ITAM/5. Titulación/4. Propuesta de Tesis 2/3. Desarrollo/6. Códigos Python/4 Regresion/Averages&Returns.json"
data = pd.read_json(file_path)

# Keep 'ticker_BB' and 'date' as columns for clustering purposes and also set them as a MultiIndex for the panel structure
data = data.set_index(['ticker_BB', 'date'], drop=False)

# Define the dependent and independent variables
y = data['price_return']
X = data[['chatgpt4_average']]

# Add a constant term to the independent variable
X = sm.add_constant(X)

# Fit the PanelOLS model with fixed effects and cluster by both 'ticker_BB' and 'date'
model = PanelOLS(y, X, entity_effects=True, time_effects=True)
results = model.fit(cov_type='clustered', clusters=data[['ticker_BB', 'date']])

# Print the summary of the regression results
print(results.summary)