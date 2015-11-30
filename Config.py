# -*- coding:utf-8 -*-
"""
Config Class.
"""
__author__ = 'Jux.Liu'


class Config(object):
    """Class for app configs, contain messages, error messages and error message functions.

    config=Config()
    """
    MSG_CODE = {
        10: 'Zip file {0} success !\nZip file in {1}.',
        11: 'Zip folder {0} success !\nZip file in {1}.',
        12: 'Unzip file {0} success !\nFile/Folder in {1}.',

        13: 'New version: {0}',
        14: 'New version: {0}\n\n'
            '{1} \nwill be deleted,\n'
            '{2} \nwill be run after process,\n'
            '{3} \nwill be installed/updated,\n'
            '{4} \nwill be run if updates failed.',
        15: '{0} \nwill be stored for backup.',
        16: 'No file need to be stored.',

        17: '',

        18: 'Delete file {0} success.',
        19: 'Delete folder {0} success.',
        20: 'Move file {0} to {1} success.',
        21: 'Move folder {0} to {1}  success.',
        22: 'Copy file {0} to {1}  success.',
        23: 'Copy folder {0} to {1}  success.',
    }

    ERR_CODE = {
        10: 'Cannot zip up file {0}.\nError message: {1}',
        11: 'Cannot zip folder {0}.\nError message: {1}',
        12: 'Cannot unzip file {0} to {1}.\nError message: {1}',

        13: 'File {0} not found, please check.',
        14: 'Folder {0} not found, please check.',

        15: 'Unknow update type.',
        16: 'Unkow filename extension.',
        17: 'Illegal type of filename extension, please use [], {}, () or set.',

        18: 'Delete file {0} failed.\nError message: {1}',
        19: 'Delete folder {0} failed.\nError message: {1}',
        20: 'Move file {0} failed.\nError message: {1}',
        21: 'Move folder {0} failed.\nError message: {1}',
        22: 'Copy file {0} failed.\nError message: {1}',
        23: 'Copy folder {0} failed.\nError message: {1}',
    }

    def zip_file_exception(self, fileName, exception):
        """Return error message when zip file failed."""
        result = False
        msg = self.ERR_CODE[10].format(fileName, exception)
        return {'result': result, 'msg': msg}

    def zip_folder_exception(self, folderPath, exception):
        """Return error message when zip folder failed."""
        result = False
        msg = self.ERR_CODE[11].format(folderPath, exception)
        return {'result': result, 'msg': msg}

    def unzip_exception(self, fileName, exception):
        """Return error message when unzip file failed."""
        result = False
        msg = self.ERR_CODE[12].format(fileName, exception)
        return {'result': result, 'msg': msg}

    def no_file_error(self, fileName):
        """Return error message when file not found."""
        result = False
        msg = self.ERR_CODE[13].format(fileName)
        return {'result': result, 'msg': msg}

    def no_folder_error(self, folderPath):
        """Return error message when folder not found."""
        result = False
        msg = self.ERR_CODE[14].format(folderPath)
        return {'result': result, 'msg': msg}

    def unknow_update_type(self):
        """Return error message when update type unknow"""
        result = False
        msg = self.ERR_CODE[15]
        return {'result': result, 'msg': msg}

    def unknow_ext(self):
        """Return error message when ext unknow"""
        result = False
        msg = self.ERR_CODE[16]
        return {'result': result, 'msg': msg}

    def illegal_ext_set(self):
        """Return error message when ext set illegal"""
        result = False
        msg = self.ERR_CODE[17]
        return {'result': result, 'msg': msg}

    def delete_file_exception(self, fileName, exception):
        """Return error message when delete file failed."""
        result = False
        msg = self.ERR_CODE[18].format(fileName, exception)
        return {'result': result, 'msg': msg}

    def delete_folder_exception(self, folderPath, exception):
        """Return error message when delete folder failed."""
        result = False
        msg = self.ERR_CODE[19].format(folderPath, exception)
        return {'result': result, 'msg': msg}

    def move_file_exception(self, fileName, exception):
        """Return error message when move file failed."""
        result = False
        msg = self.ERR_CODE[20].format(fileName, exception)
        return {'result': result, 'msg': msg}

    def move_folder_exception(self, folderPath, exception):
        """Return error message when move folder failed."""
        result = False
        msg = self.ERR_CODE[21].format(folderPath, exception)
        return {'result': result, 'msg': msg}

    def copy_file_exception(self, fileName, exception):
        """Return error message when copy file failed."""
        result = False
        msg = self.ERR_CODE[22].format(fileName, exception)
        return {'result': result, 'msg': msg}

    def copy_folder_exception(self, folderPath, exception):
        """Return error message when copy folder failed."""
        result = False
        msg = self.ERR_CODE[23].format(folderPath, exception)
        return {'result': result, 'msg': msg}
