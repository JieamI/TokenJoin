<template>
	<div v-loading="loadind"> 
		<transition name="el-zoom-in-center" mode="out-in">
			<keep-alive>
				<component :is="currentComponent" @submit="handleSubmit"></component>
			</keep-alive>
		</transition>
	</div>
</template>

<script>
	import request from '../utils/requests.js'
	import firstPage from '../components/join/firstPage.vue'
	import secondPage from '../components/join/secondPage.vue'
	import thirdPage from '../components/join/thirdPage.vue'
	import fourthPage from '../components/join/fourthPage.vue'
	export default {
		components: {
			firstPage,
			secondPage,
			thirdPage,
			fourthPage
		},
		props: ['dept'],
		data() {
			return {
				currentComponent: "firstPage",
				loadind: false,
				form: {
					name: '',
					sex: '',
					birthday: '',
					hometown: '',
					nation: '',
					// 学号
					sno: '',
					college: '',
					grade: '',
					// 专业班级
					proclass: '',
					dormitory: '',
					phone: '',
					qq: '',
					mail: '',
					department: '',
					experience: '',
					introduce: '',
					reason: '',
				}
			}
		},
		beforeCreate() {
			document.querySelector('body').setAttribute('style', 'background-color: whitesmoke;')
		},
		created() {
			let form = JSON.parse(window.localStorage.getItem('form'))
			if(form) {
				this.form = form
			}
			let depts = ['技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部']
			if(depts.indexOf(this.dept) != -1) {
				this.form.department = this.dept
			}
		},
		methods: {
			async handleSubmit() {
				let timestamp = JSON.parse(window.localStorage.getItem('timestamp'))
				// 如果本地存储存入timestamp则判断两次提交时间间隔是否超过一天,超过一天则不允许提交
				if(timestamp) {
					if((Date.parse(new Date()) - timestamp) / (24 * 60 * 60 * 1000) < 1) {
						this.$message({
							message: '您已投递简历，若需更改请在24小时后操作',
							type: 'warning',
							center: true
						})
						return
					}
				}
				// 将form的hometown和dormitory属性转化为字符串: array >>> string
				this.form.hometown = this.form.hometown.join('/')
				this.form.dormitory = this.form.dormitory.join('/')
				let res = await request({
					url: '/join/cv',
					method: 'post',
					data: this.form
				})
				if(res.data.code === 0) {
					this.$message({
						message: '您的简历投递成功',
						type: 'success',
						center: true
					})
					window.localStorage.setItem('timestamp', JSON.stringify(Date.parse(new Date())))
					// 提交后再将籍贯和寝室转化为级联选择器组件所支持的数组形式,并重新存入本地存储
					this.form.hometown = this.form.hometown.split('/')
					this.form.dormitory = this.form.dormitory.split('/')
					window.localStorage.setItem('form', JSON.stringify(this.form))
					this.$router.push({path: '/join/index'})
				}
			}
		},
		mounted() {
			window.onbeforeunload = () => {
				window.localStorage.setItem('form', JSON.stringify(this.form))
			}
		}
	}
</script>
