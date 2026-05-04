import pandas as pd

try:
    df = pd.read_excel('/mnt/c/?‹äºº/?‹äººè»Ÿé?/lenshistory/Sony FE Lens.xlsx', sheet_name='?“·Prime_å®šç„¦??)
    print("FIRST 10 ROWS:")
    # Print as a simple CSV-like format for readability
    for i in range(min(10, len(df))):
        row = df.iloc[i].values
        print(f"ROW {i}: {row}")
except Exception as e:
    print(f"Error: {e}")
