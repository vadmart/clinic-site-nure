from clinic.configs.сonfig import API_TOKEN, DOCTOR_CHAT_ID
from clinic.models import Person, Doctor, Recording
from bot.models import DoctorChat, ContractInfo, ContractStatus
import telebot
import io
import time
from telebot import formatting
from telebot.util import quick_markup
from telebot import types
from threading import Thread
from datetime import datetime

bot = telebot.TeleBot(API_TOKEN)
contracts_info: list[dict] = list()


def is_num_in_contracts_info(num: str) -> bool:
    for contract in contracts_info:
        if num == contract["person_phone_number"]:
            return True
    return False


def send_msg_about_recording_to_doctor(person: Person,
                                       doctor: Doctor,
                                       recording: Recording):
    """
    Sends info about patient's recording to doctor

    Parameters:
        person (Person): Object of class Person
        doctor (Doctor): Object of class Doctor
        recording (Recording): Object of class Recording

    """
    doctor_chat_id = DOCTOR_CHAT_ID[f"{doctor.lastname} {doctor.name} {doctor.patronymic}"]
    bot.send_message(doctor_chat_id,
                     formatting.format_text(f"Особа " + formatting.hitalic(f"{person.lastname} {person.name}") +
                                            " записана на прийом\n" +
                                            f"Дата: {recording.datetime.date().strftime('%d.%m.%Y')}, " +
                                            f"час: {recording.datetime.time().strftime('%H:%M')}\n" +
                                            "Скарга на здоров'я:", formatting.hitalic(
                         f'"{recording.health_complaint}"')), parse_mode="HTML")


def send_msg_about_contract_to_doctor(form_dict: dict):
    """
    Sends message about person's attempt of concluding the contract with doctor
    Parameters:
        form_dict (dict): dictionary, in which every key has a value of filled field
    """
    doctor_lastname, doctor_firstname, doctor_patronymic = form_dict["doctor_lfp"].split()
    doctor_chat_id = DOCTOR_CHAT_ID[f"{doctor_lastname} {doctor_firstname} {doctor_patronymic}"]
    # try:
    #     dc = DoctorChat.objects.get(id=doctor_chat_id)
    # except DoctorChat.DoesNotExist:
    #     dc = DoctorChat.objects.create(id=doctor_chat_id,
    #                                    lastname=doctor_lastname,
    #                                    name=doctor_firstname,
    #                                    patronymic=doctor_patronymic)
    #     dc.save()
    form_dict["doctor_chat_id"] = doctor_chat_id
    form_dict["sent_at"] = datetime.now()
    form_dict["status"] = "none"
    contracts_info.append(form_dict)
    # ContractInfo().create_new(data=form_dict)
    markup = quick_markup(
        {
            "Підтвердити": {"callback_data": f"{form_dict['person_phone_number']} accept"},
            "Відхилити": {"callback_data": f"{form_dict['person_phone_number']} reject"}})
    bot.send_message(doctor_chat_id,
                     formatting.format_text(
                         f"Особа " + formatting.hitalic(
                             f"{form_dict['person_lastname']} {form_dict['person_name']}") +
                         f", адреса проживання: " + \
                         formatting.hitalic(
                             f"{form_dict['street_type']}. {form_dict['street_name']}, {form_dict['house_number']}") +
                         ", номер телефону: " + formatting.hitalic(
                             f"{form_dict['person_phone_number']}") + " бажає заключити з Вами контракт.\n" +
                         "Чи бажаєте Ви підтвердити дану операцію?"), parse_mode="HTML",
                     reply_markup=markup)


@bot.message_handler(commands=["start"])
def user_start(msg):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_number = types.KeyboardButton("Відправити номер телефону", request_contact=True)
    kb.add(btn_number)
    bot.send_message(msg.chat.id, "Вітаємо!\nДля подальшого узгодження інформації щодо стану контракту Вам необхідно" +
                     " надати доступ до Вашого номеру телефона",
                     reply_markup=kb)


@bot.message_handler(content_types=["contact"])
def add_chat_id_to_user_contract(msg) -> None:
    for contract in contracts_info:
        if contract["person_phone_number"] == msg.contact.phone_number:
            contract["person_chat_id"] = msg.chat.id
            ci = ContractInfo().create_new(contract)
            send_contract_status(ci)
            return
    else:
        bot.send_message(text="Ваш номер не знайдено у списку контрактів!", chat_id=msg.chat.id)


def send_contract_status(contract: ContractInfo):
    if contract.status.status_name == "none":
        bot.send_message(chat_id=contract.person_chat_id,
                         text="Контракт за Вашим номером на даний момент розглядається")
    elif contract.status.status_name == "reject":
        bot.send_message(chat_id=contract.person_chat_id,
                         text="Контракт за Вашим номером відхилено. Зв'яжіться, будь-ласка, із нашим менеджером:\n+380661686484")
    else:
        bot.send_message(chat_id=contract.person_chat_id,
                         text="Контракт за Вашим номер підтверджено.")
        contract.sign_datetime = datetime.now()
        _send_contract_to_patient(contract)


@bot.callback_query_handler(func=lambda call: True)
def set_contract_status(call):
    phone_number, status_name = call.data.split()
    if ContractInfo.objects.filter(person_number=phone_number):
        contract = ContractInfo.objects.get(person_number=phone_number)
        contract.status = ContractStatus.objects.get(status_name=status_name)
        contract.save()
        bot.delete_message(call.message.chat.id, call.message.id)
        send_contract_status(contract)
    else:
        contract = next(filter(lambda dct: dct["person_phone_number"] == phone_number, contracts_info))
        contract["status"] = status_name
        pass


def _send_contract_to_patient(contract: ContractInfo):
    doctor_lfp = contract.doctor_chat.lastname + " " + contract.doctor_chat.name + " " + contract.doctor_chat.patronymic
    person_lf = contract.person_lastname + " " + contract.person_firstname
    addr = f"{contract.street_type} {contract.street_name}, {contract.house_number}"
    with open("contract_doc/contract.txt") as file_out:
        text = file_out.read().replace("*doctor_lfp*", doctor_lfp) \
            .replace("*person_lf*", person_lf) \
            .replace("*address*", addr) \
            .replace("*person_number*", str(contract.person_number)) \
            .replace("*post_index*", contract.post_index) \
            .replace("*date*", contract.sign_datetime.strftime("%d.%m.%Y"))
        with io.StringIO() as file:
            file.name = "contract.txt"
            file.write(text)
            file.seek(0)
            bot.send_document(contract.person_chat_id, file)
            Person().add_info(contract)


def check_contracts_datetime():
    while True:
        for contract in contracts_info:
            if (datetime.now() - contract["sent_at"]).seconds > 10:
                del contract
        time.sleep(10)


Thread(target=check_contracts_datetime, name="contract_checker").start()
Thread(target=bot.infinity_polling, name="bot_thread").start()
