# 特殊插件
以下命令固定使用 api4-wheels 提供的 `+alice.1` 版本，避免 pip 从 PyPI 选中同名包。

根据显卡选择，如果你的显卡（及其驱动）支持 CUDA 12.9：
```bash
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ "vs-mlrt-cu129==16.2.6+alice.1"
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ "vapoursynth-bm3dcuda-cu129==2.16+alice.1"
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ "vapoursynth-dfttest2-cu129==10.2+alice.1"
```
或者至少支持 CUDA 12.1：
```bash
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ "vs-mlrt-cu121==16.2.6+alice.1"
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ "vapoursynth-bm3dcuda-cu121==2.16+alice.1"
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ "vapoursynth-dfttest2-cu121==10.2+alice.1"
```
否则：
```bash
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ "vs-mlrt-generic==16.2.6+alice.1"
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ "vapoursynth-bm3dcpu==2.16+alice.1"
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ "vapoursynth-dfttest2-cpu==10.2+alice.1"
```

# 活跃维护的插件
```bash
pip install -U vapoursynth-vszip 
pip install -U vapoursynth-vszipcl
pip install -U vapoursynth-vszipcu
pip install -U vapoursynth-zsmooth
pip install -U vapoursynth-bestsource
pip install -U vapoursynth-lsmas
pip install -U vapoursynth-mvutensils
pip install -U vapoursynth-nnedi3vk
pip install -U vapoursynth-eedi3vk2
```

# 不太活跃维护的插件
```bash
pip install -U vapoursynth-descale 
pip install -U vs-placebo
pip install -U vapoursynth-cambi
pip install -U vapoursynth-fftspectrum_rs
pip install -U vapoursynth-hysteresis
pip install -U vapoursynth-manipmv
pip install -U vapoursynth-sneedif
pip install -U vapoursynth-resize2
pip install -U vsnoise
pip install -U vapoursynth-subtext
pip install -U vapoursynth-akarin
pip install -U vsfpng
pip install -U vapoursynth-deblock
pip install -U vapoursynth-dctfilter
pip install -U vapoursynth-mvtools
pip install -U vapoursynth-vivtc
pip install -U vapoursynth-znedi3
pip install -U vapoursynth-adaptivegrain
pip install -U vapoursynth-edgefixer
pip install -U vapoursynth-fillborders
pip install -U vapoursynth-awarp
pip install -U vapoursynth-sangnom
pip install -U vapoursynth-bm3d
pip install -U vapoursynth-eedi3
pip install -U vapoursynth-edgemasks
pip install -U vapoursynth-bifrost
pip install -U vapoursynth-tivtc
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vs-nlq
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vs-cfl
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vapoursynth-misc
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vapoursynth-fft3dfilter
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vapoursynth-tcanny
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vapoursynth-tcomb
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vapoursynth-retinex
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vapoursynth-knlm
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vapoursynth-dfttest
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vapoursynth-smoothuv
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U vapoursynth-nnedi3cl
pip install --extra-index-url https://jaded-encoding-thaumaturgy.github.io/vs-wheels/simple -U vapoursynth-fmtconv
pip install --extra-index-url https://jaded-encoding-thaumaturgy.github.io/vs-wheels/simple -U vapoursynth-ffms2
```

# 脚本
```bash
pip install --extra-index-url https://aliceteaparty.github.io/vapoursynth-api4-wheels/simple/ -U rkstool rksfunc vs-collection-rk
pip install -U getnative awsmfunc vsjetpack 
```
