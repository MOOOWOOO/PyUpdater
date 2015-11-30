# -*- coding:utf-8 -*-
"""
    
"""
import argparse

__author__ = 'Jux.Liu'


def update(args):
    print('Start update process...')




def rollback():
    pass


def check():
    pass


if __name__ == '__main__':
    desc = '''This Tool is for Mostfun Control Panel Check, Update and Rollback'''
    parser = argparse.ArgumentParser(description=desc)

    # update command
    subparsers = parser.add_subparsers(help="Tool command args")
    updater = subparsers.add_parser('update',
                                    help='Update the control panel package. '
                                         'Input the source folder and target filder.')

    updater.add_argument('-p', '--package-folder',
                         required=True, action='store',
                         help='package folder path')
    updater.add_argument('-b', '--backup-folder',
                         required=True, action='store',
                         help='backup folder path')
    updater.add_argument('-z', '--zip-file',
                         required=True, action='store',
                         help='zip file path *and* file name')

    updater.set_defaults(func=update)

    # rollback command
    rollbacker = subparsers.add_parser('rollback',
                                       help='Rollback the control panel package '
                                            'to the last stable version.')
    rollbacker.set_defaults(func=rollback)

    # check command
    checker = subparsers.add_parser('check',
                                    help="Check the control panel package's integrity.")
    checker.set_defaults(func=check)

    args = parser.parse_args()
    args.func(args)

    # test part
    # args = {'backup_folder': r'D:\Projects\python\updater-test\backup',
    #         'package_folder': r'D:\Projects\python\updater-test\package',
    #         'zip_file': r'D:\Projects\python\updater-test\p.zip'}
    #
    # update(args)
