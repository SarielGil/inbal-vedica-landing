import os
import glob
import re

html_files = glob.glob('/Users/sarielgilat/Documents/python/inbal-vedica-landing/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 1. Fix navbar logo jump (unify on h-16 w-auto instead of h-10 w-auto)
    if 'id="site-logo"' in content and 'class="h-10 w-auto"' in content:
        content = content.replace('class="h-10 w-auto"', 'class="h-16 w-auto"')
        modified = True

    # 2. Fix the Therapeutic Expertise layout in about.html
    if 'about.html' in filepath:
        old_bullet = '<li class="flex items-start gap-2"><div class="text-emerald-500 mt-1.5 w-1.5 h-1.5 rounded-full bg-emerald-500 flex-shrink-0"></div>'
        new_bullet = '<li class="flex items-start gap-3"><div class="mt-2 w-2 h-2 rounded-full bg-emerald-500 flex-shrink-0"></div>'
        if old_bullet in content:
            content = content.replace(old_bullet, new_bullet)
            modified = True
            
        if 'grid md:grid-cols-3 gap-8' in content:
            content = content.replace('grid md:grid-cols-3 gap-8', 'grid lg:grid-cols-3 md:grid-cols-2 gap-12')
            modified = True

        if 'ul class="space-y-4 text-slate-700"' in content:
            content = content.replace('ul class="space-y-4 text-slate-700"', 'ul class="space-y-5 text-slate-700 text-lg"')
            modified = True

    # 3. Remove the price in clinic.html
    if 'clinic.html' in filepath:
        price_snippet = """                            <div class="bg-emerald-50 p-4 rounded-xl">
                                <p class="text-emerald-900 font-bold">💰 עלות: 450 ש״ח למפגש</p>
                            </div>"""
        if price_snippet in content:
            content = content.replace(price_snippet, '')
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed layout in: {os.path.basename(filepath)}")

print("Done UI patching.")
