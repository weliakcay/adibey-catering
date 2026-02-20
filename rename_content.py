import os
import re

files = ["index.html", "hakkimizda.html", "hizmetlerimiz.html", "menuler.html", "referanslar.html", "teklif-al.html"]
base_dir = "."

for f in files:
    path = os.path.join(base_dir, f)
    if not os.path.exists(path):
        continue
        
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Replace Adıgüzel with Adıbey (case-sensitive variants)
    content = content.replace("Adıgüzel", "Adıbey")
    content = content.replace("adıgüzel", "adıbey")
    content = content.replace("ADIGÜZEL", "ADIBEY")
    
    # Clean up any varied address strings and replace with the new one
    address_patterns = [
        r'Organize Sanayi Bölgesi,\s*4\.\s*Cadde\s*No:\s*12,\s*İstanbul',
        r'Organize Sanayi Bölgesi,\s*4\.\s*Cadde\s*No:12,\s*İstanbul',
        r'Organize Sanayi Bölgesi,\s*4\.\s*Cadde\s*No:12,\s*Kocaeli',
        r'Organize Sanayi Bölgesi,\s*4\.\s*Cadde\s*No:\s*12\s*<br\s*/>\s*İstanbul,\s*Türkiye'
    ]
    
    new_address = "Altınkale, Şht. Mustafa Gürcan Cd. No:72/2, Döşemealtı/Antalya"
    new_address_multiline = "Altınkale, Şht. Mustafa Gürcan Cd.<br/>No:72/2, Döşemealtı/Antalya"
    
    for pattern in address_patterns:
        # If it contains <br />, replace with the multiline version to maintain layout
        if '<br' in pattern:
            content = re.sub(pattern, new_address_multiline, content)
        else:
            content = re.sub(pattern, new_address, content)

    # 3. Remove the broken map image div container. The container looks like:
    # <div class="relative w-24 h-32 ml-4 rounded-xl overflow-hidden shadow-lg border border-primary/20 bg-background-dark/50 p-2 group...
    
    map_div_pattern = r'<div class="relative w-24 h-32 ml-4 rounded-xl overflow-hidden.*?</div>\s*</div>'
    
    # We need to make sure we only remove the map div container and not break the flex layout. 
    # Usually it's nestled as:
    # <div class="flex gap-4">
    #     <ul class="space-y-4 text-slate-500 text-sm">...</ul>
    #     <div class="relative w-24 h-32 ml-4...
    #         <img src="...Antalya_districts.png">
    #         ...
    #     </div>
    # </div>
    
    # Use re.sub with DOTALL to carefully target and remove the map div block.
    # We will look for the div that directly contains the Antalya Haritası.
    content = re.sub(
        r'<div class="relative w-24 h-32 ml-4 rounded-xl overflow-hidden[^>]*>\s*<img[^>]*alt="Antalya Haritası"[^>]*>\s*<div[^>]*></div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

print("Renaming, address updates, and map removal applied!")
