import requests


class TurboSMSMessage:
    """
    Provides methods to interact with TurboSMS API.
    :param contract_num: number of a contract
    :param recipients: list of phone numbers, for whom the message will be sent
    """
    url = "https://api.turbosms.ua/message/send.json"

    def __init__(self, contract_num: str, recipients: list[str]):
        self.recipients = recipients
        self.json_data = {
            "recipients": recipients,
            "sms": {
                "sender": "KhClinic",
                "text": f"Ваш номер контракту: {contract_num}. Будь-ласка, зберігайте його в надійному місці!"
            }
        }

    def send(self):
        print(f"Sending SMS to numbers: {self.recipients}")
        response = requests.post(url=self.url,
                                 json=self.json_data,
                                 headers={"Authorization": "Bearer 188f6660a9d156cd3a9599a13bdfc9796925c3cf"})
        print(f"Status: {response.status_code}")
        return response.status_code
