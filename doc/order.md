用户订餐功能规划
---


逻辑：

1. 用户的唯一身份识别为学号， 手机号码可以有多个，微信号也可以不止一个，
2. 因此，注册时输入姓名、学号、生日、预留手机号、性别、个性签名。 注册成功后跳转到个人信息页， 下面应该有添加订单的链接。

3. 注册完成后，可添加订单(注册并登陆的用户才可以操作)，如用户未登录，跳转到登陆界面，如用户未注册，跳转到注册界面，添加订单时，需要输入姓名、学号(需要验证)，取餐日期(下拉菜单形式), 手机号()
具体验证方式是：先到*signed-user*表中寻找是否已注册，如注册，查询两次订餐时间间隔，防止频繁订餐，如果没有注册，则去*all_student*中寻找，找到之后，将该用户添加到*signed-user*里， 将该订单添加到*orders*.

4. 我的订单页面 —— 个人主页.

关于整个系统，共有三类用户：


1. 系统管理员，管理整个网站的数据，包括文章，所有订单等，这个对安全的要求较高
2. 餐厅工作人员， 验证身份后能在微信中通过文本获取所有订单信息
3. 订餐者， 即学生。能够通过文本获取少量自己的信息，可以通过自定义菜单注册新用户，
订餐等。


数据库该怎么设计[初步]：

1. 首先，要有一张表 *all_students*，存储所有可能的用户，即全校学生的身份信息，应记录学生的姓名、学号、性别等信息。鉴于学号太长，可以考虑为用户分配在分配一个唯一id，长度再定.

2. 注册用户要一张表*signed-user*，记录注册时填写的信息，如 订餐人(过生日的人)id，学号，姓名，性别(性别不可更改，直接从all_students里面copy)，头像(后期可以考虑添加，制作个人主页..),
生日， 上次订餐时间，手机号码， 微信号。还有注册日期，个性签名等。

3. 所有订单*orders* ,订单id，添加时间，订单状态(到取餐日期自动视为成交), 生日时间，餐品信息， 学生学号/id, 取餐电话，取餐地点， 性别，生日祝福语

4. 食堂工作人员一张表，记录微信号

5. 系统管理员一张表.

6. 用户反馈一张表： 反馈id， 反馈者姓名(可以非实名)，email/phone, 反馈内容，添加日期，
处理状态(是否已经处理完毕).

7. 所有餐品一张表

8. 最后，过期用户信息需要删除？？？ 怎样确定用户是否已经毕业？


数据库后期规划：


1. 公告一张表
2. 菜品一张表
3. 菜品评论一张表



#### 用户个人主页规划

头像、姓名[昵称]、个性签名、下次订单信息，历史订单等。

















