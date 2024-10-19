# 知路：AI驱动的电子书全内容知识发现

功能：

- 解构：电子图书知识要素解构处理：自动结构出书的关键知识要素
- 组织：
- 问答：

## 开发环境搭建

### 安装poetry

采用阿里云的pip源，先安装pipx，再利用pipx安装poetry，最后通过pipx ensurepath将执行

文件加入环境变量

```shell
pip install pip -U
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip install pipx
pip install virtualenv
pipx install poetry
pipx ensurepath
```

### 工程导入

如果系统默认的Python版本低于3.11，则需要执行以下命令：

```shell
conda create -n py311 python=3.11.1
conda activate py311
#which python
#poetry env use /path/to/your/python
poetry env use `which python`
```

安装依赖

```shell
poetry install
```

查看env的位置，并在vscode中选择“Enter Interpreter path...”部分，输入如下命令显示的路径：

```shell
poetry env info --path
```

通过以上步骤即可完成虚拟环境的创建和选择。

### 增加依赖包

如需添加包，必须通过审核后方可提交，包的添加方式，以pyhocon为例，如下：

```shell
poetry add pyhocon
```

### 运行脚本

首次运行脚本之前，首先需要激活poetry的shell环境，在当前工程目录下执行：

```shell
poetry shell
```

然后通过poetry run python 执行执行脚本，例如要运行start.py，可以执行：

```shell
poetry run python start.py
```

### 单元测试覆盖率

用pip安装coveragepy后，执行：

```shell
coverage run -m unittest
coverage report
```

## 发布

```shell
python setup.py build_ext --inplace
```
