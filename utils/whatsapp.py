import requests
from decouple import config

Token = config('INTERAKT_TOKEN')
Url = "https://api.interakt.ai/v1/public/track/events/"
UserCreateUrl = "https://api.interakt.ai/v1/public/track/users/"


def create_event():

    headers = {'Authorization': Token}

    myobj = {
        "phoneNumber": "9752157221",
        "countryCode": "+91",
        "event": "Reminder Campaign2",
        "traits": {
            "Customer": "abhishek",
            "Course": "singing",
            "Amount": "200",
            "DateOfPayment": "4 july",
            "PaymentLink": 	"https://payment.beyondaccounts.in/paynow/6789",
            "PromiseToPay": "https://beyondaccounts.in/promisetopay/9999",
            "CoachingName": "singer club",
            "Pay Now": "6789"
        }
    }

    x = requests.post(Url, json=myobj, headers=headers)

    print(x.text)


def create_user():
    headers = {'Authorization': Token}
    myobj = {
        "userId": "0123abc45d",
        "phoneNumber": "9752157221",
        "countryCode": "+91",
        "traits": {
            "name": "Gavin Roberts",
            "email": "gavinroberts01@outlook.com",
            "dob": "1996-12-01",
            "Sample trait a": "value y"
        }

    }
    x = requests.post(UserCreateUrl, json=myobj, headers=headers)
    print(x.text)
