import os
from dotenv import load_dotenv
from twilio.rest import Client

dotpath = "../regclinic/vars.env"
load_dotenv(dotpath)

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
verify_sid = os.getenv("VERIFY_SID")

client = Client(account_sid, auth_token)


def send_verification_code(verified_number: str) -> None:
    verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")
    print(verification.status)


def check_verification_code(verified_number: str, otp_code: str) -> bool:
    verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp_code)
    print(verification_check.status)
    return verification_check.status == "approved"

