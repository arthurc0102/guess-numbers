import re
import string

from itertools import permutations
from typing import Dict, Optional, Set, Tuple

NUMBER_LENGTH = 4


class GuessClient:
    def __init__(self, length: int = NUMBER_LENGTH) -> None:
        self.length = length
        self.possible_answers = self._build_possible_answers()

        self.is_end = False
        self.guess_number: Optional[str] = None
        self.guess_history: Dict[str, Tuple[int, int]] = {}

    def _compare_answer(self, guess_number: str, answer_number: str) -> Tuple[int, int]:
        a = b = 0

        for i, j in zip(guess_number, answer_number):
            if i == j:
                a += 1
            elif i in answer_number:
                b += 1

        return a, b

    def _build_possible_answers(self) -> Set[str]:
        permutations_ = permutations(string.digits, self.length)
        return set(["".join(n) for n in permutations_])

    def _get_not_possible_answers(
        self,
        a: int,
        b: int,
        guess_number: Optional[str] = None,
        possible_answers: Optional[Set[str]] = None,
    ) -> Set[str]:
        assert self.guess_number is not None, "Not guess yet."

        guess_number = guess_number or self.guess_number
        possible_answers = possible_answers or self.possible_answers

        not_possible_answers = set()
        for possible_answer in possible_answers:
            compare_result = self._compare_answer(guess_number, possible_answer)
            if (a, b) == compare_result:
                continue

            not_possible_answers.add(possible_answer)

        return not_possible_answers

    def _suggest_guess_number(self, possible_answers: Optional[Set[str]] = None) -> str:
        possible_answers = possible_answers or self.possible_answers

        assert len(possible_answers) > 0, "No possible answers."

        if self.guess_number is None or len(possible_answers) > 100:
            return list(possible_answers)[0]

        guess_exclude_mapping = {}
        for guess_number in possible_answers:
            exclude_count = 0

            for answer_number in possible_answers:
                a, b = self._compare_answer(guess_number, answer_number)
                not_possible_answers = self._get_not_possible_answers(
                    a,
                    b,
                    guess_number,
                    possible_answers,
                )
                exclude_count += len(not_possible_answers)

            guess_exclude_mapping[guess_number] = exclude_count

        return max(guess_exclude_mapping.items(), key=lambda x: x[1])[0]

    def validate(self, result: str) -> Tuple[int, int]:
        pattern = re.compile(r"(?P<A>\d+)A(?P<B>\d+)B", re.I)

        matched = pattern.match(result)
        assert matched is not None, "Result not valid."

        a_str, b_str = matched.groups()
        assert a_str.isdigit() and b_str.isdigit(), "Result not valid, not number."

        a, b = int(a_str), int(b_str)
        assert a + b <= self.length, "Result not valid, a + b bigger than length"

        return a, b

    def guess(self) -> str:
        assert not self.is_end, "Game has ended."

        if not self.guess_history:
            self.guess_number = list(self.possible_answers)[0]
        else:
            self.guess_number = self._suggest_guess_number()

        return self.guess_number

    def guess_result(self, result: str) -> None:
        assert self.guess_number is not None, "Not guess yet."

        a, b = self.validate(result)
        self.guess_history[self.guess_number] = (a, b)

        self.is_end = a == self.length
        self.possible_answers -= self._get_not_possible_answers(a, b)
