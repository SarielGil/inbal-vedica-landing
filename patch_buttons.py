import os
import glob
import re

html_files = glob.glob('/Users/sarielgilat/Documents/python/inbal-vedica-landing/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # This regex looks for anchor tags that are styled as CTA buttons but lack flex alignment
    # specifically those starting with bg-emerald-700 or bg-emerald-600
    
    # Example: class="bg-emerald-600 text-white px-8 py-4 rounded-full text-lg font-bold hover:bg-emerald-700 transition shadow-xl"
    # We want to add: inline-flex items-center justify-center
    
    pattern = r'(class="[^"]*bg-emerald-[67]00[^"]*text-white[^"]*px-8[^"]*rounded-full[^"]*")'
    
    def replacer(match):
        cls_str = match.group(1)
        if 'inline-flex' not in cls_str:
            # insert before the closing quote
            return cls_str[:-1] + ' inline-flex items-center justify-center"'
        return cls_str

    new_content = re.sub(pattern, replacer, content)
    
    # Also fix any "text-center" issues on the a tags if they exist
    if new_content != content:
        content = new_content
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated buttons in: {os.path.basename(filepath)}")

print("Done patching buttons.")
