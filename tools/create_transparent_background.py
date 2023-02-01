from PIL import Image


# сделать фон прозрачным или изменить какой-то цвет
def convert_image(path, name):
    image = Image.open(f"{path}\{name}")
    image = image.convert("RGBA")

    pixels = image.load()
    reverse_color = (0, 0, 0, 255)
    color_delete = (255, 255, 255, 255)

    x, y = image.size

    for i in range(x):
        for j in range(y):
            if pixels[i, j] == color_delete:
                pixels[i, j] = ((255, 255, 255, 0))

            elif pixels[i, j] == reverse_color:
                pixels[i, j] = (250, 250, 250, 255)

    image.save(f"{path}\\copy.png", "PNG")


if __name__ == "__main__":
    convert_image(r"C:\Users\1\PycharmProjects\different_tasks\menu_image", "sett.png")
