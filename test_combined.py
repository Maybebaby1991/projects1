from PIL import Image, ImageDraw, ImageFont

try:
    font = ImageFont.truetype("arial.ttf", 20)  
except IOError:
    font = ImageFont.load_default()

caption_text = "Тестовая подпись"
img = Image.new('RGB', (200, 100), 'white')
d = ImageDraw.Draw(img)

current_font = font 
bbox = d.textbbox(0, 0, caption_text, font=current_font) 

print("Результат textbbox:", bbox) 

img.show() 
