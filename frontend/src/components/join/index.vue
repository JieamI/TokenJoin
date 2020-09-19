<template>
	<div v-loading="loading" id="main">
		<!-- 将团队部分和部门介绍部分分开是为了只给部门介绍添加立即加入按钮 -->
		<!-- 团队介绍部分 -->
		<v-touch
			id="image0"
			class="wrapper"
			@swipeup="handleSwipeup(0)" 
			@swipedown="handleSwipedown(0)">
			<el-image :src="image_introduce[0]" class="image"></el-image>
			<el-button type="primary" @click="pushtoJoin"></el-button>
		</v-touch>
		<v-touch
			id="image1"
			class="wrapper"
			@swipeup="handleSwipeup(1)" 
			@swipedown="handleSwipedown(1)">
			<el-image :src="image_introduce[1]" class="image"></el-image>
		</v-touch>
		<!-- 部门介绍部分 -->
		<v-touch 
			v-for="(image, index) in imageList" 
			:id="'image' + (index + 2)"
			class="wrapper"
			:key="(index + 2)" 
			@swipeup="handleSwipeup(index + 2)" 
			@swipedown="handleSwipedown(index + 2)">
			<el-image :src="image" class="image" lazy></el-image>
			<el-image class="join-button" :src="image_join" @click="pushtoJoin(image.name)" lazy></el-image>
		</v-touch>
		<div id="icon-group">
			<i class="el-icon-arrow-down"></i>
			<i class="el-icon-arrow-down" style="top: 45%;"></i>
		</div>
	</div>
</template>

<script>
	import image_0 from '../../../public/common/token.jpg'
	import image_1 from '../../../public/common/时间线.jpg'
	import image_join from '../../../public/common/加入.png'
	import request from '../../utils/requests.js'
	export default {
		data() {
			return {
				loading: false,
				// 用于定时下拉箭头提示
				timeout: null,
				// 用于判断页面是否加载完成
				timer: null,
				image_introduce: [image_0, image_1],
				image_join: image_join,
				imageList: []
			}
		},
		async created() {
            // 如果使用电脑端打开则使网页以移动端的表现形式显示,以避免图片适配问题
			let width = screen.width
			if(width >= 750) {
				document.querySelector('body').setAttribute('style', 'margin: auto; max-width: 375px;')
            }
			// 获取各个部门的展示状态,有选择性地展示各个部门
			let res = await request({
				url: '/getshow',
				methods: 'get',
			})
			if(res.data.showingList.length) {
                res.data.showingList.forEach((dept) => {
                    switch(dept) {
                        case('技术部'): this.imageList.push(require('../../../public/common/技术部.jpg'));break;
                        case('产品部'): this.imageList.push(require('../../../public/common/产品部.jpg'));break;
                        case('人力资源部'): this.imageList.push(require('../../../public/common/人力资源部.jpg'));break;
                        case('设计部'): this.imageList.push(require('../../../public/common/设计部.jpg'));break;
                        case('新媒体运营'): this.imageList.push(require('../../../public/common/新媒体运营.jpg'));break;
                        case('产品运营'): this.imageList.push(require('../../../public/common/产品运营.jpg'));break;
                        case('杂志部'): this.imageList.push(require('../../../public/common/杂志部.jpg'));break;
                    }
                })
			}else {
                // 没有一个部门处于展示状态
                this.$message({
                    message: '当前没有部门在招新哦~',
                    type: 'warning',
                    center: true,
                    duration: 5000
                })
            }
        },
        // mounted() {
        //     document.querySelector('#main').setAttribute('style', 'overflow: hidden; height: 100vh;')
        //      // 判断页面是否加载完成
        //     this.timer = setInterval(() => {
        //         if (document.readyState === 'complete') {
        //             document.querySelector('#main').setAttribute('style', 'overflow: auto; height: auto')
        //             this.loading = false
        //             window.clearInterval(this.timer)
        //         }
        //     }, 1000)
        // },
		methods: {
			handleSwipeup(index) {
				if(index === this.imageList.length + 1) {
					return
				}
				// 重置定时器,避免当用户在某个页面停留时间不足5s就下滑导致下个页面的下滑箭头提示显示时间不足5s
				if(this.timeout) {
					clearTimeout(this.timeout)
				}
				document.querySelector('#icon-group').setAttribute('style', 'display: block;')
				if(index === this.imageList.length) {
					document.querySelector('#icon-group').setAttribute('style', 'display: none;')
				}
				this.timeout = setTimeout(() => {
					document.querySelector('#icon-group').setAttribute('style', 'display: none;')
				}, 5000)
				document.querySelector('#image' + (index + 1)).scrollIntoView({behavior: 'smooth'})
			},
			handleSwipedown(index) {
				if(index === 0) {
					return
				}
				document.querySelector('#image' + (index - 1)).scrollIntoView({behavior: 'smooth'})
			},
			pushtoJoin(deptname) {
				let depts = ['技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部']
				if(depts.indexOf(deptname) !== -1) {
					this.$router.push({path: '/join/apply/' + deptname})
				}else {
					this.$router.push({path: '/join/apply/'})
				}
				
			}
		}
	}
</script>

<style lang="stylus" scoped>
	.wrapper
		perspective 1px
		.image
			margin 6px
			box-shadow: 0 2px 12px 2px slategray
		.el-button
			opacity 0
			position absolute
			bottom 12%
			width 180px
			height 60px
			left 0
			right 0
			margin auto
		.join-button
			position absolute
			bottom 1%
			left 0
			right 0
			margin auto
			transform scale(0.4)
			animation button-animation 2s infinite
			@keyframes button-animation
				0%
					transform scale(0.4)
				50%
					transform scale(0.45)
				100%
					transform scale(0.4)
	.el-icon-arrow-down
		position fixed
		top 47%
		left 0
		right 0
		font-size 36px
		color lightgrey
		margin auto
		width 36px
		animation arrow-animation 1.5s infinite
	@keyframes arrow-animation
		0% 
			transform scale(1)
			opacity 0.4
		50% 
			transform scale(1.2)
			opacity 1
		100% 
			transform scale(1)
			opacity 0.4
</style>