import json

def canon_apsc_dimensions_fix_v25():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    fixed_count = 0

    # Canon APS-C 機身精確外型尺寸庫 (W x H x D)
    apsc_dimensions = {
        "eos-r7": "132.0 x 90.4 x 91.7 mm",
        "eos-r10": "122.5 x 87.8 x 83.4 mm",
        "eos-r50": "116.3 x 85.5 x 68.8 mm",
        "eos-r100": "116.3 x 85.5 x 68.8 mm"
    }

    for item in products:
        item_id = item.get('id', '')
        if item_id in apsc_dimensions:
            item['dimensions'] = apsc_dimensions[item_id]
            fixed_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"CANON_APSC_DIMENSIONS_FIX_V25_COMPLETE: Successfully updated {fixed_count} dimension entries.")

if __name__ == "__main__":
    canon_apsc_dimensions_fix_v25()
