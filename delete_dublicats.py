import requests
from PIL import Image
import imagehash
from io import BytesIO

def get_photos(urls):
    hashes = {}
    unique_urls = []

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content))
            image_hash = imagehash.phash(image)

            # Можно задать порог похожести, если нужно (например, 5)
            is_duplicate = False
            for h in hashes:
                if abs(h - image_hash) <= 5:  # Порог чувствительности
                    is_duplicate = True
                    break

            if not is_duplicate:
                hashes[image_hash] = url
                unique_urls.append(url)

        except Exception as e:
            print(f"⚠️ Ошибка при загрузке {url}: {e}")
            
    return unique_urls

    # print("\n✅ Уникальные изображения:")
    # for url in unique_urls:
    #     print(url)
