from faker import Faker
import random

fake = Faker()


def handler(event, context):
    entities = [
        {
            "entity": "Person",
            "totalCount": fake.random_int(min=5, max=20),
            "columns": [
                {
                    "header": "Name",
                    "key": "name",
                },
                {
                    "header": "Address",
                    "key": "address",
                },
                {
                    "header": "Phone number",
                    "key": "phone_number",
                }
            ]
        },
        {
            "entity": "Report",
            "totalCount": fake.random_int(min=5, max=20),
            "columns": [
                {
                    "header": "Name",
                    "key": "name",
                },
                {
                    "header": "Address",
                    "key": "address",
                },
                {
                    "header": "Phone number",
                    "key": "phone_number",
                }
            ]
        }
    ]

    return {
        "data": entities
    }
