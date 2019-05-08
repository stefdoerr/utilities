#!/home/stefan/Software/miniconda3/bin/python 

import os
from peewee import SqliteDatabase, Model, CharField
import datetime

dbloc = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'projects.db')
db = SqliteDatabase(dbloc)

class BaseModel(Model):
    class Meta:
        database = db

class Projects(BaseModel):
    name = CharField(unique=True)
    local_path = CharField(unique=True)
    # remote = CharField(unique=False)
    # remote_port = CharField(unique=False)
    remote_path = CharField(unique=True)


def init():
    db.connect()
    db.create_tables([Projects,])

def add_project(name, local_path, remote_path):
    Projects.create(name=name, local_path=local_path, remote_path=remote_path)

def sync(projname, mode):
    row = Projects.get(Projects.name == projname)
    if mode == 'send':
        inp = input('Are you sure you want to send files? This might overwrite remote results! [Y/n]')
        if inp.lower() == 'n':
            return
        command = 'rsync -rav --info=progress2 {} {}'.format(row.local_path, row.remote_path)
        print(command)
        os.system(command)
    elif mode == 'retrieve':
        command = 'rsync -rav --info=progress2 {} {}'.format(row.remote_path, row.local_path)
        print(command)
        os.system(command)
        

def list_projects():
    query = Projects.select()
    print('Name: local path <-> remote path')
    print('--------------------------------')
    for row in query:
        print('{}: {} <-> {}'.format(row.name, row.local_path, row.remote_path))


def goto(projname, mode):
    """ Add this to your bashrc to make this work:

    function pmgoto()
    {
        cd $(python /path/to/pm goto "$1")
    }
    """

    row = Projects.get(Projects.name == projname)
    if mode == 'local':
        print(row.local_path)
    if mode == 'remote':
        print('-t {}'.format(row.remote_path))

if  __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Stefan\'s project manager')
    subparsers = parser.add_subparsers(metavar='{send,retrieve,add,list,init}', help='sub-command help', dest='subparser')

    parser_send = subparsers.add_parser('send', help='Send data to remote')
    parser_send.add_argument('projectname', type=str, help='The name of the project')

    parser_retr = subparsers.add_parser('retrieve', help='Retrieve data from remote')
    parser_retr.add_argument('projectname', type=str, help='The name of the project')

    parser_add = subparsers.add_parser('add', help='Add project to database')
    parser_add.add_argument('projectname', type=str, help='The name of the project')
    parser_add.add_argument('localpath', type=str, help='The local path of the project')
    parser_add.add_argument('remotepath', type=str, help='The remote path of the project')

    parser_list = subparsers.add_parser('list', help='List all projects')
    parser_init = subparsers.add_parser('init', help='Initialize DB')

    parser_goto = subparsers.add_parser('goto', help=argparse.SUPPRESS, description='DONTUSE: Changes directory. Use this only with the pmgoto shell command in the bashrc.')
    parser_goto.add_argument('projectname', type=str, help='The name of the project')

    parser_gotor = subparsers.add_parser('gotor', help=argparse.SUPPRESS, description='DONTUSE: Changes to remote directory. Use this only with the pmgotor shell command in the bashrc.')
    parser_gotor.add_argument('projectname', type=str, help='The name of the project')

    arguments = sys.argv[1:] if len(sys.argv) > 1 else ['-h']
    args = parser.parse_args(args=arguments)

    if args.subparser == 'send':
        sync(args.projectname, 'send')
    elif args.subparser == 'retrieve':
        sync(args.projectname, 'retrieve')
    elif args.subparser == 'add':
        add_project(args.projectname, args.localpath, args.remotepath)
    elif args.subparser == 'list':
        list_projects()
    elif args.subparser == 'init':
        init()
    elif args.subparser == 'goto':
        goto(args.projectname, mode='local')
    elif args.subparser == 'gotor':
        goto(args.projectname, mode='remote')





    
