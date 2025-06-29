import os
import re
import json

def parser(sql_string):
    tokens = re.findall(f"\w+|[(),;]", sql_string)    ## provides a list like ['CREATE', 'TABLE', 'Users', '(', 'id', 'INT', 'PRIMARY', 'KEY', ',', ...]
    print(tokens)
    tables = []
    while tokens:
        if tokens[0].upper() == "CREATE":
            table = parse_create_table(tokens)
            tables.append(table)
    return {"tables":tables}

def parse_create_table(tokens):
    assert tokens.pop(0).upper() == "CREATE"    # pops the first str and create, else error is raised
    assert tokens.pop(0).upper() == "TABLE"

    print("tokens create and table extracted")

    table_name = tokens.pop(0)
    assert tokens.pop(0) == "("

    columns = []
    pk = []
    fks = []

    while tokens[0] != ')':

        if tokens[0].upper() == "FOREIGN":
            tokens.pop(0)  # FOREIGN
            tokens.pop(0)  # KEY
            assert tokens.pop(0) == "("
            col = tokens.pop(0)
            assert tokens.pop(0) == ")"
            assert tokens.pop(0).upper() == "REFERENCES"
            ref_table = tokens.pop(0)
            assert tokens.pop(0) == "("
            ref_col = tokens.pop(0)
            assert tokens.pop(0) == ")"
            fks.append({"column":col, "references":{"table":ref_table, "column":ref_col}})

        else:
            col_name = tokens.pop(0)
            col_type = tokens.pop(0)
            constraints = []
            
            if tokens[0] == "(":
                col_type += tokens.pop(0) # merging VARCHAR(100) together
                while tokens[0] != ")":
                    col_type += tokens.pop(0)
                col_type += tokens.pop(0)  # adding ")" parenthesis
            
            while tokens[0] not in [",",")"]:
                constraints.append(tokens.pop(0).upper())
            columns.append({"name": col_name, "type": col_type, "constraints": constraints})

            if "PRIMARY" in constraints and "KEY" in constraints:
                pk.append(col_name)

        if tokens[0] == ",":
            tokens.pop(0)
    
    tokens.pop(0)   # Closing parenthesis

    if tokens and tokens[0] == ";":
        print("tokens ; extracted")
        tokens.pop(0)

    return {
        "name": table_name,
        "columns": columns,
        "primary_key": pk,
        "foreign_keys": fks
    }


def parsed_sql(sql_text):
    #with open("demo.sql", "r") as file:
    #    sql = file.read()

    parsed = parser(sql_text)

    with open("output.json", "w") as f:
        json.dump(parsed, f, indent=2)
    return parsed
