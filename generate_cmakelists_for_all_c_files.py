import os
from pathlib import Path


root_directory = Path("..")
BLACKLISTED_PATHS = [
    Path(),
]
BLACKLISTED_DIRECTORY_NAMES = [
    ".git",
    "cmake-build-debug",
    "cmake-build-cygwin-debug",
]

project_name = root_directory.resolve().absolute().name
cmakelists_file_header = f"""cmake_minimum_required(VERSION 3.10)
project({project_name} C)

set(CMAKE_C_STANDARD 11)

# generated executables:
"""


def _find_c_source_files(directory: Path):
    for file in directory.iterdir():
        if file in BLACKLISTED_PATHS:
            continue
        if file.is_file():
            if file.name.endswith('.c'):
                yield file
        elif file.is_dir():
            if file.name not in BLACKLISTED_DIRECTORY_NAMES:
                yield from _find_c_source_files(file)


for cfile in _find_c_source_files(root_directory):
    print(cfile)
    file_relative_to_project_root = cfile.relative_to(root_directory)

    relative_source_file_path = "/".join(file_relative_to_project_root.parts)
    executable_name = "_".join(file_relative_to_project_root.parts)
    cmakelists_file_header += f"""add_executable("{executable_name}" "{relative_source_file_path}")\n"""

root_directory.joinpath("CMakeLists.txt").write_text(cmakelists_file_header, encoding="utf-8")
