<template>
	<el-card id="myChart"></el-card>
</template>

<script>
	import request from '../../utils/requests.js'
	export default {
		data() {
			return {
				line_data: '',
				pie_data: ''
			}
		},
		async mounted() {
			// 按需引用减少体积
			let echarts = require('echarts/lib/echarts')
			require("echarts/lib/chart/line")
			require("echarts/lib/chart/pie")
			let myChart = echarts.init(document.getElementById('myChart'))
			myChart.showLoading()
			let res = await request({
				url: '/index/data',
				method: 'get'
			})
			if(res.data) {
				myChart.hideLoading()
				myChart.setOption({
					grid: {
						top: '10%',
						height: '40%',
						width: '80%'
					},
					tooltip: {
						trigger: "axis",
						axisPointer: {
							type: "shadow"
						},
					},
					xAxis: {
						type: 'time'
					},
					yAxis: {
						// type: 'value'
					},
					series: [{
						trigger: 'axis',
						type: 'line',
						data: res.data.line_data.sort()
					},{
						type: 'pie',
						radius: 100,
						center: ['18%', '78%'],
						label: {
							formatter: '{b}:{c}(%{d})'
						},
						data: res.data.pie_data
					}]
				})
			}
		
		}
	}
</script>

<style lang="stylus" scoped>
	.el-card
		width 100%
		height 99%
</style>
