import ast
import inspect
import pathlib
import re
import os

from pprint import pprint

from engine.core import Game

IGNORE = ("collector.py")


ENGINE_PATH = pathlib.Path(__file__).parent / "engine/"
PROJECT_PATH = pathlib.Path(__file__).parent / "asi/"
NEED_IMPORTS = []
IMPORTED = set()
CLASS_TO_PATH = dict()


def get_py_files(core_path) -> list[pathlib.Path]:
    py_files = []

    for path, dirs, files in os.walk(core_path):
        for file in files:
            if file != "__init__.py" and re.match(r".*\.py$", file):
                py_files.append(
                    pathlib.Path(path) / file
                )
    
    return py_files


def get_classes_from_file(filepath: pathlib.Path):
    if filepath.is_file() and filepath.name in IGNORE:
        return []

    with open(filepath, "rb") as file:
        data = file.read()
    
    parsed = ast.parse(data)
    
    classes = []
    
    for object_ in parsed.body:
        if isinstance(object_, (ast.ClassDef, ast.FunctionDef)):
            classes.append((object_.name, object_.lineno, object_.end_lineno))
    
    return classes


def parse_all_classes(core_path):
    py_files = get_py_files(core_path)
    
    classes_ = dict()

    for filepath in py_files:
        classes = get_classes_from_file(filepath)
        
        for class_, start_line, end_line in classes:
            classes_[class_] = {
                "path": filepath,
                "start_line": start_line,
                "end_line": end_line
            }
    
    return classes_
            

def parse_used_classes(class_name, code, classes):
    if class_name not in classes:
        return ""

    if class_name not in IMPORTED:
        with open(classes[class_name]["path"], "r") as file:
            lines = file.readlines()

            for line in range(classes[class_name]["start_line"] - 1, classes[class_name]["end_line"]):
                if lines[line].strip():
                    code += lines[line]

        IMPORTED.add(class_name)

    with open(classes[class_name]["path"], "r") as file:
        data = file.read()

    for object_ in ast.parse(data).body:
        if isinstance(object_, (ast.ImportFrom, ast.Import)):
            for name in object_.names:
                if name.name in classes and name.name not in IMPORTED:
                    code += parse_used_classes(name.name, code, classes)
                else:
                        NEED_IMPORTS.append(name.name)

            IMPORTED.add(name.name)

    return code


def all_write(classes):
    with open("project.py", "w") as project_file:
        for object_ in classes.items():
            path, start, end = object_[1]["path"], object_[1]["start_line"], object_[1]["end_line"]
            
            code = ""
            
            with open(path, "r") as file:
                code += "".join(file.readlines()[start - 1:end])
            
            project_file.write(code)

    return


def write(file_name, code):
    with open(file_name, "w") as file:
        for need_import in NEED_IMPORTS:
            file.write(f"import {need_import}\n")

        file.write(code)


def main():
    engine_classes = parse_all_classes(ENGINE_PATH)
    project_classes = parse_all_classes(PROJECT_PATH)

    all_classes = dict()
    
    all_classes.update(engine_classes)
    all_classes.update(project_classes)
    
    # print(all_classes.values())
    
    all_write(all_classes)

    # engine_code = parse_used_classes("Game", "", all_classes)
    # project_code = parse_used_classes("App", "", all_classes)
    
    # write("engine_code.py", engine_code)
    
    # write("project_code.py", project_code)

    
if __name__ == "__main__":
    main()
