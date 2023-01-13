import pprint
file_path='ocs-rerate-orchestration_tables_00.cql'
i=0
# loading ddl from the file
with open(file_path, "r") as df:
    lines = [line for line in df]

# parsing ddl
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

    # print(f'len(items)={len(items)} tableStart={tableStart} {items}')

# Outputing data for PlantUML
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
        # print(type(o), o)
        table_line = 'table(' + o['table_name'] + ') {\n'
        f.write(table_line)
        # here is columns info output
        table_columns = o['columns']
        primary_keys = o['primary_keys']
        for c in table_columns:
            # primary keys
            column_name = c['name']
            # print(f'column_name={column_name} {primary_keys}')
            if column_name in primary_keys:
                column_line = 'primary_key(' + column_name + ') : ' + c['type'] + '\n'
            else:
                column_line = column_name + ' : ' + c['type'] + '\n'
            f.write(column_line)

        f.write('}\n\n')

    f.write(uml_end)

# Outputing data for html
html_start = """<html>
<head>
<title>ReRate Cassandra tables</title>
</head>
<body>
<h1>ReRate Cassandra tables</h1>
  
<p>Here we define structures of data stored in DB and in Cache - for each table and cache structure column we provide name, type, description. Structures should be groupped by storage type (like Hazelcast, Oracle DB, Cassandra DB)</p>
  

"""
# Outputing data for html
html_end = """
</body>
</html>
"""
html_table_start = """
<table>
  <tr>
    <th>Column Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
"""
html_table_end = """
</table>
"""

html_file_path = 'uml_file.html'
with open(html_file_path, 'w', encoding='utf8') as f:
    f.write(html_start)
    for o in all_objects:
        # print(type(o), o)
        table_name_l ='<h2>' + o['table_name'] + '</h2>\n'
        f.write(table_name_l)
        f.write(html_table_start)

        table_columns = o['columns']
        primary_keys = o['primary_keys']
        for c in table_columns:
            f.write('<tr>\n')

            # primary keys
            column_name = c['name']
            column_type = c['type']
            column_type = column_type.replace(">", "&#62;")
            column_type = column_type.replace("<", "&#60;")
            # print(f'column_name={column_name} {primary_keys}')
            if column_name in primary_keys:
                column_line = '<td>' + column_name + '</td><td>' + column_type + '</td><td>primary_key</td>\n'
            else:
                column_line = '<td>' + column_name + '</td><td>' + column_type + '</td><td></td>\n'
            f.write(column_line)
            f.write('</tr>\n')

        f.write(html_table_end)


    f.write(html_end)

# print(lines)
# pprint.pprint(lines)
# print(len(tables), tables)
pprint.pprint(all_objects)