from models.models import *

from utils import *


class CreateModules():
    
    def __init__(self, data_base: Database):
        self.db = data_base

    # create modules:
        # table files
        # data_access file


    def create_table_files(self):
        tables = self.db.tables

        for tbl_name in tables:
            tbl = tables[tbl_name]
            with open(tbl.get_file_name(), 'w') as f:
                f.write(self.get_table_code(tbl))
           
    def update_table_files(self):
        tables = self.db.tables

        for tbl_name in tables:
            tbl = tables[tbl_name]
            self.update_table_file(tbl)



    def get_table_code(self, tbl: Table):
        
        # Create Header
        s = ''
        s += 'B4J=true\n'
        s += 'Group=Models\n'
        s += 'ModulesStructureVersion=1\n'
        s += 'Type=Class\n'
        s += f'Version={self.db.b4j_version}\n'
        s += '@EndOfDesignText@\n'

        s += f"'[Table: {tbl.name}]\n"
        s += f"'[Database: {tbl.db_name}]\n"

        s += 'Sub Class_Globals\n'

        s += "\t'<Columns>\n"
        for field in tbl.columns:
            col = tbl.columns[field]
            # format: Public Id As Int '[PrimaryKey, AutoIncrement]
            s += "\t\t{0}\n\n".format(col.to_full_string())
        s += "\t'</Columns>\n"

        s += "\t'<Relationships>\n"
        for rel in tbl.relationships:
            tbl1_cname = self.db.get_table_cname(rel.table1)
            tbl2_cname = self.db.get_table_cname(rel.table2)

            # s += "\t\t'[{}]\n".format(rel.to_string())
            if rel.rel_type == '11':
                s += "\t\tPrivate {}_ As {} '[{}]\n\n".format(
                    tbl2_cname, tbl2_cname, rel.to_string())
            elif rel.rel_type == '1N':
                s += "\t\tPrivate {}_ As List '[{}]\n\n".format(
                    rel.table2, rel.to_string())
            elif rel.rel_type == 'N1':
                s += "\t\tPrivate {}_ As {} '[{}]\n\n".format(
                    tbl2_cname, tbl2_cname, rel.to_string())
                    
        s += "\t'</Relationships>\n"

        s += 'End Sub\n'

        s += 'Public Sub Initialize\n\n'

        s += 'End Sub\n'

        s += '#Region Relationships\n'

        # Create Relationships subs
        for rel in tbl.relationships:
            tbl1_cname = self.db.get_table_cname(rel.table1)
            tbl2_cname = self.db.get_table_cname(rel.table2)

            s += "'{}\n".format(rel.to_string())

            if rel.rel_type == '11':
                
                s += 'Public Sub get{0} As {1}\n'.format(tbl2_cname, tbl2_cname)
                s += '\tIf {0}.IsInitialized Then\n'.format(tbl2_cname)
                s += '\t\tReturn {0}_\n'.format(tbl2_cname)
                s += '\tElse\n'
                s += '\t\tDim da As {}DataAccess\n'.format(self.db.name)
                s += '\t\tda.Initialize\n'
                if rel.field1.upper() == 'ID':
                    s += '\t\t{0}_ = da.{1}_Where("{2}Id = ?", Array(Id))\n'.format(tbl2_cname, rel.table2, tbl1_cname)
                else:
                    s += '\t\t{0}_ = da.{1}_Where("Id = ?", Array({2}Id))\n'.format(tbl2_cname, rel.table2, tbl2_cname)
                s += '\t\tda.Dispose\n'
                s += '\t\tReturn {0}_\n'.format(tbl2_cname)
                s += '\tEnd If\n'
                s += 'End Sub\n'

            elif rel.rel_type == '1N':
                
                s += 'Public Sub get{0} As List\n'.format(rel.table2)
                s += '\tIf {0}_.IsInitialized then\n'.format(rel.table2)
                s += '\t\tReturn {0}_\n'.format(rel.table2)
                s += '\tElse\n'
                s += '\t\tDim da As {0}DataAccess\n'.format(self.db.name)
                s += '\t\tda.Initialize\n'
                s += '\t\t{0}_ = da.{1}_Where2("{2}Id=?", Array(Id))\n'.format(rel.table2, rel.table2, tbl1_cname)
                s += '\t\tda.Dispose\n'
                s += '\t\tReturn {0}_\n'.format(rel.table2)
                s += '\tEnd If\n'
                s += 'End Sub\n'

            elif rel.rel_type == 'N1':
                
                s += 'Public Sub get{0} As {1}\n'.format(tbl2_cname, tbl2_cname)
                s += '\tIf {0}_.IsInitialized then\n'.format(tbl2_cname)
                s += '\t\tReturn {0}_\n'.format(tbl2_cname)
                s += '\tElse\n'
                s += '\t\tDim da As {0}DataAccess\n'.format(self.db.name)
                s += '\t\tda.Initialize\n'
                s += '\t\t{0}_ = da.{1}_Where("Id=?", Array({2}Id))\n'.format(tbl2_cname, rel.table2, tbl2_cname)
                s += '\t\tda.Dispose\n'
                s += '\t\tReturn {0}_\n'.format(tbl2_cname)
                s += '\tEnd If\n'
                s += 'End Sub\n'

        s += '#End Region\n\n'

        return s




    def update_table_file(self, tbl: Table):
        
        f_obj = open(tbl.get_file_name())

        f_code = f_obj.readlines()
        # old code with all special characters
        f_old_code = list(f_code)

        # remove all special characters in file
        f_code = [code.strip() for code in f_code]

        tbl_code = self.get_table_code(tbl)

        # get index of #Region Subs
        try:
            subs_start = f_code.index('#Region Subs')
            if subs_start:
                tbl_code += '\n'
                for i in range(subs_start, len(f_code)):
                    tbl_code += f_old_code[i]
                    if f_code[i] == '#End Region':
                        break
                tbl_code += '\n'
        except:
            pass
        finally:
            with open(tbl.get_file_name(), 'w') as f:
                f.write(tbl_code)      
      

    def create_data_access_file(self):
        
        # HEADER of file
        s = ''
        s += 'B4J=true\n'
        s += 'Group=Controllers\n'
        s += 'ModulesStructureVersion=1\n'
        s += 'Type=Class\n'
        s += 'Version='+self.db.b4j_version+'\n'
        s += '@EndOfDesignText@\n'

        s += 'Sub Class_Globals\n'
        s += '\tPrivate fx as JFX\n'
        s += '\tPrivate SQL1 As SQL\n'
        s += 'End Sub\n\n'

        # FUNCTION: Initialize
        s += 'Public Sub initialize\n'
        s += '\tSQL1.InitializeSQLite(File.DirApp, "{}.db", True)\n'.format(
            self.db.name)
        s += 'End Sub\n'

        # FUNCTION: Dispose
        s += 'Public Sub Dispose\n'
        s += '\tSQL1.Close\n'
        s += 'End Sub\n\n'

        # FUNCTION: GetSQL
        s += 'Public Sub getSQL As SQL\n'
        s += '\tReturn SQL1\n'
        s += 'End Sub\n\n'

        s += '#Region Subs\n'
        s += '\t\'Write here the subs you want to save\n'
        s += '#End Region\n\n'
        # TODO: save #Region subs 

        # BODY of file
        # get code of all tables

        tables = self.db.tables
        for tbl_name in tables:
            s += self.get_data_access_code(tables[tbl_name])

        with open(self.db.get_data_access_file_name(), 'w') as f:
            f.write(s)


    def get_data_access_code(self, tbl: Table):

        # Starts with #Region table <TableName>
        s = ''
        s += '\n#Region Table <{0}>\n'.format(tbl.name)

        # SUB: CreateTable
        s += '\nPublic Sub {0}_CreateTable()'.format(tbl.name)
        s += '\n\tDim mData As Map'
        s += '\n\tmData.Initialize'
        columns = tbl.get_all_columns()
        for field in columns:
            col = columns[field]
            if col.foreign_key != ():
                t, f = col.foreign_key
            s += '\n\tmData.Put("{0}", "{1}{2}{3}{4}{5}")'.format(col.field, col.get_sql_type(),
                                                                  ' PRIMARY KEY' if col.primary_key else '',
                                                                  ' ASC AUTOINCREMENT' if col.auto_increment else '',
                                                                  ' NOT NULL' if col.not_null else '',
                                                                  ' REFERENCES {} ({})'.format(t, f) if col.foreign_key != () else '')

        s += '\n\tDBUtils.CreateTable(SQL1, "{0}", mData, "")'.format(tbl.name)
        s += '\nEnd Sub\n'

        # SUB: Insert
        s += '\nPublic Sub {0}_Insert(t As {1})'.format(tbl.name, tbl.class_name)
        s += '\n\tDim m As Map'
        s += '\n\tm.Initialize'
        for field in columns:
            if not columns[field].auto_increment:
                s += '\n\tm.Put("{0}", t.{0})'.format(columns[field].field)
        s += '\n\tDBUtils.InsertMaps(SQL1, "{0}", Array As Object(m))'.format(tbl.name)
        s += '\nEnd Sub\n'

        # SUB: Insert2
        s += '\nPublic Sub {0}_Insert2({1})'.format(tbl.name,
                                                    tbl.get_columns_csv())
        s += '\n\tDim m As Map'
        s += '\n\tm.Initialize'
        for field in columns:
            if not columns[field].auto_increment:
                s += '\n\tm.Put("{0}", {0})'.format(columns[field].field)
        s += '\n\tDBUtils.InsertMaps(SQL1, "{0}", Array As Object(m))'.format(tbl.name)
        s += '\nEnd Sub'
        s += '\n'

        # SUB: Delete
        s += '\nPublic Sub {0}_Delete(t As {1})'.format(tbl.name, tbl.class_name)
        s += '\n\tDim m As Map = CreateMap("Id": t.Id)'
        s += '\n\tDBUtils.DeleteRecord(SQL1, "{0}", m)'.format(tbl.name)
        s += '\nEnd Sub\n'

        # SUB: Update
        s += '\nPublic Sub {0}_Update(t As {1})'.format(tbl.name, tbl.class_name)
        s += '\n\tDim m As Map'
        s += '\n\tm.Initialize'
        for field in columns:
            if not columns[field].auto_increment:
                s += '\n\tm.Put("{0}", t.{0})'.format(columns[field].field)
        s += '\n\tDim WhereFields As Map = CreateMap("Id": t.Id)'
        s += '\n\tDBUtils.UpdateRecord2(SQL1, "{0}", m, WhereFields)'.format(tbl.name)
        s += '\nEnd Sub\n'

        # SUB: GetById
        s += '\nPublic Sub {0}_GetById(Id As Int) As {1}'.format(tbl.name, tbl.class_name)
        s += '\n\tReturn {0}_Where("Id=?", Array(Id))'.format(tbl.name)
        s += '\nEnd Sub\n'

        # SUB: ToList
        s += '\nPublic Sub {0}_ToList As List'.format(tbl.name)
        s += '\n\tDim rs As ResultSet'
        s += '\n\tDim lstResult As List'
        s += '\n\tlstResult.Initialize'
        s += '\n\trs = SQL1.ExecQuery("SELECT * FROM {}")'.format(tbl.name)
        s += '\n\tDo While rs.NextRow'
        s += '\n\t\tDim t As {0}'.format(tbl.class_name)
        s += '\n\t\tt.Initialize'
        for field in columns:
            s += '\n\t\tt.{0} = rs.Get{1}("{0}")'.format(field, columns[field].get_b4j_type())
        s += '\n\t\tlstResult.Add(t)'
        s += '\n\tLoop'
        s += '\n\tReturn lstResult'
        s += '\nEnd Sub\n'

        # SUB:  Where
        s += '\nPublic Sub {0}_Where(WhereCondition As String, ArgList As List) As {1}'.format(tbl.name, tbl.class_name)
        s += '\n\tDim rs As ResultSet'
        s += '\n\trs = SQL1.ExecQuery2("SELECT * FROM {0} WHERE " & WhereCondition, ArgList)'.format(tbl.name)
        s += '\n\tIf rs.NextRow = False Then Return Null'
        s += '\n\tDim t As {0}'.format(tbl.class_name)
        s += '\n\tt.Initialize'
        for field in columns:
            s += '\n\tt.{0} = rs.Get{1}("{0}")'.format(field, columns[field].get_b4j_type())
        s += '\n\tReturn t'
        s += '\nEnd Sub\n'

        # SUB:  Where2
        s += '\nPublic Sub {0}_Where2(WhereCondition As String, ArgList As List) As List'.format(tbl.name)
        s += '\n\tDim rs As ResultSet'
        s += '\n\tDim lstResult As List'
        s += '\n\tlstResult.Initialize'
        s += '\n\trs = SQL1.ExecQuery2("SELECT * FROM {0} WHERE " & WhereCondition, ArgList)'.format(tbl.name)
        s += '\n\tDo While rs.NextRow'
        s += '\n\t\tDim t As {0}'.format(tbl.class_name)
        s += '\n\t\tt.Initialize'
        for field in columns:
            s += '\n\t\tt.{0} = rs.Get{1}("{0}")'.format(field, columns[field].get_b4j_type())
        s += '\n\t\tlstResult.Add(t)'
        s += '\n\tLoop'
        s += '\n\tReturn lstResult'
        s += '\nEnd Sub\n'

        # SUB: RowCount
        s += '\nPublic Sub {0}_RowCount() As Int'.format(tbl.name)
        s += '\n\tReturn SQL1.ExecQuerySingleResult("SELECT Count(*) FROM {0}")'.format(tbl.name)
        s += '\nEnd Sub\n'

        # Ends with #End Region
        s += '\n#End Region'

        return s
