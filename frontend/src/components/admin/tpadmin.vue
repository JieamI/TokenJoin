<template>
	<el-card>
		<el-dialog
			title="模板内容"
			:visible.sync="dialogVisible"
			:before-close="handleCancel"
			center>
			<el-input type="textarea" rows="5" v-model="msg.content"></el-input>
			<span slot="footer">
				<el-button @click="handleCancel">取 消</el-button>
				<el-button type="primary" @click="handleUpdate">更 改</el-button>
			</span>
		</el-dialog>
		<div>
			<el-card v-for="(item,index) in messageList" :key="index" @click.native="updateMsg(index, item)" style="cursor: pointer;">
				<i class="el-icon-close" @click.stop="handleDelete(index)"></i>
				{{ item.length > 50? item.slice(0,50) + '……' : item }}
			</el-card>
			<el-card class="add" @click.native="add" style="cursor: pointer;">
				<i class="el-icon-circle-plus-outline"></i>
			</el-card>
		</div>
	</el-card>
</template>

<script>
	// import request from '../../utils/requests.js'
	export default {
		data() {
			return {
				dialogVisible: false,
				msg: {
					content: '',
					index: null,
					former_content: ''
				},
				// List: [
				// 	'啊达瓦安徽队坏,活塞腹黑啊的贵,妃赛等会啊等哈我和我啊达瓦安徽队坏,活塞腹黑啊的贵,妃赛等会啊等哈我和我啊达瓦安徽队坏,活塞腹黑啊的贵,妃赛等会啊等哈我和我',
				// 	'efwsrgrgrsgrsgrs',
				// 	'dafeefaefdhbtdfdvgstgsfwewgrweqwq',
				// 	'dewfesgrrrhtdrgszfewsfsdfdsfwreggggggggggggggggggggggggggggggggggggggggersfew',
				// 	'efwsrgrgrsgrsgrs'
				// ]
			}
		},
		computed: {
			messageList: {
				get() {
					return this.$store.state.deptState.Message
				},
				set(msgList) {
					this.$store.dispatch('setMessage', msgList)
				}
			}
		},
		methods: {
			// 取消或关闭对话框
			handleCancel() {
				this.msg.content = ''
				this.msg.index = null
				this.msg.former_content = ''
				this.dialogVisible = false
			},
			// 移除指定信息模板
			handleDelete(index) {
				let copy_list = this.messageList.slice()
				copy_list.splice(index, 1)
				this.messageList = copy_list
				
			},
			// 添加信息模板
			add() {
				this.dialogVisible = true
			},
			// 更新已有信息模板
			updateMsg(index, item) {
				this.dialogVisible = true
				this.msg.index = index
				this.msg.content = item
				this.msg.former_content = item
			},
			// 处理发出的更新请求或添加请求
			handleUpdate() {
				if(this.msg.index != null) {
					// 处理更改信息模板
					if(this.msg.former_content != this.msg.content) {
						// 模板信息发生变更才进行处理
						let index = this.msg.index
						// 要触发计算属性的set方法，这里需要使用深拷贝，下同
						let copy_list = this.messageList.slice()
						copy_list[index] = this.msg.content
						this.messageList = copy_list
					}
				}else {
					// 处理添加信息模板
					if(this.msg.content.trim() != '' && this.messageList.indexOf(this.msg.content) === -1) {
						// 模板信息不为空且信息不重复才进行处理
						let copy_list = this.messageList.slice()
						copy_list.unshift(this.msg.content)
						this.messageList = copy_list
					}else {
						this.$message({
							message: '模板信息为空或添加模板已存在',
							type: 'error',
							center: true
						})
					}
				}
				// 处理完后重新初始化
				this.msg.content = ''
				this.msg.index = null
				this.msg.former_content = ''
				this.dialogVisible = false
			}
		}
	}
</script>

<style lang="stylus" scoped>
	.el-card
		height 99%
		overflow-y auto
		overflow-x hidden
		.el-dialog__wrapper >>> .el-dialog
			// height auto
			margin auto
			width 500px
			// padding-bottom 20px !important
		.el-dialog__wrapper >>> textarea
			resize none
		.el-button
			width 120px
			margin 0 20px
		div
			display flex
			flex-wrap wrap
			.el-card
				width 155px
				height 155px
				margin 8px
				font-size 13px
				font-family "microsoft yahei"
				color gray
				overflow hidden
				// perspective用于在子元素使用绝对定位时指定自身为子元素的参照父元素
				perspective 1px
				.el-icon-close
					font-size 18px
					position absolute
					opacity 0.2
					top 5px
					right 5px
			.el-card:hover
				transform scale(1.1)
				transition all .2s
				.el-icon-close
					opacity 1
					transition all 1s
			.add
				align-items center
				justify-content center
				font-size 50px	
</style>
