#coding: utf-8
#Этот скрипт будет создавать вместо меня базовое приложение. Любое. Я устал, блядь. Устал от Себя и своей беспросветной тупости
#устал тысячу раз писать одно и то же говно, которое не работает. Я хочу писать один раз. Один, сука, раз, но красиво.
#Вдохновение, приди... приди!! кому сказал?!... блиин...

#Короче, этот скрипт просто будет создавать все эти дебильные папки и именно те файлы, которые используются в любом моём приложении:
#на-подобие этих settings, database и т.п.

import os, sys, urllib.request

APPTITLE_str = 'app'

ROOTDIRPATH_str = os.getcwd()

BASICFILENAMES_lst = ['main.py', 'settings.py', 'database.py', 'initialdata.txt']

FOLDERSMAP_dc = {
    APPTITLE_str:{
        'bin': [BASICFILENAMES_lst[1], BASICFILENAMES_lst[2]],
        'data': {
            'input': [BASICFILENAMES_lst[3]],
            'output': [],
            'logs': []
        },
    }
}

DATABASECLASSURL_str = 'https://raw.github.com/lavr2004/apptemplate/master/app/bin/database.py'
SETTINGSCLASSURL_str = 'https://raw.githubusercontent.com/lavr2004/apptemplate/master/app/bin/settings.py'
APPCLASSURL_str = 'https://raw.githubusercontent.com/lavr2004/apptemplate/master/app/app.py'

BASICFILESCONTENTURLS_dc = {
    BASICFILENAMES_lst[0]: '',
    BASICFILENAMES_lst[1]: SETTINGSCLASSURL_str,
    BASICFILENAMES_lst[2]: DATABASECLASSURL_str,
    BASICFILENAMES_lst[3]: ''
}


class Filesystem():
    '''Filesystem class contains methods for operating on file system'''
    def __init__(self, filesystemstructure_dc):
        self.filesystemstructure_dc = filesystemstructure_dc

    def process_fc(self, rootdirpath_str, apptitle_str):
        mainpath_str = os.path.join(rootdirpath_str, apptitle_str)
        self.makefile_fc(mainpath_str, BASICFILENAMES_lst[0])  # creation main.py
        self.makedirsstructure_fc(mainpath_str, FOLDERSMAP_dc)  # creation folders structure
        apppath_str = os.path.join(mainpath_str, APPTITLE_str)
        self.makefile_fc(apppath_str, '{}.py'.format(APPTITLE_str))  # creation applition file in root application folder

    def checkfolderandcreate_recursive_fc(self, folderpath_str):
        '''Method for recursive checking and creating folders by path'''
        if not os.path.isdir(folderpath_str):
            try:
                os.mkdir(folderpath_str)
            except:
                self.checkfolderandcreate_recursive_fc(os.path.dirname(folderpath_str))
                try:
                    os.mkdir(folderpath_str)
                except Exception as e:
                    print(e)
        print('OK - folder "{}" created'.format(folderpath_str))

    def checkfolderandcreate_usual_fc(self, folderpath_str):
        '''Method for checking and creation folders by path usually'''
        folderstocreate_lst = list()
        while True:
            if not os.path.isdir(folderpath_str):
                folderstocreate_lst.append(folderpath_str)
            else:
                break
            folderpath_str = os.path.dirname(folderpath_str)
        while folderstocreate_lst:
            os.mkdir(folderstocreate_lst.pop(-1))

    def generaterandompath_fc(self, minsize_int=3, maxsize_int=7):
        '''Method for generation random path with deep in random range'''
        import random
        deep_int = random.randrange(minsize_int, maxsize_int)
        basepath_str = ROOTDIRPATH_str
        while deep_int:
            foldertitle_str = ''
            foldersize_int = random.randint(minsize_int, maxsize_int)
            for n in range(foldersize_int):
                foldertitle_str += chr(random.randint(65, 90))
            basepath_str = os.path.join(basepath_str, foldertitle_str)
            deep_int -= 1
        return basepath_str

    def makefile_fc(self, dirpath_str, filetitle_str):
        '''Function for making file inside the folder and filling content of it with code'''
        filepath_str = os.path.join(dirpath_str, filetitle_str)
        self.checkfolderandcreate_usual_fc(dirpath_str)
        if not os.path.isfile(filepath_str):
            with open(filepath_str, 'w', encoding='utf-8-sig', errors='ignore') as fa:
                data_str = self._getdatafromgit_fc(filetitle_str)
                fa.write(data_str)

    def _getdatafromgit_fc(self, filetitle_str):
        url_str = BASICFILESCONTENTURLS_dc.get(filetitle_str)
        if isinstance(url_str, str):
            if len(url_str):
                data_str = Webcommunitation().gettextfromresponse_fc(url_str)
                return data_str
        return ''

    def makedirsstructure_fc(self, rootpath_str, dirs_dc):
        '''Function for making paths from dirs dictionary and creation fodlers file system'''
        if isinstance(dirs_dc, dict):
            self.checkfolderandcreate_usual_fc(rootpath_str)
            for foldertitle_str, subfolders_obj in dirs_dc.items():
                if foldertitle_str:
                    subfolderpath_str = os.path.join(rootpath_str, foldertitle_str)
                    if isinstance(subfolders_obj, dict):
                        self.makedirsstructure_fc(subfolderpath_str, subfolders_obj)
                    elif isinstance(subfolders_obj, list):
                        self.makefile_fc(subfolderpath_str, '__init__.py')
                        for filetitle_str in subfolders_obj:
                            self.makefile_fc(subfolderpath_str, filetitle_str)

class Webcommunitation():

    def __int__(self):
        self.response_obj = None
        self.status_int = 0

    def _resetselfdata_fc(self):
        self.status_int = 0
        self.response_obj = None

    def getcodefromgit_fc(self, filetitle_str):
        giturl_str = BASICFILESCONTENTURLS_dc.get(filetitle_str)
        if isinstance(giturl_str, str):
            if len(giturl_str):
                self.process_fc(giturl_str)

    def process_fc(self, url_str):
        self._resetselfdata_fc()
        self.response_obj = urllib.request.urlopen(url_str)
        if self.response_obj:
            self.status_int = 1

    def gettextfromresponse_fc(self, url_str):
        '''Method for getting html code'''
        self.process_fc(url_str)
        if self.status_int:
            bytes_obj = self.response_obj.read()
            if bytes_obj:
                data_str = bytes_obj.decode('utf-8')
                return data_str
        return ''

def process_instancefilesystem_fc():
    '''Main operational branch for making environment of filesystem'''
    filesystem_obj = Filesystem(FOLDERSMAP_dc)
    filesystem_obj.process_fc(ROOTDIRPATH_str, APPTITLE_str)

def main():
    process_instancefilesystem_fc()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        FOLDERSMAP_dc[sys.argv[1]] = FOLDERSMAP_dc.get(APPTITLE_str)
        FOLDERSMAP_dc.pop(APPTITLE_str)
        APPTITLE_str = sys.argv[1]
    BASICFILENAMES_lst.append('{}.py'.format(APPTITLE_str))
    BASICFILESCONTENTURLS_dc.update({BASICFILENAMES_lst[-1]: APPCLASSURL_str})
    main()