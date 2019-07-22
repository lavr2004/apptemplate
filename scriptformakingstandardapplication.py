#coding: utf-8
#Этот скрипт будет создавать вместо меня базовое приложение. Любое. Я устал, блядь. Устал от Себя и своей беспросветной тупости
#устал тысячу раз писать одно и то же говно, которое не работает. Я хочу писать один раз. Один, сука, раз, но красиво.
#Вдохновение, приди... приди!! кому сказал?!... блиин...

#Короче, этот скрипт просто будет создавать все эти дебильные папки и именно те файлы, которые используются в любом моём приложении:
#на-подобие этих settings, database и т.п.

import os, sys, urllib

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


BASICFILESCONTENT_dc = {
    BASICFILENAMES_lst[0]:'',
    BASICFILENAMES_lst[1]:'',
    BASICFILENAMES_lst[2]:''
}


def checkfolderandcreate_recursive_fc(folderpath_str):
    if not os.path.isdir(folderpath_str):
        try:
            os.mkdir(folderpath_str)
        except:
            checkfolderandcreate_recursive_fc(os.path.dirname(folderpath_str))
            try:
                os.mkdir(folderpath_str)
            except Exception as e:
                print(e)
    print('OK - folder "{}" created'.format(folderpath_str))

def checkfolderandcreate_usual_fc(folderpath_str):
    folderstocreate_lst = list()
    while True:
        if not os.path.isdir(folderpath_str):
            folderstocreate_lst.append(folderpath_str)
        else:
            break
        folderpath_str = os.path.dirname(folderpath_str)
    while folderstocreate_lst:
        os.mkdir(folderstocreate_lst.pop(-1))

def generaterandompath_fc(minsize_int = 3, maxsize_int = 7):
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


def makefile_fc(dirpath_str, filetitle_str):
    '''Function for making file inside the folder and filling content of it with code'''
    filepath_str = os.path.join(dirpath_str, filetitle_str)
    checkfolderandcreate_usual_fc(dirpath_str)
    if not os.path.isfile(filepath_str):
        with open(filepath_str, 'w', encoding='utf-8-sig', errors='ignore') as fa:
            fa.write('lol')

def makedirsstructure_fc(rootpath_str, dirs_dc):
    '''Function for making paths from dirs dictionary and creation fodlers file system'''
    if isinstance(dirs_dc, dict):
        checkfolderandcreate_usual_fc(rootpath_str)
        for foldertitle_str, subfolders_obj in dirs_dc.items():
            if foldertitle_str:
                subfolderpath_str = os.path.join(rootpath_str, foldertitle_str)
                if isinstance(subfolders_obj, dict):
                    makedirsstructure_fc(subfolderpath_str, subfolders_obj)
                elif isinstance(subfolders_obj, list):
                    makefile_fc(subfolderpath_str, '__init__.py')
                    for filetitle_str in subfolders_obj:
                        makefile_fc(subfolderpath_str, filetitle_str)

def main():
    mainpath_str = os.path.join(ROOTDIRPATH_str, APPTITLE_str)
    makefile_fc(mainpath_str, BASICFILENAMES_lst[0])#creation main.py
    makedirsstructure_fc(mainpath_str, FOLDERSMAP_dc)#creation folders structure
    apppath_str = os.path.join(mainpath_str, APPTITLE_str)
    makefile_fc(apppath_str, '{}.py'.format(APPTITLE_str))#creation applition file


if __name__ == '__main__':
    if len(sys.argv) > 1:
        FOLDERSMAP_dc[sys.argv[1]] = FOLDERSMAP_dc.get(APPTITLE_str)
        FOLDERSMAP_dc.pop(APPTITLE_str)
        APPTITLE_str = sys.argv[1]
    main()