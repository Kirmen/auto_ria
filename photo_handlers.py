import os
from typing import List

import requests
from PIL import Image


def download_and_convert_photos(photos: List[str]) -> List[str]:
    converted_photos_paths = []
    c = 0
    for photo_url in photos:
        if c == 3:
            break

        response = requests.get(photo_url)
        if response.status_code != 200:
            continue

        local_filename = f"temp_{os.path.basename(photo_url)}"
        with open(local_filename, 'wb') as f:
            f.write(response.content)

        image = Image.open(local_filename)
        converted_filename = f"converted_{os.path.basename(photo_url)}"
        converted_filename = converted_filename.replace(".webp", ".jpg")
        image.convert("RGB").save(converted_filename, "JPEG")
        converted_photos_paths.append(converted_filename)

        os.remove(local_filename)
        c += 1

    return converted_photos_paths
