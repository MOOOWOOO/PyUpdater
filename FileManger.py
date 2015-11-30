# -*- coding:utf-8 -*-
"""
    File Manager
    List, Move, Copy or Delete files and folders [Recursively].
    Read config files, check files, path.
"""

from os import access, path, R_OK, walk, remove, listdir, makedirs
from Config import Config
from PlatformSelector import Platform

__author__ = 'Jux.Liu'


class FileManager(object):
    """Class with methods to read config file, list files or folders and
       move/delete/copy files or folders.

    fileManager=FileManager(banExtList=[...]/'...', sourcePath='...')
    banExtList: Filename extensions list, add extensions into this list
                ignore this type of files on processing.
    sourcePath: The default source path
                contains the files need to be processed.
    """
    banExtList = ['pyc', 'pyd', 'pyo']

    def __init__(self, banExtList=[], sourcePath=''):
        if len(banExtList):
            if isinstance(banExtList, str):
                self.banExtList.append(banExtList)

            elif isinstance(banExtList, list):
                self.banExtList.extend(banExtList)

            else:
                raise TypeError
        else:
            pass

        self.platform = Platform()
        self.config = Config()
        self.checker = Checker()
        self.sourcePath = self.checker.path_full(
            sourcePath if self.checker.check_path(sourcePath)
                          and sourcePath not in [r'./', r'.']
            else self.platform.tmpFolder)

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def get_update_config_info(self, fileName):
        fileName_NEW = '{0}{1}'.format(self.sourcePath, fileName)
        if self.checker.check_file(fileName):
            pass
        elif self.checker.check_file(fileName_NEW):
            fileName = fileName_NEW
        else:
            return self.config.no_file_error(fileName)

        from configobj import ConfigObj
        configFile = ConfigObj(fileName)
        info = configFile['info']
        updateType = info['type']

        MSG = self.config.MSG_CODE
        if updateType == '0':
            # all replace updates.
            result = True
            msg = MSG[13].format(info['version'])
            return {'result': result, 'msg': msg}

        elif updateType == '1':
            # increment updates.
            result = True
            msg = MSG[14].format(info['version'],
                                 configFile['delete'],
                                 configFile['launcher'],
                                 configFile['requirements'],
                                 configFile['rollback'])
            return {'result': result, 'msg': msg}

        else:
            return self.config.unknow_update_type()

    def list_folder_files(self, folderPath, ext, traversal=False):
        if self.checker.check_path(folderPath):
            if type(ext) in [list, dict, tuple, set]:
                fileList = []

                for root, dirs, files in walk(folderPath):
                    for filepath in files:
                        if traversal:
                            # if traversal all child-folders, use absolute path.
                            filepath = path.join(root, filepath)

                        else:
                            pass

                        fileList.append(filepath)

                MSG = self.config.MSG_CODE
                if len(fileList) > 0:
                    msg = MSG[15].format(sorted(fileList))

                else:
                    msg = MSG[16]

                result = True
                return {'result': result, 'msg': msg}

            else:
                return self.config.illegal_ext_set()
        else:
            return self.config.no_folder_error(folderPath=folderPath)

    def delete_file(self, fileName):
        fileName_NEW = '{0}{1}'.format(self.sourcePath, fileName)
        if self.checker.check_file(fileName):
            pass
        elif self.checker.check_file(fileName_NEW):
            fileName = fileName_NEW
        else:
            return self.config.no_file_error(fileName)

        MSG = self.config.MSG_CODE
        try:
            remove(fileName)
            result = True
            msg = MSG[18].format(fileName)

        except Exception as e:
            return self.config.delete_file_exception(fileName=fileName,
                                                     exception=e)

        finally:
            return {'result': result, 'msg': msg}

    def delete_folder(self, folderPath):
        if self.checker.check_path(folderPath):
            MSG = self.config.MSG_CODE

            import shutil
            try:
                shutil.rmtree(folderPath)
                result = True
                msg = MSG[19].format(folderPath)

            except Exception as e:
                return self.config.delete_folder_exception(folderPath=folderPath,
                                                           exception=e)

            finally:
                return {'result': result, 'msg': msg}

        else:
            return self.config.no_folder_error(folderPath=folderPath)

    def copy_file(self, fileName, targetPath):
        if self.checker.check_path(targetPath):
            fileName_NEW = '{0}{1}'.format(self.sourcePath, fileName)
            if self.checker.check_file(fileName):
                pass
            elif self.checker.check_file(fileName_NEW):
                fileName = fileName_NEW
            else:
                return self.config.no_file_error(fileName)
            MSG = self.config.MSG_CODE


        else:
            return self.config.no_folder_error(folderPath=targetPath)

    def copy_folder(self, folderPath, targetPath):
        if self.checker.check_path(folderPath):

            folderPath = self.checker.path_full(folderPath)
            targetPath = self.checker.path_full(targetPath)

            MSG = self.config.MSG_CODE
            for fileItem in listdir(folderPath):
                sourceFile = path.join(folderPath, fileItem)
                targetFile = path.join(targetPath, fileItem)

                subres = True
                if self.checker.check_file(sourceFile):
                    if self.checker.check_path(targetPath):
                        pass

                    else:
                        makedirs(targetPath)

                    if '.' in targetFile:
                        if targetFile.rsplit('.', 1)[1] in self.banExtList:
                            subres = False

                        else:
                            pass

                    if subres and not self.checker.check_file(targetFile) or (
                                self.checker.check_file(targetFile) and path.getsize(targetFile) != path.getsize(
                                sourceFile)):
                        with open(targetFile, 'wb') as tf:
                            with open(sourceFile, 'rb') as sf:
                                tf.write(sf)


                    else:
                        pass

                elif self.checker.check_path(sourceFile):
                    self.copy_folder(sourceFile, targetFile)

        else:
            return self.config.no_folder_error(folderPath=folderPath)

    def move_file(self, fileName, targetPath):
        if self.checker.check_path(targetPath):
            fileName_NEW = '{0}{1}'.format(self.sourcePath, fileName)
            if self.checker.check_file(fileName):
                pass
            elif self.checker.check_file(fileName_NEW):
                fileName = fileName_NEW
            else:
                return self.config.no_file_error(fileName)
            MSG = self.config.MSG_CODE



        else:
            return self.config.no_folder_error(folderPath=targetPath)

    def move_folder(self, folderPath, targetPath):
        if self.checker.check_path(folderPath):
            if self.checker.check_path(targetPath):
                cp = self.copy_folder(folderPath=folderPath,
                                      targetPath=targetPath)

                if cp['result']:
                    rm = self.delete_folder(folderPath=folderPath)

                    if rm['result']:
                        MSG = self.config.MSG_CODE
                        result = True
                        msg = MSG[21].format(folderPath, targetPath)
                        return {'result': result, 'msg': msg}

                    else:
                        return rm

                else:
                    return cp

            else:
                return self.config.no_folder_error(folderPath=targetPath)

        else:
            return self.config.no_folder_error(folderPath=folderPath)


class Checker(object):
    """Class with method to check if files or folders exists and pull their path.

    checker=Checker()
    """

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def check_path(self, PATH=''):
        if len(PATH):
            if path.exists(PATH):
                if path.isdir(PATH):
                    return True

                else:
                    return False

            else:
                return False

        else:
            raise BaseException

    def check_file(self, FILE=''):
        if len(FILE):
            if path.exists(FILE):
                if path.isfile(FILE) and access(FILE, R_OK):
                    return True

                else:
                    return False

            else:
                return False

        else:
            raise BaseException

    def path_full(self, PATH=''):
        if len(PATH):
            if not PATH.endswith(self.platform.pathSplit):
                return '{0}{1}'.format(PATH, self.platform.pathSplit)

            else:
                return PATH

        else:
            raise BaseException
