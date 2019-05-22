[虚拟环境](#虚拟环境)  
[数据库迁移](#数据库迁移)  
[运行](#运行)  
[模板继承](#模板继承)  
[Vue和Django的冲突](#Vue和Django的冲突)    
[关于Order表中订单状态的含义(2019/5/22更新)](#关于Order表中订单状态的含义)

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

# 数据库中关于时间的操作
```python
# ------ 获取日期的方式 ------
ticks = time.time() # 获取当前时间的时间戳
time_update = time.strftime('%Y-%m-%d %H:%M', time.localtime(ticks)) # 将时间戳格式化成%Y-%m-%d %H:%M的形式
models.Order.objects.filter(expert_id=v, state=0).update(date=time_update) # 数据库中修改时间（增加信息的时候同理）
# ---------------------------
```



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

# 关于Order表中订单状态的含义

state分为4个状态，对应如下含义：
- 0：待服务  
用户刚下单，专员还未操作  

- 1：待完成  
专员已经接受订单  

- 2：已完成  
订单已经完成  

- -1：已取消  
订单被取消，可能由于用户中途取消，也可能由于专员拒绝了订单  

# 撤回commit  
1. 打开Git Bush  
2. 一顿cd操作，进入到你的项目目录(.git文件所在的目录)  
3. 输入  
```
> git reset HEAD~ 
```

# 撤回push  
1. 打开Git Bush  
2. 一顿cd操作，进入到你的项目目录(.git文件所在的目录)  
3. 查看近期 commit 的信息,找到你想回到的版本号
```
> git log
```  
比如,如下的版本号就是“aa909cff2239536df14820fe086d96305b24e9f1”
'''
commit aa909cff2239536df14820fe086d96305b24e9f1
Author: hanchao5272 <89298141@qq.com>
Date:   Sat Mar 3 23:43:03 2018 +0800
'''
4. 回退你想回到的版本号（`注意，不是你交错的版本号，而是你想回退到的版本号`）
```
> git reset --soft <你想回退到的版本号>
```




