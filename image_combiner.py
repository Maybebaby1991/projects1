import os
from PIL import Image, ImageDraw, ImageFont
import re
def combine_png_images_with_captions(folder_path, output_filename="ALPHA_RESULT_captioned.png"):
    """
    Объединяет PNG изображения из папки в горизонтальное изображение с подписями.
    Подписи извлекаются из имен файлов (EPS и R0 значения).

    Args:
        folder_path (str): Путь к папке с PNG изображениями.
        output_filename (str, optional): Имя файла для сохранения.
                                         По умолчанию "ALPHA_RESULT_captioned.png".
    """

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".png")]

    if not image_files:
        print(f"В папке '{folder_path}' не найдено PNG изображений.")
        return

    images_with_captions = []
    total_width = 0
    max_total_height = 0  # Максимальная общая высота (изображение + подпись)
    font_size = 20
    try:
        font = ImageFont.truetype("arial.ttf", font_size) # Попробуйте Arial, если есть
    except IOError:
        font = ImageFont.load_default() # Или стандартный шрифт

    for filename in image_files:
        filepath = os.path.join(folder_path, filename)
        try:
            img = Image.open(filepath)

            # Извлечение EPS и R0 из имени файла с помощью регулярных выражений
            match = re.search(r"R0-([\d\.-]+)EPS-([\d\.-]+)", filename)
            if match:
                r0_value = match.group(1)
                eps_value = match.group(2)
                caption_text = f"R0={r0_value}, EPS={eps_value}"
            else:
                caption_text = "No EPS/R0 info" # Подпись по умолчанию, если не найдено

            # Создание изображения подписи
            caption_img = Image.new('RGB', (img.width, font_size + 5), color='white') # Белый фон для подписи
            d = ImageDraw.Draw(caption_img)
            # Заменяем textsize на textbbox:
            print(f"Тип переменной font: {type(font)}")
            print(f"Значение переменной font: {font}")
            current_font = font  # Создаем временную переменную
            bbox = d.textbbox(0, 0, caption_text, font=current_font) # Используем временную переменную
            print(f"Переменная current_font: {current_font}") # Добавим печать временной переменной
            text_width = bbox[2] - bbox[0] # Ширина из bbox
            text_height = bbox[3] - bbox[1] # Высота из bbox
            text_x = (caption_img.width - text_width) // 2 # Центрирование текста
            d.text((text_x, 0), caption_text, fill='black', font=font)

            images_with_captions.append({'image': img, 'caption': caption_img})
            total_width += img.width
            max_total_height = max(max_total_height, img.height + caption_img.height)

        except IOError:
            print(f"Не удалось открыть изображение: {filename}. Пропускаем.")

    if not images_with_captions:
        print("Нет изображений для объединения после попытки открытия файлов.")
        return

    combined_image = Image.new('RGB', (total_width, max_total_height), color='white') # Белый фон для общего изображения
    x_offset = 0
    for image_data in images_with_captions:
        img = image_data['image']
        caption_img = image_data['caption']

        combined_image.paste(img, (x_offset, 0)) # Изображение вверху
        combined_image.paste(caption_img, (x_offset, img.height)) # Подпись под изображением
        x_offset += img.width

    try:
        output_filepath = os.path.join(os.getcwd(), output_filename)
        combined_image.save(output_filepath)
        print(f"Объединенное изображение с подписями сохранено как '{output_filepath}'")
    except IOError:
        print(f"Не удалось сохранить объединенное изображение в '{output_filepath}'. Проверьте права доступа или путь.")


if __name__ == "__main__":
    folder_with_pngs = "ALPHA_PICTURE"
    if not os.path.isdir(folder_with_pngs):
        print(f"Папка '{folder_with_pngs}' не найдена.")
    else:
        combine_png_images_with_captions(folder_with_pngs, "ALPHA_RESULT_captioned.png")
        print("Готово! Изображение с подписями создано.")
