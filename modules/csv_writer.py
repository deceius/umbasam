import csv
from tempfile import NamedTemporaryFile
import shutil


HEADERS = ['party_leader', 'officer_check', 'siphoned_energy', 'status', 'time_created']
FILENAME = 'oath.csv'

def write_to_csv_file(data):
    f = get_csv_file()
    row = {
        HEADERS[0]: data[0],
        HEADERS[1]: data[1],
        HEADERS[2]: data[2],
        HEADERS[3]: data[3],
        HEADERS[4]: data[4]
    }
    writer = csv.DictWriter(f, fieldnames= HEADERS)
    writer.writerow(row)

def get_csv_file():
    return open('./files/{0}'.format(FILENAME), 'a', newline='')

def update_row(data):
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open('./files/{0}'.format(FILENAME), 'r', newline='') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=HEADERS)
        writer = csv.DictWriter(tempfile, fieldnames=HEADERS)
        for row in reader:
            if row[HEADERS[0]] == data[0] and row[HEADERS[4]] == data[4] :
                row = {
                    HEADERS[0]: data[0],
                    HEADERS[1]: data[1],
                    HEADERS[2]: data[2],
                    HEADERS[3]: data[3],
                    HEADERS[4]: data[4]
                }    
            writer.writerow(row)
    shutil.move(tempfile.name, './files/{0}'.format(FILENAME))