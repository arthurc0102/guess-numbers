import logging
import random

from typing import Dict, List, Tuple

NUMBER_LENGTH = 4


logger = logging.getLogger(__name__)


class SecretNumber:
    def __init__(self, length: int = NUMBER_LENGTH) -> None:
        self.length = length
        self._target_number: List[int] = self.generate()

        logger.debug(f"target_number -> {self.answer}")

        self.guess_list: List[Dict[str, List[int]]] = []

    @property
    def target_number(self) -> List[int]:
        return self._target_number

    @property
    def answer(self) -> str:
        return "".join(map(str, self.target_number))

    def generate(self) -> List[int]:
        return random.sample(range(10), self.length)

    def validate(self, number: str) -> List[int]:
        assert number.isdigit(), "This is not a number."
        assert len(number) == self.length, f"Input should be {self.length}."
        assert len(set(number)) == self.length, "Number can't be repeated."
        return list(map(int, number))

    def get_last_result(self) -> str:
        assert len(self.guess_list) >= 1, "No item in guess list."
        return "{}A{}B".format(*self.guess_list[-1]["result"])

    def get_guess_count(self) -> int:
        return len(self.guess_list)

    def is_(self, user_input: str) -> Tuple[str, bool]:
        logger.debug(f"user_input -> {user_input}")
        guess_number = self.validate(user_input)

        a = b = 0
        for i, j in zip(guess_number, self.target_number):
            if i == j:
                a += 1
            elif i in self.target_number:
                b += 1

        self.guess_list.append({"number": guess_number, "result": [a, b]})
        return self.get_last_result(), a == 4 and b == 0
