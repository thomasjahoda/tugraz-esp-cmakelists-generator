import os
import shutil
import sys
from pathlib import Path

from fabric import Connection

if len(sys.argv) != 3:
    print("usage: [assignment directory name] [SSH connection string]")
    print("eg: assignment_b1_594 tjahoda@localhost:2222")
    exit(2)
assignment_directory_name = sys.argv[1]
ssh_connection_string = sys.argv[2]

project_root_directory = Path("..")
absolute_project_root_directory = project_root_directory.resolve().absolute()
assignment_directory = absolute_project_root_directory.joinpath(assignment_directory_name)
assert assignment_directory.is_dir()

wsl_path_for_project_root_directory_on_windows_path_str = "/mnt/c/" + (
    "/".join(absolute_project_root_directory.parts[1:]))
wsl_path_for_assignment_directory_on_windows = Path("/mnt").joinpath(assignment_directory)
wsl_path_for_assignment_directory_on_windows_path_str = "/mnt/c/" + (
    "/".join(wsl_path_for_assignment_directory_on_windows.parts[1:]))

test_execution_base_directory_str = "~/test_execution"
test_execution_assignment_directory_str = f"{test_execution_base_directory_str}/{assignment_directory_name}"
print("Executing SSH commands:")
print(wsl_path_for_assignment_directory_on_windows_path_str)
print(test_execution_base_directory_str)

results_json_file = assignment_directory.joinpath("testscripts/results/results.json")
report_html_file = assignment_directory.joinpath("testscripts/results/report.html")
results_json_file.unlink(missing_ok=True)
report_html_file.unlink(missing_ok=True)


def delete_contents(directory: Path):
    for file in directory.iterdir():
        if file.name == '.gitkeep':
            continue
        if file.is_dir():
            shutil.rmtree(file)
        else:
            file.unlink()


ssh_connection = Connection(ssh_connection_string)
ssh_connection.run('echo "=== START OF WSL-SIDE COMMANDS/OUTPUT ==="')
ssh_connection.run(f"""mkdir {test_execution_base_directory_str}""", warn=True)
ssh_connection.run(f'rsync -r {wsl_path_for_assignment_directory_on_windows_path_str} {test_execution_base_directory_str}')
try:
    ssh_connection.run(f"""cd {test_execution_assignment_directory_str} && make test""", warn=True)
finally:
    delete_contents(assignment_directory.joinpath("testscripts/tmp"))
    ssh_connection.run(
        f"""cp {test_execution_assignment_directory_str}/testscripts/results/* "{wsl_path_for_assignment_directory_on_windows_path_str}/testscripts/results/" """)
    ssh_connection.run(
        f"""cp -r {test_execution_assignment_directory_str}/testscripts/tmp/* "{wsl_path_for_assignment_directory_on_windows_path_str}/testscripts/tmp/" """)
ssh_connection.run("""echo "=== END OF WSL-SIDE COMMANDS/OUTPUT ===" """)

if report_html_file.exists():
    print("Executed tests successfully.")
    print(f"Opening {report_html_file.name}")
    os.startfile(str(report_html_file))
else:
    print("Something went wrong. Check logs.")
    exit(1)
