import ast
import inspect
import os
import pathlib
import re

from typing import List

from core.game import Game


def collect(engine_game_instance: Game, app_file_path: str) -> None:
    if not isinstance(engine_game_instance, Game):
        raise ValueError("Экземпляр класса Game не был передан")
    
    project_path = pathlib.Path(app_file_path).parent
    engine_path = pathlib.Path(inspect.getfile(engine_game_instance.__class__)).parent.parent
    
    dirs = load_dirs_by_name(project_path, "resources")
    
    for dir in dirs:
        files = load_files_by_pattern(dir, r".*\.(png)")


def load_dirs_by_name(project_path: pathlib.Path, dir_name: str) -> List[pathlib.Path]:
    dirs_by_name = []

    for path, dirs, files in os.walk(project_path):
        if dir_name in dirs:
            dirs_by_name.append(
                pathlib.Path(path) / dir_name
            )
    
    return dirs_by_name


def load_files_by_pattern(directory: pathlib.Path, pattern: str) -> List[pathlib.Path]:
    file_dirs = []

    for path, dirs, files in os.walk(directory):
        for file in files:
            if re.match(pattern, file):
                file_dirs.append(
                    (pathlib.Path(path) / file)
                )

    return file_dirs


def main():
    path = inspect.getabsfile(Game)
    
    with open(path, "r") as file:
        code = file.read()
    
    res = ast.parse(code)
    ...


if __name__ == "__main__":
    main()
