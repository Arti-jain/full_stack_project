from PIL import Image

def crop_image(image_path, output_path):
    img = Image.open(image_path)
    width, height = img.size

    new_width, new_height = 450, 350
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    img = img.crop((left, top, right, bottom))
    img.save(output_path)
