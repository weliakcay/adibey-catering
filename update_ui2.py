import os
import re

files = ["index.html", "hakkimizda.html", "hizmetlerimiz.html", "menuler.html", "referanslar.html", "teklif-al.html"]
base_dir = "."

icon_map = {
    "visibility": "fa-solid fa-eye",
    "rocket_launch": "fa-solid fa-rocket",
    "home_work": "fa-solid fa-building",
    "lunch_dining": "fa-solid fa-burger",
    "handshake": "fa-solid fa-handshake",
    "restaurant_menu": "fa-solid fa-book-open",
    "kitchen": "fa-solid fa-kitchen-set",
    "send": "fa-solid fa-paper-plane",
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
    
    def replacer(match):
        span_tag = match.group(0)
        inner_text = match.group(1).strip()
        
        if inner_text in icon_map:
            classes = re.search(r'class="([^"]*)"', span_tag)
            class_str = classes.group(1) if classes else ""
            class_str = class_str.replace("material-symbols-outlined", "").strip()
            
            return f'<i class="{icon_map[inner_text]} {class_str}"></i>'
        else:
            return span_tag
            
    content = re.sub(r'<span[^>]*material-symbols-outlined[^>]*>(.*?)</span>', replacer, content, flags=re.DOTALL)
    
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

print("Remaining updates applied!")
