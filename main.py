
from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
  # 1. поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
  # 2. привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
  # 3. объединить все дублирующиеся записи о человеке в одну.

  phone_number = '(8|\+7)?\s*(\(*)(\d{3})(\)*)(\s*|-)(\d{3})(\s*|-)(\d{2})(\s*|-)(\d{2})\s*(\(*)(\w\w\w\.)*\s*(\d{4})*(\))*'
  new_phone_number = r'+7(\3)\6-\8-\10 \12\13'

  def correct_list(contacts_list):
    """функция, корректирующая список контактов"""
    correct_contacts_list = list()
    for contact in contacts_list:
      # корректируем каждый из контактов в соответствии с требованиями
      new_contact = list()
      full_name = ",".join(contact[:3])
      result = re.findall(r'(\w+)', full_name)
      while len(result) < 3:
        result.append('')
      new_contact += result
      new_contact.append(contact[3])
      new_contact.append(contact[4])
      phone_pattern = re.compile(phone_number)
      new_phone_pattern = phone_pattern.sub(new_phone_number, contact[5])
      new_contact.append(new_phone_pattern)
      new_contact.append(contact[6])
      correct_contacts_list.append(new_contact)
    return correct_contacts_list

def remove_duplicates(correct_contacts_list):
  """"функция, удаляющая дубликаты записей"""
  phone_book = dict()
  for contact in correct_contacts_list:
    if contact[0] in phone_book:
      contact_value = phone_book[contact[0]]
      for i in range(len(contact_value)):
        if contact[i]:
          contact_value[i] = contact[i]
    else:
      phone_book[contact[0]] = contact
  return list(phone_book.values())

# TODO 2: сохраните получившиеся данные в другой файл
def write_new_data(correct_contacts_list):
  with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(correct_contacts_list)

# выполнение созданных функций
aggregate_list = correct_list(contacts_list)
final_contact_list = remove_duplicates(aggregate_list)
write_new_data(final_contact_list)

