import sys

from fabric import Connection
from invoke import UnexpectedExit

if len(sys.argv) != 2:
    print("usage: [SSH connection string]")
    print("eg: tjahoda@localhost:2222")
    exit(2)
ssh_connection_string = sys.argv[1]

ssh_connection = Connection(ssh_connection_string)
ssh_connection.run('echo "=== START OF WSL-SIDE COMMANDS/OUTPUT ==="')
try:
    ssh_connection.run('sudo echo sudotest')
except UnexpectedExit as e:
    raise Exception("please configure passwordless sudo (is effort, is big no-no)"
                    " or copy the SSH commands from the code manually (recommended)") from e
ssh_connection.run('sudo apt update')
ssh_connection.run('sudo apt install clang make xclip git ctags valgrind python3 python3-pip -y')
ssh_connection.run('sudo pip3 install --upgrade pexpect pyaml diff-match-patch')
ssh_connection.run("""echo "=== END OF WSL-SIDE COMMANDS/OUTPUT ===" """)
