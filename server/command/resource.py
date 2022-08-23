#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import os
import time
import uuid
import json
import shutil
import datetime


PATH_IS_EXIST = -11
PATH_IS_NOT_EXIST = -12

PATH_IS_FILE = -21
PATH_IS_DIR = -22

READ_ERROR = -31
WRITE_ERROR = -32
DELETE_ERROR = 33
RENAME_ERROR = -34
CREATE_ERROR = -35


class FilterRule(object):
    @staticmethod
    def filter(file):
        if file in ['__pycache__'] or file.endswith(('.pyc', '.pyd', '.o')):
            return
        return file


def read(path, is_json=False):
    if os.path.exists(path) and os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if is_json:
                    data = json.load(f)
                else:
                    data = f.read()
            return 0, data
        except Exception as e:
            return READ_ERROR, e
    elif not os.path.exists(path):
        return PATH_IS_NOT_EXIST, None
    else:
        return PATH_IS_DIR, None


def write(path, data, is_json=False):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            if is_json:
                json.dump(data, f, sort_keys=True, indent=4, skipkeys=True, separators=(',', ':'), ensure_ascii=False)
            else:
                f.write(data)
        return 0, None
    except Exception as e:
        return WRITE_ERROR, e


def create(path, data=None):
    if data is None:
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                return 0, None
            except Exception as e:
                return CREATE_ERROR, e
        else:
            return PATH_IS_EXIST, None
    else:
        return write(path, data)


def delete(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
                return 0, None
            except Exception as e:
                return DELETE_ERROR, e
        else:
            try:
                os.remove(path)
                return 0, None
            except Exception as e:
                return DELETE_ERROR, e
    else:
        return PATH_IS_NOT_EXIST, None


def rename(old_path, new_path):
    if os.path.exists(old_path):
        if not os.path.exists(new_path):
            try:
                os.rename(old_path, new_path)
                return 0, None
            except Exception as e:
                return RENAME_ERROR, e
        else:
            return PATH_IS_EXIST, None
    else:
        return PATH_IS_NOT_EXIST, None


def list_dir(path, result=None, prefix='', filter_config=True, list_type='simple'):
    prefix = '' if prefix == '/' else prefix
    if os.path.exists(path):
        if result is None:
            result = {
                'uuid': '/',
                'name': os.path.basename(path),
                'label': os.path.basename(path),
                'type': 'dir',
                # 'path': path,
                'path': '/',
            }
        result['children'] = []
        for p in os.listdir(path):
            if filter_config:
                if p == '.config':
                    continue
            if FilterRule.filter(p) is None:
                continue
            abs_p = os.path.join(path, p)
            if os.path.isdir(abs_p):
                _result = {
                    'uuid': prefix + '/' + p,
                    'name': p,
                    'label': p,
                    'type': 'dir',
                    # 'path': abs_p,
                    'path': prefix + '/' + p,
                }
                result['children'].append(_result)
                if list_type == 'detail':
                    list_dir(abs_p, _result, prefix=prefix + '/' + p, filter_config=False, list_type=list_type)
            else:
                result['children'].append({
                    'uuid': prefix + '/' + p,
                    'name': p,
                    'label': p,
                    'type': 'file',
                    # 'path': abs_p,
                    'path': prefix + '/' + p,
                })
    return result


# path = os.path.join(os.path.expanduser('~'), '.UFACTORY', 'projects', 'test', 'xarm7', 'python', 'demo')
# result = list_dir(path, list_type='detail')
# print(json.dumps(result, sort_keys=True, indent=4, skipkeys=True, separators=(',', ':'), ensure_ascii=False))


def list_projects(path):
    projects = []
    if os.path.exists(path) and os.path.isdir(path):
        for prj in os.listdir(path):
            _config_path = os.path.join(path, prj, '.config')
            code, config_data = read(_config_path, is_json=True)
            if code == 0:
                config_data['name'] = prj
                config_data['atime'] = time.strftime("%d/%m/%Y %I:%M:%S %p",
                                                     time.localtime(os.path.getatime(_config_path))),  # 访问时间
                config_data['mtime'] = time.strftime("%d/%m/%Y %I:%M:%S %p",
                                                     time.localtime(os.path.getmtime(_config_path))),  # 修改时间
                config_data['ctime'] = time.strftime("%d/%m/%Y %I:%M:%S %p",
                                                     time.localtime(os.path.getctime(_config_path))),  # 创建时间

                config_data['atime'] = config_data['atime'][0] if isinstance(
                    config_data['atime'], tuple) else config_data['atime']
                config_data['mtime'] = config_data['mtime'][0] if isinstance(
                    config_data['mtime'], tuple) else config_data['mtime']
                config_data['ctime'] = config_data['ctime'][0] if isinstance(
                    config_data['ctime'], tuple) else config_data['ctime']
                projects.append(config_data)
        return 0, projects
    elif not os.path.exists(path):
        return PATH_IS_NOT_EXIST, projects
    else:
        return PATH_IS_FILE, projects


def get_project(path):
    if os.path.exists(path):
        project = list_dir(path, list_type='detail')
        _config_path = os.path.join(path, '.config')
        _code, config_data = read(_config_path, is_json=True)
        if _code != 0:
            config_data = {}
        config_data['lastAccessTime'] = time.time()
        write(_config_path, config_data, is_json=True)
        config_data['name'] = os.path.basename(path)
        config_data['atime'] = time.strftime("%d/%m/%Y %I:%M:%S %p",
                                             time.localtime(os.path.getatime(_config_path))),  # 访问时间
        config_data['mtime'] = time.strftime("%d/%m/%Y %I:%M:%S %p",
                                             time.localtime(os.path.getmtime(_config_path))),  # 修改时间
        config_data['ctime'] = time.strftime("%d/%m/%Y %I:%M:%S %p",
                                             time.localtime(os.path.getctime(_config_path))),  # 创建时间

        config_data['atime'] = config_data['atime'][0] if isinstance(
            config_data['atime'], tuple) else config_data['atime']
        config_data['mtime'] = config_data['mtime'][0] if isinstance(
            config_data['mtime'], tuple) else config_data['mtime']
        config_data['ctime'] = config_data['ctime'][0] if isinstance(
            config_data['ctime'], tuple) else config_data['ctime']
        project['config'] = config_data
        return 0, project
    else:
        return PATH_IS_NOT_EXIST, None


def create_project(path, config_data=None):
    code, _ = create(path)
    if code == 0:
        if not isinstance(config_data, dict):
            config_data = {}
        config_data['lastAccessTime'] = time.time()
        code, _ = write(os.path.join(path, '.config'), config_data, is_json=True)
        config_data['name'] = os.path.basename(path)
        return code, config_data
    else:
        return code, None


def save_project(project_path, data):
    _config_path = os.path.join(project_path, '.config')
    code, config_data = read(_config_path, is_json=True)
    if code != 0:
        config_data = {}
    config_data['lastAccessTime'] = time.time()
    expend_keys = data.get('expendKeys')
    open_list = data.get('openList')
    selectFilePath = data.get('selectFilePath')
    config_data['expendKeys'] = list(set(expend_keys))
    config_data['openList'] = list(set(open_list))
    config_data['selectFilePath'] = selectFilePath
    write(_config_path, config_data, is_json=True)
    return code, config_data


def get_project_file(project_path, file_path):
    code, data = read(file_path)
    if code == 0:
        _config_path = os.path.join(project_path, '.config')
        _code, config_data = read(_config_path, is_json=True)
        if _code != 0:
            config_data = {}
        config_data['lastAccessTime'] = time.time()
        write(_config_path, config_data, is_json=True)
    return code, data


def delete_project_file(project_path, file_path):
    code, _ = delete(file_path)
    if code == 0:
        _config_path = os.path.join(project_path, '.config')
        _code, config_data = read(_config_path, is_json=True)
        if _code != 0:
            config_data = {}
        config_data['lastAccessTime'] = time.time()
        write(_config_path, config_data, is_json=True)
    return code, _


def rename_project_file(project_path, old_path, new_path):
    code, _ = rename(old_path, new_path)
    if code == 0:
        _config_path = os.path.join(project_path, '.config')
        _code, config_data = read(_config_path, is_json=True)
        if _code != 0:
            config_data = {}
        config_data['lastAccessTime'] = time.time()
        write(_config_path, config_data, is_json=True)
    return code, _


def write_project_file(project_path, file_path, data):
    code, _ = write(file_path, data)
    if code == 0:
        _config_path = os.path.join(project_path, '.config')
        _code, config_data = read(_config_path, is_json=True)
        if _code != 0:
            config_data = {}
        config_data['lastAccessTime'] = time.time()
        write(_config_path, config_data, is_json=True)
    return code, _


def create_project_folder(project_path, folder_path):
    code, _ = create(folder_path)
    if code == 0:
        _config_path = os.path.join(project_path, '.config')
        _code, config_data = read(_config_path, is_json=True)
        if _code != 0:
            config_data = {}
        config_data['lastAccessTime'] = time.time()
        write(_config_path, config_data, is_json=True)
    return code, _

