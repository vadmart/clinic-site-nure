from random import randint
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class DoctorChat(models.Model):
    lastname = models.CharField(max_length=30)
    name = models.CharField(max_length=15)
    patronymic = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.lastname} {self.name} {self.patronymic}"

    def create_new(self):
        ...


class ContractStatus(models.Model):
    status_name = models.CharField(max_length=6)

    def __str__(self):
        return self.status_name


class ContractInfo(models.Model):
    person_lastname = models.CharField(max_length=30)
    person_firstname = models.CharField(max_length=15)
    contract_num = models.CharField(max_length=10)
    person_chat_id = models.BigIntegerField()
    doctor_chat = models.ForeignKey(DoctorChat, on_delete=models.CASCADE)
    person_number = PhoneNumberField()
    post_index = models.CharField(max_length=5)
    street_type = models.CharField(max_length=10)
    street_name = models.CharField(max_length=40)
    house_number = models.CharField(max_length=4)
    flat_number = models.CharField(max_length=4)
    status = models.ForeignKey(ContractStatus, null=True, on_delete=models.SET_NULL)
    sign_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return f"Person: {self.person_lastname} {self.person_firstname}, contract number: {self.contract_num}"

    @staticmethod
    def __get_rand() -> str:
        res = ""
        for _ in range(10):
            res += str(randint(0, 9))
        return res

    def create_new(self, data: dict):
        """
        Adds new info to a ContractInfo object with a dictionary, returning this one.
        """
        self.person_lastname = data["person_lastname"]
        self.person_firstname = data["person_name"]
        self.person_number = data["person_phone_number"]
        self.contract_num = self.__get_rand()
        self.person_chat_id = data["person_chat_id"]
        self.street_type = data["street_type"]
        self.street_name = data["street_name"]
        self.house_number = data["house_number"]
        self.flat_number = data["flat_no"]
        self.post_index = data["post_index"]

        try:
            self.doctor_chat = DoctorChat.objects.get(id=data["doctor_chat_id"])
        except DoctorChat.DoesNotExist:
            doctor_lastname, doctor_firstname, doctor_patronymic = data["doctor_lfp"].split()
            self.doctor_chat = DoctorChat.objects.create(id=data["doctor_chat_id"],
                                                         lastname=doctor_lastname,
                                                         name=doctor_firstname,
                                                         patronymic=doctor_patronymic)
            self.doctor_chat.save()

        self.status = ContractStatus.objects.get(status_name=data["status"])
        self.save(force_insert=True)
        return self
