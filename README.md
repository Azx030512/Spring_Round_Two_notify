## **notify answer**

### **内容大概😀**

这是求是潮春季纳新的二面试题notify的解答，作者是azx

**题目给出了三个不同难度的目标网站，这里对第一阶中学工部和第二阶中咨询中心写出了相应的代码，并且对爬取的新闻信息，网站信息进行了一些简单的分类，并用pprint以字典的形式进行输出方便观看结果**

### **解题感受😐**

**第一阶的三个网站不用进行登录认证，可直接用requests下载html代码，在字符编码上，gbk无法解析copyright的花C符号，因此下载时将其去掉，用BeautifulSoup模块进行简单的信息提取(很遗憾，虽然这三个网站的爬取可以兼并到一个程序，但内容提取不太行，因为网页中的标签和命名出入较大)，分类后储存在以标题为键URL为值的字典中，应出题人要求，代码中也添加了用pymysql将字典导入到mysql数据库的部分(不过为了方便出题人检查功能，注释掉了)**

**第二阶的咨询中心网站就需要输入账号密码了，并且不是单纯的html网页，而是基于python serve page的psp动态网页，因此用了selenium模块操纵火狐浏览器进行登录并下载页面，也进行了一部分新闻的提取并且组织成了字典的形式，并且用pprint模块打印出来**

**时间和能力有限，notify的题目就完成到这一部分，希望小哥哥小姐姐们喜欢😏**