# Slackers
A library management system written using Django.


### 如何使用

确保安装依赖，Python3.6
```
pip install -r requirements.txt
```

然后执行即可
```
python manage.py runserver 8000
```
主页：
![index][0]

书目检索页面：可以根据ISBN/书名/作者检索
![][1]


书籍信息爬取自豆瓣读书Top250，读者信息用Faker生成
登陆方式为电话号码，密码为*password*

![][3]

用户界面
![][4]

[0]:http://upload-images.jianshu.io/upload_images/3645027-807d0c6c55b0e878.png
[1]:http://opsfsk07z.bkt.clouddn.com/search_page.png
[3]:http://opsfsk07z.bkt.clouddn.com/reader_info.png
[4]:http://opsfsk07z.bkt.clouddn.com/profile_1.png
