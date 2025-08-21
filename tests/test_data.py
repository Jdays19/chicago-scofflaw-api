import pandas as pd

# Test to make sure csv was loaded properly and displays first 10 addresses
violations_df = pd.read_csv("data/Building_Violations.csv")

print(violations_df["ADDRESS"].head(10))
