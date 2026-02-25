import os
import glob
import re

html_files = glob.glob('/Users/sarielgilat/Documents/python/inbal-vedica-landing/*.html')
md_files = glob.glob('/Users/sarielgilat/Documents/python/inbal-vedica-landing/*.md')

ga4_snippet = """    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-XXXXXXXXXX');
    </script>
</head>"""

for filepath in html_files + md_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False

    # Fix typo in Name
    if 'ננבל' in content:
        content = content.replace('ננבל', 'ענבל')
        modified = True

    # Add GA4 snippet to html files
    if filepath.endswith('.html') and 'G-XXXXXXXXXX' not in content:
        # We replace the closing </head> with the snippet + closing head
        content = content.replace('</head>', ga4_snippet)
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(filepath)}")

print("Done patching.")
