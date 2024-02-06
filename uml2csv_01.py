import re
"""
Python является отличным выбором для работы с текстовыми файлами.
Вы можете использовать модуль re (регулярные выражения) для извлечения необходимой информации
из исходного файла.
Ниже представлен один из вариантов решения вашей задачи.

Этот код работает следующим образом:
1. Открывает исходный uml файл и csv файл для записи.
2. Читает содержимое uml файла.
3. Извлекает все имена TABLE и TYPE из файла.
4. Проходит по всем полям и записывает их в файл в формате csv.
5. Имя текущего TABLE/TYPE хранится в отдельной переменной и обновляется, когда встречается следующая запись
    TABLE/TYPE.
Обратите внимание, в данной реализации предполагается, что в исходном файле TABLE или TYPE и его поля
всегда идут слитно - без пропусков строк. Если это не так, код потребует более сложной логики."""

def uml_to_csv(uml_file, csv_file):
    with open(uml_file, 'r') as uml, open(csv_file, 'w') as csv:
        current_table = ""
        for line in uml.readlines():
            # Если находим определение таблицы, обновляем текущую таблицу
            table_match = re.search(r'(?:TABLE|TYPE)\((.*?)\)', line)
            if table_match:
                current_table = table_match.group(1).strip()
                continue
            # Если находим определение поля, записываем его вместе с именем таблицы в CSV
            field_match = re.search(r'(?:primary_key\((.*?)\)|is_nullable\((.*?)\)|(\w+))\s:\s(.+)', line)
            if field_match and current_table:
                field_name = field_match.group(1) or field_match.group(2) or field_match.group(3)
                field_type = field_match.group(4).strip()
                csv.write(f'"{current_table}";"{field_name.strip()}";"{field_type}"\n')

if __name__ == '__main__':
    uml_to_csv('table_descriptions_14_Inventory.txt', 'table_descriptions_14_Inventory.csv')