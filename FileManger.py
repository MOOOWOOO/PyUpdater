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
        checker = self.checker
        config = self.config

        fileName_NEW = '{0}{1}'.format(self.sourcePath, fileName)
        if checker.check_file(fileName):
            pass
        elif checker.check_file(fileName_NEW):
            fileName = fileName_NEW
        else:
            return self.config.no_file_error(fileName)

        from configobj import ConfigObj
        configFile = ConfigObj(fileName)
        info = configFile['info']
        updateType = info['type']

        MSG = config.MSG_CODE
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
            return config.unknow_update_type()

    def list_folder_files(self, folderPath, ext, traversal=False):
        checker = self.checker
        config = self.config

        if checker.check_path(folderPath):
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

                MSG = config.MSG_CODE
                if len(fileList) > 0:
                    msg = MSG[15].format(sorted(fileList))

                else:
                    msg = MSG[16]

                result = True
                return {'result': result, 'msg': msg}

            else:
                return config.illegal_ext_set()
        else:
            return config.no_folder_error(folderPath=folderPath)

    def delete_file(self, fileName):
        checker = self.checker
        config = self.config

        fileName_NEW = '{0}{1}'.format(self.sourcePath, fileName)
        if checker.check_file(fileName):
            pass
        elif checker.check_file(fileName_NEW):
            fileName = fileName_NEW
        else:
            return config.no_file_error(fileName)

        MSG = config.MSG_CODE
        try:
            remove(fileName)
            result = True
            msg = MSG[18].format(fileName)

        except Exception as e:
            return config.delete_file_exception(fileName=fileName,
                                                exception=e)

        finally:
            return {'result': result, 'msg': msg}

    def delete_folder(self, folderPath):
        checker = self.checker
        config = self.config

        if checker.check_path(folderPath):
            MSG = config.MSG_CODE

            import shutil
            try:
                shutil.rmtree(folderPath)
                result = True
                msg = MSG[19].format(folderPath)

            except Exception as e:
                return config.delete_folder_exception(folderPath=folderPath,
                                                      exception=e)

            finally:
                return {'result': result, 'msg': msg}

        else:
            return config.no_folder_error(folderPath=folderPath)

    def copy_file(self, fileName, targetPath):
        checker = self.checker
        config = self.config

        if checker.check_path(targetPath):
            fileName_NEW = '{0}{1}'.format(self.sourcePath, fileName)

            if checker.check_file(fileName):
                pass

            elif checker.check_file(fileName_NEW):
                fileName = fileName_NEW

            else:
                return config.no_file_error(fileName)

            MSG = config.MSG_CODE
            sourceFile = path.join(path.dirname(fileName),
                                   path.basename(fileName))
            targetFile = path.join(targetPath,
                                   path.basename(fileName))

            with open(targetFile, 'wb') as targetfile:
                with open(sourceFile, 'rb') as sourcefile:
                    targetfile.write(sourcefile)

            result = True
            msg = MSG[22].format(fileName, targetPath)
            return {'result': result, 'msg': msg}

        else:
            return config.no_folder_error(folderPath=targetPath)

    def copy_folder(self, folderPath, targetPath):
        checker = self.checker
        config = self.config

        if checker.check_path(folderPath):
            if checker.check_path(targetPath):
                folderPath = checker.path_full(folderPath)
                targetPath = checker.path_full(targetPath)

                MSG = config.MSG_CODE
                for fileItem in listdir(folderPath):
                    sourceFileObj = path.join(folderPath, fileItem)
                    targetFileObj = path.join(targetPath, fileItem)

                    dotFlag = True  # '.' dot sign in filname or not
                    if checker.check_file(sourceFileObj):
                        if checker.check_path(targetPath):
                            pass

                        else:
                            makedirs(targetPath)

                        if '.' in targetFileObj:
                            if targetFileObj.rsplit('.', 1)[1] in self.banExtList:
                                dotFlag = False

                            else:
                                pass

                        targetFileSize = path.getsize(targetFileObj)
                        sourceFileSize = path.getsize(sourceFileObj)
                        if dotFlag and not checker.check_file(targetFileObj) \
                                or (checker.check_file(targetFileObj)
                                    and targetFileSize != sourceFileSize):

                            with open(targetFileObj, 'wb') as targetFile:
                                with open(sourceFileObj, 'rb') as sourceFile:
                                    targetFile.write(sourceFile)

                        else:
                            pass

                    elif checker.check_path(sourceFileObj):
                        self.copy_folder(sourceFileObj, targetFileObj)
            else:
                return config.no_folder_error(folderPath=targetPath)

        else:
            return config.no_folder_error(folderPath=folderPath)

    def move_file(self, fileName, targetPath):
        checker = self.checker
        config = self.config

        if checker.check_path(targetPath):
            fileName_NEW = '{0}{1}'.format(self.sourcePath, fileName)
            if checker.check_file(fileName):
                pass
            elif checker.check_file(fileName_NEW):
                fileName = fileName_NEW
            else:
                return config.no_file_error(fileName)

            cp = self.copy_file(fileName=fileName,
                                targetPath=targetPath)

            if cp['result']:
                rm = self.delete_file(fileName=fileName)

                if rm['result']:
                    MSG = config.MSG_CODE
                    result = True
                    msg = MSG[20].format(fileName, targetPath)
                    return {'result': result, 'msg': msg}

                else:
                    return config.move_file_exception(fileName=fileName,
                                                      exception=rm['msg'])

            else:
                return config.move_file_exception(fileName=fileName,
                                                  exception=cp['msg'])

        else:
            return config.no_folder_error(folderPath=targetPath)

    def move_folder(self, folderPath, targetPath):
        checker = self.checker
        config = self.config

        if checker.check_path(folderPath):
            if checker.check_path(targetPath):
                cp = self.copy_folder(folderPath=folderPath,
                                      targetPath=targetPath)

                if cp['result']:
                    rm = self.delete_folder(folderPath=folderPath)

                    if rm['result']:
                        MSG = config.MSG_CODE
                        result = True
                        msg = MSG[21].format(folderPath, targetPath)
                        return {'result': result, 'msg': msg}

                    else:
                        return config.move_folder_exception(folderPath=folderPath,
                                                            exception=rm['msg'])

                else:
                    return config.move_folder_exception(folderPath=folderPath,
                                                        exception=cp['msg'])

            else:
                return config.no_folder_error(folderPath=targetPath)

        else:
            return config.no_folder_error(folderPath=folderPath)


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
