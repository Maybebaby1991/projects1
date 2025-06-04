import os
from PIL import Image, ImageDraw, ImageFont
import re

def combine_png_images_with_captions(folder_path, output_filename="ALPHA_RESULT_captioned.png"):
    """
    Combines PNG images from a specified folder into a single image,
    adding captions extracted from filenames (R0 and EPS values).
    """
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".png")]

    if not image_files:
        print(f"No PNG images found in folder '{folder_path}'.")
        return

    images_with_captions = []
    total_width = 0
    max_total_height = 0
    font_size = 20  # Font size for captions
    try:
        # Attempt to load a specific font
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback to default font if arial.ttf is not found
        font = ImageFont.load_default()
        print("Arial font not found, using default font. Captions might look different.")

    for filename in image_files:
        filepath = os.path.join(folder_path, filename)
        try:
            img = Image.open(filepath)

            # Extract R0 and EPS values from the filename
            match = re.search(r"R0-([\d\.-]+)EPS-([\d\.-]+)", filename)
            if match:
                r0_value = match.group(1)
                eps_value = match.group(2)
                caption_text = f"R0={r0_value}, EPS={eps_value}"
            else:
                caption_text = "No EPS/R0 info" # Default caption if pattern not found

            # Create an image for the caption
            # The height of the caption image is font_size + some padding
            caption_img_height = font_size + 10 # Increased padding for better look
            caption_img = Image.new('RGB', (img.width, caption_img_height), color='white')
            d = ImageDraw.Draw(caption_img)

            # Debug prints for font (can be removed in production)
            # print(f"Font variable type: {type(font)}")
            # print(f"Font variable value: {font}")
            current_font = font
            # Use textbbox to get the bounding box of the text
            try:
                # For Pillow versions 8.0.0 and later
                bbox = d.textbbox((0, 0), caption_text, font=current_font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except AttributeError:
                # Fallback for older Pillow versions
                text_width, text_height = d.textsize(caption_text, font=current_font)


            # print(f"Current_font variable: {current_font}") # Debug print
            # Calculate position to center the text
            text_x = (caption_img.width - text_width) // 2
            text_y = (caption_img_height - text_height) // 2 # Center vertically in the caption bar

            d.text((text_x, text_y), caption_text, fill='black', font=font)

            images_with_captions.append({'image': img, 'caption': caption_img})
            total_width += img.width # Assuming images are laid out horizontally
            # Max height will be the image height + caption image height
            max_total_height = max(max_total_height, img.height + caption_img.height)

        except IOError:
            print(f"Could not open image: {filename}. Skipping.")
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}. Skipping.")


    if not images_with_captions:
        print("No images to combine after attempting to open files.")
        return

    # Create the combined image with a white background
    combined_image = Image.new('RGB', (total_width, max_total_height), color='white')
    x_offset = 0
    for image_data in images_with_captions:
        img = image_data['image']
        caption_img = image_data['caption']

        combined_image.paste(img, (x_offset, 0))  # Paste image at the top
        combined_image.paste(caption_img, (x_offset, img.height)) # Paste caption below the image
        x_offset += img.width

    try:
        output_filepath = os.path.join(os.getcwd(), output_filename) # Save in the current working directory
        combined_image.save(output_filepath)
        print(f"Combined image with captions saved as '{output_filepath}'")
    except IOError:
        print(f"Could not save combined image to '{output_filepath}'. Check permissions or path.")
    except Exception as e:
        print(f"An error occurred while saving the combined image: {e}")


if __name__ == "__main__":
    folder_with_pngs = "ALPHA_PICTURE"  # Name of the folder containing PNGs
    if not os.path.isdir(folder_with_pngs):
        print(f"Folder '{folder_with_pngs}' not found in the current directory: {os.getcwd()}")
        # You might want to create it or prompt the user for a correct path
        # For example:
        # try:
        #     os.makedirs(folder_with_pngs, exist_ok=True)
        #     print(f"Created folder '{folder_with_pngs}' as it did not exist.")
        # except OSError as e:
        #     print(f"Error creating folder '{folder_with_pngs}': {e}")
        #     exit() # Exit if folder cannot be accessed/created
    else:
        combine_png_images_with_captions(folder_with_pngs, "ALPHA_RESULT_captioned.png")
        print("Done! Image with captions creation process finished.")