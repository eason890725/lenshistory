import pandas as pd

file_path = '/mnt/c/?‹äºº/?‹äººè»Ÿé?/lenshistory/Sony FE Lens.xlsx'

# Prime sheet
df = pd.read_excel(file_path, sheet_name='?“·Prime_å®šç„¦??, skiprows=2)
print('=== PRIME COLUMNS ===')
for i, col in enumerate(df.columns):
    print(f'{i}: {col}')
print()
print('=== PRIME FIRST 2 ROWS ===')
for _, row in df.head(2).iterrows():
    for i, val in enumerate(row):
        print(f'  col[{i}] = {val}')
    print('---')

# Zoom sheet
df2 = pd.read_excel(file_path, sheet_name='?“·Zoom_è®Šç„¦??, skiprows=2)
print()
print('=== ZOOM COLUMNS ===')
for i, col in enumerate(df2.columns):
    print(f'{i}: {col}')
print()
print('=== ZOOM FIRST 2 ROWS ===')
for _, row in df2.head(2).iterrows():
    for i, val in enumerate(row):
        print(f'  col[{i}] = {val}')
    print('---')

# Check for other sheets
xl = pd.ExcelFile(file_path)
print()
print('=== ALL SHEETS ===')
for s in xl.sheet_names:
    print(f'  {s}')
