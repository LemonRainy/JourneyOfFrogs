# 虚拟环境
- 创建虚拟环境
~~~
> python -m venv venv
~~~

- 激活虚拟环境
~~~
> cd venv/Scripts & activate & cd ../..
~~~

- 在虚拟环境中安装所需要的包
~~~
> pip install -r requirments.txt
~~~

- 退出虚拟环境
~~~
> deactivate
~~~

# 数据库迁移
- 在models.py中写好每个表(model)后，创建数据库
```
> python manege.py makemigrations Frog
```
- 迁移数据库
```angular2
> python manage.py migrate
```

# 运行
~~~
> python manage.py runserver
~~~



# 模板继承

```
基础文件：templates/complete/base.html
Demo: templates/complete/indexPage.html
```

- 使用方法

```
{% extends "complete/base.html" %}
{% block content %}  
// 填入页面独有的内容（除开<head>，导航栏，footer）
// 可参照complete目录下的indexPage.html
{% endblock %}
```

  