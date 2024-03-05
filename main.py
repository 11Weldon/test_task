import os
import shutil
from PIL import Image
import requests
from urllib.parse import urlencode
import zipfile


def download_zip(public_key):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'

    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']

    response = requests.get(download_url)
    response.raise_for_status()

    with open("archive.zip", "wb") as file:
        file.write(response.content)

    archive = 'archive.zip'
    with zipfile.ZipFile(archive, 'r') as zip_file:
        zip_file.extractall('add')


def merge_images_into_tiff(input_folders, output_filename):
    images = []

    for folder in input_folders:
        folder_path = os.path.join('add/Для тестового', folder)  # Замените на реальный путь к вашей папке
        for filename in os.listdir(folder_path):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                image_path = os.path.join(folder_path, filename)
                img = Image.open(image_path)
                images.append(img)

    if images:
        width = max(img.width for img in images)
        height = max(img.height for img in images)  # Учитываем отступы между изображениями

        result_image = Image.new('RGB', ((width + 250) * 4, (height + 250) * (len(images) // 4)))

        x_offset = 200
        y_offset = 300
        for i, img in enumerate(images):
            result_image.paste(img, (x_offset, y_offset))

            if (i + 1) % 4 == 0:
                y_offset += img.height + 200
                x_offset = 200
            else:
                x_offset += width + 200

            result_image.save(output_filename)
        print(f'Файл {output_filename} успешно создан.')
    else:
        print('В выбранных папках не найдено изображений.')

    shutil.rmtree("add")
    os.remove('archive.zip')


# Пример использования
url = 'https://disk.yandex.ru/d/V47MEP5hZ3U1kg'
download_zip(url)
input_folders = ['1388_12_Наклейки 3-D_3', '1369_12_Наклейки 3-D_3', '1388_6_Наклейки 3-D_2']
output_filename = 'Result.tif'
merge_images_into_tiff(input_folders, output_filename)
