import Vue from 'vue'
import Vuex from 'vuex'
import request from './utils/requests.js'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		userInfo: JSON.parse(window.localStorage.getItem("userInfo")),
		deptState: {}
	},
	mutations: {
		setDeptState: (state, data) => {
			state.deptState = data
		},
		setShowState: (state, val) => {
			state.deptState.Show = val
		},
		setMessage: (state, msgList) => {
			state.deptState.Message = msgList
		},
		getUserInfo: (state) => {
			state.userInfo = JSON.parse(window.localStorage.getItem("userInfo"))
		}
	},
	actions: {
		setShowState: async ({commit}, val) => {
			let res = await request({
				url: '/updateshow',
				method: 'post',
				data: {
					'Show': val
				}
			})
			if(res.data.code === 0) {
				commit('setShowState', val)
			}
		},
		setMessage: async ({commit}, msgList) => {
			let res = await request({
				url: '/updatemsg',
				method: 'post',
				data: {
					'Message': msgList
				}
			})
			if(res.data.code === 0) {
				commit('setMessage', msgList)
			}
		}
	}
})
