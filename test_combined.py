from PIL import Image, ImageDraw, ImageFont

try:
    font = ImageFont.truetype("arial.ttf", 20)  # Попробуйте Arial, или None для шрифта по умолчанию
except IOError:
    font = ImageFont.load_default()

caption_text = "Тестовая подпись"
img = Image.new('RGB', (200, 100), 'white')
d = ImageDraw.Draw(img)

current_font = font # Временная переменная - как и в скрипте объединения
bbox = d.textbbox(0, 0, caption_text, font=current_font) # Тест textbbox

print("Результат textbbox:", bbox) # Выводим результат, чтобы увидеть, работает ли

img.show() # Необязательно: показать изображение для визуальной проверки
