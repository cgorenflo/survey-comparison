import csv
import codecs
from typing import NamedTuple, List


def get_email_addresses(reader: csv.reader, email_index: int, offset: int) -> List[str]:
    emails = []
    try:
        for i in range(offset):
            next(reader)
    except Exception as e:
        print(e)

    for row in reader:
        emails.append(row[email_index])

    return emails


with codecs.open("survey 1.csv", 'rU', 'UTF-8') as s1:
    with codecs.open("survey 2.csv", 'rU', 'UTF-8') as s2:
        survey1 = csv.reader(s1)
        survey2 = csv.reader(s2)

        offset1 = 1
        emails1 = get_email_addresses(survey1, 172, offset1)
        offset2 = 2
        emails2 = get_email_addresses(survey2, 5, offset2)

email_mapping = open("email_mapping.txt", 'w')
email_mapping.write("survey1_email_index,survey2_email_index\n")
for i in range(len(emails1)):
    is_mapped = False
    for j in range(len(emails2)):
        if emails1[i].lower() == emails2[j].lower():
            email_mapping.write(str(offset1 + i) + "," + str(offset2 + j) + "\n")
            is_mapped = True
