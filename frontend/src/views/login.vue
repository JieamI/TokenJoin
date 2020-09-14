<template>
	<div>
		<div class="title">
			<span>Token团队招新管理系统</span>
		</div>
		<div class="container">
			<el-button class="button" type="primary" round="" @click="handleLogin">钉钉扫码登录</el-button>
			<router-link to="/apply">
				<el-button class="button" type="success" round="">管理员申请</el-button>
			</router-link>
		</div>
		<el-container>
			<el-footer class="footer" height="1px" @click.native="vipPass">Token Team ©2020 Created by Token团队 技术部</el-footer>
		</el-container>
	</div>
</template>
<script>
	import Config from "../config/basic.js"
	import request from "../utils/requests.js"
	export default {
		data() {
			return {
			}
		},
		beforeCreate() {
			document.querySelector('body').setAttribute('style', 'background-color: antiquewhite;')
		},
		async created() {
			// 如果本地存储有用户信息则直接登录
			this.$store.commit("getUserInfo")
			if(this.$store.state.userInfo) {
				this.$router.push({path: '/admin/cvadmin'})
			}
			// 如果路径中存在查询参数(说明用户已扫码)
			var code = this.$route.query.code
			if(code) {
				let res = await request({
					url: '/login',
					method: 'post',
					data: {
						code: code
					}
				})
				if(res) {
					window.localStorage.setItem("userInfo", JSON.stringify(res.data))
					this.$store.commit("getUserInfo")
					this.$router.push({path: "/admin/cvadmin"})
				}
			}
		},
		methods: {
			handleLogin() {
				window.location.href = "https://oapi.dingtalk.com/connect/qrconnect?appid=" + Config.DingAppId +
					"&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=" + Config.frontDomain + "/login"
			},
			vipPass() {
				this.$router.push({path: '/superadmin'})
			}
		}
	}
</script>

<style lang="stylus" scoped>
	div
		display flex
		flex-direction column
		width 100%
		height 97%
		align-items center
		.title
			display flex
			flex-direction row
			align-items flex-end
			justify-content center
			span
				font-family "microsoft yahei"
				margin 3.125rem
				font-size 2.8125rem
		.container
			display flex
			.button
				width 15.625rem
				margin 0.625rem
				font-size 0.875rem
		.footer
			font-family "microsoft yahei"
			color darkgray
</style>
