from functions import *


if __name__ == "__main__":
    # Основная часть программы
    breed = input("Введите породу собаки: ").strip().lower()

    try:
        image_urls = dog_breed(breed)
    except Exception as e:
        print(e)
        exit()

    filenames = []
    for img_url in image_urls:
        parts = img_url.rsplit('/', maxsplit=1)[-1].replace("/", "-")
        filenames.append(parts)

    # Выбор способа сохранения
    while True:
        choice = input("Выберите способ сохранения:\n"
                       "0 - сохранить на устройство\n"
                       "1 - загрузить на Яндекс.Диск\n"
                       "Ваш выбор: ")
        if choice.isdigit():
            choice = int(choice)
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

    if choice == 0:
        download_images_device(image_urls, filenames)
        save_images_to_json(filenames, image_urls)
    elif choice == 1:
        download_images_disk(image_urls, filenames, breed.capitalize())
        save_images_to_json(filenames, image_urls)