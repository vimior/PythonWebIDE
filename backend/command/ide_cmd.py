#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import os
import sys
import json
import shutil
import jedi
import time
import threading
import subprocess
from tornado import gen
from .utils import convert_path
from .resource import *
from .response import response
from common import define

PROJECT_IS_EXIST = -1
PROJECT_IS_NOT_EXIST = -2

DIR_IS_EXIST = -11
DIR_IS_NOT_EXIST = -12

FILE_IS_EXIST = -21
FILE_IS_NOT_EXIST = -22

if not os.path.exists(os.path.join(define.PROJECTS, 'ide')):
    os.makedirs(os.path.join(define.PROJECTS, 'ide'))


class IdeCmd(object):
    def __init__(self):
        pass

    @gen.coroutine
    def ide_list_projects(self, client, cmd_id, data):
        ide_path = os.path.join(define.PROJECTS, 'ide')
        code, projects = list_projects(ide_path)
        response(client, cmd_id, code, projects)

    @gen.coroutine
    def ide_get_project(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        code, project = get_project(prj_path)
        response(client, cmd_id, code, project)

    @gen.coroutine
    def ide_create_project(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        code, _ = create_project(prj_path, config_data={
            'type': 'python',
            'expendKeys': ['/'],
            'openList': ['/main.py'],
            'selectFilePath': '/main.py'
        })
        if code == 0:
            write(os.path.join(prj_path, 'main.py'), '#!/usr/bin/env python3\n\n')
        response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_delete_project(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        code, _ = delete(prj_path)
        response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_rename_project(self, client, cmd_id, data):
        old_name = data.get('oldName')
        old_path = os.path.join(define.PROJECTS, 'ide', old_name)
        new_name = data.get('newName')
        new_path = os.path.join(define.PROJECTS, 'ide', new_name)
        code, _ = rename(old_path, new_path)
        response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_save_project(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        code, _ = save_project(prj_path, data)
        response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_create_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        parent_path = convert_path(data.get('parentPath'))
        file_name = data.get('fileName')
        file_path = os.path.join(prj_path, parent_path, file_name)
        code, _ = write_project_file(prj_path, file_path, '')
        response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_write_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        file_path = os.path.join(prj_path, convert_path(data.get('filePath')))
        file_data = data.get('fileData')
        code, _ = write_project_file(prj_path, file_path, file_data)
        if data.get('complete', False):
            line = data.get('line', None)
            column = data.get('column', None)
            line = line + 1 if line is not None else line
            script = jedi.api.Script(source=file_data, line=line, column=column)
            completions = set()
            for completion in script.completions():
                completions.add(completion.name)
            response(client, cmd_id, 0, list(completions))
        else:
            response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_get_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        file_path = os.path.join(prj_path, convert_path(data.get('filePath')))
        code, file_data = get_project_file(prj_path, file_path)
        response(client, cmd_id, code, file_data)

    @gen.coroutine
    def ide_delete_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        file_path = os.path.join(prj_path, convert_path(data.get('filePath')))
        code, _ = delete_project_file(prj_path, file_path)
        response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_rename_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        old_path = os.path.join(prj_path, convert_path(data.get('oldPath')))
        new_name = data.get('newName')
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        code, _ = rename_project_file(prj_path, old_path, new_path)
        response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_create_folder(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        parent_path = convert_path(data.get('parentPath'))
        folder_name = data.get('folderName')
        folder_path = os.path.join(prj_path, parent_path, folder_name)
        code, _ = create_project_folder(prj_path, folder_path)
        response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_delete_folder(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        folder_path = os.path.join(prj_path, convert_path(data.get('folderPath')))
        code, _ = delete_project_file(prj_path, folder_path)
        response(client, cmd_id, code, _)

    @gen.coroutine
    def ide_rename_folder(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        old_path = os.path.join(prj_path, convert_path(data.get('oldPath')))
        new_name = data.get('newName')
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        code, _ = rename_project_file(prj_path, old_path, new_path)
        response(client, cmd_id, code, _)

    @gen.coroutine
    def autocomplete_python(self, client, cmd_id, data):
        source = data.get('source')
        line = data.get('line', None)
        column = data.get('column', None)
        line = line + 1 if line is not None else line
        script = jedi.api.Script(source=source, line=line, column=column)
        completions = set()
        for completion in script.completions():
            completions.add(completion.name)
        response(client, cmd_id, 0, list(completions))

    @gen.coroutine
    def run_pip_command(self, client, cmd_id, data):
        command = data.get('command')
        if not isinstance(command, str) or not command:
            return response(client, cmd_id, 1111, 'pip command: {} error'.format(command))
        else:
            options = data.get('options', [])
            if not command.startswith('pip'):
                List = command.split(' ')
                if len(List) == 1:
                    cmd = [define.PYTHON, '-u', '-m', 'pip', List[0], ' '.join(options)]
                elif len(List) > 1:
                    cmd = [define.PYTHON, '-u', '-m', 'pip', List[0]]
                    for op in List[1:]:
                        cmd.append(op)
                    if List[1] == 'uninstall' and '-y' not in cmd:
                        cmd.append('-y')
                    # cmd = [define.PYTHON, '-u', '-m', 'pip', List[0], '{} {}'.format(' '.join(List[1:]), ' '.join(options))]
                else:
                    return response(client, cmd_id, 1111, 'cmd error')
            else:
                List = command.split(' ')
                if len(List) == 2:
                    cmd = [define.PYTHON, '-u', '-m', List[0], List[1], ' '.join(options)]
                elif len(List) > 2:
                    cmd = [define.PYTHON, '-u', '-m', List[0], List[1]]
                    for op in List[2:]:
                        cmd.append(op)
                    if List[1] == 'uninstall' and '-y' not in cmd:
                        cmd.append('-y')
                    # cmd = [define.PYTHON, '-u', '-m', List[0], List[1], '{} {}'.format(' '.join(List[2:]), ' '.join(options))]
                else:
                    return response(client, cmd_id, 1111, 'cmd error')
            define.subprograms[cmd_id] = SubProgramThread(cmd, cmd_id, client)
            define.subprograms[cmd_id].start()
            response(client, cmd_id, 0, None)

    @gen.coroutine
    def run_python_program(self, client, cmd_id, data):
        # define.PYTHON
        prj_name = data.get('projectName')
        prj_path = os.path.join(define.PROJECTS, 'ide', prj_name)
        file_path = os.path.join(prj_path, convert_path(data.get('filePath')))
        # print(file_path)
        if os.path.exists(file_path) and os.path.isfile(file_path) and file_path.endswith('.py'):
            cmd = [define.PYTHON, '-u', file_path]
            # print(cmd)
            define.subprograms[cmd_id] = SubProgramThread(cmd, cmd_id, client)
            define.subprograms[cmd_id].start()
            response(client, cmd_id, 0, None)
        else:
            response(client, cmd_id, 1, '')

    @gen.coroutine
    def stop_python_program(self, client, cmd_id, data):
        if cmd_id is None:
            for cmd_id, p in define.subprograms.items():
                p.alive = False
        elif cmd_id in define.subprograms:
            define.subprograms[cmd_id].alive = False
        response(client, cmd_id, 0, None)


class SubProgramThread(threading.Thread):
    def __init__(self, cmd, cmd_id, client):
        super(SubProgramThread, self).__init__()
        self.cmd = cmd
        self.cmd_id = cmd_id
        self.client = client
        self.alive = True
        self.daemon = True

    def response_to_client(self, code, stdout):
        if stdout:
            response(self.client, self.cmd_id, code, {'stdout': stdout})
            # res = {
            #     'type': 'response',
            #     'id': self.cmd_id,
            #     'code': code,
            #     'data': {'stdout': stdout}
            # }
            # if self.client.connected:
            #     try:
            #         self.client.write_message(json.dumps(res, ensure_ascii=False))
            #     except:
            #         pass

    def run_python_program(self):
        start_time = time.time()
        p = None
        print('[Program {} is start]'.format(self.cmd_id))
        try:
            p = subprocess.Popen(self.cmd, shell=False, universal_newlines=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while self.alive and p.poll() is None:
                if not self.client.connected:
                    self.alive = False
                    p.kill()
                    define.subprograms.pop(self.cmd_id)
                    print('[Program {} is kill][client is disconnect]'.format(self.cmd_id))
                    return
                stdout = p.stdout.readline()
                stdout = stdout.strip()
                self.response_to_client(0, stdout)
                time.sleep(0.002)
            if not self.alive:
                self.response_to_client(1111, '[program is terminate]')
                p.kill()
                define.subprograms.pop(self.cmd_id)
                print('[Program {} is terminate]'.format(self.cmd_id))
                return
            try:
                stdout = p.stdout.read()
                self.response_to_client(0, stdout)
            except:
                pass
            if self.client.connected:
                stdout = '[Program exit with code {code}]'.format(code=p.returncode)
            else:
                stdout = '[Finish in {second:.2f}s with exit code {code}]'.format(second=time.time() - start_time, code=p.returncode)
            self.response_to_client(1111, stdout)
            define.subprograms.pop(self.cmd_id)
            if p.returncode == 0:
                print('Program {} success'.format(self.cmd_id))
                p.kill()
                return 'ok'
            else:
                print('Program {} failed'.format(self.cmd_id))
                p.kill()
                return 'failed'
        except Exception as e:
            print('[Program {} is exception], {}'.format(self.cmd_id, e))
        finally:
            try:
                p.kill()
            except:
                pass
            try:
                define.subprograms.pop(self.cmd_id)
            except:
                pass

    def run(self):
        self.alive = True
        try:
            self.run_python_program()
        except:
            pass
        self.alive = False


