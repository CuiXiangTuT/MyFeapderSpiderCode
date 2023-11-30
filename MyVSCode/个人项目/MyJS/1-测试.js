window = global;




document = window.document
global.navigator = {
    userAgent:'node.js'
}

// document.write("<script language=javascript src='JSEncrypy.js'></scripts>")

//加密时间戳方法
function encryptByRSA(value) {
var encrypt = new JSEncrypt();
var RSAPublicKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCS2TZDs5+orLYCL5SsJ54+bPCV\n" +
"s1ZQQwP2RoPkFQF2jcT0HnNNT8ZoQgJTrGwNi5QNTBDoHC4oJesAVYe6DoxXS9Nl\n" +
"s8WbGE8ZNgOC5tVv1WVjyBw7k2x72C/qjPoyo/kO7TYl6Qnu4jqW/ImLoup/nsJp\n" +
"pUznF0YgbyU/dFFNBQIDAQAB";
encrypt.setPublicKey('-----BEGIN PUBLIC KEY-----'+RSAPublicKey+'-----END PUBLIC KEY-----')  // 放置自己的公钥
return encrypt.encrypt(value)
}

console.log(encryptByRSA('2023-10-16 17:48:00'))