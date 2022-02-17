import functools
import math

from fifth.exceptions import FifthInterpreterError


def _check_stack_has_at_least_n_elements(size):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            if len(self._stack) < size:
                raise FifthInterpreterError(
                    f"Stack size ({len(self._stack)}) below required size of {size}"
                )

            return fn(self, *args, **kwargs)

        return wrapper

    return decorator


class FifthInterpreter:
    def __init__(self):
        self._stack = []

    @_check_stack_has_at_least_n_elements(2)
    def add(self):
        first, second = self._stack.pop(), self._stack.pop()
        result = first + second
        self._stack.append(result)

    @_check_stack_has_at_least_n_elements(2)
    def subtract(self):
        first, second = self._stack.pop(), self._stack.pop()
        result = second - first
        self._stack.append(result)

    @_check_stack_has_at_least_n_elements(2)
    def multiply(self):
        first, second = self._stack.pop(), self._stack.pop()
        result = first * second
        self._stack.append(result)

    @_check_stack_has_at_least_n_elements(2)
    def divide(self):
        first, second = self._stack.pop(), self._stack.pop()
        result = math.floor(second / first)
        self._stack.append(result)

    def push(self, val: str):
        if not val.isnumeric():
            raise FifthInterpreterError(
                f"PUSH command requires an integer value argument, got `{val}`"
            )

        normalised_val = int(val)

        self._stack.append(normalised_val)

    @_check_stack_has_at_least_n_elements(1)
    def pop(self):
        self._stack.pop()

    @_check_stack_has_at_least_n_elements(2)
    def swap(self):
        first, second = self._stack.pop(), self._stack.pop()
        self._stack.append(first)
        self._stack.append(second)

    @_check_stack_has_at_least_n_elements(1)
    def duplicate(self):
        self._stack.append(self._stack[-1])

    def interpret(self, command):
        normalised_command = command.strip().lower()
        args = normalised_command.split()

        match args:
            case ["+"]:
                self.add()
            case ["-"]:
                self.subtract()
            case ["*"]:
                self.multiply()
            case ["/"]:
                self.divide()
            case ["push", x]:
                self.push(x)
            case ["pop"]:
                self.pop()
            case ["swap"]:
                self.swap()
            case ["dup"]:
                self.duplicate()
            case _:
                raise FifthInterpreterError(
                    f"Unknown command: {command} (interpreted as: {args})"
                )
