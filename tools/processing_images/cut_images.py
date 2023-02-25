from PIL import Image
import sys
from pprint import pprint

sys.setrecursionlimit(1500)


def open_image(file_params: dict) -> Image:
    try:
        image = Image.open(file_params["full_path"])

        return image

    except FileNotFoundError:
        print(fr"файл {file_params['old_name']}.{file_params['format']}, по пути {file_params['full_name']} не найден")
        exit(0)


def save_image(image: Image, file_params: dict, format="PNG") -> None:
    # print(fr"{file_params['path']}\{file_params['new_name']}{file_params['part']}.{format.lower()}")
    image.save(fr"{file_params['path']}\{file_params['new_name']}{file_params['part']}.{format.lower()}", format)


def update_coord(elem: list, i: int, j: int) -> dict:
    now_elem = {"x": elem[0] + i, "y": elem[1] + j, "all": (elem[0] + i, elem[1] + j)}

    return now_elem


def get_rect(points: list) -> tuple:
    left = right = points[0][1]
    top = lower = points[0][0]

    for point in points:
        if point[1] < left:
            left = point[1]

        if point[1] > right:
            right = point[1]

        if point[0] < top:
            top = point[0]

        if point[0] > lower:
            lower = point[0]

    return left, top, right, lower


def get_points(queue: list, pointes: list, data, skep_elem: tuple, size) -> tuple:
    if queue:
        elem = queue.pop()
        for j in range(-1, 2, 1):
            for i in range(-1, 2, 1):
                now_elem = update_coord(elem, i, j)
                if (0 <= now_elem["x"] <= size[0] - 1) and 0 <= now_elem["y"] <= size[1] - 1 and (
                data[now_elem["x"], now_elem["y"]]) != skep_elem:
                    queue.append(now_elem["all"])
                    pointes.append(now_elem["all"])
                    data[now_elem["x"], now_elem["y"]] = skep_elem
        return get_points(queue, pointes, data, skep_elem, size)
    return pointes, data


def get_file_params(path: str) -> dict:
    path = path.split("\\")
    file_params = {
        "full_path": "\\".join(path),
        "path": "\\".join(path[:-1]),
        "old_name": path[-1].split(".")[0],
        "format": path[-1].split(".")[-1],
        "new_name": f"{path[-1].split('.')[0]}_cut",
        "part": 1
    }

    return file_params


def crop_photo(image: Image, rect: tuple, file_params) -> Image:
    rect = rect[1], rect[0], rect[3] + 1, rect[2] + 1
    print(rect)
    im_crop = image.crop(rect)

    save_image(im_crop, file_params=file_params)


def main(path) -> None:
    """вырезает из картинки определенные промежутки

    Args:
        path (_type_): полный путь до картинки
    """

    file_params = get_file_params(path)

    image = open_image(file_params=file_params)
    image_copy = image.copy()

    pixels = image_copy.load()
    x, y = image_copy.size

    skep_elem = pixels[0, 0]
    rects = []

    for i in range(x):
        for j in range(y):
            if pixels[i, j] != skep_elem:
                pixels[i, j] = skep_elem
                points, pixels = get_points([(i, j)], [(i, j)], pixels, skep_elem, size=(x, y))
                rects.append(points)

    for rect in rects:
        print(get_rect(rect))
        crop_photo(image, get_rect(rect), file_params)
        file_params["part"] += 1


if __name__ == "__main__":
    path = r"C:\Users\1\PycharmProjects\photo\change_photo\letter.png"
    file_params = get_file_params(path)
    main(path)
