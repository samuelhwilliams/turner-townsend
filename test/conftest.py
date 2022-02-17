import pytest

from fifth.interpreter import FifthInterpreter


@pytest.fixture(scope="function")
def fifth_interpreter(request):
    """A fixture to provide a FifthInterpreter with a pre-defined stack.

    This could replace the following lines of setup in each of the interpreter tests:
        self.interpreter = FifthInterpreter()
        self.interpreter._stack = initial_stack

    However, the syntax for this is a little obscure and requires indirect parameterisation. So repetition may be preferable here.
    """
    interpreter = FifthInterpreter()

    interpreter._stack = request.param

    return interpreter
