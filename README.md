# 创建一个 Windows VapourSynth 工作环境

1.  在 [WinPython](https://winpython.github.io/) 中选择一个不低于 Python3.12 的发行版下载并解压到任意位置，比如 `WinPython64-3.14.5.0dot`
2.  解压后在 WinPython 目录中找到 `WinPython Command Prompt.exe` 双击启动
3.  根据网络环境配置 cmd 代理，比如 clash 的常见操作：
```bash
set http_proxy=http://127.0.0.1:7890
set https_proxy=http://127.0.0.1:7890
```
4.  执行 `pip install -U --pre vapoursynth vsstubs` 和 `vapoursynth config` 若提示缺少 vc 依赖则按照提示安装（可能需要重启）
5.  根据 [@plugin-api4.md](@plugin-api4.md) 中的提示通过 pip 完成插件与脚本安装

# VS Code 配置

1.  安装 [vsedit](https://github.com/YomikoR/VapourSynth-Editor/releases) 后打开 `Edit->Settings->Paths` 将 `WinPython\\python\\Lib\\site-packages\\vapoursynth` 添加到 `VapourSynth library (VSScript) search paths` 中。我们需要用到 vsedit 安装目录下的 vsedit-previewer。
2.  在 VS Code 中安装 Python 插件，打开任意 `.vpy` 文件，将文件关联设置成 Python。设置 Python 解释器为 `WinPython\\python` 下的 `python.exe`，此时 VS Code 中可以正常渲染 VapourSynth 插件了。每当添加了一批新的插件，可以执行 `vsstubs` 以取其语法提示
3.  在 VS Code 中安装 Code Runner 插件，将 Run Code 快捷键绑定为 F5（这是 vsedit 的习惯，你也可以不这么操作），然后在插件设置中找到“Code-runner: Executor Map By Glob”，点击“在 settings.json 中编辑”，在弹出的配置中编辑：
```json
"code-runner.executorMapByGlob": {
    "*.vpy": "vsedit-previewer的路径 $fullFileName",
    // 注意路径中的 \ 要替换为 \\，路径前后需要用双引号括起来，并且双引号前也要加一个 \，样例如下：
    // "*.vpy": "\"C:\\Program Files\\VapourSynth Editor\\vsedit-previewer.exe\" $fullFileName",
} 
```

# 将环境设置成系统默认 Python

Magic-Raws 的工具链对将 `.py` 文件赋予可执行的打开方式有刚性需求，而 Windows 对修改可执行的默认打开方式有非常繁琐的流程，我们的仓库里提供一个 `py.bat`，代替各路 `python.exe`，起到一个 launcher 的作用，只需要把系统的 `.py` 文件默认打开方式修改为 `py.bat`，在更新环境时修改 `py.bat` 中的 `PYTHON_TO_USE` 即可。具体来说：你需要先把 `py.bat` 存放到系统的某个不轻易修改的地方（为方便表述，我们假设它被放在 `C:\green\py.bat`），打开一个*具有管理员权限*的 `cmd`，运行：
```
assoc .py=pyfile
ftype pyfile="C:\green\py.bat" "%1" %*
```
然后找到任意一个 `.py` 文件（比如你可以下载本仓库中的 `test-path.py`）右键 -> 打开方式 -> 选择其它应用 -> 选择 `py.bat` -> 勾选“始终使用此应用打开 .py 文件” -> 确定。正常情况下你应该能观察到 `.py` 文件的图标变成空白文件图标。双击 `test-path.py`，如果你能看到正常的输出，那么环境配置就没有问题了。
