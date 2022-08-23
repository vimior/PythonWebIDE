// import { createStore, createLogger  } from 'vuex'
import { createStore  } from 'vuex'
import * as actions from './actions'
import * as getters from './getters'
import * as mutations from './mutations'
import modules from './modules'

const debug = process.env.NODE_ENV !== 'production'

// Create a new store instance.
const store = createStore({
  actions,
  getters,
  mutations,
  modules,
  strict: debug,
  // plugins: debug ? [createLogger()] : []
})

export default store