#======部门编码=======
01总经办
02集团财务中心
03集团技术中心
04集团客服中心
05集团行政人事中心
06集团品牌运营中心
07集团风控部
08旅居客
09线下门店
10线上事业一部
11案场代理事业部
12渠道代理事业部
13品质家
14住我房
15哪里玩
16哪里吃
17美能物业

#=======机器人worker工号=======
WF01040001雅居宝H5报备员
WF01140001住我房tujia PC后台系统同步员

#=======接口说明========
1、自动报备提交接口
请求地址：pyapi.wofang.org/report/报备单号
   参数：channelNo渠道编号
        userId客户ID
        userName客户姓名
        tel手机号
        sex性别，0为女，1为男
        desc报备说明
        projectId项目编号
        projectName项目名称
        sign加密检验值
        
响应结果：{
         reportNo：报备单号
           status: 接收结果 1为成功、0为失败
             desc：结果说明，status为0时，说明为失败原因
         }
2、报备结果查询接口
请求地址：pyapi.wofang.org/report/status/报备单号
    参数：sign加密检验值
    
响应结果：{
         reportNo：报备单号
           status: 报备结果状态 1为成功、0为失败
             desc：结果说明，status为0时，说明为失败原因
        reportLog：报备过程日志
              png: 结果拍照图片链接地址，若为多个结果则多个链接以英文逗号(,)相隔
         }

=======说明==========
1、conf配置文件
2、consoleRobot工作程序文件
3、export输出文件
4、log日志文件
5、test测试入口程序
6、util工具类程序
flaskApi对外api入口类
GlobalVar全局变量类
workshop工作间主程序
pack打包程序