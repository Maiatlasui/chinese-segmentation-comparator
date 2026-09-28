English | [简体中文](README.zh-CN.md)

# Chinese Word Segmentation Comparator

A research-oriented Streamlit tool for comparing Chinese word segmentation (CWS) outputs from **Jieba, HanLP, LTP, pkuseg, and THULAC**.

The comparator is designed to support informed and reproducible selection of segmentation methods for Chinese-language corpus and annotation workflows. It allows researchers to run multiple CWS tools on the same text, inspect where their word-boundary decisions agree or diverge, and export the results for further analysis.

## Why this tool?

Chinese word segmentation is an important preprocessing step for many corpus-based and annotation tasks, particularly when annotation requires consistent word-level spans. While segmentation can be performed manually, this can introduce inconsistency and make the preprocessing procedure difficult to reproduce across datasets and annotators.

A range of automatic CWS tools are available, but their outputs can differ considerably. Their suitability may also depend on characteristics of the data, such as genre, register, and mode of communication. Rather than assuming that one segmenter is universally preferable, **Chinese Word Segmentation Comparator** provides a simple way to run multiple CWS tools on the same text and inspect where their segmentation decisions agree or diverge.

The tool is designed to support **informed and reproducible selection of a segmentation method for a particular dataset and research context**. It does not attempt to determine a universally "correct" segmentation; instead, it makes differences between established CWS tools visible so that researchers can evaluate which approach is most appropriate for their data.

## Quick start

Python 3.8 is the required interpreter for an all-five-tool installation. A Python 3.9+ fallback can run the other four tools but cannot install pkuseg; see **Compatibility and limitations** below.

Install Anaconda or Miniconda, clone or download this repository, and run:

```bash
bash scripts/setup.sh
bash scripts/run.sh
```

Open the local URL Streamlit prints, normally:

```text
http://localhost:8501
```

The setup and launch scripts target macOS and Linux. Windows users should use WSL for the best chance of building the legacy pkuseg extension.

For manual installation:

```bash
conda env create -f environment.yml
conda activate chinese-seg38
pip install -r requirements.txt
pip install Cython==0.29.37
pip install --no-build-isolation -r requirements-pkuseg.txt
streamlit run app.py
```

## Using the app

A suggested research workflow is to select representative samples from your dataset, compare segmentation across several tools, inspect areas of agreement and disagreement, and use these observations to inform the choice of a segmentation method for the full dataset.

Paste a sentence or longer transcript excerpt into **Enter Chinese text**.

- **Use one tool** shows one selected backend's segmentation.
- **Compare tools** accepts any two to five tools and runs only those choices.
- **Highlight segmentation differences** marks tokens touching an offset where a selected tool has a word boundary and another selected tool does not.
- **Download tool result** saves that tool's segmentation as an individual UTF-8 text file using `/` to show word boundaries. Source line breaks are preserved.
- **Download comparison report** saves the original text, all successful tool outputs, package/model settings, and disputed character-boundary offsets in one UTF-8 text file.

Each result includes the package version, model/configuration details, and an expandable table of character offsets. This makes the segmentation procedure more transparent and reproducible and allows downstream research workflows to retain original-text positions.

## Segmentation backends

Every backend implements `segment(text) -> list[Token]`, where `Token` has `text`, `start`, and `end`. The Streamlit UI asks the common registry for a backend and contains no tool-specific segmentation logic.

| Tool | Fixed configuration |
|---|---|
| Jieba | Default dictionary, accurate mode, HMM enabled |
| HanLP | HanLP 2.x `COARSE_ELECTRA_SMALL_ZH` tokenizer |
| LTP | LTP 4.x `LTP/tiny` CWS pipeline |
| pkuseg | Default mixed-domain model, POS disabled |
| THULAC | Bundled model, `seg_only=True` |

HanLP and LTP obtain their named pretrained models the first time they are used. The app caches a successfully initialised backend for the Streamlit process.

## How comparison works

The comparison layer collects each token's `start` and `end` character offsets. An offset is treated as a segmentation disagreement when it occurs as a word boundary for at least one selected tool but not every selected tool.

This approach allows differences to be identified even when tools return different numbers of tokens or when a word occurs repeatedly in the source text.

Importantly, **disagreement is diagnostic rather than evaluative**. The comparator identifies *where* segmentation decisions differ; it does not determine which decision is linguistically correct. Researchers should evaluate these differences in relation to the characteristics of their data and the requirements of their downstream analysis or annotation task.

## Research context

This tool was originally developed while preparing Chinese-language interview data for metaphor annotation in **INCEpTION**. Because span-based annotation requires a consistent underlying tokenisation scheme, selecting an appropriate Chinese word segmentation method formed an important preprocessing decision.

The comparator was developed to make this decision more systematic and reproducible by allowing segmentation tools to be examined directly on the researcher's own data. Although developed in the context of metaphor annotation, the tool can be used more broadly for Chinese-language corpus preparation and other workflows where word boundaries matter.

## Compatibility and limitations

- **HanLP** uses the maintained HanLP 2.x API rather than the older `pyhanlp` interface. Version 2.1.5 and its selected model require an initial download. If HanLP's multipart downloader reports a chunk-size mismatch, download the model archive directly as its error message recommends:

```bash
curl -fL --retry 5 -o ~/.hanlp/tok/coarse_electra_small_20220616_012050.zip \
  https://file.hankcs.com/hanlp/tok/coarse_electra_small_20220616_012050.zip
```

- **LTP** uses the current 4.x `pipeline(..., tasks=["cws"])` API with the `LTP/tiny` model and may require an initial model download. LTP 4.2.14 requires `huggingface-hub==0.36.0`; Hub 1.x removed an argument used by LTP.

- **pkuseg 0.0.25** has an upstream build defect: isolated builds cannot find NumPy, and its generated extension includes CPython's removed `longintrepr.h` header. It must be installed after `requirements.txt` and Cython 0.29.37, with `--no-build-isolation`, on Python 3.8. Python 3.9 removed a C API field used by pkuseg's generated extension. The Conda environment path must not contain spaces because pkuseg's compiler command does not quote include paths.

- Any unavailable package, model download, or model initialisation is reported per tool. Other selected tools remain usable, and debug details are kept in a collapsible section.

- Offset mapping assumes a backend returns source-preserving text. If a backend normalises characters, the app reports a clear error instead of silently producing invalid offsets.

- The outputs should not be interpreted as evidence that any one segmentation is universally correct or preferable. Appropriate segmentation may depend on the dataset, linguistic characteristics, and intended downstream use.

## Tests

Run the portable unit tests with:

```bash
python -m pytest
```

The tests cover ordinary sentences, compounds, proper-name-like examples, scientific terminology, punctuation, repeated text, multiline text, offset alignment, single-tool selection, two/three/all-five comparison selection, empty input, very short input, and a tool-count validation failure.

Package-specific smoke checks should be run in the target environment because model files and Python compatibility vary.

## Licence

This project is released under the MIT License.