import os
import glob

html_files = glob.glob('/Users/sarielgilat/Documents/python/inbal-vedica-landing/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False

    # Adjust Favicon to logo.jpg (which has testing solid background)
    old_favicon = '<link rel="icon" href="assets/logo-transparent.png" type="image/png">'
    new_favicon = '<link rel="icon" href="assets/logo.jpg" type="image/jpeg">'
    
    if old_favicon in content:
        content = content.replace(old_favicon, new_favicon)
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated favicon in: {os.path.basename(filepath)}")

print("Done updating favicons.")
