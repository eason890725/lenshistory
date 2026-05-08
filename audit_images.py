import json

def audit_images():
    with open('frontend/src/data/products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    report = {}
    for p in data:
        brand = p.get('brand', 'Unknown')
        if brand not in report:
            report[brand] = {'with_img': 0, 'no_img': 0}
        
        if p.get('image_url') and p.get('image_url') != '--':
            report[brand]['with_img'] += 1
        else:
            report[brand]['no_img'] += 1
            
    print("Image Audit Report:")
    for brand, stats in report.items():
        total = stats['with_img'] + stats['no_img']
        print(f"{brand:15} | With Img: {stats['with_img']:3} | No Img: {stats['no_img']:3} | Total: {total:3}")

if __name__ == "__main__":
    audit_images()
