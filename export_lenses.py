import pandas as pd
import json
import math
from datetime import datetime

def parse_focal(val):
    if pd.isna(val): return None, None
    s = str(val).lower().replace('mm', '').strip()
    if '-' in s:
        parts = s.split('-')
        try:
            return int(float(parts[0])), int(float(parts[1]))
        except:
            return None, None
    else:
        try:
            return int(float(s)), int(float(s))
        except:
            return None, None

def parse_aperture(val):
    if pd.isna(val): return None, None
    s = str(val).lower().replace('f/', '').strip()
    if '-' in s:
        parts = s.split('-')
        try:
            return float(parts[0]), float(parts[1])
        except:
            return None, None
    else:
        try:
            return float(s), None
        except:
            return None, None

def safe_float(val):
    if pd.isna(val): return None
    s = str(val).strip()
    if s in ('x', '-', '', 'nan', 'None'): return None
    try:
        return float(s.replace('mm', '').replace('g', '').replace('$', '').replace(',', ''))
    except:
        return None

def safe_int(val):
    f = safe_float(val)
    if f is None: return None
    return int(f)

def safe_str(val):
    if pd.isna(val): return None
    s = str(val).strip()
    if s in ('', 'nan', 'None'): return None
    return s

def has_feature(val):
    """Parse 'O', 'o', 'V' etc. as True, else False"""
    if pd.isna(val): return False
    s = str(val).strip().lower()
    return s in ('o', 'v', '??, 'yes', 'y', '??)

def parse_date(val):
    if pd.isna(val): return None
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d')
    try:
        return pd.Timestamp(val).strftime('%Y-%m-%d')
    except:
        return None

try:
    file_path = '/mnt/c/?‹äºº/?‹äººè»Ÿé?/lenshistory/Sony FE Lens.xlsx'
    lenses = []

    # ============================================================
    # 1. PRIME LENSES (å®šç„¦??
    # Columns:
    #  0: (empty/index)
    #  1: Brand
    #  2: Series (GM, G, Art, etc.)
    #  3: Lens Model
    #  4: Focal Length (mm)
    #  5: F/ (aperture)
    #  6: Filter (mm)
    #  7: (L) length mm
    #  8: (D) diameter mm
    #  9: (W) weight grams
    # 10: Close Focus (cm)
    # 11: Magnification
    # 12: OIS
    # 13: IP (weather seal)
    # 14: F/ Ring (aperture ring)
    # 15: Custom Button
    # 16: Launch Date
    # 17: Launch Year
    # 18: Launch Since
    # 19: Launch Price (TWD)
    # ============================================================
    df_prime = pd.read_excel(file_path, sheet_name='?“·Prime_å®šç„¦??, skiprows=2)
    for _, row in df_prime.iterrows():
        brand = safe_str(row.iloc[1])
        model = safe_str(row.iloc[3])
        if not brand or not model: continue

        focal_min, focal_max = parse_focal(row.iloc[4])
        aperture_max, _ = parse_aperture(row.iloc[5])

        filter_size = safe_float(row.iloc[6])
        length_mm = safe_float(row.iloc[7])
        diameter_mm = safe_float(row.iloc[8])
        weight = safe_int(row.iloc[9])
        close_focus = safe_float(row.iloc[10])
        magnification = safe_float(row.iloc[11])
        has_ois = has_feature(row.iloc[12])
        has_weather_seal = has_feature(row.iloc[13])
        has_aperture_ring = has_feature(row.iloc[14])
        has_custom_button = has_feature(row.iloc[15])
        launch_date = parse_date(row.iloc[16])
        year = safe_int(row.iloc[17])
        if year is None: year = 2020
        launch_since = safe_str(row.iloc[18])
        launch_price = safe_float(row.iloc[19])
        series = safe_str(row.iloc[2])

        dims = None
        if diameter_mm and length_mm:
            dims = f"Ã¸{diameter_mm} ? {length_mm} mm"

        lenses.append({
            "brand": brand,
            "series": series,
            "modelName": model,
            "gearType": "LENS",
            "lensType": None,  # prime has no type column
            "releaseYear": year,
            "focalLengthMinMm": focal_min,
            "focalLengthMaxMm": focal_max,
            "zoomRatio": None,  # prime
            "apertureMax": aperture_max,
            "apertureMin": None,
            "filterSizeMm": filter_size,
            "lengthMm": length_mm,
            "diameterMm": diameter_mm,
            "weightGrams": weight,
            "dimensions": dims,
            "closeFocusCm": close_focus,
            "maxMagnification": magnification,
            "hasOIS": has_ois,
            "hasWeatherSeal": has_weather_seal,
            "hasApertureRing": has_aperture_ring,
            "hasCustomButton": has_custom_button,
            "launchDate": launch_date,
            "launchSince": launch_since,
            "launchPrice": launch_price,
            "sensorFormat": "Full Frame",
            "isNative": brand.lower() == 'sony'
        })

    # ============================================================
    # 2. ZOOM LENSES (è®Šç„¦??
    # Columns:
    #  0: (empty/index)
    #  1: Brand
    #  2: Series
    #  3: Lens Model
    #  4: Type (1.Wide, 2.Standard, 3.Tele, etc.)
    #  5: Focal Length (e.g. "12-24mm")
    #  6: Zoom Ratio
    #  7: F/ (e.g. "f/2.8-2.8")
    #  8: Filter (mm or 'x')
    #  9: (L) length mm
    # 10: (D) diameter mm
    # 11: (W) weight grams
    # 12: Close Focus (cm)
    # 13: Magnification
    # 14: OIS
    # 15: IP (weather seal)
    # 16: F/ Ring (aperture ring)
    # 17: Custom Button
    # 18: Launch Date
    # 19: Launch Year
    # 20: Launch Since
    # 21: Launch Price (TWD)
    # ============================================================
    df_zoom = pd.read_excel(file_path, sheet_name='?“·Zoom_è®Šç„¦??, skiprows=2)
    for _, row in df_zoom.iterrows():
        brand = safe_str(row.iloc[1])
        model = safe_str(row.iloc[3])
        if not brand or not model: continue

        lens_type = safe_str(row.iloc[4])
        focal_min, focal_max = parse_focal(row.iloc[5])
        zoom_ratio = safe_float(row.iloc[6])
        aperture_max, aperture_min = parse_aperture(row.iloc[7])

        filter_size = safe_float(row.iloc[8])
        length_mm = safe_float(row.iloc[9])
        diameter_mm = safe_float(row.iloc[10])
        weight = safe_int(row.iloc[11])
        close_focus = safe_float(row.iloc[12])
        magnification = safe_float(row.iloc[13])
        has_ois = has_feature(row.iloc[14])
        has_weather_seal = has_feature(row.iloc[15])
        has_aperture_ring = has_feature(row.iloc[16])
        has_custom_button = has_feature(row.iloc[17])
        launch_date = parse_date(row.iloc[18])
        year = safe_int(row.iloc[19])
        if year is None: year = 2020
        launch_since = safe_str(row.iloc[20])
        launch_price = safe_float(row.iloc[21])
        series = safe_str(row.iloc[2])

        dims = None
        if diameter_mm and length_mm:
            dims = f"Ã¸{diameter_mm} ? {length_mm} mm"

        lenses.append({
            "brand": brand,
            "series": series,
            "modelName": model,
            "gearType": "LENS",
            "lensType": lens_type,
            "releaseYear": year,
            "focalLengthMinMm": focal_min,
            "focalLengthMaxMm": focal_max,
            "zoomRatio": zoom_ratio,
            "apertureMax": aperture_max,
            "apertureMin": aperture_min,
            "filterSizeMm": filter_size,
            "lengthMm": length_mm,
            "diameterMm": diameter_mm,
            "weightGrams": weight,
            "dimensions": dims,
            "closeFocusCm": close_focus,
            "maxMagnification": magnification,
            "hasOIS": has_ois,
            "hasWeatherSeal": has_weather_seal,
            "hasApertureRing": has_aperture_ring,
            "hasCustomButton": has_custom_button,
            "launchDate": launch_date,
            "launchSince": launch_since,
            "launchPrice": launch_price,
            "sensorFormat": "Full Frame",
            "isNative": brand.lower() == 'sony'
        })

    with open('/mnt/c/?‹äºº/?‹äººè»Ÿé?/lenshistory/backend/src/main/resources/lenses.json', 'w', encoding='utf-8') as f:
        json.dump(lenses, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved {len(lenses)} lenses to lenses.json")
    
    # Print a sample to verify
    sample = lenses[0]
    print(f"\nSample entry ({sample['modelName']}):")
    for k, v in sample.items():
        print(f"  {k}: {v}")

except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Error: {e}")
