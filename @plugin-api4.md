# 特殊插件
根据显卡选择，如果你的显卡（及其驱动）支持 CUDA 12.9：
```bash
pip install "vapoursynth-bm3dcuda @ git+https://github.com/RyougiKukoc/VapourSynth-BM3DCUDA-api4.git@cu129"
pip install "vapoursynth-dfttest2 @ git+https://github.com/RyougiKukoc/vs-dfttest2-api4.git@cu129"
pip install "vs-mlrt @ git+https://github.com/RyougiKukoc/vs-mlrt-api4.git@cu129"
```
或者至少支持 CUDA 12.1：
```bash
pip install "vapoursynth-bm3dcuda @ git+https://github.com/RyougiKukoc/VapourSynth-BM3DCUDA-api4.git@cu121"
pip install "vapoursynth-dfttest2 @ git+https://github.com/RyougiKukoc/vs-dfttest2-api4.git@cu121"
pip install "vs-mlrt @ git+https://github.com/RyougiKukoc/vs-mlrt-api4.git@cu121"
```
否则：
```bash
pip install "vapoursynth-bm3dcuda @ git+https://github.com/RyougiKukoc/VapourSynth-BM3DCUDA-api4.git@cpu"
pip install "vapoursynth-dfttest2 @ git+https://github.com/RyougiKukoc/vs-dfttest2-api4.git@cpu"
pip install "vs-mlrt @ git+https://github.com/RyougiKukoc/vs-mlrt-api4.git@generic"
```

# 活跃维护的插件
```bash
pip install -U vapoursynth-vszip 
pip install -U vapoursynth-vszipcl
pip install -U vapoursynth-zsmooth
pip install -U vapoursynth-bestsource
pip install -U vapoursynth-lsmas
```

# 不太活跃维护的插件
```bash
pip install vapoursynth-mvutensils
pip install vapoursynth-nnedi3vk
pip install vapoursynth-eedi3vk2
pip install vapoursynth-fmtconv
pip install vapoursynth-descale 
pip install vs-placebo
pip install vapoursynth-cambi
pip install vapoursynth-fftspectrum_rs
pip install vapoursynth-hysteresis
pip install vapoursynth-manipmv
pip install vapoursynth-sneedif
pip install vapoursynth-resize2
pip install vsnoise
pip install vapoursynth-subtext
pip install vapoursynth-akarin
pip install vsfpng
pip install vapoursynth-deblock
pip install vapoursynth-dctfilter
pip install vapoursynth-mvtools
pip install vapoursynth-vivtc
pip install vapoursynth-znedi3
pip install vapoursynth-adaptivegrain
pip install vapoursynth-edgefixer
pip install vapoursynth-fillborders
pip install vapoursynth-awarp
pip install vapoursynth-sangnom
pip install vapoursynth-bm3d
pip install "vs-nlq @ git+https://github.com/RyougiKukoc/vs-nlq.git"
pip install "vapoursynth-nnedi3cl @ git+https://github.com/RyougiKukoc/VapourSynth-NNEDI3CL-api4.git"
pip install "vapoursynth-smoothuv @ git+https://github.com/RyougiKukoc/vapoursynth-smoothuv-api4.git"
pip install "vapoursynth-dfttest @ git+https://github.com/RyougiKukoc/VapourSynth-DFTTest-api4.git"
pip install "vapoursynth-knlm @ git+https://github.com/RyougiKukoc/VapourSynth-KNLMeansCL-api4.git"
pip install "vapoursynth-retinex @ git+https://github.com/RyougiKukoc/VapourSynth-Retinex-api4.git"
pip install "vapoursynth-tivtc @ git+https://github.com/RyougiKukoc/vapoursynth-tivtc-api4.git"
pip install "vapoursynth-tcomb @ git+https://github.com/RyougiKukoc/vapoursynth-tcomb-api4.git"
pip install "vapoursynth-tcanny @ git+https://github.com/RyougiKukoc/VapourSynth-TCanny-vcs.git"
pip install "vapoursynth-bifrost @ git+https://github.com/RyougiKukoc/vapoursynth-bifrost-vcs.git"
pip install "vapoursynth-misc @ git+https://github.com/RyougiKukoc/vs-miscfilters-obsolete-vcs.git"
pip install "vapoursynth-fft3dfilter @ git+https://github.com/RyougiKukoc/VapourSynth-FFT3DFilter-vcs.git"
```

# 脚本
```bash
pip install git+https://github.com/RyougiKukoc/rkstool.git
pip install git+https://github.com/RyougiKukoc/rksfunc.git
pip install getnative awsmfunc vsjetpack 
pip install "vs-collection-rk @ git+https://github.com/RyougiKukoc/VapourSynth-Scripts-Collection.git"
```
