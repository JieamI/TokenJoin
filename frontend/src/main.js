import Vue from 'vue'
import router from './router.js'
import store from './store.js'
import ElementUI from 'element-ui'
import App from './App.vue'
import VueTouch from 'vue-touch'

Vue.config.productionTip = false
Vue.use(VueTouch, {name: 'v-touch'})
Vue.use(ElementUI)


new Vue({
	router,
	store,
	render: h => h(App)
}).$mount('#app')
