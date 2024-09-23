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
                    "header": "Age",
                    "key": "age",
                },
                {
                    "header": "Sex",
                    "key": "sex",
                },
                {
                    "header": "Address",
                    "key": "address",
                },
                {
                    "header": "Phone",
                    "key": "phone",
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
                    "header": "Description",
                    "key": "description",
                },
                {
                    "header": "Date",
                    "key": "date",
                },
                {
                    "header": "Location",
                    "key": "location",
                },
                {
                    "header": "Status",
                    "key": "status",
                }
            ]
        }
    ]

    return {
        "data": entities
    }
