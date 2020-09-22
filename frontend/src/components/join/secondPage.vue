<template>
	<div>
		<div class="title">Token团队招新简历投递</div>
		<el-steps :active="1" finish-status="success" :space="100" align-center>
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
			<el-form-item label="学号" prop="sno">
				<el-input v-model="$parent.form.sno" clearable></el-input>
			</el-form-item>
			<el-form-item label="学院" prop="college">
				<el-select v-model="$parent.form.college" placeholder="请选择" clearable>
					<el-option v-for="college in collegeList" :key="college.val" :label="college.title" :value="college.val"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="年级" prop="grade">
				<el-select v-model="$parent.form.grade" placeholder="请选择" clearable>
					<el-option v-for="grade in gradeList" :key="grade.val" :label="grade.title" :value="grade.val"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="专业班级" prop="proclass">
				<el-input v-model="$parent.form.proclass" clearable></el-input>
			</el-form-item>
			<el-form-item label="寝室" prop="dormitory">
				<el-cascader
					v-model="$parent.form.dormitory"
					:options="dormitoryList"
					placeholder="请选择" 
					clearable>
				</el-cascader>
			</el-form-item>
		</el-form>
		<div class="button-group">
			<el-button type="info" @click="handleBack">上一步</el-button>
			<el-button type="primary" @click="handleNext">下一步</el-button>
		</div>
	</div>
</template>

<script>
	import dormitoryList from '../../config/dormitoryList.js'
	import gradeList from '../../config/gradeList.js'
	import collegeList from '../../config/collegeList.js'
	export default {
		data() {
			var checksno = (rule, value, callback) => {
				if(!value) {
					return callback(new Error('学号不能为空'))
				}
				var reg = /^\d{13}$/
				if(!reg.test(value)) {
					return callback(new Error('学号不合法'))
				}
				return callback()
			}
			return {
				dormitoryList,
				gradeList,
				collegeList,
				rules: {
					sno: [
						{ validator: checksno, trigger: 'blur' }
					],
					college: [
						{ required: true, message: '学院不能为空', trigger: 'blur' }
					],
					grade: [
						{ required: true, message: '年级不能为空', trigger: 'blur' }
					],
					proclass: [
						{ required: true, message: '专业班级不能为空', trigger: 'blur' }
					],
					dormitory: [
						{ required: true, message: '寝室不能为空', trigger: 'blur' }
					],
				}
			}
		},
		methods: {
			handleNext() {
				this.$refs['form'].validate((valid) => {
					if(valid) {
						this.$parent.currentComponent = 'thirdPage'
					}else {
						return false
					}
				})
			},
			handleBack() {
				this.$parent.currentComponent = 'firstPage'
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