import pandas as pd

try:
    df = pd.read_excel('/mnt/c/?‹äºº/?‹äººè»Ÿé?/lenshistory/Sony FE Lens.xlsx', sheet_name='?“·Zoom_è®Šç„¦??)
    print("FIRST 5 ROWS ZOOM:")
    for i in range(min(5, len(df))):
        row = df.iloc[i].values
        print(f"ROW {i}: {row}")
except Exception as e:
    print(f"Error: {e}")
