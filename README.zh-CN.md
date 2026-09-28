[English](README.md) | 简体中文

# 中文分词比较工具（Chinese Word Segmentation Comparator）

一个面向研究用途的 Streamlit 工具，用于比较 **Jieba、HanLP、LTP、pkuseg 和 THULAC** 的中文分词（Chinese Word Segmentation, CWS）结果。

本工具旨在帮助研究者针对自己的中文语料，**更有依据且可复现地选择合适的分词方法**。研究者可以使用多个中文分词工具处理同一段文本，直观比较不同工具在词边界判断上的一致与分歧，并导出结果用于后续分析。

## 为什么开发这个工具？

中文分词是许多语料库研究和文本标注任务中的重要预处理步骤，尤其是在后续标注依赖稳定、一致的词级跨度（word-level spans）时。虽然研究者可以手动进行分词，但这种方式可能引入人为的不一致，也较难在不同数据集、标注者或后续研究中准确复现。

目前已有多种自动中文分词工具，但不同工具产生的分词结果可能存在明显差异。同时，不同工具对于特定数据的适用程度也可能受到体裁（genre）、语域（register）、交际模态（mode）等文本特征的影响。

因此，Chinese Word Segmentation Comparator 并不预设某一种分词工具普遍优于其他工具，而是让研究者能够在自己的数据上运行多个分词工具，并直接观察不同工具在哪些位置作出了相同或不同的词边界判断。

本工具的核心目的，是帮助研究者根据具体数据和研究情境，更有依据且可复现地选择分词方法。它并不试图判断某一种分词方式是否具有普遍意义上的“正确性”，而是将不同工具之间的差异可视化，从而为研究者选择适合自身数据的分词方案提供依据。

## 快速开始

如果希望安装并运行全部五个分词工具，需要使用 **Python 3.8**。Python 3.9 及以上版本可以运行其中四个工具，但无法安装 pkuseg。详见下方的**兼容性与局限**。

安装 Anaconda 或 Miniconda 后，克隆或下载本仓库，并运行：

```bash
bash scripts/setup.sh
bash scripts/run.sh
```

随后打开 Streamlit 提供的本地地址，通常为：

```text
http://localhost:8501
```

安装及启动脚本主要面向 macOS 和 Linux。Windows 用户建议使用 WSL，以提高成功构建旧版 pkuseg 扩展的可能性。

也可以手动安装：

```bash
conda env create -f environment.yml
conda activate chinese-seg38
pip install -r requirements.txt
pip install Cython==0.29.37
pip install --no-build-isolation -r requirements-pkuseg.txt
streamlit run app.py
```

## 如何使用

建议的研究流程是：首先从研究语料中选取具有代表性的文本样本，使用多个工具进行分词；随后比较不同工具之间的一致与分歧；最后结合语料本身的语言特征以及后续研究需求，选择用于完整数据集的分词方法。

将一个中文句子或较长的文本/访谈片段粘贴至 **Enter Chinese text** 输入框。

- **Use one tool**：显示一个指定工具的分词结果。
- **Compare tools**：可选择任意 2–5 个工具进行比较，并仅运行所选工具。
- **Highlight segmentation differences**：标记不同工具在词边界判断上存在分歧的位置。
- **Download tool result**：将某一工具的分词结果保存为独立的 UTF-8 文本文件，并使用 `/` 标示词边界；原始文本中的换行将被保留。
- **Download comparison report**：将原始文本、所有成功运行的工具结果、软件包/模型设置以及存在分歧的字符边界位置保存至同一个 UTF-8 文本文件。

每个结果还包括所使用的软件包版本、模型/配置，以及可展开查看的字符位置（character offsets）表。这些信息有助于提高分词预处理过程的透明度和可复现性，同时保留文本位置，以支持后续研究和标注。

## 分词工具

所有后端均实现 `segment(text) -> list[Token]`，其中 `Token` 包含 `text`、`start` 和 `end`。Streamlit 界面通过统一的注册机制调用各分词工具，不包含针对某一工具单独编写的分词逻辑。

| 工具 | 固定配置 |
|---|---|
| Jieba | 默认词典；精确模式；启用 HMM |
| HanLP | HanLP 2.x `COARSE_ELECTRA_SMALL_ZH` tokenizer |
| LTP | LTP 4.x `LTP/tiny` CWS pipeline |
| pkuseg | 默认混合领域模型；关闭词性标注 |
| THULAC | 内置模型；`seg_only=True` |

HanLP 和 LTP 会在首次使用时下载指定的预训练模型。成功初始化的后端会在当前 Streamlit 进程中缓存。

## 比较机制

比较模块收集每个 token 的 `start` 和 `end` 字符位置。如果某个字符位置被至少一个所选工具识别为词边界，但并非所有工具都在该位置进行切分，则该位置被视为一个**分词分歧（segmentation disagreement）**。

这种基于字符位置的比较方式可以处理不同工具产生不同 token 数量的情况，也能够正确处理原始文本中重复出现的词语。

需要特别说明的是，工具所识别出的**分歧具有诊断意义，而非评价意义**。也就是说，本工具用于显示不同分词器**在哪里**作出了不同判断，而不会自动判断哪一种结果在语言学意义上更“正确”。

研究者仍需要结合数据本身的语言特征、研究目的以及后续分析或标注任务的需求，对这些差异进行判断。

## 研究背景

本工具最初开发于一个中文访谈语料的隐喻标注项目。在使用 **INCEpTION** 进行文本标注的过程中，由于基于跨度（span-based）的标注需要建立在稳定的底层分词方案之上，因此如何选择合适的中文分词方法成为数据预处理中的一个重要方法论问题。

Chinese Word Segmentation Comparator 因此被开发出来，希望通过直接比较不同分词工具在**研究者自身数据**上的表现，使这一选择过程更加系统、透明且可复现。

虽然本工具最初服务于隐喻标注研究，但其用途并不限于隐喻研究，也可以用于中文语料预处理以及其他对词边界有要求的研究和文本标注任务。

## 兼容性与局限

- **HanLP** 使用目前维护中的 HanLP 2.x API，而非较旧的 `pyhanlp` 接口。2.1.5 版本及所选模型首次运行时需要下载。如果 HanLP 的分块下载器（multipart downloader）报告 chunk-size mismatch，可按照错误信息提示直接下载模型：

```bash
curl -fL --retry 5 -o ~/.hanlp/tok/coarse_electra_small_20220616_012050.zip \
  https://file.hankcs.com/hanlp/tok/coarse_electra_small_20220616_012050.zip
```

- **LTP** 使用目前的 4.x `pipeline(..., tasks=["cws"])` API 和 `LTP/tiny` 模型，首次运行时可能需要下载模型。LTP 4.2.14 需要 `huggingface-hub==0.36.0`；Hub 1.x 移除了 LTP 所使用的一个参数。

- **pkuseg 0.0.25** 存在上游构建兼容性问题：隔离构建（isolated builds）无法找到 NumPy，其生成的扩展还包含 CPython 已移除的 `longintrepr.h` header。因此，需要在 Python 3.8 环境中先安装 `requirements.txt` 和 Cython 0.29.37，再使用 `--no-build-isolation` 安装 pkuseg。Python 3.9 移除了 pkuseg 生成扩展所依赖的一个 C API 字段。由于 pkuseg 的编译命令不会正确处理包含空格的 include path，因此 Conda 环境路径中不应包含空格。

- 如果某个软件包、模型下载或模型初始化失败，应用会针对该工具单独报告错误，而其他已选择的工具仍可继续使用。调试信息会保留在可折叠区域中。

- 字符位置映射假定分词后端返回与原始文本字符一致的结果。如果某个后端对字符进行了规范化处理，应用会明确报告错误，而不会生成可能不正确的字符位置。

- 本工具的比较结果不应被视为某一种分词方法普遍“正确”或“更优”的证据。合适的分词方法可能取决于具体数据、语言特征以及后续研究用途。

## 测试

运行可移植的单元测试：

```bash
python -m pytest
```

测试覆盖普通句子、复合词、类似专名的表达、科学术语、标点、重复文本、多行文本、字符位置对齐、单工具选择、两/三/五工具比较、空输入、极短输入以及工具数量验证失败等情况。

由于不同工具的模型文件和 Python 兼容性有所不同，针对具体软件包的 smoke tests 应在目标运行环境中进行。

## 许可证

本项目采用 MIT License。