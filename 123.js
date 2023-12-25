const crypto = require('crypto');

function encryptWithRSA(data) {
    // 你的公钥字符串
    const publicKey = `
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCCsYUGHMhjSzdMqn9JzPfKs9Jb
xXTPtHofTv7reV0HrEz4brnE6ZJpNn5s934KO3L4QDF7ELHysIiounhhpF1bewW9
jKdcpZA5M1CkGHKcwpLA2liaqOlt/0Mf3ui9jxR9AHxUMFVGfJ6Q4+cEmDBUAEOX
lxqk4ZjGpubwGNk9XQIDAQAB
-----END PUBLIC KEY-----`;
    const bufferData = Buffer.from(data, 'utf-8');
    const encrypted = crypto.publicEncrypt(
        {
            key: publicKey,
            padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
            oaepHash: 'sha256',
        },
        bufferData
    );

    return encrypted.toString('base64');
}

// // 要加密的数据
// const dataToEncrypt = '250';
//
// // 使用RSA加密
// const encryptedResult = encryptWithRSA(dataToEncrypt);
//
// // 输出结果
// console.log(encryptedResult);
