#!python
from io import FileIO
import sys
import json
from faker import Faker

def write_fake_data(file: FileIO, size: int = 1000):
    fake = Faker()
    while True:
        file.write(json.dumps({
            "name": fake.name(),
            "address": fake.address(),
            "company": fake.company(),
            "phone_number": fake.phone_number(),
            "job": fake.job(),
        }) + '\n')
        if (size := size - 1) == 0:
            break

if __name__ == "__main__":
    filepath = sys.argv[1]
    size = int(sys.argv[2])
    with open(filepath, 'w') as f:
        write_fake_data(f, size)
