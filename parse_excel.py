import pandas as pd
import json
import sys

try:
    df = pd.read_excel('/mnt/c/?‹äºº/?‹äººè»Ÿé?/lenshistory/Sony FE Lens.xlsx')
    # Fill NaN with None so JSON handles it properly
    df = df.where(pd.notnull(df), None)
    
    print("COLUMNS:")
    print(df.columns.tolist())
    
    print("\nDATA SAMPLE (first 3 rows):")
    print(df.head(3).to_json(orient='records', force_ascii=False, indent=2))
except Exception as e:
    print(f"Error reading excel: {e}")
