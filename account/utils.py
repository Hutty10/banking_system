import random
import string

from django.conf import settings


class Utils:
    @staticmethod
    def generate_account_no() -> str:
        acc_no = settings.ACCOUNT_NUMBER_START_FROM + "".join(
            random.choice(string.digits) for _ in range(7)
        )
        return acc_no
