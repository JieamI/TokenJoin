<template>
	<el-container class="container-wrap">
		<el-aside>
			<el-menu default-active="1" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
				<div class="title">Token招新管理系统</div>
				<el-menu-item index="0" :disabled="unauthorized" @click="handlePush(0)">
					<i class="el-icon-s-home"></i>
					<span>首页</span>
				</el-menu-item>
				<el-menu-item index="1" @click="handlePush(1)">
					<i class="el-icon-edit-outline"></i>
					<span>招新简历管理</span>
				</el-menu-item>
				<el-menu-item index="2" :disabled="unauthorized" @click="handlePush(2)">
					<i class="el-icon-tickets"></i>
					<span>信息模板管理</span>
				</el-menu-item>
				<el-menu-item index="3" :disabled="unauthorized" @click="handlePush(3)">
					<i class="el-icon-setting"></i>
					<span>管理员权限设定</span>
				</el-menu-item>
				<el-menu-item index="4" :disabled="unauthorized" @click="handlePush(4)">
					<i class="el-icon-date"></i>
					<span>管理员操作记录</span>
				</el-menu-item>
			</el-menu>
		</el-aside>
		
		<el-container>
			<el-header>
				<div class="switch_wrapper">
					<span>部门展示</span>
					<el-switch
						v-model="show"
						active-color="#13ce66"
						inactive-color="#ff4949"
						:disabled="unauthorized">
					</el-switch>
				</div>
				<div class="logout_wrapper">
					<span>当前用户：{{ this.$store.state.userInfo.nick }}</span>
					<i class="el-icon-switch-button" @click="handleLogout" style="cursor: pointer;"></i>
				</div>
			</el-header>
			
			<el-main class="main">
				<keep-alive>
					<router-view></router-view>
				</keep-alive>
			</el-main>
			<el-footer height="30px">Token Team ©2020 Created by Token团队 技术部</el-footer>
		</el-container>
	</el-container>
</template>

<script>
	import request from '../utils/requests.js'
	export default {
		data() {
			return {
				unauthorized: this.$store.state.userInfo.authcode === 0
			}
		},
		async created() {
			if(!this.$store.state.userInfo.authcode) {
				return
			}
			let res = await request({
				url: '/deptstate',
				method: 'get'
			})
			if(res && res.data) {
				this.$store.commit('setDeptState', res.data)
			}
		},
		mounted() {
			// 根据不同设备设置不同的宽度,确保内容在所有设备上都能完整显示
			var el = document.querySelector('.container-wrap')
			var width = screen.width
			if(width >= 1500) {
				el.setAttribute('style', 'width: ' + width + 'px')
			}else {
				el.setAttribute('style', 'width: 1500px;')
			}
			// 禁用纵向滚动条,优化移动端体验
			document.querySelector('#app').setAttribute('style', 'overflow-y: hidden;')
		},
		computed: {
			show: {
				get() {
					return this.$store.state.deptState.Show
				},
				set(val) {
					if(!val) {
						this.$confirm("确定要关闭部门展示吗？关闭部门展示后将无法向该部门投递简历", '提示', {
							type: 'warning',
							confirmButtonText: '确定',
							cancelButtonText: '取消',
							center: true
						}).then(() => {
							this.$store.dispatch('setShowState', val)
						}).catch(() => {})
					}else {
						this.$store.dispatch('setShowState', val)
					}
				}
			}
		},
		methods: {
			handlePush(index) {
				if(this.unauthorized && index != 1) {
					return
				}
				switch(index) {
					case(0): this.$router.push({path: '/admin/index'});break;
					case(1): this.$router.push({path: '/admin/cvadmin'});break;
					case(2): this.$router.push({path: '/admin/tpadmin'});break;
					case(3): this.$router.push({path: '/admin/setting'});break;
					case(4): this.$router.push({path: '/admin/record'});break;	
				}
			},
			handleLogout() {
				window.localStorage.removeItem('userInfo')
				this.$router.push({path: '/login'})
			}
		}
	}
</script>

<style lang="stylus" scoped>
	.container-wrap
		height 100%
		width 100%
		background-color ghostwhite
		.el-aside
			background-color #545c64
			width 220px !important
			.title
				height 70px
				background-color #545c64
				color white
				font-family "microsoft yahei"
				font-size 20px
				display flex
				justify-content center
				align-items center
			.el-menu-item
				font-family "microsoft yahei"
				font-size 16px
		.el-header
			margin 3px
			display flex
			align-items center
			justify-content space-between
			background-color whitesmoke
			box-shadow 0px 3px 10px grey
			.switch_wrapper
				display flex
				flex-direction column
				font-family "microsoft yahei"
				font-size 12px
				color gray
				div
					margin 5px auto
			.logout_wrapper i
				margin 0 10px
				font-size 20px
		.el-footer
			font-family "microsoft yahei"
			color darkgray
			text-align center
</style>
