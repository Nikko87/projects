
def get_b4j_type(sql_type: str):
    sqlt = sql_type.lower()
    if 'integer' in sqlt:
        return 'Int'
    elif 'blob' in sqlt:
        return 'Object'
    else:
        return sql_type

def get_sql_type(b4j_type: str):
    b4jt = b4j_type.lower()
    if 'int' in b4jt:
        return 'Integer'
    elif 'boolean' in b4jt:
        return 'Integer'
    elif 'object' in b4jt:
        return 'Blob'
    else:
        return b4j_type