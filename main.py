import logging
import os
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict

from guess_number.guess_client import GuessClient
from guess_number.secret_number import SecretNumber

DEBUG = os.environ.get("DEBUG", "").lower() in ("1", "true", "on", "yes")

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)


def user_guess() -> None:
    secret_number = SecretNumber()

    while True:
        input_ = input("Number: ")

        try:
            result, is_finish = secret_number.is_(input_)
        except Exception as e:
            print(e)
            continue

        print(result)

        if is_finish:
            guess_count = secret_number.get_guess_count()
            print(f"Get it by guessing {guess_count} times.")
            break


def computer_guess() -> None:
    guess_client = GuessClient()

    while True:
        guess_number = guess_client.guess()
        input_ = input(f"{guess_number}: ")

        try:
            guess_client.guess_result(input_)
        except Exception as e:
            print(e)
            continue

        if guess_client.is_end:
            break


def auto_mode() -> int:
    secret_number = SecretNumber()
    guess_client = GuessClient()

    while True:
        input_ = guess_client.guess()
        result, is_finish = secret_number.is_(input_)

        logger.debug(f"{input_} -> {result}")

        if is_finish:
            return secret_number.get_guess_count()

        guess_client.guess_result(result)


def test_auto_mode(test_count: int = 100, worker_count: int = 10) -> None:
    test_info = []

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        results = [executor.submit(auto_mode) for _ in range(test_count)]

        for i, r in enumerate(as_completed(results), 1):
            test_info.append(r.result())
            print(f"Finish: {i}/{test_count}", end="\r")

        print()

    print("Max:", max(test_info))
    print("Min:", min(test_info))
    print("Avg:", sum(test_info) / len(test_info))


def main() -> Any:
    mode = "user"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    mode_mapping: Dict[str, Callable[..., Any]] = {
        "test": test_auto_mode,
        "user": user_guess,
        "auto": computer_guess,
    }

    return mode_mapping.get(mode, user_guess)()


if __name__ == "__main__":
    main()
