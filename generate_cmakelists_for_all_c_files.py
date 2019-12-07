import os
from pathlib import Path

file_content = """cmake_minimum_required(VERSION 3.10)
project(esp_ku C)

set(CMAKE_C_STANDARD 11)

# generated executables:
"""

BLACKLISTED_DIRECTORY_NAMES = [
    ".git",
    "cmake-build-debug",
]


def _find_c_source_files(directory: Path):
    for file in directory.iterdir():
        if file.is_file():
            if file.name.endswith('.c'):
                yield file
        elif file.is_dir():
            if file.name not in BLACKLISTED_DIRECTORY_NAMES:
                yield from _find_c_source_files(file)


for cfile in _find_c_source_files(Path(".")):
    print(cfile)

    relative_source_file_path = "/".join(cfile.parts)
    executable_name = "_".join(cfile.parts)
    file_content += f"""add_executable("{executable_name}" "{relative_source_file_path}")\n"""

Path("CMakeLists.txt").write_text(file_content, encoding="utf-8")
