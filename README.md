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

  

# Vue和Django的冲突

```
如何解决Django与Vue语法的冲突
当我们在django web框架中,使用vue的时候,会遇到语法冲突.
因为vue使用{{}},而django也使用{{}},因此会冲突.

解决办法1:
在django1.5以后,加入了标签:
{% verbatim myblock %} {% endverbatim myblock %}
被此标签包裹的代码将不会被Django的模板引擎渲染。
```

