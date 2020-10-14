<template>
	<el-card v-loading="loading">
		<!-- 邮件发送对话框 -->
		<el-dialog class="mail-dialog" title="发送信息" :visible.sync="dialogMailVisible" width="500px">
			<el-form label-position="top" size="small">
				<el-form-item label="已选简历">
					<div class="selected">
						<el-tag v-for="val in multipleSelection" :key="val.name">{{ val.name }}</el-tag>
					</div>
				</el-form-item>
				<el-form-item label="邮件主题">
					<el-input placeholder="请输入邮件主题" v-model="mailConfig.data.subject" clearable></el-input>
				</el-form-item>
				<el-form-item label="信息模板">
					<el-select v-model="mailConfig.data.text" placeholder="请选择信息模板" clearable>
						<el-option v-for="(msg, index) in this.$store.state.deptState.Message" :key="index" :label="msg" :value="msg"></el-option>
					</el-select>
					<el-input type="textarea" resize="none" rows="5" v-model="mailConfig.data.text"></el-input>
				</el-form-item>
			</el-form>
			<el-upload
				class="upload"
				ref="upload"
				:action="mailConfig.action"
				name='files'
				:limit="1"
				:on-error="onError"
				:on-change="onChange"
				:file-list="fileList"
				:on-success="handleSuccess"
				:data="mailConfig.data"
				:auto-upload="false">
				<el-button slot="trigger" size="medium" type="primary">添加附件</el-button>
				<el-button class="sendbutton" size="medium" type="success" @click="handleSend">发送邮件</el-button>
				<div slot="tip" class="el-upload__tip">只能上传一个附件，文件大小不宜过大</div>
			</el-upload>
		</el-dialog>
		<!-- 面试评价对话框 -->
		<el-dialog
			class="comment-dialog"
			title="面试评价"
			:visible.sync="dialogCommentVisible"
			width="500px"
			center>
			<el-input type="textarea" rows="5" v-model="commentData.content" resize="none"></el-input>
			<span slot="footer">
				<el-button type="primary" @click="handleConfirm">确定</el-button>
			</span>
		</el-dialog>
		<!-- 简历详细信息对话框 -->
		<el-dialog
			class="cvinfo-dialog"
			title="详细信息"
			:visible.sync="dialogCvinfoVisible"
			width="700px"
			@closed="comment_select = ''"
			center>
		<el-card class="cvinfo-wrapper">
			<el-form size="small">
				<el-form-item label="姓名:">{{ cvinfoDialog.name }}</el-form-item>
				<el-form-item label="性别:">{{ cvinfoDialog.sex }}</el-form-item>
				<el-form-item label="出生日期:">{{ cvinfoDialog.birthday }}</el-form-item>
				<el-form-item label="籍贯:">{{ cvinfoDialog.hometown }}</el-form-item>
				<el-form-item label="民族:">{{ cvinfoDialog.nation }}</el-form-item>
				<el-form-item label="学号:">{{ cvinfoDialog.sno }}</el-form-item>
				<el-form-item label="学院:">{{ cvinfoDialog.college }}</el-form-item>
				<el-form-item label="年级:">{{ cvinfoDialog.grade }}</el-form-item>
				<el-form-item label="专业班级:">{{ cvinfoDialog.proclass }}</el-form-item>
				<el-form-item label="宿舍:">{{ cvinfoDialog.dormitory }}</el-form-item>
				<el-form-item label="手机:">{{ cvinfoDialog.phone }}</el-form-item>
				<el-form-item label="QQ:">{{ cvinfoDialog.qq }}</el-form-item>
				<el-form-item label="邮箱:">{{ cvinfoDialog.mail }}</el-form-item>
				<el-form-item label="个人经历:">
					<el-input type="textarea" resize="none" rows="6" :value="cvinfoDialog.experience" readonly></el-input>
				</el-form-item>
				<el-form-item label="自我介绍:">
					<el-input type="textarea" resize="none" rows="6" :value="cvinfoDialog.introduce" readonly></el-input>
				</el-form-item>
				<el-form-item label="加入原因:">
					<el-input type="textarea" resize="none" rows="6" :value="cvinfoDialog.reason" readonly></el-input>
				</el-form-item>
				<el-form-item label="面试评价:">
					<el-select v-model="comment_select" placeholder="请选择评价人" clearable>
						<el-option v-for="(value, key) in cvinfoDialog.comment" :label="key" :value="key" :key="key"></el-option>
					</el-select>
					<el-input type="textarea" resize="none" rows="4" :value="comment_select.length? cvinfoDialog.comment[comment_select] : ''" readonly></el-input>
				</el-form-item>
			</el-form>
		</el-card>
		</el-dialog>
		<!-- 邮件发送按钮 -->
		<el-button 
			type="primary" 
			class="mail-button"
			icon="el-icon-message" 
			:disabled="multipleSelection.length === 0 || unauthorized" 
			size="medium" 
			@click="opendialogMail"
			plain round>
		</el-button>
		<el-table 
			class="table"
			:data="tableData"
			height=1024
			@selection-change="handleSelectionChange" stripe>
			<el-table-column type="selection" width="50" align="center">
			</el-table-column>
			<el-table-column label="姓名" width="120" align="center">
				<template v-slot="scope">
					<el-tag @click="seeCvinfo(scope.row)" style="cursor: pointer;">{{ scope.row.name}}</el-tag>
				</template>
			</el-table-column>
			<el-table-column 
				label="标签" 
				width="120" 
				:filters="[{text: '已标记', value: true}, {text: '未标记', value: false}]"
				:filter-method="filterBySign"
				align="center">
				<template v-slot="scope">
					<i 
						:class="scope.row.sign === true? 'el-icon-star-on' : 'el-icon-star-off'" 
						style="font-size: 20px;cursor: pointer;"
						@click="handleSign(scope.row)"
						disabled>
					</i>
				</template>
			</el-table-column>
			<el-table-column 
				label="状态" 
				width="120" 
				:filters="[{text: '未审核', value: '未审核'}, {text: '简历通过', value: '简历通过'}, {text: '面试完成', value: '面试完成'}]" 
				:filter-method="filterByState"
				align="center">
				<template v-slot="scope">	
					<el-select 
						v-model="scope.row.state" 
						placeholder="请选择" size="small" 
						@change="handleState(scope.row)" 
						:disabled="unauthorized">
						<el-option
							label="未审核"
							value="未审核">
						</el-option>
						<el-option
							label="简历通过"
							value="简历通过">
						</el-option>
						<el-option
							label="笔试完成"
							value="笔试完成">
						</el-option>
						<el-option
							label="面试完成"
							value="面试完成">
						</el-option>
						<el-option
							label="已录取"
							value="已录取">
						</el-option>
						<el-option
							label="未录取"
							value="未录取">
						</el-option>
					</el-select>
				</template>
			</el-table-column>
			<el-table-column 
				label="性别" 
				prop="sex" 
				width="120" 
				align="center"
				:filters="[{text: '男', value: '男'}, {text: '女', value: '女'}]"
				:filter-method="filterBySex">
			</el-table-column>
			<el-table-column 
				label="年级" 
				prop="grade" 
				width="120" 
				align="center"
				:filters="gradeList"
				:filter-method="filterByGrade">
			</el-table-column>
			<el-table-column label="投递部门" prop="department" width="120" align="center">
			</el-table-column>
			<el-table-column label="专业班级" prop="proclass" width="120" align="center">
			</el-table-column>
			<el-table-column label="申请时间" prop="time" width="180" align="center">
			</el-table-column>
			<el-table-column label="面试评价" align="center">
				<template v-slot="scope">
					<el-button type="primary" size="small" @click="handleEvaluate(scope.row)">面试评价</el-button>
				</template>
			</el-table-column>
		</el-table>
	</el-card>
</template>

<script>
	import request from '../../utils/requests.js'
	import Config from '../../config/basic.js'
	import qs from 'qs'
	export default {
		data() {
			return {
				unauthorized: this.$store.state.userInfo.authcode === 0,
				loading: true,
				fileList: [],
				mailConfig: {
					action: Config.backendDomain + '/join/sendemail',
					data: {
						recipients: '',
						subject: '',
						text: '',
						token: JSON.parse(window.localStorage.getItem('userInfo')).access_token
					}
				},
				dialogMailVisible: false,
				dialogCommentVisible: false,
				dialogCvinfoVisible: false,
				commentData: {
					content: '',
					row: ''
				},
				tableData: [],
				cvinfoDialog: {},
				comment_select: '',
				multipleSelection: []
			}
		},
		async created() {
			let res = await request({
				url: '/join/cvinfo',
				method: 'get'
			})
			if(res.data.cvinfo_lis.length) {
				this.tableData = res.data.cvinfo_lis
			}
			this.loading = false
		},
		computed: {
			// 由于tableData里简历投递者的年级是动态变化的,因此需要先获得tableData里的所有年级才能用于年级过滤
			gradeList: function() {
				let gradeList = []
				this.tableData.forEach((val) => {
					if(gradeList.indexOf(val.grade) === -1) {
						gradeList.push({text: val.grade, value: val.grade})
					}
				})
				gradeList.sort((a, b) => {return a.value - b.value})
				return gradeList
			}
		},
		methods: {
			handleSelectionChange(val) {
				this.multipleSelection = val
			},
			// 过滤处理
			filterByState(val, row) {
				return row.state === val
			},
			filterBySign(val, row) {
				return row.sign === val
			},
			filterBySex(val, row) {
				return row.sex === val
			},
			filterByGrade(val, row) {
				return row.grade === val
			},
			// 切换标记
			async handleSign(row) {
				if(this.unauthorized) {
					this.$message({
						message: '你无权进行此操作',
						type: 'warning',
						center: true
					})
					return
				}
				let res = await request({
					url: '/join/updatecv',
					method: 'post',
					data: {
						sno: row.sno,
						sign: !row.sign
					}
				})
				if(res.data.code === 0) {
					row.sign = !row.sign
				}
			},
			// 切换简历状态
			async handleState(row) {
				let res = await request({
					url: '/join/updatecv',
					method: 'post',
					data: {
						sno: row.sno,
						state: row.state
					}
				})
				if(res.data.code === 0) {
					this.$message({
						message: '简历状态更改成功',
						type: 'success',
						center: true
					})
				}
			},
			// 打开面试评价对话框
			handleEvaluate(row) {
				this.dialogCommentVisible = true
				this.commentData.row = row
				if(row.comment[this.$store.state.userInfo.nick]) {
					this.commentData.content = row.comment[this.$store.state.userInfo.nick]
				}
			},
			// 提交面试评价
			async handleConfirm() {
				var content = this.commentData.content
				if(!content.trim().length) {
					this.$message({
						message: '内容不能为空',
						type: 'error',
						center: true
					})
					return
				}
				var nick = this.$store.state.userInfo.nick
				let res = await request({
					url: '/join/setcomment',
					method: 'post',
					data: {
						sno: this.commentData.row.sno,
						comment: content
					}
				})	
				if(res.data.code === 0) {
					this.commentData.row.comment[nick] = content
					this.dialogCommentVisible = false
					this.$message({
						message: '面试评价提交成功',
						type: 'success',
						center: true
					})
				}
			},
			// 打开邮件发送对话框
			opendialogMail() {
				// 初始化recipients数组
				let recipients = []
				this.multipleSelection.forEach((val) => {
					recipients.push(val.mail)
				})
				this.mailConfig.data.recipients = recipients.join(',')
				this.dialogMailVisible = true
			},
			// 带附件邮件发送错误回调
			onError(res) {
				this.$message({
					message: res,
					type: 'error',
					center: true
				}) 
			},
			// 附件列表改变回调,用于判断发送的邮件是否带有附件
			onChange(file, fileList) {
				this.fileList = fileList
			},
			// 发送邮件
			async handleSend() {
				if(this.mailConfig.data.subject.length === 0 || this.mailConfig.data.text.length === 0) {
					this.$message({
						message: '邮件主题/信息内容不能为空',
						type: 'warning',
						center: true
					})
					return
				}
				// 如果添加了附件
				if(this.fileList.length) {
					this.$refs.upload.submit()
				}else { 
					// 如果未添加附件
					let res = await request({
						url: this.mailConfig.action,
						method: 'post',
						headers: {
							'Content-Type': 'application/x-www-form-urlencoded'
						},
						data: qs.stringify(this.mailConfig.data)
					})
					if(res.data.code === 0) {
						this.$message({
							message: '邮件发送成功',
							type: 'success',
							center: true
						})
						this.dialogMailVisible = false
					}
				}
			},
			// 带附件的邮件发送成功回调
			handleSuccess(res) {
				if(res.code === 0) {
					this.$message({
						message: '邮件发送成功',
						type: 'success',
						center: true
					})
					this.dialogMailVisible = false
				}
			},
			seeCvinfo(row) {
				this.cvinfoDialog = row
				this.dialogCvinfoVisible = true
			}
		}
	}
</script>

<style lang="stylus" scoped>
	.el-card
		height 99%
		// 简历信息对话框样式
		.cvinfo-dialog
			// height 500px
			overflow hidden
			.cvinfo-wrapper
				height 560px
				overflow-y auto
				.el-form-item
					color gray
		// 邮件发送对话框样式
		.el-form
			padding 0 50px
			.el-form-item
				margin 2px 0
				.selected
					display flex
					flex-wrap wrap
					max-height 100px
					// height 100px
					overflow-y auto
					.el-tag
						margin 5px
				.el-select
					width 100%
					margin-bottom 10px
		.upload
			margin 20px
			.sendbutton
				margin-left 20px
		// 邮件发送按钮样式
		.mail-button
			background-color steelblue
		.upload >>> .el-upload__tip
			text-align center
		.mail-dialog >>> .el-dialog__body
			padding 10px 20px
		.mail-dialog >>> .el-form-item__label
			padding 2px
		.mail-dialog >>> .el-upload
			padding-left 100px
		.comment-dialog >>> .el-dialog__body
			padding 10px 35px
		.comment-dialog >>> .el-button
			width 120px
		.cvinfo-dialog >>> .el-dialog
			margin-top 2vh !important
</style>
