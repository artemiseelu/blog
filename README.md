

# Blog_101

[简体中文](README.md)       
[English](README_EN.md)

  
感谢cursor，虽然我们也经常鸡同鸭讲，但没有你就没有这个速成项目hhh
   
  ## 目录
  
  - [上手指南](#上手指南)
    - [本机配置](#本机配置)
    - [安装步骤](#安装步骤)
  - [文件目录说明](#文件目录说明)
  - [部署](#部署)
  - [TODO](#TODO)
  - [作者](#作者)
  - [鸣谢](#鸣谢)
  
  ### 上手指南
  
  ##### 本机配置
  - **操作系统**： Linux 系统（Ubuntu 20.04）& Windows
  - **Python 环境**：本机Python 3.9
  - **数据库**：PostgreSQL
  - **开发框架**：Django
  依赖详见requirement.txt
    
  ###### 安装步骤
  
  1. 克隆该项目
  
  ```sh
  git clone https://github.com/shaojintian/    Best_README_template.git
  ```
  2. 创建并激活虚拟环境
  ```sh
  python3 -m venv myenv
  source myenv/bin/activate
  ```
  3. 安装项目依赖
  ```sh
  pip install -r requirements.txt
  ```  
  4. 配置数据库
  在项目的 settings.py 文件中，配置数据库连接信息。数据库用于后端信息记录。
  ```py
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'your_database_host',
        'PORT': 'your_database_port',
    }
  }
  ``` 
  或在根目录下创建 .env 文件
  ```py
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'your_database_host',
        'PORT': 'your_database_port',
    }
  }
  ``` 

  5. 执行数据库迁移
  ```sh
  python manage.py makemigrations
  python manage.py migrate
  ```    
  6. 创建超级用户
  用于登录django后台，按照提示输入用户名、邮箱和密码。
  ```sh
  python manage.py createsuperuser
  ```  
  7. 本地预览
  ```sh
  python manage.py runserver
  ```  
  在浏览器中访问 `http://127.0.0.1:8000` 即可查看项目运行情况。
  
  ### 文件目录说明
 
  ```
  blog/
  │
  ├── manage.py               # Django 项目管理脚本
  ├── settings.py             # 项目配置文件
  ├── urls.py                 # 项目 URL 配置文件
  ├── wsgi.py                 # WSGI 应用入口文件
  │
  ├── app_name/               # 应用目录
  │   ├── migrations/         # 数据库迁移文件
  │   ├── models.py           # 数据库模型定义
  │   ├── views.py            # 视图函数定义
  │   ├── urls.py             # 应用 URL 配置文件
  │   ├── templates/          # 模板文件目录
  │   └── static/             # 静态文件目录
  │
  ├── static/                 # 全局静态文件目录
  ├── templates/              # 全局模板文件目录
  ├── media/                  # 媒体文件目录
  └── requirements.txt        # 项目依赖文件
  
  ```
  
  ### 部署
  
  推荐使用以下步骤将项目部署到生产环境：
  1. **服务器准备**：选择合适的云服务器（如阿里云、腾讯云等），安装必要的软件（如 Nginx、Gunicorn、Supervisor 等）。
  2. **配置 Nginx**：创建 Nginx 配置文件，将请求转发到 Gunicorn 服务器。示例配置如下：
  ```sh
  server {
    listen 80;
    server_name your_domain_or_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/your/project;
    } 

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
  }
  ```
  关联配置文件
  ```sh
  sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/  sites-enabled
  sudo nginx -t
  sudo systemctl restart nginx
  ```
  3. **配置 Gunicorn**：创建 Gunicorn 启动脚本并配置 Supervisor 管理 Gunicorn 进程。
  ```sh
  #!/bin/bash
  source /path/to/your/venv/bin/activate
  cd /path/to/your/project
  exec gunicorn --bind unix:/run/gunicorn.sock your_project.wsgi:application
  ```
  4. **配置Supervisor**：
   配置文件（/etc/supervisor/conf.d/projectname.conf）示例:
  ```sh
  [program:projectname]
  command = /path/to/you/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock project.wsgi:application
  directory = /path/to/your/project
  user = your_user
  autostart = true
  autorestart = true
  stderr_logfile = /var/log/projectname.err.log
  stdout_logfile = /var/log/projectname.out.log
  ```
  5. **重新加载配置并启动服务**
  ```sh
  sudo supervisorctl reread
  sudo supervisorctl update
  sudo systemctl restart nginx
  ```  

  
  ### TODO
  
  - [ ]  
  
  ### 作者
  
  xxx@xxxx
     

  
  ### 鸣谢


  
