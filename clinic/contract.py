from clinic.models import Patient
from random import randrange


def get_rand_contract_num():
    """
    Return a new contract number, checking if it's not in the database
    """
    contract_num = ""
    for _ in range(10):
        contract_num += str(randrange(10))
