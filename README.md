# 创建一个 Windows VapourSynth 工作环境

1.  在 [WinPython](https://winpython.github.io/) 中选择一个不低于 Python3.12 的发行版下载并解压到任意位置，比如 `WinPython64-3.14.5.0dot`
2.  解压后在 WinPython 目录中找到 `WinPython Command Prompt.exe` 双击启动
3.  根据网络环境配置 cmd 代理，比如 clash 的常见操作：
```bash
set http_proxy=http://127.0.0.1:7890
set https_proxy=http://127.0.0.1:7890
```
4.  执行 `pip install vapoursynth` 和 `vapoursynth config` 若提示缺少 vc 依赖则按照提示安装（可能需要重启）
5.  根据 [@plugin-api4.md](@plugin-api4.md) 中的提示通过 pip 完成插件与脚本安装