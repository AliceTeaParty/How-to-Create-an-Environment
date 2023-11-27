# 前言

在***阅读完下一章***之后，你需要给环境添加各种滤镜脚本和插件。仓库里的 @plugins.txt 是我的插件列表，大多数情况下你只需要手动安装最前面的 `Special` 和 `Modules` 部分，剩下四个板块的可以直接去 [Release](https://github.com/AliceTeaParty/How-to-Create-an-Environment/releases) 里下载最新合集包。***注意***，`Plugin-Levelx` 中的 `.py` 文件需要丢到 site-packages 文件夹里，其他的任何文件、文件夹，保留压缩包中的相对位置，丢到 plugins 文件夹里。安装 `Modules` 部分需要运行对应的的命令，请保证命令行中的 pip 是本环境的（你可以输入 `where pip` 来确认）。

# 创建一个 VapourSynth 环境

本文语意中的 VapourSynth 环境基本上由 Python 的 Windows embeddable package、VapourSynth-Portable、动态链接库插件、Python 脚本插件和一些 Python 包组成。

## 组建基本的 Python 环境
到 [VapourSynth 的 GitHub 仓库](https://github.com/vapoursynth/vapoursynth/releases)里下载一个 `VapourSynth64-Portable`，在文档中确定该版本需要的 Python 版本。下载对应版本的 [WinPython](https://winpython.github.io/)。

解压 WinPython 到本地，一般解压出来的文件夹里有一个类似 `python-3.11.5.amd64` 的子文件夹，和 Python Embeddable Package 看起来差不多，我们一般把这个子文件夹当做 Python 的环境根目录。将 VapourSynth64-Portable 解压到根目录里，应该会提示有几个文件重复，直接替换就好。
<details>
    <summary>【旧版】组建基本的 Python 环境</summary>

众所周知 VapourSynth 是搭建在 Python 上的，在 [Python 官网](https://www.python.org/downloads/windows/)下载一个 `Windows embeddable package (64-bit)`，注意 VapourSynth 版本对应的 Python 版本，不确定在群里问一问。他应该是一个压缩包，解压到某个文件夹里，比如说 `Python-VapourSynth`，那么这就是环境的主目录了。

接下来需要到 [VapourSynth 的 GitHub 仓库](https://github.com/vapoursynth/vapoursynth/releases)里下载一个 `VapourSynth64-Portable`，直接解压到主目录 `Python-VapourSynth` 文件夹下，应该会提示有几个文件重复，直接替换就好。

这一部分的内容在 [VapourSynth 官方文档](http://vapoursynth.com/doc/installation.html#windows-installation-portable)里有提及，可以参考看看。

然后，找到 `VapourSynth64-Portable` 下一个后缀为 `._pth` 的文件，他的文件名应该正好是你的 Python 版本号，把这个文件删除或重命名为后缀不是 `._pth` 的文件。

最后我们需要给这个环境安装 pip，在[这个链接](https://bootstrap.pypa.io/get-pip.py)里保存 `get-pip.py`，或者使用命令行：

```
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
```

把 `get-pip.py` 放在 `VapourSynth64-Portable` 文件夹下，在该文件夹打开命令行或新建命令行游历到此，运行：

```
python get-pip.py
```

如果没有 Error 发生（有几个 Warning 是正常的），pip 就被成功地安装了。

为了方便地引入这个环境，你可以在新建命令行所在的文件夹建立一个 `path.bat`，假设 `VapourSynth64-Portable` 在 `C:\` 下，里面写：

```commandline
set PATH=%PATH%;C:\VapourSynth64-Portable;C:\VapourSynth64-Portable\Scripts;
```

如果你把 `VapourSynth64-Portable` 放在了其他地方，对应修改即可。这样每当你新建一个命令行时，在命令行内运行 `path.bat`，即可把这个 Python 环境放入系统环境变量中。
</details>

为了方便地引入这个环境，你可以在新建命令行所在的文件夹建立一个 `path.bat`，里面写：

```commandline
set PATH=$环境根目录$;$环境根目录$\Scripts;%PATH%;
```

上面 `$环境根目录$` 替换成你的机器上环境根目录的地址。这样每当你新建一个命令行时，在命令行内运行 `path.bat`，即可把这个 Python 环境放入系统环境变量中。

此外，WinPython 在与根目录同级的地方放了一堆包装过的控制台（比如 `WinPython Command Prompt.exe`），双击他们，自动会将 Python 环境引入系统环境变量。

## 塞入各种插件

搭建好基本环境之后，就可以往里面塞插件了。插件分为三种：

1. 动态链接库插件：这类插件的特点是编译后形成一个 `.dll` 文件，他们大多数都被作者放在 GitHub 仓库里，一般来说只需要到 Release 里找作者编译好的文件就行。但要注意，直接点 Release 会进入最新的一个 Release 页，如果这个 Release 不包括作者编译好的插件，可以回退几个 Release 版本找。获取到 `.dll` 文件以后，把它放在 `Python-VapourSynth\\vapoursynth64\\plugins` 下即可。
2. Python 脚本插件：这类插件其实又分为两种。
    1. 第一种是单独一个 `.py` 文件，比如 [havsfunc](https://github.com/HomeOfVapourSynthEvolution/havsfunc)。这种插件只需把仓库中的对应文件保存到本地，然后放在 `Python-VapourSynth\\Lib\\site-packages` 下即可。
    2. 第二种比较复杂，他们以 Python 模块的形式存在，比如 [yvsfunc](https://github.com/YomikoR/yvsfunc)。这种插件需要首先识别出仓库中的哪个文件夹代表了这个模块本体（通常是与模块同名，比如上述例子中就是 `yvsfunc` 文件夹。把整个仓库下载下来，然后把对应文件夹放在 `Python-VapourSynth\\Lib\\site-packages` 下即可。
3. Python 模块插件：有一些 Python 模块可能直接复制会有一点点问题，这时候我推荐使用模块安装的方法。我已经在 `@plugin.txt` 中提供了模块名和对应的安装命令，对着抄即可。
~~比如要安装 `vsutil`，先在命令行内运行 `path.bat`、引入你想安装到的环境，然后输入 `pip install --no-deps vsutil` 即可安装。你可以在任意仓库下载源代码、解压到任意路径，该项目根目录下往往会有 `setup.py` 或者 `setup.cfg` 这种文件。先在命令行内运行 `path.bat`、引入你想安装到的环境，然后命令行游历到项目根目录，输入 `pip install .` 就好了。特别注意：有很多这种类型的模块会在安装文件中指定一些依赖包，你可以打开 `setup.cfg` 或者 `setup.py` 找到里面 dependancy 或者 requirement 字样的代码，下面很可能包括了他们的依赖列表（有些是引用同目录下的文件，这时候你要修改对应的文件），你需要把里面的 VapourSynth 删除，其他可以保持不变。因为这个教程安装的 VapourSynth 环境没法被 pip 检测到。~~