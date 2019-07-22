import pymysql
from pymysql.err import OperationalError

class Database:
    '''Abstract database class'''

    def __init__(self,
                 login_str='',
                 password_str='',
                 hostname_str='',
                 schemename_str=''):
        self.status_int = 0
        self.login_str = login_str
        self.password_str = password_str
        self.hostname_str = hostname_str
        self.schemename_str = schemename_str
        self.database_db = None
        self.cursor_db = None
        self.countprintchars_int = 200
        self.logfilepath_str = 'sqlqueryexception.txt'
        self._instance_cf()

    def __str__(self):
        if self.status_int:
            return 'OK - Database {} connected'.format(self.hostname_str)
        else:
            return 'ERROR - Database - Database {} not connected'.format(self.hostname_str)

    def _instance_cf(self):
        '''Virtual function without implementation for instance every one object parentheises'''
        self.disconnection_cf()
        raise NotImplementedError()

    def processquery_fc(self, query_str, fetching_int=0):
        '''Function for making some query to SQL DB and getting response from it
        fetching_int:
        0 - query for inserting
        1 - fetching query for getting one value - .fetchone
        2 - fetching query for getting list of values - .fetchall
        3 - inserting query with getting last row id
        4 - query for executing DLL script with multiple queries
        '''
        if fetching_int != 4:
            try:
                if len(query_str) > self.countprintchars_int:
                    print(query_str[:self.countprintchars_int],'...')
                else:
                    print(query_str)
                self.cursor_db.execute(query_str)
            except pymysql.err.OperationalError as e:
                print(e)
                self._instance_cf()
            except Exception as e:
                self.loggingerror_fc(str(e) + '\n' + query_str)
                assert False, str(e)
        else:
            self.cursor_db.executescript(query_str)
        data_tuple = tuple()
        if fetching_int == 1:
            data_tuple = self.cursor_db.fetchone()
        elif fetching_int == 2:
            data_tuple = self.cursor_db.fetchall()
        elif fetching_int == 0:
            self.database_db.commit()
        elif fetching_int == 3:
            data_tuple = tuple([self.cursor_db.lastrowid])
            self.database_db.commit()
        return data_tuple

    def makequeryfromlist_fc(self, firstpart_qstr, objects, template_qstr = '{}'):
        '''Method for making query from data structure'''
        if len(objects):
            if isinstance(objects[0], tuple) or isinstance(objects, list):
                for mutable_obj in objects:
                    firstpart_qstr += '('
                    for e in mutable_obj:
                        firstpart_qstr += template_qstr.format(e) + ', '
                    firstpart_qstr = firstpart_qstr[:-2] + '), '
                firstpart_qstr = firstpart_qstr[:-2] + ';'
            else:
                for immutable_obj in objects:
                    firstpart_qstr += '(' + template_qstr.format(immutable_obj) + '), '
                firstpart_qstr = firstpart_qstr[:-2] + ';'
            return firstpart_qstr
        return ''

    def loggingerror_fc(self, query_str):
        '''Writing exception query into the file'''
        try:
            with open(self.logfilepath_str, 'w', encoding='utf-8-sig', errors='ignore') as fw:
                fw.write(query_str)
        except Exception as e:
            print(e)

    def disconnection_cf(self):
        '''Method for disconnection from DB. Need fo trying reconnection without destruction object'''
        if self.cursor_db:
            self.cursor_db.close()
        if self.database_db:
            self.database_db.close()
            print('OK - host {} disconnected temporarely'.format(self.hostname_str))


    def __del__(self):
        '''Destructor'''
        if self.cursor_db:
            self.cursor_db.close()
        if self.database_db:
            try:
                self.database_db.close()
            except Exception:
                pass
        print('OK - host {} disconnected'.format(self.hostname_str))

class Database_mysql(Database):
    '''Object describes database based on MySQL DBMS'''

    def __init__(self,
                 login_str='',
                 password_str='',
                 hostname_str='',
                 schemename_str=''):
        super().__init__(login_str, password_str, hostname_str, schemename_str)


    def checktableindb_cf(self, schema_title_str, tablename_str):
        '''Method for checking if some table inside database'''
        if self.status_int:
            datatuples_lst = self.processquery_fc('SELECT table_name FROM information_schema.tables WHERE table_schema = \'{0}\' AND table_name = \'{1}\';'.format(schema_title_str, tablename_str), 2)
            if len(datatuples_lst):
                return 1
            return 0

    def createschema_cf(self, instance_schema_qstr, instance_tables_qstr):
        '''Method for instance database schema'''
        if self.status_int:
            try:
                self.processquery_fc(instance_schema_qstr)
            except Exception as e:
                print(e)
            try:
                self.processquery_fc(instance_tables_qstr)
            except Exception as e:
                print(e)

    def _instance_cf(self):
        '''Method for instance object parameters'''
        try:
            self.database_db = pymysql.connect(host=self.hostname_str,
                                               user=self.login_str,
                                               password=self.password_str,
                                               database=self.schemename_str,
                                               charset='utf8')
            if self.database_db:
                self.cursor_db = self.database_db.cursor()
            if self.cursor_db:
                self.status_int = 1
            print('OK - database {} get connected'.format(self.hostname_str))
        except OperationalError as e:
            print(e)
            print('ERROR - Database_mysql - database {} not connected'.format(self.hostname_str))

    def escapestring_fc(self, query_str):
        if self.status_int:
            return self.database_db.escape_string(query_str)

    def getdatafromdb_fc(self, tabletitle_str, schematitle_str,  *fields_tuple):
        getdata_qstr = 'SELECT '
        if self.status_int:
            if len(fields_tuple):
                for fieldtitle_str in fields_tuple:
                    getdata_qstr += '{}, '.format(fieldtitle_str)
                getdata_qstr = getdata_qstr[:-2]
                getdata_qstr += ' FROM {}.{};'.format(schematitle_str, tabletitle_str)
                return self.processquery_fc(getdata_qstr, 2)
        return tuple()

    def insertdataintodb_fc(self, tabletitle_str, schematitle_str, **keyvalue_dc):
        if keyvalue_dc:
            query_str = 'INSERT INTO {}.{} ('.format(schematitle_str, tabletitle_str)
            fieldtitles_lst = list(keyvalue_dc.keys())
            for fieldtitle_str in fieldtitles_lst:
                query_str += '{}, '.format(fieldtitle_str)
            query_str = query_str[:-2] + ') VALUES ('
            for fieldtitle_str in fieldtitles_lst:
                datatoinsert_lst = keyvalue_dc.get(fieldtitle_str)
                if len(datatoinsert_lst):
                    for datavalue_obj in datatoinsert_lst:
                        sub_qstr = '{}'.format(datavalue_obj)
                        if fieldtitle_str[-4:] == '_str':
                            sub_qstr = '"{}"'.format(sub_qstr)
                        sub_qstr += ', '
                else:
                    continue


class Initializer:
    '''Class for instance schema'''
    def __init__(self, schematitle_str, schema_dc, database_obj):
        '''schema_dc - {'tablename1_str':['attr1_str','attr2_str', 'attr3_str'], 'tablename2_str':...}'''
        self.database_obj = database_obj
        self.schematitle_str = schematitle_str
        self.schema_dc = schema_dc
        self.needtocreatetables_dc = dict()
        self.engine_str = ' ENGINE=INNODB DEFAULT CHARSET=utf8 '

    def makeddl_fc(self, table_str):
        '''Function for making DDL script from dictionary
        foreignkeytables_lst - uses for instance tables in correct sequence
        '''
        attrs_lst = self.schema_dc.get(table_str)
        if len(attrs_lst):
            foreignkeytables_lst = []
            ddl_str = ''
            if '.' not in table_str:
                ddl_str = 'CREATE TABLE if not exists {}.{} (\n'.format(self.schematitle_str, table_str)
            else:
                ddl_str = 'CREATE TABLE if not exists {} (\n'.format(table_str)
            ddl_foreignkeys_str = ''#concated with ddl_str for making foreign keys
            ddl_appendinx_str = ''#added at the end for creation unique indexes
            foreignkeyappend_int = 0
            for attr_str in attrs_lst:
                foreignkeyappend_int = 0
                if attr_str == 'id':
                    ddl_str += '\tid int auto_increment primary key, \n'
                elif attr_str == 'tstamp':
                    ddl_str += '\ttstamp timestamp default CURRENT_TIMESTAMP not null, \n'
                else:
                    attr_lst = attr_str.split('_')
                    if len(attr_lst) > 1:
                        checking_str = attr_lst[-1]
                        if len(attr_lst) > 2:
                            #branch for adding UNIQUE index of attribute to DDL for attrs with structure: xxx_index_yyy
                            if (attr_lst[-2]) == 'index':
                                if '.' not in table_str:
                                    ddl_appendinx_str += '\ncreate unique index {0}_{1}_uindex on {2}.{0} ({1});\n'.format(table_str, attr_str, self.schematitle_str)
                                else:
                                    ddl_appendinx_str += '\ncreate unique index {0}_{1}_uindex on {0} ({1});\n'.format(table_str, attr_str)
                        if checking_str == 'str':
                            ddl_str += '\t{} varchar(255) not null, \n'.format(attr_str)
                        elif checking_str == 'int':
                            ddl_str += '\t{} int default 0 not null, \n'.format(attr_str)
                        elif checking_str == 'id':
                            foreignkeyappend_int += 1
                            otherattribute_str = '_'.join(attr_lst[:-1])
                            if otherattribute_str in self.schema_dc:
                                ddl_foreignkeys_str += '\nconstraint {0}_{1}_fk foreign key ({1}) references {2} (id), \n'.format(table_str, attr_str, otherattribute_str)
                            ddl_str += '\t{} int, \n'.format(attr_str)
                            foreignkeytables_lst.append(otherattribute_str)
            if foreignkeyappend_int:
                ddl_foreignkeys_str = ddl_foreignkeys_str[:-3] + '\n){0};'.format(self.engine_str)
                ddl_str += ddl_foreignkeys_str
            else:
                ddl_str = ddl_str[:-3] + '\n){0};'.format(self.engine_str)
            return [ddl_str, ddl_appendinx_str], foreignkeytables_lst

    def instanceschema_fc(self):
        databases_lst_lst = self.database_obj.processquery_fc('SELECT schema_name FROM information_schema.schemata', 2)
        if len(databases_lst_lst):
            databases_lst = [databases_lst[0] for databases_lst in databases_lst_lst if databases_lst]
            if self.schematitle_str not in databases_lst:
                self.database_obj.processquery_fc('CREATE schema if not exists {}'.format(self.schematitle_str))

    def instancetables_fc(self):
        counter_int = 0
        tables_lst_lst = self.database_obj.processquery_fc('SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA LIKE "{}"'.format(self.schematitle_str), 2)
        instancedtables_lst = list()
        foreignkeytables_dc = dict()
        if len(tables_lst_lst):
            instancedtables_lst = [tables_lst[0] for tables_lst in tables_lst_lst if tables_lst]
        for table_str in self.schema_dc.keys():
            if table_str not in instancedtables_lst:
                ddls_lst, foreignkeytables_lst = self.makeddl_fc(table_str)
                self.needtocreatetables_dc.update({table_str: ddls_lst})
                foreignkeytables_dc.update({table_str: foreignkeytables_lst})
        #process of instancing
        # print(self.needtocreatetables_dc)
        # print('======+++++++++===========')
        # input('pause')
        if len(foreignkeytables_dc):
            instanced_lst = list()
            needtoinstance_set = set(foreignkeytables_dc.keys())
            while needtoinstance_set:
                for table_str, foreignkeytables_lst in foreignkeytables_dc.items():
                    if table_str not in instanced_lst:
                        if not len(foreignkeytables_lst):
                            ddls_lst = self.needtocreatetables_dc.get(table_str)
                            for ddl_str in ddls_lst:
                                if len(ddl_str):
                                    # !!hmm... i don't design convention to setup size of varchar field, so try to KOLXO3 solution for it
                                    ddl_str = ddl_str
                                    self.database_obj.processquery_fc(ddl_str)
                            instanced_lst.append(table_str)
                            needtoinstance_set.remove(table_str)
                            print('OK - instanced table {}'.format(table_str))
                            counter_int += 1
                            # input('PRESS ENTER TO PROCEED...')
                        else:
                            control_set= set()
                            for foreigntable_str in foreignkeytables_lst:
                                if foreigntable_str in instanced_lst:
                                    control_set.add(foreigntable_str)
                            if len(list(control_set)) == len(foreignkeytables_lst):
                                ddls_lst = self.needtocreatetables_dc.get(table_str)
                                for ddl_str in ddls_lst:
                                    if len(ddl_str):
                                        #!!hmm... i don't design convention to setup size of varchar field, so try to KOLXO3 solution for it
                                        ddl_str = ddl_str
                                        self.database_obj.processquery_fc(ddl_str)
                                instanced_lst.append(table_str)
                                needtoinstance_set.remove(table_str)
                                print('OK - instanced table {}'.format(table_str))
                                counter_int += 1
                                # input('PRESS ENTER TO PROCEED...')
                            # else:
                            #     print('ER - {} need to be instanced later'.format(table_str))
                            #     continue
                    # print('OK - STEP of infinity while LOOP finished. Data inside the set: ', needtoinstance_set)
        print('ALL TABLES INSTANCED...')
        return counter_int

    def process_fc(self):
        if self.database_obj:
            self.instanceschema_fc()
            return self.instancetables_fc()

    def completecustomddl_fc(self, query_str):
        '''Function for complete custom ddl script used for instance relation between current database
         and other non-based-on-convention database'''
        if query_str.lower()[:6] == 'create':
            if self.database_obj:
                try:
                    self.database_obj.processquery_fc(query_str)
                    return 1
                except Exception as e:
                    print(e)
                    return 0
