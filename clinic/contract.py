from clinic.models import Patient
from random import randrange


def get_rand_contract_num() -> str:
    """
    Return a new contract number, checking if it's not in the database
    """
    contract_nums = Patient.objects.values("contract_num")
    contract_num = ""
    while True:
        for _ in range(10):
            contract_num += str(randrange(10))
        if contract_num not in contract_nums:
            return contract_num
