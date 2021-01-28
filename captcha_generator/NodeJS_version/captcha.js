// Author: ShayXU

// 如果NodeJS安装在C盘需要以管理员权限运行
// 26 + 10 - 8 = 28， 28^4 = 614656, 是4位数字验证码的62倍。

SvgCaptcha = require("svg-captcha")
const fs = require('fs')
let i = 0
let dir_name = 'img_raw/'

// 可以稍多一些，会有异常场景
while(i<2000) {
let n = SvgCaptcha.create({
        size: 4,
        ignoreChars: "0o1itILl",  // 8个
        noise: 1,
        color: true
    })

// console.log(n['data'])
fs.writeFile(dir_name + i + '_' + n['text'] + '.svg', n['data'], err => {
    if (err) {
      console.error(err)
      i -= 1
    }
  })
i += 1
}