import pandas as pd
from datetime import datetime
import os, re
import openpyxl

def excel_to_dict(filename):
    df = pd.read_excel(filename)
    cols = [1, 3, 5, 7, 9, 11, 13]
    rows = df.values.tolist()
    days = []

    block_starts = []
    for i, row in enumerate(rows):
        val = str(row[1]).strip().upper() if not pd.isna(row[1]) else ""
        if val == "PAZAR" or val.startswith("PAZAR"):
            block_starts.append(i)

    for idx, start_row in enumerate(block_starts):
        end_row = block_starts[idx+1] if idx+1 < len(block_starts) else len(rows)
        header_row = rows[start_row]
        date_row = rows[start_row+1] if start_row+1 < len(rows) else None

        for col_idx in cols:
            d_name = str(header_row[col_idx]).strip().capitalize() if not pd.isna(header_row[col_idx]) else ""
            if not d_name or d_name.lower() == "nan":
                continue

            raw_date = date_row[col_idx] if date_row else None
            if pd.isna(raw_date): continue
            
            if isinstance(raw_date, datetime):
                d_str = raw_date.strftime("%d.%m.%Y")
            else:
                d_str = str(raw_date).strip().replace("KALORİ", "").strip().rstrip('.')
            
            if not d_str or d_str.lower() == "nan":
                continue

            items = []
            for i in range(start_row+2, end_row):
                if not pd.isna(rows[i][col_idx]):
                    item_str = str(rows[i][col_idx]).strip()
                    if item_str and item_str.lower() != "nan" and not item_str.startswith("NOT:"):
                        if item_str.startswith("MAİL") or item_str.startswith("İLTEŞİM"):
                            continue
                        # Remove empty / weird stuff
                        if "KALORİ" not in item_str and "KADINLAR İÇİN" not in item_str and "ERKEKLER" not in item_str and "TEDARİKTE AKSAKLIK" not in item_str:
                            items.append(item_str)
            
            days.append({
                "day_name": d_name.upper(),
                "date": d_str,
                "items": items
            })

    def get_sort_key(d):
        try:
            return datetime.strptime(d["date"][:10], "%d.%m.%Y")
        except:
            return datetime.max
            
    days.sort(key=get_sort_key)
    # Group by week (Monday = start of week)
    weeks = []
    current_week = []
    for d in days:
        current_week.append(d)
        if d["day_name"] == "PAZAR":
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)
    return weeks

def render_week(week, week_num, variant="cesit4"):
    if not week: return ""
    first_date = week[0]["date"]
    last_date = week[-1]["date"]
    # Change "2026-03-XX" to "XX.03.2026" if needed
    def fdate(ds):
        if "-" in ds:
            p = ds.split()[0].split("-")
            return f"{p[2]}.{p[1]}.{p[0]}"
        return ds

    first_date = fdate(first_date)
    last_date = fdate(last_date)
    
    # Example format: 02 – 08 Mart 2026
    # Let's just use first day to last day exactly
    try:
        dfirst = datetime.strptime(first_date[:10], "%d.%m.%Y")
        dlast = datetime.strptime(last_date[:10], "%d.%m.%Y")
        header_range = f"{dfirst.strftime('%d')} – {dlast.strftime('%d %B %Y').replace('March', 'Mart').replace('03', 'Mart')}"
    except:
        header_range = f"{first_date} – {last_date}"

    html = f"""
            <!-- H{week_num}: {header_range} -->
            <div class="week-section">
                <div class="week-header">
                    <span class="week-badge"><i class="fa-solid fa-calendar-week mr-1"></i> {week_num}. Hafta</span>
                    <span class="text-white/30 text-xs">{header_range}</span>
                    <div class="week-line"></div>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-3">"""

    for i, d in enumerate(week):
        extra_class = ""
        extra_style = ""
        # if Sunday or Saturday, maybe no special styling unless they have it.
        # Original code has special styling manually, let's keep it simple.
        html += f"""
                    <div class="day-card">
                        <div class="day-label">{d["day_name"].capitalize()}</div><div class="day-date">{fdate(d["date"])}</div>"""
        
        for idx, item in enumerate(d["items"]):
            html += f"""
                        <div class="menu-item"><i class="fa-solid fa-circle"></i>{item}</div>"""
        html += """
                    </div>"""

    html += """
                </div>
            </div>"""
    return html

def render_tab_content(weeks, tab_id, c_count):
    if c_count == 4:
        title = "4 Çeşit Tabldot Menü"
        desc = "Çorba · Ana Yemek · Pilav/Makarna · Salata/Tatlı/İçecek"
        badge = ""
    elif c_count == 5:
        title = "5 Çeşit Tabldot Menü"
        desc = "Çorba · Ana Yemek · Pilav/Makarna · Salata/Tatlı · Ek Salata/İçecek"
        badge = ""
    else:
        title = "6 Çeşit Tabldot Menü"
        desc = "Çorba · Ana Yemek · Pilav/Makarna · Salata/Tatlı · Zeytinyağlı/Meze · Ek"
        badge = """
                <div class="ml-auto hidden md:flex items-center gap-3 bg-emerald-600/10 border border-emerald-600/20 rounded-xl px-4 py-3">
                    <i class="fa-solid fa-leaf text-emerald-500"></i>
                    <div><p class="text-xs font-bold uppercase text-white">Zeytinyağlı</p><p class="text-white/40 text-xs">Haftalık Ek Çeşit</p></div>
                </div>"""
        
    if not badge and c_count in [4,5]:
        badge = """
                <div class="ml-auto hidden md:flex items-center gap-3 bg-primary/10 border border-primary/20 rounded-xl px-4 py-3">
                    <i class="fa-solid fa-check-circle text-primary"></i>
                    <div><p class="text-xs font-bold uppercase text-white">ISO 22000</p><p class="text-white/40 text-xs">Gıda Güvenliği</p></div>
                </div>"""

    active_cls = " active" if c_count == 4 else ""
    html = f"""
        <!-- ══════════════════════════════════════════ -->
        <!-- {c_count} ÇEŞİT -->
        <!-- ══════════════════════════════════════════ -->
        <div id="tab-content-cesit{c_count}" class="tab-content{active_cls}">
            <div class="flex items-center gap-4 mb-10">
                <div>
                    <h2 class="text-3xl font-extrabold text-white">{title}</h2>
                    <p class="text-white/40 text-sm mt-1">{desc}</p>
                </div>{badge}
            </div>
"""
    for i, w in enumerate(weeks):
        html += render_week(w, i+1, f"cesit{c_count}")
    html += """
        </div>"""
    return html

base = "/Users/veliakcay/Documents/projeler/adıgüzel catering/"
with open(base + "menuler.html", "r", encoding="utf-8") as f:
    text = f.read()

# Generate new HTML blocks
from pathlib import Path
w4 = excel_to_dict(base + "menuler_data/mart menü 4 çeşit.xlsx")
w5 = excel_to_dict(base + "menuler_data/mart menü 5 çeşit.xlsx")
w6 = excel_to_dict(base + "menuler_data/mart menü 6 çeşit.xlsx")

html4 = render_tab_content(w4, "tab-content-cesit4", 4)
html5 = render_tab_content(w5, "tab-content-cesit5", 5)
html6 = render_tab_content(w6, "tab-content-cesit6", 6)

full_tabs_html = html4 + "\n" + html5 + "\n" + html6

# We need to replace everything from <!-- 4 ÇEŞİT --> up to BUT NOT INCLUDING <footer class="...">? No, wait!
# in `menuler.html`, the tabs end at <!-- Chef --> or similar?
# Let's use regex matching <!-- 4 ÇEŞİT --> until the end of the tabs section.
# Actually, the file has a closing </main> right after the tabs!
# Let's replace the content between:
#         <!-- ══════════════════════════════════════════ -->\n        <!-- 4 ÇEŞİT -->
# and 
#     </main>
text = re.sub(
    r"(<!-- ══════════════════════════════════════════ -->\s*<!-- 4 ÇEŞİT -->.*?)(?=</main>)",
    full_tabs_html + "\n    ",
    text,
    flags=re.DOTALL
)

# Also update the month references: `Şubat 2026` -> `Mart 2026`
text = text.replace("Şubat 2026", "Mart 2026")

with open(base + "menuler_mart_updated.html", "w", encoding="utf-8") as f:
    f.write(text)

print("HTML generation successful.")
