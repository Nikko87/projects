from models.models import *
from models.create_modules import CreateModules
from models.b4jproject import B4JProject
from models.sqlite_control import SQLiteControl
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('-f', help='Select the b4j project file')
parser.add_argument('-db', help='Define Database to open')
parser.add_argument('-dbp', help='Path to database file')

args = parser.parse_args()

# print('Args: ')
# print(args.f)
# print(args.db)
# print(args.dbp)

args.f = "BE.b4j"
proj = B4JProject(load_from_file=args.f)
# proj.db.print_info()

sqlc = SQLiteControl(proj.db)
cm = CreateModules(proj.db)

# UPDATE:
#   Table files
#   Tables in database
tbl = Table()
for tbl in proj.db.tables.values():
    # tbl = proj.db.tables[tbl_name]
    cm.update_table_file(tbl)
    sqlc.update_table(tbl, create_if_not_exists=True)


# create data access file
print('> Creating DataAccess file...')
cm.create_data_access_file()
print('>> Done.')

# update b4j project file
print('> Updating B4j project file...')
proj.update_file(args.f)
print('>> Done.')



# proj = B4JProject(load_from_file='BE.b4j')

# proj.db.print_info()

# sqlc = SQLiteControl(proj.db)

# tbl = proj.db.get_table('Loteamentos')

# # tbl.print_info()
# sqlc.update_table(tbl, create_if_not_exists=True)

# # sqlc.add_column(tbl, 'Fiador', 'String')

# sqlc.dispose()  


# db = Database('DBDados')
# tbl1 = Table(file_name="Lote.bas")
# tbl2 = Table(file_name="Parcela.bas")
# tbl3 = Table(file_name='Loteamento.bas')

# proj.db.add_table(tbl1)
# proj.db.add_table(tbl2)
# proj.db.add_table(tbl3)
# proj.update_file('BE.b4j')

# s = 'comando=argumento'
# cmd, sep, code = s.partition('=')
# print('{} {}'.format(cmd, code))

# db.add_table(tbl1)
# db.add_table(tbl2)
# db.add_table(tbl3)

# cm = CreateModules(db)
# # cm.update_table_file(tbl1)
