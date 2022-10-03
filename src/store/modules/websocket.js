import ReconnectingWebSocket from 'reconnecting-websocket';

const wsInfoMap = {
  default: {
    location: {
      protocol: 'ws:',
      host: window.location.hostname,
      port: '10086',
      pathname: '/ws',
      search: '?v=1', // 请求参数
    },
    protocols: [],
    options: {
      WebSocket: WebSocket, // WS
      maxReconnectionDelay: 10000,
      minReconnectionDelay: 1000 + Math.random() * 4000,
      reconnectionDelayGrowFactor: 1.3,
      minUptime: 5000,
      connectionTimeout: 4000,
      maxRetries: Infinity,
      maxEnqueuedMessages: Infinity,
      startClosed: false,
      debug: false,
    },
    logger: console,
    rws: null, // websocket实例
    connected: false, // 连接状态
    msgId: 1, // 发送的消息ID，递增
    jsonMsgCallbacks: {}, // 接收到消息的回调
    jsonMsgHandlers: [], // 消息处理函数列表, 这里函数参数是经过JSON.parse(event.data)处理的数据
  }
};

const state = {
  wsInfoMap: wsInfoMap,
};

const getters = {
  wsInfo: (state) => {
    return (wsKey) => {
      return state.wsInfoMap[wsKey || 'default'];
    }
  }
};

const mutations = {
  setLocation(state, { wsKey, location }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (location && typeof location === 'object')
      wsInfo.location = Object.assign(wsInfo.location, location);
  },
  setProtocols(state, { wsKey, protocols }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (protocols && typeof options === 'object')
      wsInfo.protocols = Object.assign(wsInfo.protocols, protocols);
  },
  setOptions(state, { wsKey, options }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (options && typeof options === 'object')
      wsInfo.options = Object.assign(wsInfo.options, options);
  },
  setRws(state, { wsKey, rws }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    wsInfo.rws = rws;
  },
  setConnected(state,  { wsKey, connected }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    wsInfo.connected = connected;
  },
  setMsgId(state, { wsKey, msgId }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    wsInfo.msgId = msgId;
  },
  addJsonMsgCallback(state, { wsKey, msgId, callback }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    wsInfo.jsonMsgCallbacks[msgId] = callback;
  },

  /**
   * 删除消息回调，删除前会先触发一遍
   * @param wsKey: websocket实例key, 默认用'default'
   * @param msgId: 指定要删除回调的msgId，如果不指定则删除所有的回调
   * @param trigger: 删除前是否触发，默认不会触发，触发参数是{code: 10086}
   * 调用:
   *  1. this.$store.commit('websocket/delJsonMsgCallback', {trigger: true})
   *  2. commit('websocket/delJsonMsgCallback', {trigger: true}, { root: true })
   */
  delJsonMsgCallback(state, { wsKey, msgId, trigger }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (msgId) {
      const callbackObj = wsInfo.jsonMsgCallbacks[msgId];
      if (callbackObj) {
        if (trigger === true && callbackObj.limits !== 0) {
          callbackObj.callback({ code: 10086 });
        }
        delete wsInfo.jsonMsgCallbacks[msgId];
      }
    }
    else {
      for (const msgId in wsInfo.jsonMsgCallbacks) {
        const callbackObj = wsInfo.jsonMsgCallbacks[msgId];
        if (callbackObj && trigger === true && callbackObj.limits !== 0) {
          callbackObj.callback({ code: 10086 });
        }
        delete wsInfo.jsonMsgCallbacks[msgId];
      }
    }
  },
  setJsonMsgCallback(state, { wsKey, msgId, limits, finished }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    wsInfo.jsonMsgCallbacks[msgId].limits = limits || wsInfo.jsonMsgCallbacks[msgId].limits;
    wsInfo.jsonMsgCallbacks[msgId].limits = finished || wsInfo.jsonMsgCallbacks[msgId].finished;
  },
  callJsonMsgCallback(state,  { wsKey, dict }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    const callbackObj = wsInfo.jsonMsgCallbacks[dict.id];
    if (callbackObj) {
      if (callbackObj.limits !== 0) {
        callbackObj.callback(dict);
        callbackObj.limits -= 1;
      }
      callbackObj.finished = true;

      if (callbackObj.limits === 0) {
        delete wsInfo.jsonMsgCallbacks[dict.id];
      }
    }
  },
  
  /**
   * 断开WebSocket连接，会触发并删除所有消息回调，触发参数是{code: 10086}
   * @param wsKey: websocket实例key, 默认用'default'
   * 调用
   *  1. this.$store.commit('websocket/close', { wsKey: 'default' })
   *  2. commit('websocket/close', { wsKey: 'default' }, { root: true })
   */
  close(state, { wsKey }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (wsInfo && wsInfo.rws) {
      wsInfo.rws.onopen = null;
      wsInfo.rws.onclose = null;
      wsInfo.rws.onerror = null;
      wsInfo.rws.onmessage = null;
      wsInfo.rws.close();
      // wsInfo.delJsonMsgCallback(null, true);
      // wsInfo.rws = null;
    }
  },
  
  /**
   * 重新进行WebSocket连接
   * @param wsKey: websocket实例key, 默认用'default'
   * 调用
   *  1. this.$store.commit('websocket/reconnect', { wsKey: 'default' })
   *  2. commit('websocket/reconnect', { wsKey: 'default' }, { root: true })
   */
  reconnect(state, { wsKey }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (wsInfo.rws) {
      wsInfo.rws.reconnect();
    }
  },

  /**
   * 发送消息命令
   * @param wsKey: websocket实例key, 默认用'default'
   * @param msgId: 消息ID，如果不指定，则使用递增ID
   * @param cmd: 命令/接口名称
   * @param data: 命令/接口参数
   * @param callback: 回调函数(dict) => {}或包含回调函数的对象{callback: (dict) => {}, limits: 1}
   *    callback: 回调函数
   *    limits: 限制回调次数，为0时不回调，为负数为不限制回调次数，默认为1
   * 调用:
   *  1. this.$store.commit('websocket/sendCmd', {cmd: 'xxxxx', data: {}, callback: (dict) => {}})
   *  2. commit('websocket/sendCmd', {cmd: 'xxxxx', data: {}, callback: (dict) => {}}, { root: true })
   */
  sendCmd(state, { wsKey, msgId, cmd, data, callback }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (!wsInfo.rws) {
      wsInfo.logger.error(`Websocket is not init`);
      return -1;
    }
    if (wsInfo.rws.readyState !== ReconnectingWebSocket.OPEN) {
      wsInfo.logger.error(`Websocket readyState is not open`);
      return -2;
    }
    const msg = {
      cmd: cmd,
      data: data || {},
    };
    msg.id = msgId || wsInfo.msgId;
    if (msg.id === wsInfo.msgId) {
      wsInfo.msgId += 1;
      if (wsInfo.msgId > 10000) {
        wsInfo.msgId = 1;
      }
    }
    if (callback) {
      if (typeof callback === 'function') {
        wsInfo.jsonMsgCallbacks[msg.id] = {
          callback: callback,
          limits: 1,
          finished: false,
        };
      }
      else if (typeof callback === 'object' && callback.callback) {
        if (callback.limits === undefined) {
          callback.limits = 1;
        }
        callback.finished = false;
        wsInfo.jsonMsgCallbacks[msg.id] = callback;
      }
    }
    const msgStr = JSON.stringify(msg);
    if (wsInfo.options.debug) {
      wsInfo.logger.log(`Websocket send: ${msgStr}`);
    }
    wsInfo.rws.send(msgStr);
    return msg.id;
    // wsOp.sendCmd(wsInfo, {msgId, cmd, data, callback});
  },

  /**
   * 增加Websocket事件监听器
   * @param wsKey: websocket实例key, 默认用'default'
   * @param type: 事件类型, open/close/error/message
   * @param listener: 处理方法，参数为事件event
   * 调用
   *  1. this.$store.dispatch('websocket/addEventListener', { wsKey: 'default', type: 'open', (evt) => {} })
   *  2. dispatch('websocket/addEventListener', { wsKey: 'default', type: 'open', (evt) => {} }, { root: true })
   */
   addEventListener(state, { wsKey, type, listener }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (wsInfo.rws) {
      wsInfo.rws.addEventListener(type, listener);
    }
    // wsOp.addEventListener(wsInfo, type, listener);
  },
  
  /**
   * 增加Websocket消息处理器
   * @param wsKey: websocket实例key, 默认用'default'
   * @param handler: 消息处理方法，参数为消息对象
   * 调用
   *  1. this.$store.commit('websocket/addJsonMsgHandler', { wsKey: 'default', (dict) => {} })
   *  2. commit('websocket/addJsonMsgHandler', { wsKey: 'default', (dict) => {} }, { root: true })
   */
  addJsonMsgHandler(state, { wsKey, handler }) {
    const wsInfo = state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (!wsInfo.jsonMsgHandlers.includes(handler)) {
      wsInfo.jsonMsgHandlers.push(handler);
    }
    // wsOp.addEventListener(wsInfo, handler);
  }
}

const actions = {
  /**
   * 初始化WebSocket并连接
   * @param wsKey: websocket实例key, 默认用'default'
   * @param location: object, 要连接的URL信息, 参见WsInfo里面的location
   * @param options: object, 连接的附加选项, 参加WsInfo里面的options
   * 调用:
   *  1. this.$store.dispatch('websocket/init', { wsKey: 'default' })
   *  2. dispatch('websocket/init', { wsKey: 'default' }, { root: true })
   */
  init(context, { wsKey, location, options }) {
    const wsInfo = context.state.wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    context.commit('setLocation', { wsKey: wsKey, location: location });
    context.commit('setOptions', { wsKey: wsKey, options: options });
    const url = `${wsInfo.location.protocol}//${wsInfo.location.host}${wsInfo.location.port ? ':' + wsInfo.location.port : ''}${wsInfo.location.pathname}${wsInfo.location.search}`;
    wsInfo.logger.log(`Websocket init: ${url}`);

    if (wsInfo.rws) {
      context.dispatch('close', { wsKey: wsKey });
    }
    const rws = new ReconnectingWebSocket(url, wsInfo.protocols, wsInfo.options);

    rws.onopen = function (evt) {
      context.commit('setConnected', { wsKey: wsKey, connected: true });
      if (wsInfo.options.debug) {
        wsInfo.logger.log(`Websocket onopen event`);
      }
    };
    rws.onclose = function (evt) {
      context.commit('setConnected', { wsKey: wsKey, connected: false });
      if (wsInfo.options.debug) {
        wsInfo.logger.log(`Websocket onclose event`);
      }
    };
    rws.onerror = function (evt) {
      context.commit('setConnected', { wsKey: wsKey, connected: false });
      if (wsInfo.options.debug) {
        wsInfo.logger.log(`Websocket onerror event`);
      }
    };
    rws.onmessage = function (evt) {
      if (wsInfo.options.debug) {
        wsInfo.logger.log(`Websocket onmessage: ${evt.data}`);
      }
      const dict = JSON.parse(evt.data) || {};
      // 消息回调
      context.commit('callJsonMsgCallback', { wsKey: wsKey, dict: dict });
      // 消息处理
      for (const handler of wsInfo.jsonMsgHandlers) {
        handler(dict);
      }
    };
    context.commit('setRws', { wsKey: wsKey, rws: rws });
  },
  
  /**
   * 断开WebSocket连接，会触发并删除所有消息回调，触发参数是{code: 10086}
   * @param wsKey: websocket实例key, 默认用'default'
   * 调用
   *  1. this.$store.dispatch('websocket/close', { wsKey: 'default' })
   *  2. dispatch('websocket/close', { wsKey: 'default' }, { root: true })
   */
  close(context, { wsKey }) {
    const wsInfo = wsInfoMap[wsKey || 'default'];
    if (wsInfo && wsInfo.rws) {
      context.commit('close', { wsKey: wsKey });
      context.commit('delJsonMsgCallback', { wsKey: wsKey, msgId: null, trigger: true });
      context.commit('setRws', { wsKey: wsKey, rws: null });
    }
  },
  
  /**
   * 重新进行WebSocket连接
   * @param wsKey: websocket实例key, 默认用'default'
   * 调用
   *  1. this.$store.dispatch('websocket/reconnect', { wsKey: 'default' })
   *  2. dispatch('websocket/reconnect', { wsKey: 'default' }, { root: true })
   */
  reconnect(context, { wsKey }) {
    const wsInfo = wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    context.commit('reconnect', { wsKey: wsKey });
  },

  /**
   * 发送消息命令
   * @param wsKey: websocket实例key, 默认用'default'
   * @param msgId: 消息ID，如果不指定，则使用递增ID
   * @param cmd: 命令/接口名称
   * @param data: 命令/接口参数
   * @param callback: 回调函数(dict) => {}或包含回调函数的对象{callback: (dict) => {}, limits: 1}
   *    callback: 回调函数
   *    limits: 限制回调次数，为0时不回调，为负数为不限制回调次数，默认为1
   * 调用:
   *  1. this.$store.dispatch('websocket/sendCmd', {cmd: 'xxxxx', data: {}, callback: (dict) => {}})
   *  2. dispatch('websocket/sendCmd', {cmd: 'xxxxx', data: {}, callback: (dict) => {}}, { root: true })
   */
  sendCmd(context, { wsKey, msgId, cmd, data, callback }) {
    const wsInfo = wsInfoMap[wsKey || 'default'];
    if (!wsInfo) return -1;
    if (!wsInfo.rws) {
      wsInfo.logger.error(`Websocket is not init`);
      return -1;
    }
    if (wsInfo.rws.readyState !== ReconnectingWebSocket.OPEN) {
      wsInfo.logger.error(`Websocket readyState is not open`);
      return -2;
    }
    const msg = {
      cmd: cmd,
      data: data || {},
    };
    msg.id = msgId || wsInfo.msgId;
    if (msg.id === wsInfo.msgId) {
      context.commit('setMsgId', { wsKey: wsKey, msgId: wsInfo.msgId + 1 });
      if (wsInfo.msgId > 10000) {
        context.commit('setMsgId', { wsKey: wsKey, msgId: 1 });
      }
    }
    if (callback) {
      if (typeof callback === 'function') {
        context.commit('addJsonMsgCallback', { wsKey: wsKey, msgId: msg.id, callback: {
          callback: callback,
          limits: 1,
          finished: false,
        } });
      }
      else if (typeof callback === 'object' && callback.callback) {
        if (callback.limits === undefined) {
          callback.limits = 1;
        }
        callback.finished = false;
        context.commit('addJsonMsgCallback', { wsKey: wsKey, msgId: msg.id, callback: callback });
      }
    }
    const msgStr = JSON.stringify(msg);
    if (wsInfo.options.debug) {
      wsInfo.logger.log(`Websocket send: ${msgStr}`);
    }
    wsInfo.rws.send(msgStr);
    return msg.id;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
