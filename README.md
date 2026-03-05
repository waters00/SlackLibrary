# Slackers — 数字图书馆管理系统

基于 Django 的图书馆管理系统，支持图书检索、借阅、归还、续借、统计等功能。

## 技术栈

| 组件 | 版本 |
|------|------|
| Python | 3.12+ |
| Django | 5.2 LTS |
| django-crispy-forms | 2.6 |
| Pillow | 12.1.1 |
| Faker | 40.8.0 |
| 数据库 | SQLite3 |
| 前端 | Bootstrap 3 |

## 功能

- 用户注册 / 登录（手机号）
- 图书检索（ISBN / 书名 / 作者）
- 图书借阅、归还、续借
- 逾期罚款计算
- 个人中心（头像、借阅记录）
- 借阅统计（读者排行、热门图书）
- 后台管理

## 快速开始

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 2. 初始化数据库

```bash
python3 manage.py migrate
```

### 3. 创建管理员

```bash
python3 manage.py create_admin_account --username admin --password admin
```

### 4. 启动服务

```bash
python3 manage.py runserver 8000
```

- 主页: http://localhost:8000/
- 后台: http://localhost:8000/admin/

### 5. 初始化测试数据（可选）

书籍数据爬取自豆瓣读书 Top250，读者信息由 Faker 生成，登录方式为手机号，默认密码 `password`。

```bash
python3 init_db_data.py all
```

## 运行测试

```bash
python3 manage.py test library
```

## 项目结构

```
├── manage.py                   # Django 入口
├── requirements.txt            # 依赖清单
├── init_db_data.py             # 测试数据生成脚本
├── books.json                  # 图书种子数据
├── slack_management/           # 项目配置
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── library/                    # 主应用
    ├── models.py               # Reader / Book / Borrowing
    ├── views.py                # 视图函数
    ├── forms.py                # 表单定义
    ├── admin.py                # 后台注册
    ├── tests.py                # 单元测试
    ├── apps.py
    ├── management/             # 自定义命令
    ├── templates/library/      # HTML 模板
    └── static/library/         # 静态资源
```

## 截图

主页：
![index][0]

书目检索页面（支持 ISBN / 书名 / 作者）：
![][1]

读者信息：
![][3]

管理界面：
![][4]

用户界面：
![][5]

[0]:http://upload-images.jianshu.io/upload_images/3645027-807d0c6c55b0e878.png
[1]:http://opsfsk07z.bkt.clouddn.com/search_page.png
[3]:http://opsfsk07z.bkt.clouddn.com/reader_info.png
[4]:http://opsfsk07z.bkt.clouddn.com/admin.png
[5]:http://oh6k349gl.bkt.clouddn.com/slack_profile.jpg
