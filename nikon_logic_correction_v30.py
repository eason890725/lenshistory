import json

def nikon_logic_correction_v30():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    fixed_count = 0

    # Nikon 專業參數修正庫 (邏輯撥亂反正)
    nikon_logic_db = {
        "z9": {
            "logSupport": "N-Log / HLG / ProRes RAW / N-RAW",
            "videoColorDepth": "12-bit (N-RAW/ProRes RAW) / 10-bit (H.265)",
            "isoRange": "64-25600 (Ext: 32-102400)",
            "sensorType": "Stacked CMOS"
        },
        "z8": {
            "logSupport": "N-Log / HLG / N-RAW",
            "videoColorDepth": "12-bit (N-RAW) / 10-bit (H.265)",
            "isoRange": "64-25600 (Ext: 32-102400)",
            "sensorType": "Stacked CMOS"
        },
        "z6-iii": {
            "logSupport": "N-Log / HLG / N-RAW",
            "videoColorDepth": "12-bit (N-RAW) / 10-bit (H.265)",
            "isoRange": "100-64000 (Ext: 50-204800)",
            "sensorType": "Partially Stacked CMOS"
        },
        "zf": {
            "logSupport": "N-Log / HLG",
            "videoColorDepth": "10-bit 4:2:2 (Internal)",
            "isoRange": "100-64000 (Ext: 50-204800)",
            "sensorType": "BSI CMOS"
        },
        "z7-ii": {
            "logSupport": "N-Log (External)",
            "videoColorDepth": "10-bit 4:2:2 (via HDMI)",
            "isoRange": "64-25600 (Ext: 32-102400)",
            "sensorType": "BSI CMOS"
        },
        "z6-ii": {
            "logSupport": "N-Log (External)",
            "videoColorDepth": "10-bit 4:2:2 (via HDMI)",
            "isoRange": "100-51200 (Ext: 50-204800)",
            "sensorType": "BSI CMOS"
        },
        "z7": {
            "logSupport": "N-Log (External)",
            "videoColorDepth": "10-bit (via HDMI)",
            "isoRange": "64-25600 (Ext: 32-102400)",
            "sensorType": "BSI CMOS"
        },
        "z6": {
            "logSupport": "N-Log (External)",
            "videoColorDepth": "10-bit (via HDMI)",
            "isoRange": "100-51200 (Ext: 50-204800)",
            "sensorType": "BSI CMOS"
        },
        "z5": {
            "logSupport": "No (Flat Picture Control)",
            "videoColorDepth": "8-bit",
            "isoRange": "100-51200 (Ext: 50-102400)",
            "sensorType": "BSI CMOS"
        },
        "z50": {
            "logSupport": "No",
            "isoRange": "100-51200 (Ext: 204800)",
            "sensorType": "BSI CMOS"
        },
        "z30": {
            "logSupport": "No",
            "isoRange": "100-51200 (Ext: 204800)",
            "sensorType": "BSI CMOS"
        }
    }

    for item in products:
        item_id = item.get('id', '')
        if item_id in nikon_logic_db:
            specs = nikon_logic_db[item_id]
            for key, val in specs.items():
                item[key] = val
                fixed_count += 1
        
        # 全域清理：移除任何殘留的 "Sony" 或 "Canon" 字眼於 Nikon 產品中
        if item.get('brand') == 'Nikon':
            for key in ['logSupport', 'processor', 'sensorType']:
                val = str(item.get(key, ''))
                if 'Log3' in val or 'S-Cinetone' in val:
                    item[key] = '--' # 強制重置為缺失，待後續邏輯補全
                    fixed_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"NIKON_LOGIC_CORRECTION_V30_COMPLETE: Fixed {fixed_count} logic and depth fields.")

if __name__ == "__main__":
    nikon_logic_correction_v30()
