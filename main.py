from fifth.exceptions import FifthInterpreterError
from fifth.interpreter import FifthInterpreter


if __name__ == "__main__":
    interpreter = FifthInterpreter()

    while (command := input("Enter Fifth command: ").upper()) != "EXIT":
        try:
            interpreter.interpret(command)

            # Print the stack as well, as a form of debug. Reaching into a 'private' variable here though.
            print(f"Stack is {interpreter._stack}")

        except FifthInterpreterError as e:
            print(f"ERROR: {e}")
