import os
import glob
import re

html_files = glob.glob('/Users/sarielgilat/Documents/python/inbal-vedica-landing/*.html')

gtm_head = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-WZKF36P7');</script>
<!-- End Google Tag Manager -->
</head>"""

gtm_body = """
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WZKF36P7"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove previous GA4 placeholder snippet if present
    content = re.sub(r'[ \t]*<!-- Google tag \(gtag\.js\) -->.*?</script>[ \t]*\n?', '', content, flags=re.DOTALL)

    if 'GTM-WZKF36P7' not in content:
        # 1. Insert into head
        content = content.replace('</head>', gtm_head)
        
        # 2. Insert into body right after the tag
        content = re.sub(r'(<body[^>]*>)', r'\1' + gtm_body, content, count=1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated GTM in: {os.path.basename(filepath)}")

print("Done GTM patching.")
