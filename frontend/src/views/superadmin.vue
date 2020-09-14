<template>
	<div class="wrapper">
		<transition name=".el-fade-in-linear" mode="out-in">
			<div v-if="login" class="login">
				<el-input v-model="usr" type="password"></el-input>
				<el-input v-model="pwd" type="password"></el-input>
				<el-button type="primary" @click="handleLogin">登录</el-button>
			</div>
		</transition>
		<transition name=".el-fade-in-linear" mode="out-in">
			<div class="main" v-if="!login">
				<div class="container">
					<div class="handle">
						<span>管理员</span>
						<el-button class="button" type="primary" @click="handleRemove" round>移除</el-button>
					</div>
					<el-card class="card">
						<el-table class="table" :data="adminData" width="650" height="220" @selection-change="adminChange" stripe>
							<el-table-column type="selection" width="50" align="center">
							</el-table-column>
							<el-table-column prop="Nick" label="姓名" width="300" align="center">
							</el-table-column>
							<el-table-column prop="Department_name" label="所属部门" width="300" align="center">
							</el-table-column>
						</el-table>
					</el-card>
				</div>
				<div class="container">
					<div class="handle">申请列表
						<div class="button-group">
							<el-button class="button" type="primary" @click="handleAccept" round>同意</el-button>
							<el-button class="button" type="primary" @click="handleRefuse" round>拒绝</el-button>
						</div>
					</div>
					<el-card class="card">
						<el-table class="table" :data="applyData" width="650" height="220" @selection-change="applyChange" stripe>
							<el-table-column type="selection" width="50px" align="center">
							</el-table-column>
							<el-table-column prop="Nick" label="姓名" width="300" align="center">
							</el-table-column>
							<el-table-column prop="Department_name" label="申请部门" width="300" align="center">
							</el-table-column>
						</el-table>
					</el-card>
				</div>
			</div>
		</transition>
	</div>
</template>

<script>
	// import Config from '../config/basic.js'
	import request from '../utils/requests.js'
	export default {
		data() {
			return {
				login: true,
				usr: '',
				pwd: '',
				adminSelection: [],
				applySelection: [],
				adminData: [],
				applyData: []
			}
		},
		mounted() {
			// 根据不同设备设置不同的宽度,确保内容在所有设备上都能完整显示
			var el = document.querySelector('.wrapper')
			var width = screen.width
			if(width >= 1500) {
				el.setAttribute('style', 'width: ' + width + 'px')
			}else {
				el.setAttribute('style', 'width: 1500px;')
			}
			// 禁用纵向滚动条,优化移动端体验
			document.querySelector('#app').setAttribute('style', 'overflow-y: hidden;')
		},
		methods: {
			adminChange(val) {
				this.adminSelection = val
			},
			applyChange(val) {
				this.applySelection = val
			},
			async handleLogin() {
				let res = await	request({
					url: 'super/getalltabledata',
					method: 'post',
					data: {
						usr: this.usr,
						pwd: this.pwd
					}
				})
				if(res.data) {
					this.adminData = res.data.admin_lis
					this.applyData = res.data.apply_lis	
					this.login = false
				}
			},
			async handleAccept() {
				if(!this.applySelection.length) {
					this.$message({
						message: '没有用户被勾选哦',
						type: 'warning',
						center: true
					})
					return
				}
				let res = await request({
					url: '/super/authorsetting',
					method: 'post',
					data: {
						accept_lis: this.applySelection,
						usr: this.usr,
						pwd: this.pwd
					}
				})
				if(res.data.code === 0) {
					this.applySelection.forEach((val) => {
						let index = this.applyData.indexOf(val)
						this.adminData.unshift(this.applyData[index])
						this.applyData.splice(index, 1)
					})
				}
			},
			async handleRefuse() {
				if(!this.applySelection.length) {
					this.$message({
						message: '没有用户被勾选哦',
						type: 'warning',
						center: true
					})
					return
				}
				let res = await request({
					url: '/super/authorsetting',
					method: 'post',
					data: {
						refuse_lis: this.applySelection,
						usr: this.usr,
						pwd: this.pwd,
					}
				})
				if(res.data.code === 0) {
					this.applySelection.forEach((val) => {
						let index = this.applyData.indexOf(val)
						this.applyData.splice(index, 1)
					})
				}
			},
			async handleRemove() {
				if(!this.adminSelection.length) {
					this.$message({
						message: '没有用户被勾选哦',
						type: 'warning',
						center: true
					})
					return
				}
				this.$confirm("确定移除所选管理员吗？", '提示', {
					type: 'warning',
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					center: true
				}).then(async () => {
					let res = await request({
						url: '/super/authorsetting',
						method: 'post',
						data: {
							remove_lis: this.adminSelection,
							usr: this.usr,
							pwd: this.pwd,
						}
					})
					if(res.data.code === 0) {
						this.adminSelection.forEach((val) => {
							let index = this.adminData.indexOf(val)
							this.adminData.splice(index, 1)
						})
					}
				}).catch(() => {})
			}
		}
	}
</script>

<style lang="stylus" scoped>
	.login
		width 400px
		height 200px
		margin auto
		margin-top 10%
		.el-input
			margin 12px
		.el-button
			margin 10px 30%
			width 180px
	.main
		display flex
		flex-direction column
		align-items center
		justify-content center
		width 100%
		height 100%
		.container
			display flex
			width 100%
			justify-content space-around
			margin 10px
			.card
				width 700px
			.handle
				display flex
				margin-right -200px
				flex-direction column
				justify-content space-around
				align-items center
				font-family "microsoft yahei"
				font-size 30px
				.button
					width 150px
					margin 10px
				.button-group
					display flex
					flex-direction column
					.button
						margin 10px
						width 150px
</style>
