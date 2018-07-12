import Model from './model';
import Constant from './constant';

const socketInfo = {
  protocol: 'ws',
  host: window.location.hostname + ':10086',
  path: '/ws',
};
if (process.env.NODE_ENV === 'production') {
  socketInfo.host = window.location.host;
  console.log = () => {};
  console.warn = () => {};
}

const GlobalUtil = {};
const self = GlobalUtil;
window.GlobalUtil = self;
self.model = Model;
self.constant = Constant;
self.socketInfo = socketInfo;

export default self;
