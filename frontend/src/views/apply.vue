<template>
	<div>
		<div class="title">
			<span>Token招新系统管理员申请</span>
		</div>
		<div class="container">
			<el-button v-if="!success" class="button" type="info" @click="handleApply" round>扫码提交申请</el-button>
			<el-button v-if="success" class="success" type="success" icon="el-icon-check" circle></el-button>
		</div>
		<el-container>
			<el-footer class="footer" height="1px">Token Team ©2020 Created by Token团队 技术部</el-footer>
		</el-container>
	</div>
</template>
<script>
	import Config from "../config/basic.js"
	import request from "../utils/requests.js"
	export default {
		beforeCreate () {
			// 创建示例前设置body背景色
			document.querySelector('body').setAttribute('style', 'background-color:antiquewhite;')
		},
		data() {
			return {
				success: false
			}
		},
		async created() {
			// 如果路径中存在查询参数(说明用户已扫码)
			var code = this.$route.query.code
			if(code) {
				let res = await request({
					url: '/apply',
					method: 'post',
					data: {
						code: code
					}
				})
				if(res.data.code === 0) {
					this.success = true
					this.$message({
						message: '申请成功',
						type: 'success',
						center: true
					})
					this.$router.push({path: '/apply'})
				}
			}
		},
		methods: {
			handleApply() {
				window.location.href = "https://oapi.dingtalk.com/connect/qrconnect?appid=" + Config.DingAppId +
					"&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=" + Config.frontDomain + "/apply"
			},
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
				margin 1.25rem
				width 15.625rem
				
			.success
				width 6.25rem
				height 6.25rem
				font-size 2.8125rem
		.footer
			font-family "microsoft yahei"
			color darkgray
</style>
