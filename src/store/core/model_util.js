const UtilModel = {};
const self = UtilModel;

self.checkStrIsLegal = (str, isFile) => {
  const errStr = `'Name contains "only letter, numbers, '_' and no more than 15 characters in total.${[]}`;
  if (str === null || str === undefined || str.length === 0) {
    return false;
  }
  if (str.length > 15) {
    return errStr;
  }
  for (let i = 0; i < str.length; i++) {
    if (isFile !== true) {
      if (!((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z') || str[i] === '_' || (str[i] >= '0' && str[i] <= '9'))) {
        return errStr;
      };
    }
    else {
      if (!((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z') || str[i] === '_' || str[i] === '.' || (str[i] >= '0' && str[i] <= '9'))) {
        return errStr;
      };
    };
  };
  return true;
}

export default self;
