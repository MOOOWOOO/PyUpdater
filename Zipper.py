# !/usr/bin/env python
# coding: utf-8
'''
    zip folders & unzip zip-files
'''
from zipfile import ZipFile, ZIP_DEFLATED, BadZipfile
from os import path, walk, mkdir

from Config import Config
from FileManger import Checker
from PlatformSelector import Platform

__author__ = 'Jux.Liu'


class Zipper(object):
    """Class with methods to zip or unzip files.

    zipper=Zipper(sourcePath='...')
    sourcePath: The default source path
                contains the files/folders need to be zipped or unzipped.
    """

    def __init__(self, sourcePath=''):
        self.platform = Platform()
        self.config = Config()
        self.checker = Checker()
        self.sourcePath = self.checker.path_full(sourcePath if self.checker.check_path(sourcePath) \
                                        and sourcePath not in [r'./', r'.'] \
            else self.platform.tmpFolder)


    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def zip_file(self, fileName, targetPath):
        MSG = self.config.MSG_CODE

        if self.checker.check_path(targetPath):
            targetPath = self.checker.path_full(targetPath)
            fileName_NEW = '{0}{1}'.format(self.sourcePath, fileName)

            if self.checker.check_file(fileName):
                pass

            elif self.checker.check_file(fileName_NEW):
                fileName = fileName_NEW

            else:
                return self.config.no_file_error(fileName=fileName)

            zipFile = object()

            try:
                zipFile = ZipFile(file=targetPath,
                                  mode='a',
                                  compression=ZIP_DEFLATED)

                zipFile.write(filename=fileName,
                              arcname=fileName,
                              compress_type=ZIP_DEFLATED)

            except Exception as e:
                zipFile.close()
                return self.config.zip_file_exception(fileName=fileName,
                                                      exception=e)

            else:
                result = True
                msg = MSG[10].format(fileName, targetPath)

            finally:
                zipFile.close()
                return {'result': result, 'msg': msg}

        else:
            return self.config.no_folder_error(targetPath)

    def zip_folder(self, folderPath, targetPath):
        MSG = self.config.MSG_CODE

        if self.checker.check_path(folderPath):
            if self.checker.check_path(targetPath):
                folderPath = self.checker.path_full(folderPath)
                targetPath = self.checker.path_full(targetPath)

                parentFolder = self.checker.path_full(path.dirname(folderPath))

                zipFile = object()
                fileName = '{0}{1}'.format(targetPath,
                                           folderPath.split(
                                               self.platform.pathSplit)[-1])

                try:
                    zipFile = ZipFile(file=fileName,
                                      mode='a',
                                      compression=ZIP_DEFLATED)

                    for dirpath, dirnames, filenames in walk(folderPath):
                        for dirname in dirnames:
                            abs_path = path.join(dirpath, dirname)
                            rel_path = abs_path.replace(parentFolder, '')
                            zipFile.write(filename=abs_path,
                                          arcname=rel_path,
                                          compress_type=ZIP_DEFLATED)

                        for filename in filenames:
                            abs_path = path.join(dirpath, filename)
                            rel_path = abs_path.replace(parentFolder, '')
                            zipFile.write(filename=abs_path,
                                          arcname=rel_path,
                                          compress_type=ZIP_DEFLATED)

                except IOError as e:
                    zipFile.close()
                    return self.config.zip_folder_exception(folderPath, e)

                except OSError as e:
                    zipFile.close()
                    return self.config.zip_folder_exception(folderPath, e)

                except BadZipfile as e:
                    zipFile.close()
                    return self.config.zip_folder_exception(folderPath, e)

                except Exception as e:
                    zipFile.close()
                    return self.config.zip_folder_exception(folderPath, e)

                else:
                    result = True
                    msg = MSG[11].format(folderPath, targetPath)

                finally:
                    zipFile.close()
                    return {'result': result, 'msg': msg}

            else:
                return self.config.no_folder_error(targetPath)
        else:
            return self.config.no_folder_error(folderPath)

    def unzip(self, zipfileName, targetPath):
        MSG = self.config.MSG_CODE
        if self.checker.check_path(targetPath):
            zipfileName_NEW = '{0}{1}'.format(self.sourcePath, zipfileName)
            if self.checker.check_file(zipfileName):
                pass

            elif self.checker.check_file(zipfileName_NEW):
                zipfileName = zipfileName_NEW

            else:
                self.config.no_file_error(fileName=zipfileName)

                unzipFile = object()
                fileHandle = object()

            try:
                unzipFile = ZipFile(file=zipfileName)
                fileList = unzipFile.namelist()

                for fileName in fileList:
                    if fileName.endswoth(self.platform.pathSplit):
                        mkdir(path=path.join(targetPath, fileName))
                    else:
                        fileHandle = open(path.join(targetPath, fileName), 'wb')
                        fileHandle.write(unzipFile.read(fileName))

            except Exception as e:
                fileHandle.close()
                unzipFile.close()
                self.config.unzip_exception(fileName=zipfileName,
                                            exception=e)

            else:
                result = True
                msg = MSG[12].format(zipfileName, targetPath)

            finally:
                fileHandle.close()
                unzipFile.close()
                return {'result': result, 'msg': msg}

        else:
            return self.config.no_folder_error(targetPath)
