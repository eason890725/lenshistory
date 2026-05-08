import json

def nikon_full_field_perfection_v28():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    filled_count = 0

    # Nikon 全機身深度規格庫
    nikon_specs = {
        "z9": {
            "afRange": "EV -6.5 to 19 (Starlight: -9 to 19)",
            "evfMagnification": "0.8x",
            "lcdSpec": "3.2-inch 2.1M-dot 4-axis Tilting Touchscreen",
            "cardSlots": "2x CFexpress Type B / XQD",
            "ports": "USB-C (3.2 Gen 2), HDMI Type A, RJ-45, Mic, Headphone, 10-pin Terminal"
        },
        "z8": {
            "afRange": "EV -7 to 19 (Starlight: -9 to 19)",
            "evfMagnification": "0.8x",
            "lcdSpec": "3.2-inch 2.1M-dot 4-axis Tilting Touchscreen",
            "cardSlots": "1x CFexpress Type B + 1x SD (UHS-II)",
            "ports": "Dual USB-C (Data + Power), HDMI Type A, Mic, Headphone, 10-pin"
        },
        "z6-iii": {
            "afRange": "EV -10 to 19",
            "evfMagnification": "0.76x",
            "lcdSpec": "3.2-inch 2.1M-dot Vari-angle Touchscreen",
            "cardSlots": "1x CFexpress Type B + 1x SD (UHS-II)",
            "ports": "USB-C, HDMI Type A, Mic, Headphone"
        },
        "z7-ii": {
            "videoResolution": "4K 60p / FHD 120p",
            "afPoints": "493 Points",
            "burstSpeed": "10 fps",
            "afRange": "EV -3 to 19",
            "evfMagnification": "0.8x",
            "lcdSpec": "3.2-inch 2.1M-dot Tilting Touchscreen",
            "cardSlots": "1x CFexpress Type B + 1x SD (UHS-II)"
        },
        "z7": {
            "videoResolution": "4K 30p / FHD 120p",
            "afPoints": "493 Points",
            "evfResolution": "3.69M-dot OLED",
            "burstSpeed": "9 fps",
            "afRange": "EV -2 to 19",
            "evfMagnification": "0.8x",
            "lcdSpec": "3.2-inch 2.1M-dot Tilting Touchscreen",
            "cardSlots": "1x XQD / CFexpress Type B"
        },
        "z6-ii": {
            "videoResolution": "4K 60p / FHD 120p",
            "afPoints": "273 Points",
            "burstSpeed": "14 fps",
            "afRange": "EV -4.5 to 19",
            "evfMagnification": "0.8x",
            "lcdSpec": "3.2-inch 2.1M-dot Tilting Touchscreen",
            "cardSlots": "1x CFexpress Type B + 1x SD (UHS-II)"
        },
        "z6": {
            "videoResolution": "4K 30p / FHD 120p",
            "afPoints": "273 Points",
            "evfResolution": "3.69M-dot OLED",
            "burstSpeed": "12 fps",
            "afRange": "EV -2 to 19",
            "evfMagnification": "0.8x",
            "lcdSpec": "3.2-inch 2.1M-dot Tilting Touchscreen",
            "cardSlots": "1x XQD / CFexpress Type B"
        },
        "z5": {
            "videoResolution": "4K 30p (Cropped 1.7x) / FHD 60p",
            "afPoints": "273 Points",
            "evfResolution": "3.69M-dot OLED",
            "burstSpeed": "4.5 fps",
            "afRange": "EV -2 to 19",
            "evfMagnification": "0.8x",
            "lcdSpec": "3.2-inch 1.04M-dot Tilting Touchscreen",
            "cardSlots": "2x SD (UHS-II)"
        },
        "zf": {
            "afRange": "EV -10 to 19",
            "evfMagnification": "0.8x",
            "lcdSpec": "3.2-inch 2.1M-dot Vari-angle Touchscreen",
            "cardSlots": "1x SD (UHS-II) + 1x MicroSD (UHS-I)"
        },
        "z50": {
            "videoResolution": "4K 30p / FHD 120p",
            "afPoints": "209 Points",
            "evfResolution": "2.36M-dot OLED",
            "burstSpeed": "11 fps",
            "afRange": "EV -2 to 19",
            "evfMagnification": "0.68x",
            "lcdSpec": "3.2-inch 1.04M-dot Flip-down Touchscreen",
            "cardSlots": "1x SD (UHS-I)"
        },
        "z30": {
            "videoResolution": "4K 30p / FHD 120p",
            "afPoints": "209 Points",
            "evfResolution": "No EVF",
            "burstSpeed": "11 fps",
            "afRange": "EV -2 to 19",
            "lcdSpec": "3.0-inch 1.04M-dot Vari-angle Touchscreen",
            "cardSlots": "1x SD (UHS-I)"
        }
    }

    for item in products:
        item_id = item.get('id', '')
        if item_id in nikon_specs:
            specs = nikon_specs[item_id]
            for key, val in specs.items():
                item[key] = val
                filled_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"NIKON_FULL_FIELD_PERFECTION_V28_COMPLETE: Successfully updated {filled_count} fields.")

if __name__ == "__main__":
    nikon_full_field_perfection_v28()
