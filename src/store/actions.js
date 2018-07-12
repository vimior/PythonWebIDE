import * as types from './mutation-types';

export const openWebsocket = ({ commit }) => {
  window.GlobalUtil.model.socketModel.init_socket(window.GlobalUtil.socketInfo);
  window.GlobalUtil.model.socketModel.init_onopen(()=> {
    window.GlobalUtil.model.socketModel.socketInfo.connected = true;
    window.GlobalUtil.model.socketModel.cleanPenddingCmd();
    window.GlobalUtil.model.ideModel.listProjects();
  });
  window.GlobalUtil.model.socketModel.init_onclose((evt) => {
    window.GlobalUtil.model.socketModel.socketInfo.connected = false;
    window.GlobalUtil.model.socketModel.cleanPenddingCmd();
  });
  window.GlobalUtil.model.socketModel.init_onerror((evt) => {
    window.GlobalUtil.model.socketModel.socketInfo.connected = false;
    console.log(`onerror onerror onerror = ${evt.data}`);
  });
  window.GlobalUtil.model.socketModel.init_onmessage((evt) => {
    window.GlobalUtil.model.socketModel.onmessage(evt);
  });
};
