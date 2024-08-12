# Special

-   [dfttest2](https://github.com/AmusementClub/vs-dfttest2)

    *   把 dfttest2.py 丢到根目录或 site-packages 下，cufft-windows 压缩包里面有一个 vsmlrt-cuda 文件夹，把该文件夹扔到 plugins 里（不能把里面的 dll 直接丢到 plugins 里），vs-dfttest2-cuda-windows 压缩包里面的 dll 则直接扔到 vs-plugins 里。

-   [vs-mlrt](https://github.com/AmusementClub/vs-mlrt)
    
    *   只需下载 vsmlrt-windows-x64-cuda.v*.7z 即可，压缩包里的 vsmlrt.py 丢到根目录或 site-packages 下，其余的文件夹和 dll 原封不动丢到 vs-plugins 下即可。

-   [BM3DCUDA](https://github.com/WolframRhodium/VapourSynth-BM3DCUDA)
    
    *   CPU 版本需要选择对应你 CPU 架构的。一般只下显卡版的，如果你用的是英伟达显卡，下载 cudartc 就够了。

-   [dgdecnv](https://www.rationalqm.us/dgdecnv/binaries/)

    *   注意看发布日期。下载最新版后解压，把 DGDecodeNV.dll 扔到 vs-plugins 里，其余内容保存到你喜欢的目录，添加到系统 Path 中（在任意位置打开控制台能访问 DGIndexNV.exe 即可）。

# Modules

-   mvsfunc 
    
    ```
    pip install git+https://github.com/HomeOfVapourSynthEvolution/mvsfunc
    ```

-   getnative 

    ```
    pip install getnative
    ```

-   awsmfunc

    ```
    pip install awsmfunc
    ```

-   vsdehalo vsutil 
    
    ```
    pip install vsdehalo
    ```

-   yvsfunc, rksfunc
    
    *   [yvsfunc](https://github.com/YomikoR/yvsfunc) 和 [rksfunc](https://github.com/RyougiKukoc/rksfunc) 不能使用 pip 安装，安装方法参考 [README 2.2.2.ii](https://github.com/AliceTeaParty/How-to-Create-an-Environment#22-塞入各种插件)

# Plugin-Level1

-   [tcanny](https://github.com/AmusementClub/VapourSynth-TCanny) `latest (r14.AC4)`
-   [lsmas](https://github.com/HomeOfAviSynthPlusEvolution/L-SMASH-Works) `latest (20240408 1194.0.0.0)`
    *   如果出现问题，回退到 [akarin](https://github.com/AkarinVS/L-SMASH-Works) `vA.3k`
-   [bestsource](https://github.com/vapoursynth/bestsource) `latest (R6)`
-   [descale](https://github.com/Irrational-Encoding-Wizardry/descale) `latest (r8)`
    *   descale.py 丢到根目录下
-   [fmtc](https://github.com/EleonoreMizo/fmtconv) `latest (r30)`
    *   项目已迁移到 [gitlab](https://gitlab.com/EleonoreMizo/fmtconv/) 但暂无 Release
-   [akarin](https://github.com/AkarinVS/vapoursynth-plugin) `latest (v0.96g3)`
-   [placebo](https://github.com/AmusementClub/vs-placebo) `latest (v1.4.4-mod)`
-   [subtext](https://github.com/vapoursynth/subtext) `latest (R5)`
-   [DualSynth-madVR](https://github.com/Jaded-Encoding-Thaumaturgy/DualSynth-madVR) `R4 | madVR Test Build 206`
    *   在 dll 同目录下创建 madVR 子文件夹，放入仓库提到的三个文件 madVR64.ax、madHcNet64.dll 和 mvrSettings64.dll。
    *   [madVR](https://www.videohelp.com/software/madVR) 注意要下载 Test Build xxx 而非 0.92.17

# Plugin-Level2

-   [knlm](https://github.com/AmusementClub/KNLMeansCL) `v1.1.1e-AC`
-   [nlm_ispc](https://github.com/AmusementClub/vs-nlm-ispc) `v2`
-   [nlm_cuda](https://github.com/AmusementClub/vs-nlm-cuda) `v1`
-   [w2xnvk](https://github.com/Nlzy/vapoursynth-waifu2x-ncnn-vulkan) `R5`
    *   记得下载模型文件。
-   [bilateral](https://github.com/AmusementClub/VapourSynth-Bilateral) `r3.AC`
-   [imwri](https://github.com/AmusementClub/vs-imwri) `vA.R2`
-   [f3kdb](https://github.com/AmusementClub/flash3kyuu_deband) `2.0.1-AC`
-   [neo_f3kdb](https://github.com/HomeOfAviSynthPlusEvolution/neo_f3kdb) `r9`
-   [rgvs](https://github.com/vapoursynth/vs-removegrain) `R1`
-   [mvtools](https://github.com/Mr-Z-2697/vapoursynth-mvtools) `v23+16`
-   [dfttest](https://github.com/AmusementClub/VapourSynth-DFTTest) `r7.AC`
-   [vivtc](https://github.com/vapoursynth/vivtc) `R1`
-   [tivtc](https://github.com/dubhater/vapoursynth-tivtc) `v2`
-   [addgrain](https://github.com/HomeOfVapourSynthEvolution/VapourSynth-AddGrain) `r10`
-   [adaptivegrain](https://github.com/Irrational-Encoding-Wizardry/adaptivegrain) `0.3.1`
-   [eedi3](https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3) `r4`
-   [znedi3](https://github.com/sekrit-twc/znedi3) `r2.1`
-   *   nnedi3_weights.bin 有一个就够了
-   [nnedi3cl](https://github.com/HomeOfVapourSynthEvolution/VapourSynth-NNEDI3CL) `r8`
-   [sangnom](https://github.com/dubhater/vapoursynth-sangnom) `r42`
-   [awarpsharp2](https://github.com/dubhater/vapoursynth-awarpsharp2) `v4`
-   [retinex](https://github.com/HomeOfVapourSynthEvolution/VapourSynth-Retinex) `r4`
-   [fillborders](https://github.com/dubhater/vapoursynth-fillborders) `v2`
-   [edgefixer](https://github.com/sekrit-twc/EdgeFixer) `r2`
-   [tcomb](https://github.com/dubhater/vapoursynth-tcomb) `v4`
-   [bifrost](https://github.com/dubhater/vapoursynth-bifrost) `v3.0`
-   [smoothuv](https://github.com/dubhater/vapoursynth-smoothuv) `v3`
-   *   注意还要下 Source code 里的 [RainbowSmooth.py](https://github.com/dubhater/vapoursynth-smoothuv/blob/master/RainbowSmooth.py) 丢到根目录下
-   [hist](https://github.com/AmusementClub/vapoursynth-histogram) `v2.1-AC`
-   [misc](https://github.com/vapoursynth/vs-miscfilters-obsolete) `R2`


# Script-Level1

-   [kagefunc](https://github.com/Irrational-Encoding-Wizardry/kagefunc/blob/master/kagefunc.py) `96947a1`
-   [TAAmbk](https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk/blob/master/vsTAAmbk.py) `fef19f8`
-   [fvsfunc](https://github.com/Irrational-Encoding-Wizardry/fvsfunc/blob/master/fvsfunc.py) `076dbde `
-   [muvsfunc](https://github.com/WolframRhodium/muvsfunc/blob/master/muvsfunc.py) `3ee08a0`
-   [getfnative](https://github.com/YomikoR/GetFnative/blob/main/getfnative.py) `9edcd58`

# Script-Level2

-   [havsfunc](https://gist.github.com/RyougiKukoc/ea451bd51d0dc33ba5e0c4d5566653cf)
-   [nnedi3_rpow2](https://gist.github.com/RyougiKukoc/6c9225aa3f010ef65d341cc5f770cf23)
-   [nnedi3_resample](https://github.com/HomeOfVapourSynthEvolution/nnedi3_resample/blob/master/nnedi3_resample.py) `314c644`
-   [CSMOD](https://github.com/fdar0536/VapourSynth-Contra-Sharpen-mod/blob/master/CSMOD.py) `b9ff725`
-   [sdering_fix](https://gist.github.com/RyougiKukoc/c3832d96a8dce6f609f6e29888af94a6)
