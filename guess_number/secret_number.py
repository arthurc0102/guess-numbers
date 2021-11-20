import logging
import random
import string

from typing import Any, Dict, List, Tuple

NUMBER_LENGTH = 4


logger = logging.getLogger(__name__)


class SecretNumber:
    def __init__(self, length: int = NUMBER_LENGTH) -> None:
        self.length = length
        self._answer = self.generate()

        logger.debug(f"target_number -> {self.answer}")

        self.guess_list: List[Dict[str, Any]] = []

    def _compare_answer(self, guess_number: str, answer_number: str) -> Tuple[int, int]:
        a = b = 0

        for i, j in zip(guess_number, answer_number):
            if i == j:
                a += 1
            elif i in answer_number:
                b += 1

        return a, b

    @property
    def answer(self) -> str:
        return self._answer

    def generate(self) -> str:
        return "".join(random.sample(string.digits, self.length))

    def validate(self, number: str) -> str:
        assert number.isdigit(), "This is not a number."
        assert len(number) == self.length, f"Input should be {self.length}."
        assert len(set(number)) == self.length, "Number can't be repeated."

        return number

    def get_last_result(self) -> str:
        assert len(self.guess_list) >= 1, "No item in guess list."
        return "{}A{}B".format(*self.guess_list[-1]["result"])

    def get_guess_count(self) -> int:
        return len(self.guess_list)

    def is_(self, user_input: str) -> Tuple[str, bool]:
        logger.debug(f"user_input -> {user_input}")
        guess_number = self.validate(user_input)

        a, b = self._compare_answer(guess_number, self._answer)
        self.guess_list.append({"number": guess_number, "result": [a, b]})

        return self.get_last_result(), a == 4 and b == 0
