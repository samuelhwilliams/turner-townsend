import subprocess
import textwrap


class TestMain:
    def test_entrypoint(self):
        process = subprocess.Popen(
            ["python", "main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate(
            (
                "PUSH 3\n"
                + "PUSH 11\n"
                + "+\n"
                + "DUP\n"
                + "PUSH 2\n"
                + "*\n"
                + "SWAP\n"
                + "/\n"
                + "+\n"
                + "EXIT\n"
            ),
            timeout=2,
        )

        assert (
            stdout
            == """Enter Fifth command: Stack is [3]
Enter Fifth command: Stack is [3, 11]
Enter Fifth command: Stack is [14]
Enter Fifth command: Stack is [14, 14]
Enter Fifth command: Stack is [14, 14, 2]
Enter Fifth command: Stack is [14, 28]
Enter Fifth command: Stack is [28, 14]
Enter Fifth command: Stack is [2]
Enter Fifth command: ERROR: Stack size (1) below required size of 2
Enter Fifth command: """
        )
