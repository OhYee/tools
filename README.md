# Tool

Python 实现的命令行聚合工具

```bash
git clone https://github.com/OhYee/tools.git
BIN=$(pwd)/tools/bin
export PATH=$PATH:$BIN

echo "Add export PATH=\$PATH:$BIN to your .bashrc"
```

将子命令放入 addon 目录，添加自己的功能插件（使用 `.local.py` 结尾实现私有化插件）

## 插件列表

- colorful: 带颜色替换的 `tail`
- store: 存储变量到硬盘中
