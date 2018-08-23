from models.models import *

import sqlite3


# TODO: explorar a biblioteca deepdiff para tratar as mudancas de colunas

class SQLiteControl():

    def __init__(self, db: Database):
        self.conn = sqlite3.connect(db.get_file_name())

    def update_table(self, tbl: Table, create_if_not_exists=False):
        # if table not exists: create or exit
        if self.table_exists(tbl) is False:
            if create_if_not_exists:
                print("> Creating table: {}".format(tbl.name))
                c = self.conn.cursor()
                c.execute(tbl.get_sqlite_create_table_string())
            return

        print("> Updating table: {} ...".format(tbl.name))

        c = self.conn.cursor()
        query = 'PRAGMA table_info ({})'.format(tbl.name)
        c.execute(query)

        # get all column fields from *.db file. Ex: (0, 'Id', 'Integer', 0, None, 1)
        db_cols = [col[1] for col in c.fetchall()]
        
        # get all column fields from Project
        new_cols = [tbl.columns[col_name].field for col_name in tbl.columns]

        # check if have new columns
        if len(new_cols) > len(db_cols):
            # have new columns 
            # add col
            cols_to_add = set(new_cols).difference(set(db_cols))
            for col_name in cols_to_add:
                col = tbl.columns[col_name]
                print(f'>> Add column [{col.field}: {col.get_sql_type()}]')
                self.add_column(tbl, col.field, col.type)

            new_cols = ', '.join(new_cols)
            db_cols = new_cols
        else:
            # new_cols < db_cols
            # delete col
            # TODO: delete column
            db_cols = ', '.join(db_cols)
            new_cols = ', '.join(new_cols)

        try:
            c.execute('DROP TABLE IF EXISTS temp_table;')
            c.execute('PRAGMA foreign_keys=OFF')
            c.execute('ALTER TABLE [{}] RENAME TO temp_table;'.format(tbl.name))
            c.execute(tbl.get_sqlite_create_table_string())
            c.execute('INSERT INTO {} ({}) SELECT {} FROM temp_table;'.format(tbl.name, new_cols,   db_cols))

            # commit changes
            self.conn.commit()
            c.execute('PRAGMA foreign_keys=ON')

            print('>> Done.')
        except:
            import traceback
            print('>> Error')
            self.conn.rollback()
            traceback.print_exc()
        

    def add_column(self, tbl: Table, field: str, stype: str):
        # if table not exists, return
        if self.table_exists(tbl) is False:
            return

        c = self.conn.cursor()
        query = 'PRAGMA table_info ({})'.format(tbl.name)
        c.execute(query)

        # get all column fields. Ex: (0, 'Id', 'Integer', 0, None, 1)
        cols = [col[1] for col in c.fetchall()]

        # add column if not exists
        if field not in cols:
            query = 'ALTER TABLE {} ADD COLUMN {} {}'.format(tbl.name, field, stype)
            c.execute(query)

    
    def dispose(self):
        self.conn.close()

    def table_exists(self, tbl: Table):
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(tbl.name))
        if c.fetchone() is None:
            return False
        else:
            return True
