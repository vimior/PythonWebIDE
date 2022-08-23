import * as types from '../mutation-types';
const path = require('path');

const ideInfo = {
  codeHeight: 0,
  codeItems: [],
  consoleItems: [],
  codeSelected: {},
  consoleSelected: {},
  consoleId: 10001,
  currProj: {
    config: {},
    data: {},
    expandedKeys: [],
    pathSelected: null,
  },
  treeRef: null,
  nodeSelected: null,
  projList: [],
}

const state = {
  ideInfo: ideInfo
};

const getters = {
  ideInfo(state) {
    return state.ideInfo;
  }
};

const mutations = {
  handleProjects(state, data) {
    state.ideInfo.projList = data;
    let lastAccessTime = 0;
    for (var i = 0; i < state.ideInfo.projList.length; i++) {
      if (state.ideInfo.projList[i].lastAccessTime > lastAccessTime) {
        lastAccessTime = state.ideInfo.projList[i].lastAccessTime;
        state.ideInfo.currProj.config.name = state.ideInfo.projList[i].name;
      }
    }
  },
  handleProject(state, data) {
    state.ideInfo.codeItems = [];
    state.ideInfo.currProj.expandedKeys = [];
    state.ideInfo.currProj.config = data.config || {};
    state.ideInfo.currProj.data = data;
    state.ideInfo.currProj.pathSelected = state.ideInfo.currProj.config.selectFilePath;
    if (data.config !== undefined && data.config.expendKeys !== undefined) {
      state.ideInfo.currProj.expandedKeys = data.config.expendKeys;
      state.ideInfo.currProj.expandedKeys.sort();
    }
    if (state.ideInfo.currProj.pathSelected && state.ideInfo.treeRef) {
      state.ideInfo.nodeSelected = state.ideInfo.treeRef.getCurrentNode();
    }
  },
  handleDelProject(state, projectName) {
    for (var i = 0; i < state.ideInfo.projList.length; i++) {
      if (state.ideInfo.projList[i].name === projectName) {
        state.ideInfo.projList.splice(i, 1);
        break;
      }
    }
  },
  handleDelFolder(state, {parentData, folderPath}) {
    for (var i = 0; i < parentData.children.length; i++) {
      if (parentData.children[i].path === folderPath) {
        parentData.children.splice(i, 1);
        break;
      }
    }
    const codeItems = [];
    for (let i = 0; i < state.ideInfo.codeItems.length; i++) {
      if (state.ideInfo.codeItems[i].path.indexOf(folderPath) !== 0) {
        codeItems.push(state.ideInfo.codeItems[i]);
      }
    }
    state.ideInfo.codeItems = codeItems;
    if (state.ideInfo.currProj.pathSelected.indexOf(folderPath) === 0) {
      state.ideInfo.currProj.pathSelected = codeItems.length > 0 ? codeItems[0].path : '';
    }
    const expandedKeys = [];
    for (let i = 0; i < state.ideInfo.currProj.expandedKeys.length; i++) {
      if (state.ideInfo.currProj.expandedKeys[i].indexOf(folderPath) !== 0) {
        expandedKeys.push(state.ideInfo.currProj.expandedKeys[i]);
      }
    }
    state.ideInfo.currProj.expandedKeys = expandedKeys;
  },
  handleGetFile(state, {filePath, data, save}) {
    for (let i = 0; i < state.ideInfo.codeItems.length; i++) {
      if (state.ideInfo.codeItems[i].path === filePath) {
        state.ideInfo.currProj.pathSelected = filePath;
        state.ideInfo.codeSelected = state.ideInfo.codeItems[i];
        return;
      }
    }
    state.ideInfo.codeItems.push({
      name: path.basename(filePath),
      content: data,
      path: filePath,
      codemirror: null,
    });    
    if (save !== false || state.ideInfo.currProj.pathSelected === filePath) {
      state.ideInfo.currProj.pathSelected = filePath;
      state.ideInfo.codeSelected = state.ideInfo.codeItems[state.ideInfo.codeItems.length - 1];
      // self.saveProject();
      state.ideInfo.treeRef.setCurrentKey(state.ideInfo.currProj.pathSelected);
      state.ideInfo.nodeSelected = state.ideInfo.treeRef.getCurrentNode();
    }
  },
  handleDelFile(state, {parentData, filePath}) {
    for (let i = 0; i < state.ideInfo.codeItems.length; i++) {
      if (state.ideInfo.codeItems[i].path === filePath) {
        if (i > 0) {
          state.ideInfo.currProj.pathSelected = state.ideInfo.codeItems[i - 1].path;
        }
        else if (i < state.ideInfo.codeItems.length - 1) {
          state.ideInfo.currProj.pathSelected = state.ideInfo.codeItems[i + 1].path; 
        }
        state.ideInfo.codeItems.splice(i, 1);
        break;
      }
    }
    if (parentData) {
      for (let i = 0; i < parentData.children.length; i++) {
        if (parentData.children[i].path === filePath) {
          parentData.children.splice(i, 1);
          break;
        }
      }
    }
    // self.saveProject(self.getProject);
  },
  addChildrenNode(state, {name, path, type}) {
    if (!state.ideInfo.nodeSelected || state.ideInfo.nodeSelected.type !== 'dir') return;
    state.ideInfo.nodeSelected.children.push({
      name: name,
      label: name,
      uuid: path,
      path: path,
      type: type,
      children: [],
    });
    state.ideInfo.currProj.expandedKeys.push(state.ideInfo.nodeSelected.path);
    if (type == 'file') {
      state.ideInfo.currProj.pathSelected = path;

      state.ideInfo.codeItems.push({
        name: name,
        content: '',
        path: path,
        codemirror: null,
      });
      state.ideInfo.codeSelected = state.ideInfo.codeItems[state.ideInfo.codeItems.length - 1];
    }
    else {
      state.ideInfo.currProj.expandedKeys.push(path);
    }
  },
  handleRename(state, name) {
    if (!state.ideInfo.nodeSelected || !state.ideInfo.nodeSelected.type) return;
    if (state.ideInfo.nodeSelected.path === '/') {
      // rename project
      state.ideInfo.currProj.config.name = name;
      state.ideInfo.currProj.data.name = name;
      state.ideInfo.currProj.data.label = name;
    }
    else {
      // rename file/folder
      const renameNodeData = (nodeData, parentPath) => {
        nodeData.path = path.join(parentPath, nodeData.name);
        nodeData.uuid = nodeData.path;
        if (nodeData.type === 'dir' && nodeData.children) {
          for (let i = 0; i < nodeData.children.length; i++) {
            renameNodeData(nodeData.children[i], nodeData.path);
          }
        }
      }
      const newPath = path.join(path.dirname(state.ideInfo.nodeSelected.path), name);

      // rename code item
      for (let i = 0; i < state.ideInfo.codeItems.length; i++) {
        if (state.ideInfo.codeItems[i].path === state.ideInfo.nodeSelected.path) {
          state.ideInfo.codeItems[i].name = name;
          state.ideInfo.codeItems[i].path = newPath;
        }
        else if (state.ideInfo.codeItems[i].path.indexOf(state.ideInfo.nodeSelected.path) === 0) {
          state.ideInfo.codeItems[i].path = state.ideInfo.codeItems[i].path.replace(state.ideInfo.nodeSelected.path, newPath);
        }
      }
      // rename console item
      for (let i = 0; i < state.ideInfo.consoleItems.length; i++) {
        if (state.ideInfo.consoleItems[i].path === state.ideInfo.nodeSelected.path) {
          state.ideInfo.consoleItems[i].name = name;
          state.ideInfo.consoleItems[i].path = newPath;
        }
        else if (state.ideInfo.consoleItems[i].path.indexOf(state.ideInfo.nodeSelected.path) === 0) {
          state.ideInfo.consoleItems[i].path = state.ideInfo.consoleItems[i].path.replace(state.ideInfo.nodeSelected.path, newPath);
        }
      }
      // rename expand key
      for (let i = 0; i < state.ideInfo.currProj.expandedKeys.length; i++) {
        if (state.ideInfo.currProj.expandedKeys[i].indexOf(state.ideInfo.nodeSelected.path) === 0) {
          state.ideInfo.currProj.expandedKeys[i] = state.ideInfo.currProj.expandedKeys[i].replace(state.ideInfo.nodeSelected.path, newPath);
        }
      }
      // rename path selected
      if (state.ideInfo.currProj.pathSelected.indexOf(state.ideInfo.nodeSelected.path) === 0) {
        state.ideInfo.currProj.pathSelected = state.ideInfo.currProj.pathSelected.replace(state.ideInfo.nodeSelected.path, newPath);
      }

      // rename node selected name
      state.ideInfo.nodeSelected.name = name;
      state.ideInfo.nodeSelected.label = name;
      // rename node selected path and all children item path
      renameNodeData(state.ideInfo.nodeSelected, path.dirname(state.ideInfo.nodeSelected.path));
    }
  },
  handleCreateFile(state, filePath) {
    state.ideInfo.currProj.expandedKeys.push(filePath);
    state.ideInfo.currProj.pathSelected = filePath;
  },
  handleCreateFolder(state, folderPath) {
    state.ideInfo.currProj.expandedKeys.push(folderPath);
  },
  handleRunResult(state, dict) {
    if (dict.code === 0) {
      if (dict.data === null || dict.data.stdout === undefined || dict.data.stdout === null) {
        // 程序开始, 先把运行状态置为True，把输出清空
        for (let i = 0; i < state.ideInfo.consoleItems.length; i++) {
          if (state.ideInfo.consoleItems[i].id !== dict.id) continue;
          if (!state.ideInfo.consoleItems[i].run) {
            state.ideInfo.consoleItems[i].resultList = [];
          }
          state.ideInfo.consoleItems[i].run = true;
          break;
        }
      }
      else {
        for (let i = 0; i < state.ideInfo.consoleItems.length; i++) {
          if (state.ideInfo.consoleItems[i].id !== dict.id) continue;
          // 限制保存结果的最大30000行
          if (state.ideInfo.consoleItems[i].resultList.length > 30000) {
            // 超过最大行数，把前100行扔掉
            state.ideInfo.consoleItems[i].resultList.splice(0, 100);
          }
          // 把结果压进结果列表
          state.ideInfo.consoleItems[i].resultList.push(`${dict.data.stdout}`);
          // 限制只刷新选中的Console的结果
          // if (state.ideInfo.consoleSelected.id !== state.ideInfo.consoleItems[i].id && !window.GlobalUtil.model.socketModel.socketInfo.connected) {
          //   break;
          // }
          // const textArea = document.getElementById('console-' + state.ideInfo.consoleItems[i].id)
          // if (textArea !== undefined && textArea !== null) {
          //   textArea.scrollTop = textArea.scrollHeight;
          // }
          break;
        }
      }
    }
    else {
      // 程序结束，把程序状态置为False，显示所有输出
      for (let i = 0; i < state.ideInfo.consoleItems.length; i++) {
        if (state.ideInfo.consoleItems[i].id !== dict.id) continue;
        // 如果当前终端没有程序在运行，则先清空输出（一般发生在文件不存在或非py文件或输入的命令为空或命令不是字符串）
        if (!state.ideInfo.consoleItems[i].run && !state.ideInfo.consoleItems[i].stop) {
          state.ideInfo.consoleItems[i].resultList = [];
        }
        if (dict.data && dict.data.stdout) {
          state.ideInfo.consoleItems[i].resultList.push(`${dict.data.stdout}`);
        }
        const textArea = document.getElementById('console-' + state.ideInfo.consoleItems[i].id)
        if (textArea !== undefined && textArea !== null) {
          textArea.scrollTop = textArea.scrollHeight;
        }
        state.ideInfo.consoleItems[i].run = false;
        break;
      }
    }
  },
  handleStopResult(state, { consoleId, dict }) {
    if (dict.code === 0) {
      for (let i = 0; i < state.ideInfo.consoleItems.length; i++) {
        if (consoleId && state.ideInfo.consoleItems[i].id !== consoleId) continue;
        state.ideInfo.consoleItems[i].stop = true;
        state.ideInfo.consoleItems[i].run = false;
      }
    }
  },
  addExpandNodeKey(state, key) {
    if (state.ideInfo.currProj.expandedKeys.indexOf(key) < 0) {
      state.ideInfo.currProj.expandedKeys.push(key);
      // _this.saveProject();
    }
  },
  delExpandNodeKey(state, key) {
    state.ideInfo.currProj.expandedKeys.splice(state.ideInfo.currProj.expandedKeys.findIndex(item => item === key), 1);
  },
  setNodeSelected(state, selected) {
    state.ideInfo.nodeSelected = selected;
  },
  setPathSelected(state, selected) {
    state.ideInfo.currProj.pathSelected = selected;
  },
  setCodeSelected(state, selected) {
    state.ideInfo.codeSelected = selected;
  },
  setConsoleSelected(state, selected) {
    state.ideInfo.consoleSelected = selected;
  },
  setTreeRef(state, treeRef) {
    state.ideInfo.treeRef = treeRef;
  },
  assignConsoleSelected(state, item) {
    if (item && typeof item === 'object')
      Object.assign(state.ideInfo.consoleSelected, item);
  },
  spliceConsoleItems(state, { start, count }) {
    state.ideInfo.consoleItems.splice(start, count);
  },
  setConsoleId(state, consoleId) {
    state.ideInfo.consoleId = consoleId;
  },
  addConsoleItem(state, item) {
    state.ideInfo.consoleItems.push(item);
  },
  setConsoleItems(state, items) {
    state.ideInfo.consoleItems = items;
  },

  addCodeItem(state, item) {
    state.ideInfo.codeItems.push(item);
  },
  setCodeItems(state, items) {
    state.ideInfo.codeItems = items;
  },
  setCodeItemMirror(state, { index, codemirror }) {
    state.ideInfo.codeItems[index].codemirror = codemirror;
  },
  setCodeItemContent(state, { index, content }) {
    state.ideInfo.codeItems[index].content = content;
  },
  setCodeHeight(state, height) {
    state.ideInfo.codeHeight = height;
  }
};

const actions = {
  [types.IDE_LIST_PROJECTS](context, { wsKey, msgId, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      msgId: msgId,
      cmd: types.IDE_LIST_PROJECTS,
      data: {}, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_GET_PROJECT](context, { wsKey, projectName, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_GET_PROJECT,
      data: {
        projectName: projectName
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_CREATE_PROJECT](context, { wsKey, projectName, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_CREATE_PROJECT,
      data: {
        projectName: projectName
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_DEL_PROJECT](context, { wsKey, projectName, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_DEL_PROJECT,
      data: {
        projectName: projectName
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_RENAME_PROJECT](context, { wsKey, oldName, newName, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_RENAME_PROJECT,
      data: {
        oldName: oldName,
        newName: newName,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_SAVE_PROJECT](context, { wsKey, callback }) {
    const openList = []
    for(let i = 0; i < context.state.ideInfo.codeItems.length; i++) {
      openList.push(context.state.ideInfo.codeItems[i].path);
    }
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_SAVE_PROJECT,
      data: {
        projectName: context.state.ideInfo.currProj.data.name,
        expendKeys: context.state.ideInfo.currProj.expandedKeys,
        openList: openList,
        selectFilePath: context.state.ideInfo.currProj.pathSelected,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_CREATE_FILE](context, { wsKey, projectName, parentPath, fileName, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_CREATE_FILE,
      data: {
        projectName: projectName || context.state.ideInfo.currProj.data.name,
        parentPath: parentPath || context.state.ideInfo.nodeSelected.path,
        fileName: fileName,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_WRITE_FILE](context, { wsKey, projectName, filePath, fileData, complete, line, column, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_WRITE_FILE,
      data: {
        projectName: projectName || context.state.ideInfo.currProj.data.name,
        filePath: filePath,
        fileData: fileData,
        complete: complete,
        line: line,
        column: column
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_GET_FILE](context, { wsKey, projectName, filePath, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_GET_FILE,
      data: {
        projectName: projectName || context.state.ideInfo.currProj.data.name,
        filePath: filePath
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_DEL_FILE](context, { wsKey, projectName, filePath, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_DEL_FILE,
      data: {
        projectName: projectName || context.state.ideInfo.currProj.data.name,
        filePath: filePath
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_RENAME_FILE](context, { wsKey, projectName, oldPath, fileName, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_RENAME_FILE,
      data: {
        projectName: projectName || context.state.ideInfo.currProj.data.name,
        oldPath: oldPath || context.state.ideInfo.nodeSelected.path,
        newName: fileName,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_CREATE_FOLDER](context, { wsKey, projectName, parentPath, folderName, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_CREATE_FOLDER,
      data: {
        projectName: projectName || context.state.ideInfo.currProj.data.name,
        parentPath: parentPath || context.state.ideInfo.nodeSelected.path,
        folderName: folderName,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_DEL_FOLDER](context, { wsKey, projectName, folderPath, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_DEL_FOLDER,
      data: {
        projectName: projectName || context.state.ideInfo.currProj.data.name,
        folderPath: folderPath,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_RENAME_FOLDER](context, { wsKey, projectName, oldPath, folderName, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_RENAME_FOLDER,
      data: {
        projectName: projectName || context.state.ideInfo.currProj.data.name,
        oldPath: oldPath || context.state.ideInfo.nodeSelected.path,
        newName: folderName,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_AUTOCOMPLETE_PYTHON](context, { wsKey, source, line, column, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_AUTOCOMPLETE_PYTHON,
      data: {
        source: source,
        line: line,
        column: column,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_RUN_PIP_COMMAND](context, { wsKey, msgId, command, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      msgId: msgId,
      cmd: types.IDE_RUN_PIP_COMMAND,
      data: {
        command: command,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_RUN_PYTHON_PROGRAM](context, { wsKey, msgId, projectName, filePath, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      msgId: msgId,
      cmd: types.IDE_RUN_PYTHON_PROGRAM,
      data: {
        projectName: projectName || context.state.ideInfo.currProj.data.name,
        filePath: filePath,
      }, 
      callback: callback,
    }, { root: true });
  },
  [types.IDE_STOP_PYTHON_PROGRAM](context, { wsKey, consoleId, callback }) {
    context.dispatch('websocket/sendCmd', {
      wsKey: wsKey,
      cmd: types.IDE_STOP_PYTHON_PROGRAM,
      data: {
        program_id: consoleId,
      }, 
      callback: callback,
    }, { root: true });
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
