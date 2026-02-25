import os
import glob
import re

html_files = glob.glob('/Users/sarielgilat/Documents/python/inbal-vedica-landing/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False

    # 1. Add Favicon if not exists
    if '<link rel="icon"' not in content:
        content = content.replace('</head>', '    <link rel="icon" href="assets/logo-transparent.png" type="image/png">\n</head>')
        modified = True
    
    # 2. Fix the flex menu to be scrollable
    # We replace both variations that might exist
    menu_str1 = '<div class="space-x-reverse space-x-6 flex font-medium">'
    new_menu_str = '<div class="space-x-reverse space-x-6 flex font-medium overflow-x-auto whitespace-nowrap pb-2 md:pb-0 items-center" style="scrollbar-width: none;">'
    
    if menu_str1 in content:
        content = content.replace(menu_str1, new_menu_str)
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(filepath)}")

print("Done updating HTML files.")
