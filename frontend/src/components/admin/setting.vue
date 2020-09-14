<template>
	<div class="main" v-loading="loading">
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
</template>

<script>
	import request from '../../utils/requests.js'
	// import mapState from 'vuex'
	export default {
		data() {
			return {
				loading: true,
				adminSelection: [],
				applySelection: [],
				adminData: [],
				applyData: []
			}
		},
		async created() {
			// 获取adminData,applyData数据
			let res = await	request({
				url: '/setting/tabledata',
				method: 'get'
				})
			if(res) {
				this.adminData = res.data.admin_lis
				this.applyData = res.data.apply_lis	
				this.loading = false
			}
		},
		methods: {
			adminChange(val) {
				this.adminSelection = val
			},
			applyChange(val) {
				this.applySelection = val
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
					url: '/setting/accept',
					method: 'post',
					data: this.applySelection
				})
				if(res.data.code === 0) {
					this.applySelection.forEach((val) => {
						let index = this.applyData.indexOf(val)
						this.adminData.unshift(this.applyData[index])
						this.applyData.splice(index, 1)
					})
					// sessionStorage.setItem('adminData', JSON.stringify(this.adminData))
					// sessionStorage.setItem('applyData', JSON.stringify(this.applyData))
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
					url: '/setting/refuse',
					method: 'post',
					data: this.applySelection
				})
				if(res.data.code === 0) {
					this.applySelection.forEach((val) => {
						let index = this.applyData.indexOf(val)
						this.applyData.splice(index, 1)
					})
					// sessionStorage.setItem('applyData', JSON.stringify(this.applyData))
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
						url: '/setting/remove',
						method: 'post',
						data: this.adminSelection
					})
					if(res.data.code === 0) {
						this.adminSelection.forEach((val) => {
							let index = this.adminData.indexOf(val)
							this.adminData.splice(index, 1)
						})
						// sessionStorage.setItem('adminData', JSON.stringify(this.adminData))
					}
				}).catch(() => {})
			}
		}
	}
</script>

<style lang="stylus" scoped>
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
