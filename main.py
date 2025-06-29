from splitsql import split_sql_file
from relations import find_table_relations
from parser import parsed_sql

create_cmds, insert_cmds = split_sql_file("demo.sql")

create_sql_cmds = "\n".join(create_cmds)

parsed = parsed_sql(create_sql_cmds)
relations = find_table_relations(parsed["tables"])
print(relations)
