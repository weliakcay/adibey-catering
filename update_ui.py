import os
import re

files = ["index.html", "hakkimizda.html", "hizmetlerimiz.html", "menuler.html", "referanslar.html", "teklif-al.html"]
base_dir = "."

icon_map = {
    "mail": "fa-solid fa-envelope",
    "call": "fa-solid fa-phone",
    "location_on": "fa-solid fa-location-dot",
    "restaurant": "fa-solid fa-utensils",
    "celebration": "fa-solid fa-champagne-glasses",
    "stars": "fa-solid fa-star",
    "star": "fa-solid fa-star",
    "verified": "fa-solid fa-check-circle",
    "eco": "fa-solid fa-leaf",
    "schedule": "fa-solid fa-clock",
    "workspace_premium": "fa-solid fa-award",
    "expand_more": "fa-solid fa-chevron-down",
    "arrow_back": "fa-solid fa-arrow-left",
    "trending_flat": "fa-solid fa-arrow-right",
    "public": "fa-brands fa-instagram",
    "apartment": "fa-solid fa-building",
    "factory": "fa-solid fa-industry",
    "school": "fa-solid fa-school",
    "local_hospital": "fa-solid fa-hospital",
    "directions_car": "fa-solid fa-car",
    "business": "fa-solid fa-briefcase",
    "engineering": "fa-solid fa-helmet-safety",
    "construction": "fa-solid fa-trowel-bricks",
    "store": "fa-solid fa-store",
    "hub": "fa-solid fa-network-wired",
    "local_shipping": "fa-solid fa-truck",
    "energy_savings_leaf": "fa-solid fa-leaf",
    "format_quote": "fa-solid fa-quote-left",
    "person": "fa-solid fa-user",
    "groups": "fa-solid fa-users",
    "calendar_today": "fa-solid fa-calendar-day"
}

for f in files:
    path = os.path.join(base_dir, f)
    if not os.path.exists(path):
        continue
        
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # 1. Replace Font Link for Material Symbols
    content = content.replace(
        '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&display=swap"\n        rel="stylesheet" />',
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />'
    )
    # Also handle single-line version if format slightly different
    content = re.sub(
        r'<link href="https://fonts.googleapis.com/css2\?family=Material\+Symbols\+Outlined[^"]*"[^>]*>',
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />',
        content
    )
    
    # 2. Replace phone numbers
    content = content.replace("+90 212 555 44 33", "+90 544 475 14 10")
    
    # 3. Handle Teklif Al nav button -> Sizi Arayalım
    # The html looks like:
    # <span class="material-symbols-outlined text-sm">mail</span>
    # Teklif Al
    content = re.sub(
        r'<a href="teklif-al\.html"\s*class="([^"]*)".*?>\s*<span class="material-symbols-outlined[^>]*>mail</span>\s*Teklif Al\s*</a>',
        r'<a href="teklif-al.html" class="\1"><i class="fa-solid fa-phone text-sm"></i> Sizi Arayalım</a>',
        content,
        flags=re.DOTALL
    )

    # 4. Remove check_circle text
    content = re.sub(
        r'<span[^>]*material-symbols-outlined[^>]*>\s*check_circle\s*</span>',
        '',
        content
    )

    # 5. Remove arrow_forward text
    content = re.sub(
        r'<span[^>]*material-symbols-outlined[^>]*>\s*arrow_forward\s*</span>',
        '',
        content
    )
    
    # 6. Replace all remaining material icons with FontAwesome
    def replacer(match):
        span_tag = match.group(0)
        inner_text = match.group(1).strip()
        
        if inner_text in icon_map:
            # retain the class attributes from the span, but mapped to <i>
            classes = re.search(r'class="([^"]*)"', span_tag)
            class_str = classes.group(1) if classes else ""
            # remove material-symbols-outlined
            class_str = class_str.replace("material-symbols-outlined", "").strip()
            
            return f'<i class="{icon_map[inner_text]} {class_str}"></i>'
        else:
            return span_tag # leave as is if not in map
            
    content = re.sub(r'<span[^>]*material-symbols-outlined[^>]*>(.*?)</span>', replacer, content, flags=re.DOTALL)
    
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

print("Updates applied to all files!")
