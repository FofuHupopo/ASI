import os


class Resources:
    dirs = []

    @staticmethod
    def load():
        for rootdir, dirs, files in os.walk(os.getcwd()):
            if "resources" in dirs:
                Resources.dirs.append(rootdir + "/resources")

    @staticmethod
    def get(path: str):
        for resources_dir in Resources.dirs:
            fullname = os.path.join(resources_dir, path)

            if os.path.isfile(fullname):
                break
        else:
            raise FileNotFoundError(f"Файл по пути '{path}' не найден")

        return fullname


def hello():
    print("hi")
