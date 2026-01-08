import streamlit as st


st.set_page_config(page_title="블록으로 배우는 사칙연산", layout="centered")

st.title("블록으로 배우는 사칙연산")

BLOCK_STYLE = """
<style>
.block {display:inline-block; width:34px; height:34px; margin:4px; background:linear-gradient(180deg,#6ea8fe,#4f8bf9); border-radius:6px; box-shadow:0 3px 6px rgba(0,0,0,0.15); transition:transform .12s ease}
.block:hover{transform:translateY(-4px) scale(1.05)}
.empty {display:inline-block; width:34px; height:34px; margin:4px; background:transparent}
.group-box {display:inline-block; vertical-align:top; margin:8px; padding:8px; border-radius:8px; background:linear-gradient(180deg,#fff,#f3f9ff); box-shadow:0 2px 6px rgba(0,0,0,0.08); min-width:90px}
.group-header {font-weight:600; text-align:center; margin-bottom:6px; font-size:14px}
.group-label {text-align:center; font-size:13px; margin-top:6px}
.array-grid {display:inline-block; border-radius:6px; padding:8px; background:linear-gradient(180deg,#fff,#fbfbff); box-shadow:inset 0 0 0 1px rgba(0,0,0,0.06)}
.cell {width:34px; height:34px; display:inline-flex; align-items:center; justify-content:center; border:1px solid rgba(0,0,0,0.06); background:transparent}
.small-muted {color:#555; font-size:14px}
</style>
"""

st.markdown(BLOCK_STYLE, unsafe_allow_html=True)

tabs = st.tabs(["덧셈", "곱셈(배열)", "나눗셈(같이 나누기)"])


def render_blocks_grid(total, cols=10):
    # use a CSS grid-like inline layout for nicer wrapping
    html = f"<div class='array-grid' style='display:grid; grid-template-columns: repeat({cols}, 34px); gap:8px;'>"
    for i in range(total):
        html += "<div class='block' title='블록'></div>"
    # fill remaining cells in last row as transparent spaces to keep grid shape
    remainder = (cols - (total % cols)) % cols
    for _ in range(remainder):
        html += "<div class='empty'></div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_array(rows, cols):
    # render as a neat grid with visible cells
    html = f"<div class='array-grid' style='display:grid; grid-template-columns: repeat({cols}, 34px); gap:6px;'>"
    for r in range(rows):
        for c in range(cols):
            html += "<div class='cell'><div class='block' style='width:28px; height:28px; margin:0'></div></div>"
    html += "</div>"
    # add small caption showing rows and cols
    html += f"<div class='small-muted' style='margin-top:8px'>배열: {rows}행 × {cols}열</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_division_groups(N, groups):
    q = N // groups
    r = N % groups
    html = "<div>"
    # render each equal group
    html += "<div style='display:flex; flex-wrap:wrap; gap:10px'>"
    for g in range(groups):
        html += "<div class='group-box'>"
        html += f"<div class='group-header'>그룹 {g+1}</div>"
        html += "<div style='display:grid; grid-template-columns:repeat(5,34px); gap:6px; justify-content:center'>"
        # blocks for this group
        for b in range(q):
            html += "<div class='block' title='블록'></div>"
        # if group empty, show placeholder
        if q == 0:
            html += "<div class='small-muted' style='padding:6px'>없음</div>"
        html += "</div>"
        html += f"<div class='group-label'>몫: {q}</div>"
        html += "</div>"
    html += "</div>"
    # render remainder if exists
    if r:
        html += "<div style='margin-top:12px'>"
        html += "<div class='group-header' style='color:#c0392b'>나머지</div>"
        html += "<div style='display:flex; gap:6px; margin-top:8px'>"
        for b in range(r):
            html += "<div class='block' style='background:linear-gradient(180deg,#ffb3a7,#f95e4f)'></div>"
        html += "</div></div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ------- 덧셈 탭 -------
with tabs[0]:
    st.subheader("덧셈: 블록으로 합을 확인해요")
    a = st.slider("a", 0, 20, 5)
    b = st.slider("b", 0, 20, 3)
    total = a + b
    st.markdown(f"<h1 style='font-size:44px'>{a} + {b} = {total}</h1>", unsafe_allow_html=True)
    render_blocks_grid(total, cols=10)


# ------- 곱셈 탭 -------
with tabs[1]:
    st.subheader("곱셈(배열): 가로×세로 배열로 이해해요")
    rows = st.slider("rows", 1, 10, 3)
    cols = st.slider("cols", 1, 10, 4)
    product = rows * cols
    st.markdown(f"<h1 style='font-size:44px'>{rows} × {cols} = {product}</h1>", unsafe_allow_html=True)
    render_array(rows, cols)


# ------- 나눗셈 탭 -------
with tabs[2]:
    st.subheader("나눗셈(같이 나누기): 같은 수로 나눠볼까요")
    N = st.slider("N (블록 수)", 1, 50, 20)
    groups = st.slider("groups (몇 명에게)", 1, 10, 4)
    q = N // groups
    r = N % groups
    st.markdown(f"<h1 style='font-size:44px'>{N} ÷ {groups} = {q} … {r}</h1>", unsafe_allow_html=True)
    if r != 0:
        st.warning("똑같이 나눌 수 없어요")
    render_division_groups(N, groups)
