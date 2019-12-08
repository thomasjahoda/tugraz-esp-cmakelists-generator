import os
import sys
from pathlib import Path

from fabric import Connection

if len(sys.argv) != 2:
    print("provide the assignment name for which to execute the tests")
    exit(2)
assignment_directory_name = sys.argv[1]

project_root_directory = Path("..")
absolute_project_root_directory = project_root_directory.resolve().absolute()
assignment_directory = absolute_project_root_directory.joinpath(assignment_directory_name)
assert assignment_directory.is_dir()

wsl_path_for_project_root_directory_on_windows_path_str = "/mnt/c/" + (
    "/".join(absolute_project_root_directory.parts[1:]))
wsl_path_for_assignment_directory_on_windows = Path("/mnt").joinpath(assignment_directory)
wsl_path_for_assignment_directory_on_windows_path_str = "/mnt/c/" + (
    "/".join(wsl_path_for_assignment_directory_on_windows.parts[1:]))
# SubProcessExecution.execute(["ssh", "tjahoda@localhost"],
#                             follow_output=True,
#                             custom_input=f"""echo test""")

test_execution_base_directory = "~/test_execution"
test_execution_assignment_directory = f"{test_execution_base_directory}/{assignment_directory_name}"
print("Executing SSH commands:")
print(wsl_path_for_assignment_directory_on_windows_path_str)
print(test_execution_base_directory)

results_json_file = absolute_project_root_directory.joinpath("results.json")
report_html_file = absolute_project_root_directory.joinpath("report.html")
results_json_file.unlink(missing_ok=True)
report_html_file.unlink(missing_ok=True)

ssh_connection = Connection('tjahoda@localhost')
ssh_connection.run("""echo "=== START OF WSL-SIDE COMMANDS/OUTPUT ===" """)
ssh_connection.run(f"""mkdir {test_execution_base_directory}""", warn=True)
ssh_connection.run(f"""rsync -r {wsl_path_for_assignment_directory_on_windows_path_str} {test_execution_base_directory}""")
try:
    ssh_connection.run(f"""cd {test_execution_assignment_directory} && make test""", warn=True)
finally:
    ssh_connection.run(f"""cp {test_execution_assignment_directory}/testscripts/results/* {wsl_path_for_project_root_directory_on_windows_path_str}/""")
ssh_connection.run("""echo "=== END OF WSL-SIDE COMMANDS/OUTPUT ===" """)


if report_html_file.exists():
    print("Executed tests successfully.")
    print(f"Opening {report_html_file.name}")
    os.startfile(str(report_html_file))
else:
    print("Something went wrong. Check logs.")
    exit(1)
