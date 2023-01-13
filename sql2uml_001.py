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
        table['primary_keys'] = []
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

    # PRIMARY KEYs
    if tableStart and len(items) > 2 and items[0] == 'PRIMARY' and items[1] == 'KEY':
        for item in items[2:]:
            # print(f'PRIMARY KEY item = {item}')
            # print(f'items[2]={items[2]} items[-1:]={items[-1]}')
            primary_key_item = item
            if item == items[2]:
                primary_key_item = primary_key_item[1:-1]
            else:
                primary_key_item = primary_key_item[:-1]

            # print(f'primary_key_item={primary_key_item}')
            cur_table['primary_keys'].append(primary_key_item)

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

rerateTask "*" -up- "1" rerateRequest : request_id 
rerateCostedEvents "*" -up- "1" rerateRequest : request_id
rerateBucketAdjustments "*" -up- "1" rerateRequest : request_id
rerateAccountLock "*" -up- "1" rerateRequest : request_id
aggregationAccountLevel "*" -up- "1" rerateRequest : request_id
aggregationSubscriberLevel "*" -up- "1" rerateRequest : request_id
aggregationPeriodicSummaryLevel "*" -up- "1" rerateRequest : request_id
aggregationDiscountLevel "*" -up- "1" rerateRequest : request_id
aggregationLevel "*" -up- "1" rerateRequest : request_id
currentRequest "*" -up- "1" rerateRequest : request_id
notification "*" -up- "1" rerateRequest : request_id
roamingAccountCeKey "*" -up- "1" rerateRequest : request_id

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
        primary_keys = o['primary_keys']
        for c in table_columns:
            # primary keys
            column_name = c['name']
            print(f'column_name={column_name} {primary_keys}')
            if column_name in primary_keys:
                column_line = 'primary_key(' + column_name + ') : ' + c['type'] + '\n'
            else:
                column_line = column_name + ' : ' + c['type'] + '\n'
            f.write(column_line)

        f.write('}\n\n')

    f.write(uml_end)

# print(lines)
# pprint.pprint(lines)
# print(len(tables), tables)
pprint.pprint(all_objects)