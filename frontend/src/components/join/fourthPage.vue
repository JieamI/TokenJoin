<template>
	<div>
		<div class="title">Token团队招新简历投递</div>
		<el-steps :active="3" finish-status="success" :space="100" align-center>
			<el-step title="基础信息"></el-step>
			<el-step title="学生信息"></el-step>
			<el-step title="联系方式"></el-step>
			<el-step title="申请信息"></el-step>
		</el-steps>
		<el-form 
			label-position="top" 
			size="small"
			ref="form"
			:model="$parent.form"
			:rules="rules" 
			status-icon>
			<el-form-item label="要加入的部门:" prop="department">
				<el-select v-model="$parent.form.department" placeholder="请选择" clearable>
					<el-option v-for="department in departmentList" :key="department.val" :label="department.title" :value="department.val"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="个人经历（社团、学生干部经历或获奖情况）:" prop="experience">
				<el-input v-model="$parent.form.experience" type="textarea" rows="4" resize="none"></el-input>
			</el-form-item>
			<el-form-item label="自我介绍（性格、爱好、专业技能或作品简介）:" prop="introduce">
				<el-input v-model="$parent.form.introduce" type="textarea" rows="4" resize="none"></el-input>
			</el-form-item>
			<el-form-item label="加入Token团队的目的或原因:" prop="reason">
				<el-input v-model="$parent.form.reason" type="textarea" rows="4" resize="none"></el-input>
			</el-form-item>
		</el-form>
		<div class="button-group">
			<el-button type="info" @click="handleBack">上一步</el-button>
			<el-button type="primary" @click="handleSubmit">提交</el-button>
		</div>
	</div>
</template>

<script>
	import request from '../../utils/requests.js'
	export default {
		data() {
			return {
				departmentList: [],
				rules: {
					department: [
						{ required: true, message: '部门不能为空', trigger: 'blur' }
					],
					experience: [
						{ required: true, message: '个人经历不能为空', trigger: 'blur' }
					],
					introduce: [
						{ required: true, message: '自我介绍不能为空', trigger: 'blur' }
					],
					reason: [
						{ required: true, message: '目的或原因不能为空', trigger: 'blur' }
					]
				}
			}
		},
		async created() {
			let res = await request({
				url: '/dept/getshow',
				method: 'get',
			})
			// 未处于显示状态的部门不能显示在部门下拉框中
            if(res.data.code === 0) {
                let resList = res.data.data
                if(resList.length) {
                    resList.forEach(dept => {
                        this.departmentList.push({title: dept, val: dept})
                    })
                }
            }
           
		},
		methods: {
			handleSubmit() {
				this.$refs['form'].validate((valid) => {
					if(valid) {
						this.$confirm("确定提交吗？", '提示', {
							customClass: 'confirm-submit',
							type: 'info',
							confirmButtonText: '确定',
							cancelButtonText: '取消',
						}).then(() => {
							this.$emit('submit')
						}).catch(() => {})
					}else {
						return false
					}
				})
			},
			handleBack() {
				this.$parent.currentComponent = 'thirdPage'
			}
		}
	}
</script>

<style lang="stylus" scoped>
	// 手机端显示
	@media screen and (max-width: 750px)
		div
			display flex
			flex-direction column
			justify-content flex-start
			.title
				height 5%
				margin 10% 0 
				text-align center
				font-family "microsoft yahei"
				font-size 2.5em
				color gray
			.el-steps
				flex-direction row
				justify-content center
			.el-form-item
				margin 2% 12%
			.button-group
				display flex
				flex-direction row
				justify-content space-around
				.el-button
					margin 10% 0
					width 100px
	// 电脑端显示
	@media screen and (min-width: 750px)
		div
			display flex
			height 100%
			flex-direction column
			justify-content flex-start
			.title
				padding 2% 0
				text-align center
				font-size 2.3rem
				font-family "microsoft yahei"
				color gray
			.el-steps
				flex-direction row
				justify-content center
			.el-form
				margin 0 38%
				.el-form-item
					margin 4% 0
			.button-group
				display flex
				flex-direction row
				justify-content center
				padding 4% 0
				.el-button
					margin 0 5%
					width 100px
</style>
<style lang="stylus">
	@media screen and (max-width: 750px)
		.confirm-submit
			width auto
	</style>