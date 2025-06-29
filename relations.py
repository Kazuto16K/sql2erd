def find_table_relations(tables):
    relations = []

    for table in tables:
        fks =  table.get("foreign_keys",[])
        if len(fks) < 1:
            continue
        
        # Heuristic : if table has only foreign keys (and maybe composite PK) -> then a join table
        col_names = [col["name"] for col in table["columns"]]
        is_relationship_table = (
            len(fks) >= 2 and
            len(col_names) <= len(fks) + 1
        )

        if is_relationship_table: # many-many case
            if len(fks) == 2:
                entity1 = fks[0]["references"]["table"]
                entity2 = fks[1]["references"]["table"]

                relation_name = table["name"]  # better word with nlp later
                relation = {
                    "name": relation_name,
                    "from": entity1,
                    "to": entity2,
                    "via": table["name"],
                    "type": "many-to-many",
                    "participation": {
                        entity1: "unknown",
                        entity2: "unknown"
                    }
                }
                relations.append(relation)
        else:
            # infer as many-to-one (typical FK situation)
            for fk in fks:
                from_table = table["name"]
                to_table = fk["references"]["table"]
                from_col = fk["column"]

                # Check constraints on the FK column to infer participation/cardinality
                col = next((c for c in table["columns"] if c["name"] == from_col), {})
                constraints = col.get("constraints", []) if col else []

                relation = {
                    "name": f"{from_table}_to_{to_table}",
                    "from": from_table,
                    "to": to_table,
                    "via": None,
                    "type": "many-to-one",
                    "participation": {
                        from_table: "total" if "NOT NULL" in constraints else "partial",
                        to_table: "partial"
                    }
                }
                relations.append(relation)

    return relations
