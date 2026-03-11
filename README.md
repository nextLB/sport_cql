# 体育场所预订系统

基于Python Django框架开发的体育场所在线预订系统。

## 技术栈

- **后端**: Python 3.x + Django 6.x
- **数据库**: SQLite (内置，无需安装配置)
- **前端**: HTML + CSS + JavaScript + Bootstrap 5
- **开发工具**: PyCharm / VS Code

## 功能特性

### 用户功能
- 用户注册、登录、退出
- 个人资料管理
- 修改密码
- 浏览场馆列表
- 查看场馆详情
- 场地预约
- 查看我的预约
- 取消预约
- 评价预约

### 管理员功能
- 管理面板仪表盘
- 场馆管理（增删改查）
- 场地管理（增删改查）
- 预约管理（审批、拒绝、编辑、删除）
- 用户管理

## 项目结构

```
sports_booking/
├── sports_booking/          # 项目配置
│   ├── settings.py          # 项目设置
│   ├── urls.py              # 路由配置
│   └── wsgi.py              # WSGI配置
├── users/                   # 用户应用
│   ├── models.py            # 用户模型
│   ├── views.py             # 视图函数
│   ├── forms.py             # 表单
│   ├── urls.py              # 路由
│   └── admin.py             # 后台管理
├── venues/                  # 场馆应用
│   ├── models.py            # 场馆和场地模型
│   ├── views.py             # 视图函数
│   ├── forms.py             # 表单
│   ├── urls.py              # 路由
│   └── admin.py             # 后台管理
├── bookings/                # 预约应用
│   ├── models.py            # 预约模型
│   ├── views.py             # 视图函数
│   ├── forms.py             # 表单
│   ├── urls.py              # 路由
│   └── admin.py             # 后台管理
├── templates/               # 模板目录
│   ├── base.html            # 基础模板
│   ├── home.html            # 首页
│   ├── users/               # 用户模板
│   ├── venues/              # 场馆模板
│   ├── bookings/            # 预约模板
│   └── dashboard/           # 仪表板模板
├── static/                  # 静态文件
├── media/                   # 媒体文件
├── manage.py                # Django管理脚本
└── requirements.txt         # 依赖列表
```

## 安装步骤

### 1. 环境准备

```bash
# 安装Python依赖
pip install -r requirements.txt
```

### 2. 数据库配置

项目已配置为使用SQLite数据库（默认），无需额外配置。数据库文件会自动创建为 `db.sqlite3`。

如需使用MySQL，可自行在`settings.py`中修改：
```

### 3. 初始化项目

```bash
# 进入项目目录
cd code

# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户（管理员）
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic
```

### 4. 运行项目

```bash
# 启动开发服务器
python manage.py runserver
```

访问 http://127.0.0.1:8000/

## 使用说明

### 1. 普通用户

1. 访问首页，点击"注册"创建账号
2. 登录后可以浏览场馆列表
3. 选择场馆查看详情和场地
4. 选择场地进行预约
5. 在"我的预约"中查看预约状态
6. 预约完成后可以评价

### 2. 管理员

1. 使用超级用户账号登录后台 /admin/
2. 可以管理所有场馆和场地
3. 可以审批/拒绝用户预约
4. 可以查看和管理所有用户

## 角色说明

- **普通用户(user)**: 可以预约场地、查看自己的预约
- **管理员(admin)**: 可以管理所有数据，拥有所有权限

## 预约状态说明

- **待审批(pending)**: 等待管理员确认
- **已确认(confirmed)**: 预约成功
- **已取消(cancelled)**: 用户已取消
- **已拒绝(rejected)**: 管理员拒绝
- **已完成(completed)**: 预约已完成

## 开发指南

### 添加新功能

1. 在对应的app中创建models
2. 在views中创建视图函数
3. 在forms中创建表单
4. 在urls中添加路由
5. 创建模板文件

### 静态文件

将CSS、JS等静态文件放在`static/`目录下，模板中使用`{% load static %}`加载。

### 媒体文件

用户上传的图片等媒体文件存储在`media/`目录下。

## 技术要点

- 使用Django内置用户认证系统实现权限管理
- 使用Bootstrap 5实现响应式布局
- 使用MySQL数据库存储数据
- 遵循MVC设计模式

## 参考文档

- [Django官方文档](https://docs.djangoproject.com/)
- [Bootstrap 5文档](https://getbootstrap.com/docs/5.1/)

## 作者

- 陈权令 - 海南热带海洋学院

## 指导教师

- 吴淑婷 - 讲师
- 马鹏程 - 高级工程师
