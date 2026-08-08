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
pip install -U vapoursynth-fmtconv
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
pip install "vs-cfl @ git+https://github.com/RyougiKukoc/vs-cfl-vcs.git"
```

# 脚本
```bash
pip install --force-reinstall git+https://github.com/RyougiKukoc/rkstool.git
pip install --force-reinstall git+https://github.com/RyougiKukoc/rksfunc.git
pip install --U getnative awsmfunc vsjetpack 
pip install --force-reinstall "vs-collection-rk @ git+https://github.com/RyougiKukoc/VapourSynth-Scripts-Collection.git"
```
