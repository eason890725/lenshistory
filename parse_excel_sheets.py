import pandas as pd

try:
    xl = pd.ExcelFile('/mnt/c/?‹äºº/?‹äººè»Ÿé?/lenshistory/Sony FE Lens.xlsx')
    print("SHEET NAMES:")
    print(xl.sheet_names)
    
    # Print columns and first row of each sheet
    for sheet in xl.sheet_names:
        df = xl.parse(sheet).head(1)
        print(f"\n--- SHEET: {sheet} ---")
        print("Columns:", df.columns.tolist())
except Exception as e:
    print(f"Error: {e}")
