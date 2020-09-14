<template>
	<div>
		<div class="title">Token团队招新简历投递</div>
		<el-steps :active="2" finish-status="success" :space="100" align-center>
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
			<el-form-item label="手机号码" prop="phone">
				<el-input v-model="$parent.form.phone"></el-input>
			</el-form-item>
			<el-form-item label="QQ号" prop="qq">
				<el-input v-model="$parent.form.qq"></el-input>
			</el-form-item>
			<el-form-item label="邮箱" prop="mail">
				<el-input v-model="$parent.form.mail"></el-input>
			</el-form-item>
		</el-form>
		<div class="button-group">
			<el-button type="info" @click="handleBack">上一步</el-button>
			<el-button type="primary" @click="handleNext">下一步</el-button>
		</div>
	</div>
</template>

<script>
	export default {
		data() {
			// 邮箱验证
			var checkmail = (rule, value, callback) => {
				if(!value) {
					return callback(new Error('邮箱不能为空'))
				}
				var reg=/^\w+@[a-zA-Z0-9]{2,10}(?:\.[a-z]{2,4}){1,3}$/
				if(!reg.test(value)) {
					return callback(new Error('邮箱格式不合法'))
				}
				return callback()
			}
			// QQ号验证
			var checkqq = (rule, value, callback) => {
				if(!value) {
					return callback(new Error('QQ号不能为空'))
				}
				var reg=/^[0-9]{5,11}$/
				if(!reg.test(value)) {
					return callback(new Error('QQ号格式不合法'))
				}
				return callback()
			}
			// 手机号验证
			var checkphone = (rule, value, callback) => {
				if(!value) {
					return callback(new Error('手机号不能为空'))
				}
				var reg= /^((0\d{2,3}-\d{7,8})|(1[3584]\d{9}))$/
				if(!reg.test(value)) {
					return callback(new Error('手机号格式不合法'))
				}
				return callback()
			}
			return {
				rules: {
					phone: [
						{ validator: checkphone, trigger: 'blur' }
					],
					qq: [
						{ validator: checkqq, trigger: 'blur' }
					],
					mail: [
						{ validator: checkmail, trigger: 'blur' }
					]
				},
			}
		},
		methods: {
			handleNext() {
				this.$refs['form'].validate((valid) => {
					if(valid) {
						this.$parent.currentComponent = 'fourthPage'
					}else {
						return false
					}
				})
			},
			handleBack() {
				this.$parent.currentComponent = 'secondPage'
			}
		}
	}
</script>

<style lang="stylus" scoped>
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
	@media screen and (min-width: 750px)
		div
			display flex
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
				padding-top 4%
				.el-button
					margin 0 6%
</style>