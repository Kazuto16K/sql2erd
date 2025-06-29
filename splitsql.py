import re

def split_sql_file(filepath):
    with open(filepath, 'r') as f:
        sql = f.read()

    # Remove comments
    sql = re.sub(r'--.*?\n', '', sql)
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)

    # Split all statements by semicolon
    statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]

    create_table_cmds = []
    insert_into_cmds = []

    for stmt in statements:
        if stmt.upper().startswith("CREATE TABLE"):
            create_table_cmds.append(stmt + ';')
        elif stmt.upper().startswith("INSERT INTO"):
            insert_into_cmds.append(stmt + ';')

    return create_table_cmds, insert_into_cmds
