from argparse import FileType
import contextlib
import pytest
from fifth.exceptions import FifthInterpreterError
from fifth.interpreter import FifthInterpreter, _check_stack_has_at_least_n_elements


class TestDecorators:
    @pytest.mark.parametrize(
        ["insert_n_elements", "require_n_elements", "should_error"],
        (
            (0, 0, False),
            (0, 1, True),
            (1, 1, False),
            (2, 1, False),
            (2, 3, True),
        ),
    )
    def test_check_stack_has_at_least_n_elements(
        self, insert_n_elements, require_n_elements, should_error
    ):
        class _Stack:
            def __init__(self):
                self._stack = []

            @_check_stack_has_at_least_n_elements(require_n_elements)
            def noop(self):
                pass

            def push(self, val):
                self._stack.append(val)

        stack = _Stack()

        for x in range(insert_n_elements):
            stack.push(1)

        if should_error:
            with pytest.raises(FifthInterpreterError) as e:
                stack.noop()

        else:
            stack.noop()

    def test_check_stack_has_at_least_n_elements_error_message(self):
        class _Stack:
            def __init__(self):
                self._stack = []

            @_check_stack_has_at_least_n_elements(1)
            def noop(self):
                pass

        stack = _Stack()

        with pytest.raises(FifthInterpreterError) as e:
            stack.noop()

        assert (
            str(e.value)
            == f"Stack size ({len(stack._stack)}) below required size of {1}"
        )


class TestFifthInterpreter:
    @pytest.mark.parametrize(
        "initial_stack, expected_result",
        (
            ([1, 2], 3),
            ([0, 2], 2),
            ([3, 5], 8),
        ),
    )
    def test_add(self, initial_stack, expected_result):
        self.interpreter = FifthInterpreter()
        self.interpreter._stack = initial_stack

        self.interpreter.add()
        assert self.interpreter._stack[-1] == expected_result

    def test_add_stack_fewer_than_2_elements(self):
        self.interpreter = FifthInterpreter()

        with pytest.raises(FifthInterpreterError) as e:
            self.interpreter.add()

        assert str(e.value) == "Stack size (0) below required size of 2"

    @pytest.mark.parametrize(
        "initial_stack, expected_result",
        (
            ([1, 2], -1),
            ([0, 2], -2),
            ([5, 3], 2),
        ),
    )
    def test_subtract(self, initial_stack, expected_result):
        self.interpreter = FifthInterpreter()
        self.interpreter._stack = initial_stack

        self.interpreter.subtract()
        assert self.interpreter._stack[-1] == expected_result

    def test_subtract_stack_fewer_than_2_elements(self):
        self.interpreter = FifthInterpreter()

        with pytest.raises(FifthInterpreterError) as e:
            self.interpreter.subtract()

        assert str(e.value) == "Stack size (0) below required size of 2"

    @pytest.mark.parametrize(
        "initial_stack, expected_result",
        (
            ([1, 2], 2),
            ([0, 2], 0),
            ([5, 3], 15),
        ),
    )
    def test_multiply(self, initial_stack, expected_result):
        self.interpreter = FifthInterpreter()
        self.interpreter._stack = initial_stack

        self.interpreter.multiply()
        assert self.interpreter._stack[-1] == expected_result

    def test_multiply_stack_fewer_than_2_elements(self):
        self.interpreter = FifthInterpreter()

        with pytest.raises(FifthInterpreterError) as e:
            self.interpreter.multiply()

        assert str(e.value) == "Stack size (0) below required size of 2"

    @pytest.mark.parametrize(
        "initial_stack, expected_result",
        (
            ([1, 2], 0),
            ([0, 2], 0),
            ([5, 3], 1),
            ([8, 2], 4),
        ),
    )
    def test_divide(self, initial_stack, expected_result):
        self.interpreter = FifthInterpreter()
        self.interpreter._stack = initial_stack

        self.interpreter.divide()
        assert self.interpreter._stack[-1] == expected_result

    def test_divide_stack_fewer_than_2_elements(self):
        self.interpreter = FifthInterpreter()

        with pytest.raises(FifthInterpreterError) as e:
            self.interpreter.divide()

        assert str(e.value) == "Stack size (0) below required size of 2"

    @pytest.mark.parametrize(
        "initial_stack, value, expected_result",
        (
            ([], "0", [0]),
            ([], "1", [1]),
            ([1], "2", [1, 2]),
        ),
    )
    def test_push(self, initial_stack, value, expected_result):
        self.interpreter = FifthInterpreter()
        self.interpreter._stack = initial_stack

        self.interpreter.push(value)
        assert self.interpreter._stack == expected_result

    def test_push_non_numeric(self):
        self.interpreter = FifthInterpreter()

        with pytest.raises(FifthInterpreterError) as e:
            self.interpreter.push("abc")

        assert (
            str(e.value)
            == f"PUSH command requires an integer value argument, got `abc`"
        )

    @pytest.mark.parametrize(
        "initial_stack, expected_stack",
        (
            ([0], []),
            ([0, 1], [0]),
            ([1, 2, 3], [1, 2]),
        ),
    )
    def test_pop(self, initial_stack, expected_stack):
        self.interpreter = FifthInterpreter()
        self.interpreter._stack = initial_stack

        self.interpreter.pop()

        assert self.interpreter._stack == expected_stack

    def test_pop_empty_stack(self):
        self.interpreter = FifthInterpreter()

        with pytest.raises(FifthInterpreterError) as e:
            self.interpreter.pop()

        assert str(e.value) == "Stack size (0) below required size of 1"

    @pytest.mark.parametrize(
        "initial_stack, expected_stack",
        (
            ([0, 1], [1, 0]),
            ([1, 2, 3], [1, 3, 2]),
        ),
    )
    def test_swap(self, initial_stack, expected_stack):
        self.interpreter = FifthInterpreter()
        self.interpreter._stack = initial_stack

        self.interpreter.swap()

        assert self.interpreter._stack == expected_stack

    def test_swap_stack_fewer_than_2_elements(self):
        self.interpreter = FifthInterpreter()

        with pytest.raises(FifthInterpreterError) as e:
            self.interpreter.swap()

        assert str(e.value) == "Stack size (0) below required size of 2"

        self.interpreter.push("1")
        with pytest.raises(FifthInterpreterError) as e:
            self.interpreter.swap()

        assert str(e.value) == "Stack size (1) below required size of 2"

    @pytest.mark.parametrize(
        "initial_stack, expected_stack",
        (
            ([0], [0, 0]),
            ([1, 2], [1, 2, 2]),
        ),
    )
    def test_duplicate(self, initial_stack, expected_stack):
        self.interpreter = FifthInterpreter()
        self.interpreter._stack = initial_stack

        self.interpreter.duplicate()

        assert self.interpreter._stack == expected_stack

    def test_duplicate_empty_stack(self):
        self.interpreter = FifthInterpreter()

        with pytest.raises(FifthInterpreterError) as e:
            self.interpreter.duplicate()

        assert str(e.value) == "Stack size (0) below required size of 1"
