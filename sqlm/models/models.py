from texttable import Texttable
import re


class Table():

    def __init__(self, name="", file_name=""):
        self.name = name
        self.db_name = ""
        self.class_name = ""
        self.columns = {}
        self.relationships = []

        if file_name != "":
            self.load_from_file(file_name)

    # LOAD table from .BAS file
    def load_from_file(self, file_name):

        try:
            file_obj = open(file_name, 'r')
            lines = file_obj.readlines()

            # trim list
            lines = [line.strip() for line in lines]

            # get class name
            self.class_name = file_name[:-4]

            # 6: table name
            s = re.search(r"Table: (\w+)", lines[6], re.I)
            self.name = s.group(1)

            # 7: database name
            s = re.search(r"Database: (\w+)", lines[7], re.I)
            self.db_name = s.group(1)

            # get columns
            columns_start = lines.index("'<Columns>")
            columns_end = lines.index("'</Columns>")

            if columns_start is not None and columns_end is not None:
                for i in range(columns_start+1, columns_end):
                    if lines[i] is not '':
                        col = Column(from_code=lines[i])
                        if col.is_valid:
                            self.add_column(col)
                        else:
                            print('Error: [{}] is not a valid column code.'.format(lines[i]))


            # get Relationships
            rel_start = lines.index("'<Relationships>")
            rel_end   = lines.index("'</Relationships>")

            if rel_start is not None and rel_end is not None:
                for i in range(rel_start+1, rel_end+1):
                    rel = Relationship(from_code=lines[i])
                    if rel.is_valid:
                        self.add_rel(rel)
            # Success
            return True

        except:
            # print("Error while parsing table file! [{}]".format(file_name))
            return False

    # add Relationship
    def add_rel(self, rel):
        self.relationships.append(rel)

    # add column to table
    def add_column(self, col):
        self.columns[col.field] = col

    def del_column(self, col_name):
        return self.columns.pop(col_name)

    def get_column(self, col_name):
        return self.columns[col_name]

    # comentario de linha: CTRL + ;
    # def get_columns_csv(self):
    #     csv = ""
    #     for col_name in self.columns:
    #         csv += self.columns[col_name].to_string() + ", "
    #     return csv[:-2]

    def get_columns_csv(self, include_autoinc_field=False):
        s = ''
        for field in self.columns:
            if self.columns[field].auto_increment:
                if include_autoinc_field is True:
                    s += self.columns[field].to_string() + ', '
                else:
                    continue
            s += self.columns[field].to_string() + ', '
        return s[:-2]

    def get_all_columns(self):
        return self.columns

    def get_file_name(self):
        return self.class_name + '.bas'


    def get_sqlite_create_table_string(self, use_default_value=False):
        query = 'CREATE TABLE IF NOT EXISTS [{}] ('.format(self.name) 
        col = Column()
        for col_name in self.columns:
            col = self.columns[col_name]
            query += '{} {}'.format(col.field, col.get_sql_type())
            query += ' PRIMARY KEY' if col.primary_key else ''
            query += ' ASC AUTOINCREMENT' if col.auto_increment else ''
            query += ' NOT NULL' if col.not_null else ''
            query += ' REFERENCES {} ({})'.format(col.foreign_key[0], col.foreign_key[1]) if col.foreign_key != () else ''
            query += ' DEFAULT (0)' if use_default_value else ''
            query += ', '
        query = query[:-2] + ')'
        return query

    def print_info(self):
        tbl = Texttable()
        tbl.set_deco(tbl.HEADER | tbl.BORDER)
        tbl.header(["Field", "Type", "PrimaryKey", "AutoInc", "NotNull", "ForeignKey"])
        for col_name in self.columns:
            col = self.columns[col_name]
            tbl.add_row([col.field, col.type, col.primary_key, col.auto_increment, col.not_null, col.foreign_key])

        print("[Table name = '{}' class_name = '{}' Columns = {}]".format(self.name, self.class_name, len(self.columns)))
        print(tbl.draw())
        print("[Relationships]")
        [print("> " + item.to_string()) for item in self.relationships]
        print("_" * 30)


class Database():
    
    def __init__(self, name='', b4j_version='6.0'):
        self.name = name
        self.path = ""
        self.tables = {}
        self.b4j_version = b4j_version
       
    def add_table(self, table):
        self.tables[table.name] = table

    def del_table(self, table_name):
        self.tables.pop(table_name)

    def get_table(self, table_name):
        return self.tables[table_name]

    def get_data_access_file_name(self):
        return self.name + 'DataAccess.bas'

    def get_table_cname(self, table_name):
        try:
            return self.tables[table_name].class_name
        except:
            return '{table_cname}'

    def get_file_name(self):
        return self.name + '.db'
       
    def print_info(self):
        print('> Database: {}'.format(self.name))
        print('> Tables [{}]'.format(len(self.tables)))
        for tbl in self.tables:
            print('>>> {}'.format(self.tables[tbl].name))










class Column():
    def __init__(self, field="", type="", auto_increment=False, not_null=False, primary_key=False, foreign_key=(), from_code=""):
        self.field = field
        self.type = type
        self.auto_increment = auto_increment
        self.not_null = not_null
        self.primary_key = primary_key
        self.foreign_key = foreign_key

        # is valid flag
        self.is_valid = False

        if from_code != "":
            if self.parse_from_code(from_code):
                self.is_valid = True

    def get_attr_csv(self):
        if self.foreign_key != ():
            t, f = self.foreign_key
            return 'ForeignKey({0}.{1})'.format(t, f)
        return '{0}{1}{2}'.format('PrimaryKey, ' if self.primary_key else '',
                                    'NotNull, ' if self.not_null else '',
                                    'AutoIncrement, ' if self.auto_increment else '')[:-2]


    
    def to_string(self):
        # String with Field declaration only
        # Ex: Public [Field] As [Type]
        return "{} As {}".format(self.field, self.type)
   
        
    def to_full_string(self):
        # Full string with attributes
        # Ex: Public [Field] As [Type] '[AutoIncrement, NotNull, ForeignKey(Table2.Id)]
        return 'Public ' + self.to_string() + " '[{}]".format(self.get_attr_csv())

    def parse_from_code(self, code):

        # Expression Ex: Public Field1 As String '[AutoIncrement, NotNull, ForeignKey(Table2.Id)]
        try:
            exprObj = re.match(r"\w+ (\w+) As (\w+)", code, re.I)
            if exprObj:
                # field / type
                self.field = exprObj.group(1)
                self.type = exprObj.group(2)

                # parse args
                if re.search(r"AutoIncrement", code, re.I):
                    self.auto_increment = True
                if re.search(r"PrimaryKey", code, re.I):
                    self.primary_key = True
                if re.search(r"NotNull", code, re.I):
                    self.not_null = True
                if re.search(r"ForeignKey", code, re.I):
                    # parse foreign key
                    fk = re.search(r"ForeignKey\((\w+)\.(\w+)\)", code, re.I)
                    self.foreign_key = (fk.group(1), fk.group(2))
                return True
            else:
                return False  # no match
        except:
            # error: return false
            return False

    # Converts to B4j type
    def get_b4j_type(self):
        sqlt = self.type.lower()
        if 'integer' in sqlt:
            return 'Int'
        elif 'blob' in sqlt:
            return 'Object'
        else:
            return self.type

    # Converts to SQLite Type
    def get_sql_type(self):
        b4jt = self.type.lower()
        if 'int' in b4jt:
            return 'Integer'
        elif 'boolean' in b4jt:
            return 'Integer'
        elif 'object' in b4jt:
            return 'Blob'
        else:
            return self.type


    def print_info(self):
        tbl = Texttable()
        tbl.header(["Field", "Type", "PrimaryKey", "AutoInc", "NotNull", "ForeignKey"])
        tbl.add_row([self.field, self.type, self.primary_key, self.auto_increment, self.not_null, self.foreign_key])
        print(tbl.draw())













class Relationship():

    def __init__(self, table1="", field1="", table2="", field2="", rel_type="", from_code=""):
        self.table1   = table1
        self.field1   = field1
        self.rel_type = rel_type
        self.table2   = table2
        self.field2   = field2

        # is_valid flag
        self.is_valid = False

        if from_code != "":
            if self.parse_from_code(from_code):
                self.is_valid = True

    def parse_from_code(self, code):
        r = re.search(r"(\w+)\.(\w+) \<(\w+)\> (\w+)\.(\w+)", code, re.I)
        if r:
            self.table1   = r.group(1)
            self.field1   = r.group(2)
            self.rel_type = r.group(3)
            self.table2   = r.group(4)
            self.field2   = r.group(5)
            return True
        else:
            return False

    def to_string(self):
        return "%s.%s <%s> %s.%s" % (self.table1, self.field1, self.rel_type, self.table2, self.field2)
