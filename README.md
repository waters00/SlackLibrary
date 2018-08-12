# Slackers
A library management system written using Django.


### 如何使用

确保安装依赖(python3)
```
pip3 install -r requirements.txt
```

然后执行即可
```
python3 manage.py runserver 8000
```


主页：
http://localhost:8000/

后台页面:
http://localhost:8000/admin/

初始化用户名密码:

```shell
python3 manage.py create_admin_account --username admin --password admin
```


主页：
![index][0]

书目检索页面：可以根据ISBN/书名/作者检索
![][1]


书籍信息爬取自豆瓣读书Top250，读者信息用Faker生成
登陆方式为电话号码，密码为*password*

![][3]


管理界面

![][4]

用户界面

![][5]

[0]:http://upload-images.jianshu.io/upload_images/3645027-807d0c6c55b0e878.png
[1]:http://opsfsk07z.bkt.clouddn.com/search_page.png
[3]:http://opsfsk07z.bkt.clouddn.com/reader_info.png
[4]:http://opsfsk07z.bkt.clouddn.com/admin.png
[5]: http://oh6k349gl.bkt.clouddn.com/slack_profile.jpg
