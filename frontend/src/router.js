import Vue from 'vue'
import VueRouter from 'vue-router'

// 禁用路由跳转报错
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

let router =  new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes: [{
		path: '/login',
		component: () => import(/* webpackChunkName: "login" */ './views/login.vue')
	},{
		path: '/apply',
		component: () => import(/* webpackChunkName: "apply" */ './views/apply.vue')
	},{
		path: '/superadmin',
		component: () => import(/* webpackChunkName: "admin" */ './views/superadmin.vue')
	},{
		path: '/join/index',
		component: () => import(/* webpackChunkName: "join" */ './components/join/index')
	},{
		path: '/join/apply/:dept?',
		component: () => import(/* webpackChunkName: "join" */ './views/join.vue'),
		props: true
	},{
		path: '/join*',
		redirect: '/join/index'
	},{
		path: '/admin',
		component: () => import(/* webpackChunkName: "admin" */ './views/admin.vue'),
		redirect: '/admin/cvadmin',
		children: [{
			path: 'setting',
			component: () => import(/* webpackChunkName: "admin" */ './components/admin/setting.vue')
		},{
			path: 'index',
			component: () => import(/* webpackChunkName: "admin" */ './components/admin/index.vue')
		},{
			path: 'cvadmin',
			component: () => import(/* webpackChunkName: "admin" */ './components/admin/cvadmin.vue')
		},{
			path: 'tpadmin',
			component: () => import(/* webpackChunkName: "admin" */ './components/admin/tpadmin.vue')
		},{
			path: 'record',
			component: () => import(/* webpackChunkName: "admin" */ './components/admin/record.vue')
		}
		]},{
		path: '/admin/*',
		redirect: '/admin/cvadmin'
		},{
		path: '/*',
		redirect: '/login'
	}]
})

// 注册全局导航守卫
router.beforeEach((to, from, next) => {
		if(to.path === '/superadmin' || /join.*/.test(to.path) || to.path === '/login' || to.path === '/apply') {
			next()
			return
		}
		let userInfo = JSON.parse(window.localStorage.getItem('userInfo'))
		// 如果本地没有用户信息则跳转至登陆界面要求用户重新登录
		if(!userInfo) {
			Vue.prototype.$message({
				message: '令牌失效，请重新登录',
				type: 'warning',
				center: true
			})
			next('/login')
		}
		// 如果用户授权码为0且试图访问简历管理以外的页面则强制定向至简历管理页面
		if(!userInfo.authcode && to.path != '/admin/cvadmin' && /admin\/./.test(to.path)) {	
			next('/admin/cvadmin')
			Vue.prototype.$message({
				message: '你无权访问其它页面！',
				type: 'warning',
				center: true
			})
		}else {
			next()
		}
})

export default router