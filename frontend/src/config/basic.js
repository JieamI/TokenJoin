let frontDomain = process.env.TOKEN_FRONT_DOMAIN ? process.env.TOKNE_FRONT_DOMAIN : "https://recruit.itoken.team"
let backendDomain = process.env.TOKEN_BACKEND_DOMAIN ? process.env.TOKEN_BACKEND_DOMAIN : "http://localhost:8000/api"
const Config = {
	//前端的域名（必须是域名，不能是ip:port形式），注意域名最后不要加斜杠
	frontDomain: frontDomain,
	//后端域名（可以是ip:port形式），注意最后不要加斜杠
	backendDomain: backendDomain,
	// //钉钉AppId
	DingAppId: "xxxxxxxxxxxxxx",
	// //钉钉AppSecret
	DingAppSecret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
}

export default Config;