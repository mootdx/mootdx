# 安装方式

## 普通安装

### 标准安装

> 新手建议使用 `pip install -U 'mootdx[all]'` 安装

```shell
# 包含核心依赖安装
pip install -U 'mootdx'

# 包含命令行依赖安装, 如果使用命令行工具可以使用这种方式安装
pip install -U 'mootdx[cli]'

# 包含所有扩展依赖安装, 如果不清楚各种依赖关系就用这个命令
pip install -U 'mootdx[all]'
```

## 升级版本

```shell
pip install -U mootdx
```

## 源码安装[不建议, 速度较慢]

直接远程源码安装

```shell
pip install git+https://github.com/mootdx/mootdx.git
```

