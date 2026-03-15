import os
from PIL import Image

assets_dir = "/Users/sarielgilat/Documents/python/inbal-vedica-landing/assets"
max_size = (1920, 1920)

for filename in os.listdir(assets_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filepath = os.path.join(assets_dir, filename)
        name, _ = os.path.splitext(filename)
        out_filepath = os.path.join(assets_dir, name + ".webp")
        
        try:
            with Image.open(filepath) as img:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img.save(out_filepath, 'webp', quality=80)
                print(f"Converted {filename} to {name}.webp")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
