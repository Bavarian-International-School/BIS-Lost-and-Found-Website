from typing import Dict, List

import requests


class PostMaster:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.mailjet_api = "https://api.mailjet.com/v3.1/send"

    def send_email(
        self, from_email: str, to_emails: List[str], subject: str, text: str
    ) -> Dict[str, Dict[str, List[Dict]]]:
        """
        Sends an email to a specified address
        """

        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "Messages": [
                {
                    "From": {
                        "Email": from_email,
                    },
                    "To": [{"Email": email} for email in to_emails],
                    "Subject": subject,
                    "TextPart": text,
                },
            ],
        }

        response = requests.post(
            self.mailjet_api,
            headers=headers,
            json=data,
            auth=(self.api_key, self.api_secret),
        )

        """
        Sample Response:
        {
          "Messages": [
            {
              "Status": "success",
              "To": [
                {
                  "Email": "passenger1@mailjet.com",
                  "MessageUUID": "123",
                  "MessageID": 456,
                  "MessageHref": "https://api.mailjet.com/v3/message/456"
                }
              ]
            }
          ]
        }
        """

        return response.json()
