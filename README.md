# captcha-recognizer
识别各种验证码生成工具产生的验证码。  

|验证码类型|支持情况|
| - | :-: |
| NodeJS svg-captcha | [√] |
<br>

执行顺序  
cd captcha_generator/NodeJS_version  
node captcha.js  
captcha_preprocess.py  
captcha_classifier.train_model()  
captcha_classifier.prefict()  
