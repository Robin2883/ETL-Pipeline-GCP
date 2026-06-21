from faker import Faker
import random
import string

num_employees=20

fake=Faker()

employee_data=[]

password_chars=string.ascii_letters+string.digits+ 'm'

for _ in range(num_employees):
    employee={
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "job_title": fake.job(),
        "email": fake.email(),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
        "salary": fake.random_number(digits=5),
        "password": ''.join(random.choice(password_chars) for _ in range(8))
    }
    employee_data.append(employee)

print(employee_data)

import json
with open ('employee.json', 'w') as f:
    json.dump(employee_data, f, indent=2)

import csv
with open('employees.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=employee_data[0].keys())
    writer.writeheader()
    writer.writerows(employee_data)

from google.cloud import storage

def upload_csv_to_gcs(bucket_name, source_file_path, destination_blob_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Create blob (file in bucket)
    blob = bucket.blob(destination_blob_name)

    # Upload file
    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to gs://{bucket_name}/{destination_blob_name}")

upload_csv_to_gcs(
    bucket_name="employees-data-2883",
    source_file_path="employees.csv",
    destination_blob_name="raw_data/employees.csv"
)
