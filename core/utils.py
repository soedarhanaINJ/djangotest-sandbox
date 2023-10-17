import os
import random
import string
from io import BufferedReader
from typing import List

from django.conf import settings


def get_random_words(length: int) -> str:
    letters = random.choices(string.ascii_lowercase, k=length)
    return "".join(letters)


def compose_words(texts: List[str]) -> str:
    if len(texts) == 1:
        return texts[0]
    if len(texts) == 2:
        return f"{texts[0]} dan {texts[1]}"

    front_words = texts[:-1]
    return f"{','.join(front_words)} dan {texts[-1]}"


def save_to_temp(data: BufferedReader, filename: str) -> str:
    filepath = os.path.join(settings.MEDIA_ROOT, "temp", filename)
    with open(filepath, "wb") as fp:
        fp.write(data)  # type:ignore
    return f"/media/temp/{filename}"
