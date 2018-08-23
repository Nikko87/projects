from models.models import *
import re


class B4JProject():

    def __init__(self, load_from_file=''):
        self.version = ''
        self.db = Database()

        if load_from_file != '':
            self.load_from_file(load_from_file)

    def load_from_file(self, f_name: str):
        try:
            f_obj = open(f_name)
            f_code = f_obj.read()

            table_list = []
            db_list = []

            print("> Loading project file: {}".format(f_name))

            # get project version
            regex = re.search(r'Version=(\d+\.\d+)', f_code, re.I)
            self.version = regex.group(1) 

            # get all modules
            regex = re.compile(r'Module\d+=(\w+)', re.IGNORECASE | re.MULTILINE)
            for match in regex.finditer(f_code):
                # check if module is a Table Module
                module_name = match.group(1)

                tbl = Table()
                if tbl.load_from_file(module_name+'.bas'):
                    # This is a table file
                    print('> Table module found: [{}]. Adding to database...'.format(module_name))
                    table_list.append(tbl)
                    # check all databases in tables_list
                    if tbl.db_name not in db_list:
                        print('> Database found: [{}]'.format(tbl.db_name))
                        db_list.append(tbl.db_name)

            if len(db_list) > 1:
                # 2 or more databases in project
                # choose a database to open
                print('There are [{}] databases in this project. Select one you want to open: '.format(len(db_list)))
                for db_name in db_list:
                    print('[{}] {}'.format(db_list.index(db_name), db_name))

                idx_db = int(input('Database selected: '))
            else:
                idx_db = 0

            # Load the database
            self.db.name = db_list[idx_db]
            self.db.b4j_version = self.version
            for tbl in table_list:
                self.db.add_table(tbl)
        
            # Success loading the file 
            return True

        except:
            # Error while loading file
            return False

    def update_file(self, f_name: str):
        try:
            f_obj = open(f_name)
            f_code = f_obj.read()

            modules_list = []

            # get all modules
            regex = re.compile(r'Module\d+=(\w+)', re.IGNORECASE | re.MULTILINE)
            for match in regex.finditer(f_code):
                modules_list.append(match.group(1))

            # check if Table exists in modules list: add, if not
            for tbl_name in self.db.tables:
                tbl = self.db.tables[tbl_name]
                if tbl.class_name not in modules_list:
                    modules_list.append(tbl.class_name)
                    
            # check if module DataAccess exists: add, if not
            if self.db.name+'DataAccess' not in modules_list:
                modules_list.append(self.db.name+'DataAccess')

            f_list = re.split('\n', f_code)

            i = 0
            while(i <= len(f_list)):
                # find and remove all modules lines
                if f_list[i].startswith('Module'):
                    f_list.pop(i)
                    i -= 1
                elif f_list[i].startswith('NumberOfFiles'):
                    end_of_modules = i
                    break
                i += 1
            
            n_modules = len(modules_list)
            
            # update NumberOfModules: index = end_of_modules + 2
            f_list[end_of_modules+2] = 'NumberOfModules={}'.format(n_modules)

            for i in range(0, len(modules_list)):
                s = 'Module{0}={1}'.format(int(n_modules)-i, modules_list[i])
                f_list.insert(end_of_modules, s)
           
            # update *.b4j file       
            f_obj = open(f_name, 'w')
            f_obj.writelines('{}\n'.format(item) for item in f_list)
            
            return True
        except:
            import traceback; traceback.print_exc()
            return False
