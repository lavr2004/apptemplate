﻿# coding: utf-8
import os
from .database import Initializer

LOGIN_str = 'lavr2004'
PASSWORD_str = '1402'
HOST_str = '10.0.0.126'
SCHEMA_str = 'app'

class Settings:
    '''Default object with settings to all applicaitons based on it'''
    settingsfoldertitle_str = 'settings'
    binfoldertitlte_str = 'bin'
    datafoldertitle_str = 'data'
    inputfoldertitle_str = 'input'
    outputfoldertitle_str = 'output'
    logfoldertitle_str = 'logs'

    def __init__(self, initializer_obj = None, database_obj=None, appfoldertitle_str='app'):
        # database settings
        self.appfoldertitle_str = self.schematitle_str = appfoldertitle_str
        self.schema_dc = {'portal': ['id', 'portal_str'],
                          'country': ['id', 'country_str'],
                          'status': ['id', 'status_str'],
                          'portallink': ['id', 'portal_id', 'country_id', 'status_id' ,'portallink_str', 'tstamp'],
                          'data': ['id', 'jobtitle_str', 'location_str', 'contracttype_str', 'salary_str', 'descr_str', 'url_str'],
                          'refkey': ['id', 'data_id', 'refkey_index_str']}
        # dictionary with initial table titles as a keys. Initial tables is completely normalized and need to be filled after datanase instamce
        self.grade1_tables_dc = {'portal':['portal_str'],
                                 'country':['country_str'],
                                 'status':['status_str']}
        self.grade2_tables_dc = {'portallink':['portal_id', 'country_id', 'status_id']}
        # os local environment settings
        self.database_obj = database_obj
        self.rootdirpath_str = os.getcwd()
        self.applicationpath_str = os.path.join(self.rootdirpath_str, self.appfoldertitle_str)
        self.systemdelimiter_str = '/'
        self.csvdelimiter_str = ';'
        self.txtdelimiter_str = '\t'
        # basic folders fierarchy
        self.folders_lst = [self.settingsfoldertitle_str,
                          self.binfoldertitlte_str,
                          {self.datafoldertitle_str:[self.inputfoldertitle_str,
                                                     self.outputfoldertitle_str,
                                                     self.logfoldertitle_str]}]
        self.paths_dc = dict()
        # logging directory
        self.inputfiletitle_str = 'initialdata.txt'
        self.__instanceenvironment_fc(database_obj, initializer_obj)

    def __str__(self):
        response_str = 'OK - root directory is: {}'.format(self.rootdirpath_str)
        for k, v in self.paths_dc.items():
            response_str += '\n{}\t-\t{}'.format(k, v)
        return response_str

    def __instanceenvironment_local_fc(self):
        '''Function for instance local working environment'''
        if self.rootdirpath_str[0] != self.systemdelimiter_str:
            self.systemdelimiter_str = '\\'
        self.__setpaths_cf(self.applicationpath_str, self.folders_lst)
        print('OK - local environment successfully instanced...')

    def __instanceenvironment_database_fc(self, database_obj, initializer_obj):
        '''Function for instance database working environment'''
        if database_obj:
            initializer_obj = Initializer(self.schematitle_str,
                                          self.schema_dc,
                                          database_obj)
            countinstanced_int = initializer_obj.process_fc()
            print('OK - {} objects instanced in database'.format(countinstanced_int))

    def __instanceenvironment_fc(self, database_obj, initializer_obj):
        '''Function for instance working evinronment'''
        self.__instanceenvironment_local_fc()
        self.__instanceenvironment_database_fc(database_obj, initializer_obj)

    def _makedcfromtupleslst_cf(self, data_tuple_lst, reverse_bool=False):
        '''Method for making dc data structure from tuples'''
        if len(data_tuple_lst) > 0:
            if reverse_bool:
                return {value: id for (id, value) in data_tuple_lst if value}
            return {id: value for (id, value) in data_tuple_lst if id}
        return dict()

    def makepathtofile_cf(self, folderpath_str, filetitle_str):
        return os.path.join(folderpath_str, filetitle_str)

    def __setpaths_cf(self, processdirpath_str, folders_lst):
        '''Function for setting paths to folders'''
        if folders_lst:
            for foldertitle_obj in folders_lst:
                if isinstance(foldertitle_obj, str):
                    foldertitle_str = foldertitle_obj
                    if foldertitle_str not in self.paths_dc:
                        checkingtpath_str = self.makepathtofile_cf(processdirpath_str, foldertitle_str)
                        if not os.path.isdir(checkingtpath_str):
                            os.mkdir(checkingtpath_str)
                        self.paths_dc.update({foldertitle_str: checkingtpath_str})
                else:
                    for foldertitle_str, subfolders_lst in foldertitle_obj.items():
                        checkingtpath_str = self.makepathtofile_cf(processdirpath_str, foldertitle_str)
                        if not os.path.isdir(checkingtpath_str):
                            os.mkdir(checkingtpath_str)
                        self.paths_dc.update({foldertitle_str: checkingtpath_str})
                        if isinstance(subfolders_lst, list):
                            if len(subfolders_lst):
                                self.__setpaths_cf(checkingtpath_str, subfolders_lst)

    def getfolderpath_cf(self, foldertitle_str):
        return self.paths_dc.get(foldertitle_str)

if __name__ == '__main__':
    test_obj = Settings(os.getcwd())
    print(test_obj)