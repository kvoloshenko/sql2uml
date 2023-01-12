import pprint
file_path='ocs-rerate-orchestration_tables_00.cql'
i=0
with open(file_path, "r") as df:
    lines = [line for line in df]

tables = []
all_objects = []
cur_table = dict()
for l in lines:
    items = l.split()

    if len(items) > 5 and items[0] == 'CREATE' and items[1] == 'TABLE':
        table = dict()
        table['table_name'] = items[5]
        table['columns'] = []
        cur_table = table
        tables.append(items[5])
        tableStart = True

    if len(items) == 1 and items[0] == ');':
        tableStart = False
        all_objects.append(cur_table)

    if tableStart and len(items) > 0 and items[0] != 'PRIMARY' and items[0] != 'CREATE':
        column = dict()
        column['name'] = items[0]
        # remove last character ',' from the string
        column_type = items[1]
        column_type = column_type[:-1]
        column['type'] = column_type
        cur_table['columns'].append(column)

    print(f'len(items)={len(items)} tableStart={tableStart} {items}')

uml_start = """
@startuml
!define table(x) class x << (T,#FFAAAA) >>
!define TABLE(x) class x << (T,#FFAAAA) >>
!define TYPE(x) class x << (C,#FFAAAA) >>
!define primary_key(x) <u>x</u>
hide methods	
hide stereotypes

title ReRate Cassandra tables 
"""

uml_end = """
@enduml
"""

uml_file_path = 'uml_file.txt'
with open(uml_file_path, 'w', encoding='utf8') as f:
    f.write(uml_start)

    for o in all_objects:
        print(type(o), o)
        table_line = 'table(' + o['table_name'] + ') {\n'
        f.write(table_line)
        # here is columns info output
        table_columns = o['columns']
        for c in table_columns:
            column_line = c['name'] + ' : ' + c['type'] + '\n'
            f.write(column_line)

        f.write('}\n\n')

    f.write(uml_end)

# print(lines)
# pprint.pprint(lines)
# print(len(tables), tables)
pprint.pprint(all_objects)