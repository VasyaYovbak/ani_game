import requests
from PIL import Image


def create_one_row_collage(df, one_img_size: int = 150):
    number_of_img: int = len(df.index)

    collage_width: int = number_of_img * one_img_size

    collage = Image.new("RGB", (collage_width, one_img_size), color=(255, 255, 255))
    i = 0
    for x in range(0, number_of_img * one_img_size + 1, one_img_size):
        image = df['image'].iloc[[i]]
        image = image.to_string(header=False, index=False)
        im = Image.open(requests.get(image, stream=True).raw)
        rgb_im = im.convert('RGB')
        photo = rgb_im.resize((150, 150))
        collage.paste(photo, (x, 0))
        print(i)
        if i >= number_of_img - 1:
            return collage
        i += 1


def create_optimal_square_collage(df, one_img_size: int = 150):
    pass
