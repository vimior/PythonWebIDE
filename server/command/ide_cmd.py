#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import os
import jedi
import time
import asyncio
import threading
import subprocess
from tornado.ioloop import IOLoop
from jedi import __version__ as jedi_version
from distutils.version import StrictVersion
from .utils import convert_path
from .resource import *
from .response import response
from common.config import Config

PROJECT_IS_EXIST = -1
PROJECT_IS_NOT_EXIST = -2

DIR_IS_EXIST = -11
DIR_IS_NOT_EXIST = -12

FILE_IS_EXIST = -21
FILE_IS_NOT_EXIST = -22

jedi_is_gt_17 = StrictVersion(jedi_version) >= StrictVersion('0.17.0')

if not os.path.exists(os.path.join(Config.PROJECTS, 'ide')):
    os.makedirs(os.path.join(Config.PROJECTS, 'ide'))


class IdeCmd(object):
    def __init__(self):
        pass

    async def ide_list_projects(self, client, cmd_id, data):
        ide_path = os.path.join(Config.PROJECTS, 'ide')
        code, projects = list_projects(ide_path)
        await response(client, cmd_id, code, projects)

    async def ide_get_project(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        code, project = get_project(prj_path)
        await response(client, cmd_id, code, project)

    async def ide_create_project(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        code, _ = create_project(prj_path, config_data={
            'type': 'python',
            'expendKeys': ['/'],
            'openList': ['/main.py'],
            'selectFilePath': '/main.py'
        })
        if code == 0:
            write(os.path.join(prj_path, 'main.py'), '#!/usr/bin/env python3\n\n')
        await response(client, cmd_id, code, _)

    async def ide_delete_project(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        code, _ = delete(prj_path)
        await response(client, cmd_id, code, _)

    async def ide_rename_project(self, client, cmd_id, data):
        old_name = data.get('oldName')
        old_path = os.path.join(Config.PROJECTS, 'ide', old_name)
        new_name = data.get('newName')
        new_path = os.path.join(Config.PROJECTS, 'ide', new_name)
        code, _ = rename(old_path, new_path)
        await response(client, cmd_id, code, _)

    async def ide_save_project(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        code, _ = save_project(prj_path, data)
        await response(client, cmd_id, code, _)

    async def ide_create_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        parent_path = convert_path(data.get('parentPath'))
        file_name = data.get('fileName')
        file_path = os.path.join(prj_path, parent_path, file_name)
        code, _ = write_project_file(prj_path, file_path, '')
        await response(client, cmd_id, code, _)

    async def ide_write_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        file_path = os.path.join(prj_path, convert_path(data.get('filePath')))
        file_data = data.get('fileData')
        code, _ = write_project_file(prj_path, file_path, file_data)
        if data.get('complete', False):
            line = data.get('line', None)
            column = data.get('column', None)
            line = line + 1 if line is not None else line
            completions = set()
            if jedi_is_gt_17:
                script = jedi.api.Script(code=file_data, path=file_path, project=jedi.api.Project(file_path, added_sys_path=[]))
                for completion in script.complete(line=line, column=column):
                    completions.add(completion.name)
            else:
                script = jedi.api.Script(source=file_data, line=line, column=column, path=file_path)
                completions = set()
                for completion in script.completions():
                    completions.add(completion.name)
            await response(client, cmd_id, 0, list(completions))
        else:
            await response(client, cmd_id, code, _)

    async def ide_get_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        file_path = os.path.join(prj_path, convert_path(data.get('filePath')))
        code, file_data = get_project_file(prj_path, file_path)
        await response(client, cmd_id, code, file_data)

    async def ide_delete_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        file_path = os.path.join(prj_path, convert_path(data.get('filePath')))
        code, _ = delete_project_file(prj_path, file_path)
        await response(client, cmd_id, code, _)

    async def ide_rename_file(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        old_path = os.path.join(prj_path, convert_path(data.get('oldPath')))
        new_name = data.get('newName')
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        code, _ = rename_project_file(prj_path, old_path, new_path)
        await response(client, cmd_id, code, _)

    async def ide_create_folder(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        parent_path = convert_path(data.get('parentPath'))
        folder_name = data.get('folderName')
        folder_path = os.path.join(prj_path, parent_path, folder_name)
        code, _ = create_project_folder(prj_path, folder_path)
        await response(client, cmd_id, code, _)

    async def ide_delete_folder(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        folder_path = os.path.join(prj_path, convert_path(data.get('folderPath')))
        code, _ = delete_project_file(prj_path, folder_path)
        await response(client, cmd_id, code, _)

    async def ide_rename_folder(self, client, cmd_id, data):
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        old_path = os.path.join(prj_path, convert_path(data.get('oldPath')))
        new_name = data.get('newName')
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        code, _ = rename_project_file(prj_path, old_path, new_path)
        await response(client, cmd_id, code, _)

    async def autocomplete_python(self, client, cmd_id, data):
        source = data.get('source')
        line = data.get('line', None)
        column = data.get('column', None)
        line = line + 1 if line is not None else line
        script = jedi.api.Script(source=source, line=line, column=column)
        completions = set()
        for completion in script.completions():
            completions.add(completion.name)
        await response(client, cmd_id, 0, list(completions))

    async def run_pip_command(self, client, cmd_id, data):
        command = data.get('command')
        if not isinstance(command, str) or not command:
            return await response(client, cmd_id, 1111, {'stdout': 'pip command: {} error'.format(command)})
        else:
            options = data.get('options', [])
            if not command.startswith('pip'):
                List = command.split(' ')
                if len(List) == 1:
                    cmd = [Config.PYTHON, '-u', '-m', 'pip', List[0], ' '.join(options)]
                elif len(List) > 1:
                    cmd = [Config.PYTHON, '-u', '-m', 'pip', List[0]]
                    for op in List[1:]:
                        cmd.append(op)
                    if List[1] == 'uninstall' and '-y' not in cmd:
                        cmd.append('-y')
                    # cmd = [Config.PYTHON, '-u', '-m', 'pip', List[0], '{} {}'.format(' '.join(List[1:]), ' '.join(options))]
                else:
                    return await response(client, cmd_id, 1111, {'stdout': 'cmd error'})
            else:
                List = command.split(' ')
                if len(List) == 2:
                    cmd = [Config.PYTHON, '-u', '-m', List[0], List[1], ' '.join(options)]
                elif len(List) > 2:
                    cmd = [Config.PYTHON, '-u', '-m', List[0], List[1]]
                    for op in List[2:]:
                        cmd.append(op)
                    if List[1] == 'uninstall' and '-y' not in cmd:
                        cmd.append('-y')
                    # cmd = [Config.PYTHON, '-u', '-m', List[0], List[1], '{} {}'.format(' '.join(List[2:]), ' '.join(options))]
                else:
                    return await response(client, cmd_id, 1111, {'stdout': 'cmd error'})
            client.handler_info.set_subprogram(cmd_id, SubProgramThread(cmd, cmd_id, client, asyncio.get_event_loop()))
            await response(client, cmd_id, 0, None)
            client.handler_info.start_subprogram(cmd_id)

    async def run_python_program(self, client, cmd_id, data):
        # Config.PYTHON
        prj_name = data.get('projectName')
        prj_path = os.path.join(Config.PROJECTS, 'ide', prj_name)
        file_path = os.path.join(prj_path, convert_path(data.get('filePath')))
        # print(file_path)
        if os.path.exists(file_path) and os.path.isfile(file_path) and file_path.endswith('.py'):
            cmd = [Config.PYTHON, '-u', file_path]
            client.handler_info.set_subprogram(cmd_id, SubProgramThread(cmd, cmd_id, client, asyncio.get_event_loop()))
            await response(client, cmd_id, 0, None)
            client.handler_info.start_subprogram(cmd_id)
        else:
            await response(client, cmd_id, 1111, {'stdout': 'File can not run'})

    async def stop_python_program(self, client, cmd_id, data):
        program_id = data.get('program_id', None)
        client.handler_info.stop_subprogram(program_id)
        await response(client, cmd_id, 0, None)


class SubProgramThread(threading.Thread):
    def __init__(self, cmd, cmd_id, client, event_loop):
        super(SubProgramThread, self).__init__()
        self.cmd = cmd
        self.cmd_id = cmd_id
        self.client = client
        self.alive = True
        self.daemon = True
        self.event_loop = event_loop
        self.p = None
    
    def stop(self):
        self.alive = False
        if self.p:
            try:
                self.p.kill()
            except:
                pass
            self.p = None

    def response_to_client(self, code, stdout):
        if stdout:
            IOLoop.current().spawn_callback(response, self.client, self.cmd_id, code, {'stdout': stdout})

    def run_python_program(self):
        start_time = time.time()
        p = None
        asyncio.set_event_loop(self.event_loop)
        print('[{}-Program {} is start]'.format(self.client.id, self.cmd_id))
        try:
            p = subprocess.Popen(self.cmd, shell=False, universal_newlines=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.p = p
            while self.alive and p.poll() is None:
                if not self.client.connected:
                    self.alive = False
                    p.kill()
                    self.client.handler_info.remove_subprogram(self.cmd_id)
                    print('[{}-Program {} is kill][client is disconnect]'.format(self.client.id, self.cmd_id))
                    return
                stdout = p.stdout.readline()
                stdout = stdout.strip()
                self.response_to_client(0, stdout)
                time.sleep(0.002)
            if not self.alive:
                self.response_to_client(1111, '[program is terminate]')
                p.kill()
                self.client.handler_info.remove_subprogram(self.cmd_id)
                print('[{}-Program {} is terminate]'.format(self.client.id, self.cmd_id))
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
            self.client.handler_info.remove_subprogram(self.cmd_id)
            if p.returncode == 0:
                print('{}-Program {} success'.format(self.client.id, self.cmd_id))
                p.kill()
                return 'ok'
            else:
                print('{}-Program {} failed'.format(self.client.id, self.cmd_id))
                p.kill()
                return 'failed'
        except Exception as e:
            print('[{}-Program {} is exception], {}'.format(self.client.id, self.cmd_id, e))
            self.response_to_client(1111, '[Program is exception], {}'.format(e))
        finally:
            try:
                p.kill()
            except:
                pass
            try:
                self.client.handler_info.remove_subprogram(self.cmd_id)
            except:
                pass

    def run(self):
        self.alive = True
        try:
            self.run_python_program()
        except Exception as e:
            print(e)
            pass
        self.alive = False


