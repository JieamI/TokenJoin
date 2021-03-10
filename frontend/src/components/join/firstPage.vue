<template>
	<div>
        <div class="title">Token团队招新简历投递</div>
        <el-steps :active="0" finish-status="success" :space="100" align-center>
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
            <el-form-item label="姓名" prop="name">
                <el-input v-model="$parent.form.name" clearable></el-input>
            </el-form-item>
            <el-form-item label="性别" prop="sex">
                <el-select v-model="$parent.form.sex" placeholder="请选择" clearable>
                    <el-option label="男" value="男"></el-option>
                    <el-option label="女" value="女"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="出生日期" prop="birthday">
                <el-date-picker
                    v-model="$parent.form.birthday"
                    type="date"
                    editable
                    placeholder="选择日期"
                    :default-value="new Date().setFullYear(2000,0,1)"
                    value-format="yyyy年MM月dd日"
                    :picker-options="{
                        disabledDate: (time) => {
                        return time.getTime() > Date.now()
                    }}" 
                    clearable>
                </el-date-picker>
            </el-form-item>
            <el-form-item label="籍贯" prop="hometown">
                <el-cascader 
                v-model="$parent.form.hometown" 
                :options="nativeList"
                :props="{value: 'label'}"
                placeholder="请选择" 
                clearable>
                </el-cascader>
            </el-form-item>
            <el-form-item label="民族" prop="nation">
                <el-select v-model="$parent.form.nation" placeholder="请选择" clearable>
                    <el-option v-for="nation in nationList" :key="nation.value" :label="nation.label" :value="nation.value"></el-option>
                </el-select>
            </el-form-item>
        </el-form>
        <div class="button-group">
            <el-button type="info" disabled>上一步</el-button>
            <el-button type="primary" @click="handleNext">下一步</el-button>
        </div>
	</div>
	
</template>

<script>
	import nationList from '../../config/nationList.js'
	import nativeList from '../../config/nativeList.js'
	export default {
		mounted() {
			// 重写日期选择组件,禁用输入，避免移动端点击该组件时弹出输入法影响体验
			document.querySelector('#app > div > div > form > div:nth-child(3) > div > div > input').setAttribute('readonly', true)
		},
		data() {
			return {
				nationList,
				nativeList,
				rules: {
					name: [
						{ required: true, message: '请输入姓名', trigger: 'blur' }
					],
					sex: [
						{ required: true, message: '性别不能为空', trigger: 'blur' }
					],
					birthday: [
						{ required: true, message: '出生日期不能为空', trigger: 'blur' }
					],
					hometown: [
						{ required: true, message: '籍贯不能为空', trigger: 'blur' }
					],
					nation: [
						{ required: true, message: '民族不能为空', trigger: 'blur' }
					]	
				}
			}
		},
		methods: {
			handleNext() {
				this.$refs['form'].validate((valid) => {
					if(valid) {
						this.$parent.currentComponent = 'secondPage'
					}else {
						return false
					}
				})
				
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
			.el-date-editor
				width 100%
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
					width 100%
					margin 4% 0
				.el-date-editor					
					width 100%
			.button-group
				display flex
				flex-direction row
				justify-content center
				padding-top 4%
				.el-button
					margin 0 6%
</style>

<style lang="stylus">
	// 修复移动端籍贯级联选择器内容显示不全的问题
	@media screen and (max-width: 750px)
		.el-cascader__dropdown
			left 0 !important
		.el-cascader-menu
			min-width 0
			max-width 130px
</style>