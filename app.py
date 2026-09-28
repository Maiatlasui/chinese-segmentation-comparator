"""Streamlit entry point for the Chinese word segmentation comparator."""

from __future__ import annotations

import html
import traceback

import streamlit as st

from comparison.alignment import disagreement_boundaries
from comparison.export import comparison_report, export_filename, segmented_text
from comparison.validation import request_error
from segmenters.base import Token
from segmenters.registry import TOOL_NAMES, create_backend


st.set_page_config(page_title="Chinese Word Segmentation Comparator", layout="wide")


@st.cache_resource(show_spinner=False)
def cached_backend(name: str):
    """Keep expensive model initialisation out of the button callback."""
    return create_backend(name)


def get_backend(name: str):
    try:
        return cached_backend(name), None
    except Exception as exc:  # The UI must survive an unavailable optional backend.
        details = traceback.format_exc()
        message = str(exc) or exc.__class__.__name__
        return None, (message, details)


def token_html(tokens: list[Token], marked_boundaries: set[int]) -> str:
    """Render tokens with a warm highlight where a token edge is disputed."""
    rendered: list[str] = []
    for token in tokens:
        changed = token.start in marked_boundaries or token.end in marked_boundaries
        css_class = "token token-difference" if changed else "token"
        title = f"characters {token.start}-{token.end}"
        rendered.append(
            f'<span class="{css_class}" title="{title}">{html.escape(token.text)}</span>'
        )
    return "".join(rendered) or '<span class="empty-result">No tokens returned.</span>'


def show_result(name: str, backend, tokens: list[Token], boundaries: set[int]) -> None:
    with st.container(border=True):
        st.subheader(name)
        st.markdown(token_html(tokens, boundaries), unsafe_allow_html=True)
        metadata = backend.metadata()
        st.caption(
            f"Package: {metadata['package_version']}  |  "
            f"Model: {metadata['model']}  |  Settings: {metadata['settings']}"
        )
        st.download_button(
            f"Download {name} result",
            data=segmented_text(tokens).encode("utf-8"),
            file_name=export_filename(name),
            mime="text/plain; charset=utf-8",
            key=f"download-{export_filename(name)}",
        )
        with st.expander("Token offsets"):
            st.dataframe(
                [{"Token": token.text, "Start": token.start, "End": token.end} for token in tokens],
                hide_index=True,
                use_container_width=True,
            )


st.markdown(
    """
    <style>
    .token { display: inline-block; margin: 0 0.25rem 0.25rem 0; padding: 0.18rem 0.38rem;
             border-radius: 0.25rem; background: #f1f3f5; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
    .token-difference { background: #ffe08a; box-shadow: inset 0 -2px 0 #d97706; }
    .empty-result { color: #6b7280; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Chinese Word Segmentation Comparator")
st.write("Run one segmenter or compare selected segmenters on the same Chinese text.")

EXAMPLE = "知识就是力量；时间就是生命；时间是检验真理的唯一标准。"

if "input_text" not in st.session_state:
    st.session_state.input_text = EXAMPLE

if st.button("Use example text"):
    st.session_state.input_text = EXAMPLE

text = st.text_area(
    "Enter Chinese text",
    key="input_text",
    height=220,
    placeholder="Paste one or more Chinese sentences here...",
)

mode = st.radio("Mode", ["Use one tool", "Compare tools"], horizontal=True)
highlight = False

if mode == "Use one tool":
    selected_tools = [st.selectbox("Select segmentation tool", TOOL_NAMES)]
else:
    selected_tools = st.multiselect("Select tools to compare", TOOL_NAMES, default=TOOL_NAMES[:2])
    highlight = st.checkbox("Highlight segmentation differences", value=True)

run = st.button("Run segmentation", type="primary")

if run:
    validation_error = request_error(text, mode, selected_tools)
    if validation_error:
        st.warning(validation_error)
    else:
        results: dict[str, tuple[object, list[Token]]] = {}
        errors: dict[str, tuple[str, str]] = {}
        progress = st.progress(0, text="Preparing selected tools...")
        for index, name in enumerate(selected_tools, start=1):
            backend, backend_error = get_backend(name)
            if backend_error:
                errors[name] = backend_error
            else:
                try:
                    results[name] = (backend, backend.segment(text))
                except Exception as exc:
                    errors[name] = (str(exc) or exc.__class__.__name__, traceback.format_exc())
            progress.progress(index / len(selected_tools), text=f"Finished {name}")
        progress.empty()

        if errors:
            st.subheader("Unavailable tools")
            for name, (message, details) in errors.items():
                st.error(f"{name}: {message}")
                with st.expander(f"Debug details for {name}"):
                    st.code(details, language="text")

        if results:
            token_sets = {name: tokens for name, (_, tokens) in results.items()}
            all_disagreements = disagreement_boundaries(token_sets)
            marked = all_disagreements if highlight and len(results) > 1 else set()
            st.subheader("Results")
            if mode == "Compare tools" and len(results) > 1:
                report_results = {
                    name: (tokens, backend.metadata())
                    for name, (backend, tokens) in results.items()
                }
                st.download_button(
                    "Download comparison report",
                    data=comparison_report(text, report_results, all_disagreements).encode("utf-8"),
                    file_name="segmentation-comparison.txt",
                    mime="text/plain; charset=utf-8",
                    key="download-comparison-report",
                )
            if marked:
                st.caption("Amber tokens touch a character boundary on which the selected tools disagree.")

            columns = st.columns(min(2, len(results)))
            for index, (name, (backend, tokens)) in enumerate(results.items()):
                with columns[index % len(columns)]:
                    show_result(name, backend, tokens, marked)

        if not results:
            st.error("None of the selected tools could run. See the diagnostic details above.")
