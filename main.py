import csv
import re
from pprint import pprint


def read_csv():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    pprint(contacts_list)
    return contacts_list


def write_csv(new_contacts_list):
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',', lineterminator='\n')
        datawriter.writerows(new_contacts_list)


def normalization_fio(row):
    fio_parts = []
    for part in row[:3]:
        if part:
            fio_parts.extend(part.split())
    if len(fio_parts) == 2:
        fio_parts.append('')
    elif len(fio_parts) == 1:
        fio_parts.extend(['', ''])
    return fio_parts + row[3:]


def normalization_phone(phone):
    pattern = r'(8|\+7)(?:\s?\((\d{3})\)|[\s-]?(\d{3}))[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})\s?\(?(доб\.)?\s?(\d{4})?\)?'
    if not phone:
        return ''
    elif 'доб' in phone:
        new_phone = re.sub(pattern, r'+7(\2\3)\4-\5-\6 \7\8', phone)
    else:
        new_phone = re.sub(pattern, r'+7(\2\3)\4-\5-\6', phone)
    return new_phone


def merge_duplicate(contacts_list):
    merged_dict = {}
    for row in contacts_list:
        key = (row[0], row[1])
        if key not in merged_dict:
            merged_dict[key] = row.copy()
        else:
            for i in range(len(row)):
                if row[i] and not merged_dict[key][i]:
                    merged_dict[key][i] = row[i]
    return list(merged_dict.values())


if __name__ == '__main__':
    contacts_list = read_csv()
    new_contacts_list = []
    new_contacts_list.append(contacts_list[0])
    for row in contacts_list[1:]:
        row = normalization_fio(row)
        row[5] = normalization_phone(row[5])
        new_contacts_list.append(row)
    write_csv(merge_duplicate(new_contacts_list))
