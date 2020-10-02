// import axios from "axios"
import Config from "../config/basic.js"
import router from "../router.js"
import axios from 'axios'
import Vue from 'vue'

export default async function request(options) {
	options.baseURL = Config.backendDomain
	options.timeOut = 5000
	
	var userInfo = JSON.parse(window.localStorage.getItem('userInfo'))
	axios.interceptors.request.use(config => {
		if(userInfo && userInfo.access_token) {
			config.headers.Authorization = userInfo.token_type + ' ' + userInfo.access_token 
		}
		return config
	})
	
	// if(!window.$source) {
	// 	// 首次请求
	// 	window.$source = axios.CancelToken.source()
	// }else {
	// 	// 取消上一次请求
	// 	window.$source.cancel()
	// 	window.$source = axios.CancelToken.source()
	// 	options.cancelToken = window.$source.token
	// }
	
	try{
		var res = await axios(options)
	}catch(e){
        console.log(e)
        if(e.response.data.detail) {
            Vue.prototype.$message({
                message: e.response.data.detail,
                type: 'error',
                center: true
            })
        }
		// 如果错误码是未授权，则清除本地用户信息，回到登录界面
		if(e.response.status == 401) {
			window.localStorage.removeItem("userInfo")
			router.push({path: "/login"})
			
		}
		return null
	}
	return res
}