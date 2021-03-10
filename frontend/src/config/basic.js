let frontDomain = process.env.TOKEN_FRONT_DOMAIN ? process.env.TOKNE_FRONT_DOMAIN : "https://join.itoken.team"
// let backendDomain = process.env.TOKEN_BACKEND_DOMAIN ? process.env.TOKEN_BACKEND_DOMAIN : "https://join.itoken.team/api"
let backendDomain = process.env.TOKEN_BACKEND_DOMAIN ? process.env.TOKEN_BACKEND_DOMAIN : "https://apitoken.vaiwan.com/api"
const Config = {
	//前端的域名（必须是域名，不能是ip:port形式），注意域名最后不要加斜杠
	frontDomain: frontDomain,
	//后端域名（可以是ip:port形式），注意最后不要加斜杠
	backendDomain: backendDomain,
	// //钉钉AppId
	DingAppId: "dingoalrnidom4p3khixr0",
	// //钉钉AppSecret
	DingAppSecret: "QNDiNQbWbJfiLLuTkR523G8VDRT79Geo-2VplHBEZVJqOKQ62mE8v03lySvPRpoT",
	//钉钉AppId
	// DingAppId: "dingoapm6ohzqxmd1kzesi",
	//钉钉AppSecret
	// DingAppSecret: "ccBS_06R4SFXSevbHCKrQco2aQzLVGavH3AkAjeUWuQwt3KK-RxmI5Nw_PK9HLe6"
}

export default Config;