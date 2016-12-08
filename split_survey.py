import csv

with open("survey 1.csv", 'r') as survey1:
    with open("email_mapping.txt", 'r') as email_file:
        survey1_participants = open("survey1_participants.txt", 'w')
        survey1_participants.write(survey1.readline())
        email_reader = csv.DictReader(email_file)
        row = next(email_reader)
        survey1_index = int(row["survey1_email_index"])
        survey2_index = int(row["survey2_email_index"])
        i=1
        participants = [None]*26
        for line in survey1:
            if survey1_index == i:
                participants[survey2_index] = line
                try:
                    row = next(email_reader)
                except StopIteration:
                    break
                survey1_index = int(row["survey1_email_index"])
                survey2_index = int(row["survey2_email_index"])
            i=i+1

        for line in participants[1:]:
            if line is None:
                survey1_participants.write("\n")
            else:
                survey1_participants.write(line)