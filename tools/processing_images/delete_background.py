from PIL import Image


def open_image(name: str, format="RGBA"):
    """open image and covert in RGBA"""
    image = Image.open(f"photos\{name}")
    image = image.convert(format)
    return image


def image_save(image, name: str, format="PNG") -> None:
    """save image - defoult and true fomat PNG"""
    image.save(f"new_photos\{name}.{format.lower()}", format)
    print(f"{name}.{format.lower()}")


def convert_image(name: str, alpha_color=None):
    file = {
        "full_name": name,
        "name": name.split(".")[0],
        "format": name.split(".")[1]
    }
    image = open_image(file["full_name"])

    pixels = image.load()  # список с пикселями
    x, y = image.size  # ширина (x) и высота (y) изображения

    alpha_color = alpha_color if alpha_color else (255, 255, 255, 0)

    for i in range(x):
        for j in range(y):
            r, g, b, a = pixels[i, j]
            if int(alpha_color[0] * 0.9) <= r <= int(alpha_color[0] * 1.1) and int(alpha_color[1] * 0.9) <= g <= int(alpha_color[1] * 1.1) and int(alpha_color[2] * 0.9) <= b <= int(alpha_color[2] * 1.1):
                pixels[i, j] = (255, 255, 255, 0)

    image_save(image, file["name"] + "_new")


all_images = ("Дима.png", )
print(len(all_images))

for name in all_images:
    convert_image(name)
