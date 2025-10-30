import json
import os
import requests
import time

def dog_breed(breed):
    """Получаем список ссылок на изображения конкретной породы"""
    url_dog = f'https://dog.ceo/api/breed/{breed}/images'
    response = requests.get(url_dog)

    if response.status_code != 200:
        raise Exception(f"Ошибка: {response.status_code}, сообщение: {response.text}")

    data = response.json()
    if not isinstance(data['message'], list):
        raise ValueError("Нет списка изображений")

    return data['message']


def download_images_device(urls, names):
    """
    Скачивает изображения на устройство, сохраняет файлы в папку 'Загрузки'.
    """
    downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

    print(f"Очередь загрузки: {len(urls)}.")
    for i, url in enumerate(urls):
        time.sleep(1)
        filename = os.path.join(downloads_dir, names[i])
        try:
            r = requests.get(url)
            r.raise_for_status()

            with open(filename, 'wb') as file:
                file.write(r.content)

            print(f"Файл '{names[i]}' успешно сохранён в папку 'Загрузки'.")
            print(f"Прогресс загрузки: {i + 1} из {len(urls)}.")
        except requests.RequestException as e:
            print(f"Произошла ошибка при сохранении файла {names[i]}: {e}")


def download_images_disk(urls, names, breed_name):
    """
    Загрузка изображений на Яндекс.Диск.
    """
    token_disk = ''  # Токен
    base_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
    folder_path = '/' + breed_name + '/'

    # Создание папки на диске, если её ещё нет
    headers = {'Authorization': f'OAuth {token_disk}'}
    response = requests.put(base_url, params={'path': folder_path}, headers=headers)
    if response.status_code not in (201, 409):
        raise Exception(f"Ошибка при создании папки: {response.status_code}, сообщение: {response.json()}")

    # Начинаем загрузку изображений
    print(f"Очередь загрузки: {len(urls)}.")
    for i, (url, name) in enumerate(zip(urls, names)):
        upload_url = base_url + 'upload?'
        path_to_file = folder_path + name
        upload_params = {'path': path_to_file}
        resp_get_upload_link = requests.get(upload_url, params=upload_params, headers=headers)
        if resp_get_upload_link.status_code != 200:
            print(f"Произошла ошибка при получении ссылки для загрузки файла '{name}'.")
            continue

        upload_href = resp_get_upload_link.json()['href']

        # Загружаем файл на Яндекс.Диск
        file_data = requests.get(url).content
        file_response = requests.put(upload_href, data=file_data)
        if file_response.status_code != 201:
            print(f"Файл '{name}' не загружен.")
        else:
            print(f"Успешно загрузил файл '{name}'!")
            print(f"Прогресс загрузки: {i + 1} из {len(urls)}.")


def save_images_to_json(filename, images):
    # Проверяем наличие файла, создаем пустой словарь, если файла нет
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    # Добавляем картинки в словарь
    if 'images' not in data:
        data['photos'] = []
    data['photos'].extend(images)

    # Сохраняем обновленные данные обратно в файл
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)