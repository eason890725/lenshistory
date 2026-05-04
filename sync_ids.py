import json
import re

def generate_slug(name):
    s = str(name).lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    return s.strip('-')

def sync():
    path = 'frontend/src/data/products.json'
    with open(path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    seen_slugs = {}
    for item in products:
        name = item.get('modelName', 'unknown')
        base_slug = generate_slug(name)
        if not base_slug:
            base_slug = 'product'
            
        slug = base_slug
        counter = 1
        while slug in seen_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        seen_slugs[slug] = True
        item['slug'] = slug
        # Keep numeric ID if exists, otherwise use slug
        if 'id' not in item:
            item['id'] = slug
        else:
            item['id'] = str(item['id'])

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"Sync complete. Processed {len(products)} items.")

if __name__ == "__main__":
    sync()
