<template>
	<el-card>
		<el-card v-for="(item, index) in record_lis" :key="index">
			<el-tag>{{ item.Operator }}</el-tag>
			<el-tag type="danger" class="operation">{{ item.Operation }}</el-tag>
			<el-tag type="success" class="time">{{ item.Time }}</el-tag>
		</el-card>
	</el-card>
</template>

<script>
	// import request from '../../utils/requests.js'
	export default {
		data() {
			return {
				// record_lis: [{
				// 	Operator: 'jie',
				// 	Operation: '同意了xxx的申请',
				// 	Time: '2020/4/5 12:30:45'
				// },{
				// 	Operator: 'jie',
				// 	Operation: '同意了xxx的申请',
				// 	Time: '2020/4/5 12:30:45'
				// },{
				// 	Operator: '的hi哎i',
				// 	Operation: '同意了xxx达瓦达瓦的申请',
				// 	Time: '2020/4/5 12:30:45'
				// },{
				// 	Operator: 'jie',
				// 	Operation: '同意了xxx的申请',
				// 	Time: '2020/4/5 12:30:45'
				// },{
				// 	Operator: 'jie',
				// 	Operation: '同意了xxx的申请',
				// 	Time: '2020/4/5 12:30:45'
				// },{
				// 	Operator: 'jie',
				// 	Operation: '同意了xxx的申请',
				// 	Time: '2020/4/5 12:30:45'
				// },{
				// 	Operator: 'jie',
				// 	Operation: '同意了xxx的申请',
				// 	Time: '2020/4/5 12:30:45'
				// },{
				// 	Operator: 'jie',
				// 	Operation: '同意了xxx的申请',
				// 	Time: '2020/4/5 12:30:45'
				// },{
				// 	Operator: 'jie',
				// 	Operation: '同意了xxx的申请',
				// 	Time: '2020/4/5 12:30:45'
				// },{
				// 	Operator: 'jie',
				// 	Operation: '同意了xxx的申请',
				// 	Time: '2020/4/5 12:30:45'
				// }]
			}
		},
		computed: {
			record_lis: function() {
				return this.$store.state.deptState.Record
			}
		},
		methods: {
			
		}
	}
</script>

<style lang="stylus" scoped>
	.el-card
		height 99%
		overflow-y auto
		overflow-x hidden
		.el-card
			margin 8px 0
			overflow hidden
		.el-card >>> .el-card__body
			padding 12px
			width 100%
			perspective 1px
			.operation
				position absolute
				left 40%
			.time
				position absolute
				right 45px
</style>
