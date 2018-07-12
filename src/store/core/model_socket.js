import ReconnectingWebSocket from '@/assets/lib/reconnecting-websocket';

const SocketModel = {};
const self = SocketModel;

self.socketInfo = {
  socket: null,
  protocol: 'ws',
  host: null,
  path: '/ws',
  connected: false,
};

self.msgid = 0;
self.response = '';
self.penddingCmds = {};

self.init_socket = (args) => {
  const self = SocketModel;
  args = args || {};
  args.logger = args.logger || console;
  self.socketInfo.protocol = args.protocol || self.socketInfo.protocol;
  self.socketInfo.host = args.host || self.socketInfo.host;
  self.socketInfo.path = args.path || self.socketInfo.path;
  const ws_url = `${self.socketInfo.protocol}://${self.socketInfo.host}${self.socketInfo.path}`;
  console.log('ws url:', ws_url);
  self.socketInfo.socket = new ReconnectingWebSocket(ws_url, null, {
    debug: false,
    logger: args.logger,
    reconnectInterval: 1000,
  });
};

self.init_onopen = (onopen) => {
  self.socketInfo.socket.onopen = onopen;
};

self.init_onclose = (onclose) => {
  self.socketInfo.socket.onclose = onclose;
};

self.init_onmessage = (onmessage) => {
  self.socketInfo.socket.onmessage = onmessage;
};

self.init_onerror = (onerror) => {
  self.socketInfo.socket.onerror = onerror;
};

self.sendMsg = (msg, callback, id) => {
  const self = SocketModel;
  if (self.socketInfo.socket === null || self.socketInfo.socket === undefined) {
    console.log('self.socketInfo.socket.readyState is not init');
    return -1;
  }
  if (self.socketInfo.socket.readyState !== ReconnectingWebSocket.OPEN) {
    console.log('self.socketInfo.socket.readyState is not open');
    return -1;
  }
  if (id !== undefined) {
    msg.id = id;
  }
  else {
    if (self.msgid > 10000) {
      self.msgid = 0;
    }
    self.msgid += 1;
    msg.id = self.msgid;
  }
  if (callback) {
    self.penddingCmds[msg.id] = callback;
  }
  const js_msg = JSON.stringify(msg);
  console.log(`send: msg.id = ${msg.id}, js_msg = ${js_msg}`);
  self.socketInfo.socket.send(js_msg);
  return msg.id;
}

self.sendCmd = (cmd, data, callback, id) => {
  const self = SocketModel;
  const msg = {};
  data = data || {};
  msg.cmd = cmd;
  msg.data = data;
  self.sendMsg(msg, callback, id);
};

self.onmessage = (evt) => {
  const dict = JSON.parse(evt.data) || {};
  const callback = self.penddingCmds[dict.id];
  if (dict.type !== 'response') {
    return;
  }
  if (dict.id === null) {
    return;
  }
  if (callback) {
    callback(dict);
  }
}

self.cleanPenddingCmd = () => {
  for (const key in self.penddingCmds) {
    const callback = self.penddingCmds[key];
    if (callback) {
      callback({
        code: 10086,
      });
    }
  }
  self.penddingCmds = {};
};

export default self;
