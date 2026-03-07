import pandas as pd
from src.consolidation_algorithm import consolidate_shipments

# Load dataset
df = pd.read_csv("data/shipments.csv")

# Run consolidation
trucks, weights = consolidate_shipments(df)

# Print results
for i in range(len(trucks)):
    print(f"Truck {i+1}")
    print("Shipments:", trucks[i])
    print("Total Weight:", weights[i])
    print("-----------------------")