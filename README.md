# Chinese Word Segmentation Comparator

A local Streamlit app for running and comparing Chinese word segmentation with
Jieba, HanLP, LTP, pkuseg, and THULAC. It is a research prototype for examining
word-boundary variation, not an annotation or INCEpTION export tool.

## Quick start

Python 3.8 is the required interpreter for an all-five-tool installation. A
Python 3.9+ fallback can run the other four tools but cannot install pkuseg;
see **Compatibility**.

Install [Anaconda](https://www.anaconda.com/download) or
[Miniconda](https://docs.conda.io/projects/miniconda/en/latest/), clone or
download this repository, and run:

```bash
bash scripts/setup.sh
bash scripts/run.sh
```

Open the local URL Streamlit prints, normally `http://localhost:8501`.

The setup and launch scripts target macOS and Linux. Windows users should use
WSL for the best chance of building the legacy pkuseg extension.

For manual installation:

```bash
conda env create -f environment.yml
conda activate chinese-seg38
pip install -r requirements.txt
pip install Cython==0.29.37
pip install --no-build-isolation -r requirements-pkuseg.txt
streamlit run app.py
```

New to GitHub? Follow the complete [GitHub Publishing Workbook](GITHUB_WORKBOOK.md).

## Using the app

Paste a sentence or longer transcript excerpt into **Enter Chinese text**.

- **Use one tool** shows one selected backend's segmentation.
- **Compare tools** accepts any two to five tools and runs only those choices.
- **Highlight segmentation differences** marks tokens touching an offset where a
  selected tool has a word boundary and another selected tool does not.
- **Download _tool_ result** saves that tool's segmentation as an individual
  UTF-8 text file using ` / ` to show word boundaries. Source line breaks are
  preserved.
- **Download comparison report** saves the original text, all successful tool
  outputs, package/model settings, and disputed character-boundary offsets in
  one UTF-8 text file.

Each result includes package version, model/configuration details, and an
expandable table of character offsets. This makes a result reproducible and
allows downstream research workflows to retain original-text positions.

## Backends

Every backend implements `segment(text) -> list[Token]`, where `Token` has
`text`, `start`, and `end`. The Streamlit UI asks the common registry for a
backend and contains no tool-specific segmentation logic.

| Tool | Fixed configuration |
| --- | --- |
| Jieba | Default dictionary, accurate mode, HMM enabled |
| HanLP | HanLP 2.x `COARSE_ELECTRA_SMALL_ZH` tokenizer |
| LTP | LTP 4.x `LTP/tiny` CWS pipeline |
| pkuseg | Default mixed-domain model, POS disabled |
| THULAC | Bundled model, `seg_only=True` |

HanLP and LTP obtain their named pretrained model the first time they are used.
The app caches a successfully initialised backend for the Streamlit process.

## Difference detection

The comparison layer collects each token's `start` and `end` character offsets.
An offset is highlighted when it occurs as a boundary for at least one selected
tool but not every selected tool. This remains dependable even when tools return
different numbers of tokens or when a word occurs repeatedly.

## Compatibility and limitations

- HanLP is intentionally the maintained HanLP 2.x API, not the older `pyhanlp`
  interface. Version 2.1.5 and its selected model require an initial download.
  If HanLP's multipart downloader reports a chunk-size mismatch, download the
  model archive directly as its error message recommends:

  ```bash
  curl -fL --retry 5 -o ~/.hanlp/tok/coarse_electra_small_20220616_012050.zip \
    https://file.hankcs.com/hanlp/tok/coarse_electra_small_20220616_012050.zip
  ```
- LTP's `LTP/tiny` model is loaded through the current 4.x `pipeline(...,
  tasks=["cws"])` API and may require its initial model download. LTP 4.2.14
  requires `huggingface-hub==0.36.0`; Hub 1.x removed an argument used by LTP.
- pkuseg 0.0.25 has an upstream build defect: isolated builds cannot find
  NumPy, and its generated extension includes CPython's removed `longintrepr.h`
  header. It must be installed after `requirements.txt` and Cython 0.29.37,
  with `--no-build-isolation`, on Python 3.8. Python 3.9 removed a C API field
  used by pkuseg's generated extension. The Conda environment path must not
  contain spaces because pkuseg's compiler command does not quote include paths.
- Any unavailable package, model download, or model initialisation is reported
  per tool. Other selected tools remain usable, and debug details are kept in a
  collapsible section.
- Offset mapping assumes a backend returns source-preserving text. If a backend
  normalises characters, the app reports a clear error instead of silently
  producing invalid offsets.
- These tokenizations are comparison outputs, not a claim that one segmentation
  is linguistically correct or best for a particular corpus.

## Tests

Run the portable unit tests with:

```bash
python -m pytest
```

The tests cover ordinary sentences, compounds, proper-name-like examples,
scientific terminology, punctuation, repeated text, multiline text, offset
alignment, single-tool selection, two/three/all-five comparison selection,
empty input, very short input, and a tool-count validation failure.
Package-specific smoke checks should be run in the target environment because
model files and Python compatibility vary.
