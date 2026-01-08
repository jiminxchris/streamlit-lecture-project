
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 전문적인 페이지 레이아웃 및 스타일
st.set_page_config(
    page_title="수학 함수 그래프 & ε-δ 연속성 시각화",
    page_icon="📈",
    layout="wide",
)

st.markdown("""
<style>
.main {background-color: #f7f7fa;}
.stApp {font-family: 'Noto Sans KR', 'Roboto', Arial, sans-serif;}
.stTitle, .stHeader, .stMarkdown h2 {color: #1976d2;}
.stMarkdown code {background: #eaf1fb; color: #1a2b3c;}
.result-card {
  background: linear-gradient(90deg,#e3f2fd 60%,#fff 100%);
  border-radius: 12px;
  box-shadow: 0 2px 8px #b3c6e0;
  padding: 1.2em 1em;
  margin-bottom: 1em;
  border: 1px solid #bbdefb;
}
.graph-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px #b3c6e0;
  padding: 1.5em 1em;
  margin-bottom: 1.5em;
  border: 1px solid #e3f2fd;
}
/* 사이드바 기본(라이트 모드) 스타일 */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#ffffff 0%, #f7fbff 100%);
    color: #0f1724;
}
section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText {
    color: #0f1724;
}
section[data-testid="stSidebar"] .stButton>button, section[data-testid="stSidebar"] button {
    background-color: #f1f5f9;
    color: #0f1724;
    border: 1px solid rgba(16,24,40,0.06);
}
section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] textarea, section[data-testid="stSidebar"] .stNumberInput input {
    background: #ffffff;
    color: #0f1724;
    border: 1px solid rgba(16,24,40,0.06);
}
section[data-testid="stSidebar"] .stImage img {
    filter: none;
}
/* 사이드바 예시/도움말 (클래스 기반으로 다크/라이트 모드 전환 처리) */
.sidebar-examples {
    background: #e3f2fd;
    border-radius: 8px;
    padding: 0.7em 0.5em;
    margin-bottom: 1em;
}
.sidebar-examples .accent { color: #1976d2; }
.sidebar-help { font-size:0.95em; color: #333; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@media (prefers-color-scheme: dark) {
    .main { background-color: #06121a !important; }
    .stApp { font-family: 'Noto Sans KR', 'Roboto', Arial, sans-serif; color: #e6eef8; }
    .stTitle, .stHeader, .stMarkdown h2 { color: #90caf9 !important; }
    .stMarkdown, .stText, .stCodeBlock { color: #e6eef8 !important; }
    .stMarkdown code { background: #0f1724; color: #dbeafe; }
    .result-card {
        background: linear-gradient(90deg,#0b2b3a 60%,#071622 100%);
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.6);
        padding: 1.2em 1em;
        margin-bottom: 1em;
        border: 1px solid rgba(144,202,249,0.12);
        color: #e6eef8;
    }
    .graph-card {
        background: #071622;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.6);
        padding: 1.5em 1em;
        margin-bottom: 1.5em;
        border: 1px solid rgba(79,195,247,0.06);
        color: #e6eef8;
    }
    .result-card b, .graph-card h3 { color: #e3f2fd; }
    a, a:link, a:visited { color: #90caf9 !important; }
    /* 사이드바 스타일 조정 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#04202a 0%, #02121a 100%) !important;
        color: #e6eef8;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText {
        color: #e6eef8 !important;
    }
    section[data-testid="stSidebar"] .stButton>button, section[data-testid="stSidebar"] button {
        background-color: #083047 !important;
        color: #e6eef8 !important;
        border: 1px solid rgba(144,202,249,0.08) !important;
    }
    section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] textarea, section[data-testid="stSidebar"] .stNumberInput input {
        background: #071622 !important;
        color: #e6eef8 !important;
        border: 1px solid rgba(144,202,249,0.06) !important;
    }
    section[data-testid="stSidebar"] .stImage img {
        filter: brightness(1.1) contrast(1.05) !important;
    }
    /* 사이드바 내부 텍스트와 폼 컨트롤 가독성 보강 */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] .stHeader,
    section[data-testid="stSidebar"] .stRadio,
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stNumberInput,
    section[data-testid="stSidebar"] .stSlider,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .css-1hynsf2,
    section[data-testid="stSidebar"] .css-1y4p8pa {
        color: #e6eef8 !important;
    }
    /* 입력 필드, 텍스트박스, 숫자 입력의 배경/테두리 강조 */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] .stNumberInput input,
    section[data-testid="stSidebar"] .stTextInput input {
        background: #0b2b3a !important;
        color: #e6eef8 !important;
        border: 1px solid rgba(144,202,249,0.12) !important;
    }
    /* 버튼 스타일 명확화 */
    section[data-testid="stSidebar"] .stButton>button,
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] .stSelectbox>div {
        background-color: #083047 !important;
        color: #e6eef8 !important;
        border: 1px solid rgba(144,202,249,0.12) !important;
    }
    /* 선택된 옵션/토글 강조 */
    section[data-testid="stSidebar"] .stRadio input:checked + label,
    section[data-testid="stSidebar"] .stCheckbox input:checked + label {
        color: #bbdefb !important;
    }
    /* 사이드바 예시/도움말(다크모드 전용) 가시성 보강 */
    section[data-testid="stSidebar"] .sidebar-examples {
        background: linear-gradient(180deg, rgba(79,195,247,0.06), rgba(3,19,28,0.06)) !important;
        border-radius: 8px;
        padding: 0.7em 0.5em;
        margin-bottom: 1em;
        border: 1px solid rgba(144,202,249,0.06) !important;
        color: #e6eef8 !important;
    }
    section[data-testid="stSidebar"] .sidebar-examples .accent { color: #bbdefb !important; }
    section[data-testid="stSidebar"] .sidebar-examples span, 
    section[data-testid="stSidebar"] .sidebar-examples b {
        color: #e6eef8 !important;
    }
    section[data-testid="stSidebar"] .sidebar-help {
        color: #cfe8ff !important;
        font-size: 0.95em;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(90deg,#1976d2 60%,#fff 100%);border-radius:16px;padding:1.5em 1em;margin-bottom:1.5em;'>
<h1 style='color:#fff;font-weight:700;'>수학 함수 그래프 & ε-δ 연속성 시각화</h1>
<p style='color:#e3f2fd;font-size:1.1em;'>
이 페이지는 수학에서 자주 사용하는 주요 함수들의 그래프 개형과, <b>코시의 연속 정의(ε-δ)</b>를 시각적으로 탐구할 수 있도록 설계되었습니다.<br>
함수 종류를 선택하거나 직접 입력하면, 해당 함수의 그래프와 연속성(δ, ε)을 직관적으로 확인할 수 있습니다.<br>
함수의 정의역, 불연속점, 점근선, 치역 등도 자동으로 반영됩니다.
</p>
</div>
""", unsafe_allow_html=True)


# 주요 함수 종류별 대표 수식, 정의역, 그래프 스타일
func_types = {
    "상수함수 y=c": {"expr": "2", "domain": (-10, 10)},
    "일차함수 y=ax+b": {"expr": "x", "domain": (-10, 10)},
    "이차함수 y=ax^2+bx+c": {"expr": "x**2", "domain": (-10, 10)},
    "삼차함수 y=ax^3+...": {"expr": "x**3", "domain": (-10, 10)},
    "사차함수 y=ax^4+...": {"expr": "x**4", "domain": (-10, 10)},
    "유리함수 y=1/x": {"expr": "1/x", "domain": (-10, 10)},
    "무리함수 y=sqrt(x)": {"expr": "np.sqrt(x)", "domain": (0, 10)},
    "지수함수 y=exp(x)": {"expr": "np.exp(x)", "domain": (-3, 3)},
    "로그함수 y=log(x)": {"expr": "np.log(x)", "domain": (0.01, 10)},
    "사인함수 y=sin(x)": {"expr": "np.sin(x)", "domain": (-2*np.pi, 2*np.pi)},
    "코사인함수 y=cos(x)": {"expr": "np.cos(x)", "domain": (-2*np.pi, 2*np.pi)},
    "탄젠트함수 y=tan(x)": {"expr": "np.tan(x)", "domain": (-2*np.pi, 2*np.pi)},
    "절댓값함수 y=|x|": {"expr": "np.abs(x)", "domain": (-10, 10)},
    "계단함수 y=floor(x)": {"expr": "np.floor(x)", "domain": (-10, 10)},
    "가우스함수 y=exp(-x^2)": {"expr": "np.exp(-x**2)", "domain": (-4, 4)},
    "직접 입력": {"expr": None, "domain": (-10, 10)}
}

# 사이드바: 함수 선택 및 입력
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graph.png", width=64)
    st.header("함수 종류 및 입력")
    func_name = st.selectbox("함수 종류 선택", list(func_types.keys()))
    # n차 함수 계수 입력
    if func_name == "일차함수 y=ax+b":
        a_coef = st.number_input("a (일차항 계수)", value=1.0)
        b_coef = st.number_input("b (상수항)", value=0.0)
        func_str = f"{a_coef}*x + {b_coef}"
        domain = func_types[func_name]["domain"]
    elif func_name == "이차함수 y=ax^2+bx+c":
        a_coef = st.number_input("a (이차항 계수)", value=1.0)
        b_coef = st.number_input("b (일차항 계수)", value=0.0)
        c_coef = st.number_input("c (상수항)", value=0.0)
        func_str = f"{a_coef}*x**2 + {b_coef}*x + {c_coef}"
        domain = func_types[func_name]["domain"]
    elif func_name == "삼차함수 y=ax^3+...":
        a_coef = st.number_input("a (삼차항 계수)", value=1.0)
        b_coef = st.number_input("b (이차항 계수)", value=0.0)
        c_coef = st.number_input("c (일차항 계수)", value=0.0)
        d_coef = st.number_input("d (상수항)", value=0.0)
        func_str = f"{a_coef}*x**3 + {b_coef}*x**2 + {c_coef}*x + {d_coef}"
        domain = func_types[func_name]["domain"]
    elif func_name == "사차함수 y=ax^4+...":
        a_coef = st.number_input("a (사차항 계수)", value=1.0)
        b_coef = st.number_input("b (삼차항 계수)", value=0.0)
        c_coef = st.number_input("c (이차항 계수)", value=0.0)
        d_coef = st.number_input("d (일차항 계수)", value=0.0)
        e_coef = st.number_input("e (상수항)", value=0.0)
        func_str = f"{a_coef}*x**4 + {b_coef}*x**3 + {c_coef}*x**2 + {d_coef}*x + {e_coef}"
        domain = func_types[func_name]["domain"]
    elif func_types[func_name]["expr"] is None:
        func_str = st.text_input("함수 f(x) 직접 입력 (예: a*x**3 + b*x**2 + c*x + d)", value="a*x**2 + b*x + c")
        domain = st.slider("그래프 x축 범위", min_value=-20.0, max_value=20.0, value=(-10.0, 10.0), step=0.1)
        # 계수 자동 추출 및 입력 UI 생성
        import re
        coef_names = sorted(set(re.findall(r'([a-zA-Z])\*x', func_str)))
        coef_inputs = {}
        for coef in coef_names:
            coef_inputs[coef] = st.number_input(f"{coef} (계수)", value=1.0 if coef=='a' else 0.0)
        # 상수항 추출
        if 'c' in func_str and 'c' not in coef_names:
            coef_inputs['c'] = st.number_input("c (상수항)", value=0.0)
        # 함수식에 계수값 반영
        def user_func(x):
            local_dict = {**coef_inputs, 'x': x, 'np': np}
            try:
                return eval(func_str, local_dict)
            except Exception:
                return np.nan
        f = user_func
        st.markdown("""
        **계수의 역할:**
        - 최고차항: 그래프의 양 끝 방향과 폭 결정
        - 상수항: y절편(그래프의 상하 이동)
        - 중간항: 그래프의 굴곡, 극값, 변곡점 결정
        """)
    else:
        func_str = func_types[func_name]["expr"]
        domain = func_types[func_name]["domain"]
        def f(x):
            try:
                return eval(func_str, {"x": x, "np": np, "__builtins__": {}})
            except Exception:
                return np.nan
    st.markdown("""
    <div class='sidebar-examples'>
    <b>함수 예시</b><br>
    <span class='accent'>상수함수</span>: y=c<br>
    <span class='accent'>일차함수</span>: y=ax+b<br>
    <span class='accent'>이차함수</span>: y=ax²+bx+c<br>
    <span class='accent'>삼차/사차함수</span>: y=ax³+.../y=ax⁴+...<br>
    <span class='accent'>유리함수</span>: y=1/x<br>
    <span class='accent'>무리함수</span>: y=√x<br>
    <span class='accent'>지수/로그함수</span>: y=exp(x), y=log(x)<br>
    <span class='accent'>삼각함수</span>: y=sin(x), y=cos(x), y=tan(x)<br>
    <span class='accent'>절댓값/계단/가우스</span>: y=|x|, y=floor(x), y=exp(-x²)
    </div>
    <div class='sidebar-help'>
    <b>도움말</b><br>
    - 직접 입력 시 계수(a, b, c, ...)를 변수로 사용 가능<br>
    - δ, ε는 연속성의 수치적 의미를 시각적으로 보여줍니다<br>
    </div>
    """, unsafe_allow_html=True)


col1, col2 = st.columns([2,1])
with col2:
    st.subheader("연속성 판정 파라미터")
    a = st.slider("연속성 판정 점 a", min_value=float(domain[0]), max_value=float(domain[1]), value=float((domain[0]+domain[1])/2), step=0.1)
    epsilon = st.slider("ε 값 (양수)", min_value=0.001, max_value=2.0, value=0.1, step=0.001)

if func_types[func_name]["expr"] is not None and func_name not in ["직접 입력"]:
    def f(x):
        try:
            return eval(func_str, {"x": x, "np": np, "__builtins__": {}})
        except Exception:
            return np.nan

with col1:
    st.markdown("""
    <div class='graph-card'>
    <h3 style='color:#1976d2;'>함수 그래프 및 δ-ε 시각화</h3>
    <ul style='font-size:1.05em;'>
    <li><span style='color:#1976d2'>파란 곡선</span>: 함수 <b>f(x)</b>의 그래프</li>
    <li><span style='color:#ffd600'>노란 영역</span>: <b>|f(x)-f(a)|&lt;ε</b> 범위</li>
    <li><span style='color:#4fc3f7'>하늘색 영역</span>: <b>|x-a|&lt;δ</b> 범위</li>
    <li><span style='color:#d32f2f'>빨간 x</span>: 불연속점/정의불가</li>
    <li><span style='color:#388e3c'>초록선</span>: <b>f(a)</b>, <span style='color:#c62828'>빨간선</span>: <b>a</b></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    found_delta = None
    if st.button("그래프 그리기 및 δ-ε 시각화", key="draw_graph_delta_epsilon_1"):
        # 모든 ε에 대해 δ(최대 δ) 값 계산
        epsilons = np.linspace(0.01, 2.0, 30)
        deltas = []
        fa = f(a)
        for eps in epsilons:
            delta_candidates = np.linspace(eps/2, 2*eps, 500)
            found_delta = None
            for delta in delta_candidates:
                x_left = np.linspace(a-delta, a, 50)
                x_right = np.linspace(a, a+delta, 50)
                x_vals = np.concatenate([x_left, x_right])
                fx_vals = np.array([f(xi) for xi in x_vals])
                valid = np.isfinite(fx_vals)
                if np.all(valid) and np.all(np.abs(fx_vals[valid] - fa) < eps):
                    found_delta = delta
                    break
            deltas.append(found_delta if found_delta else np.nan)
        # 표로 δ-ε 관계 출력
        st.markdown("<div class='result-card'><b>ε-δ 관계표</b></div>", unsafe_allow_html=True)
        st.dataframe({"ε": epsilons, "δ(최대)": deltas})

        # 선택한 ε에 대한 δ 및 그래프 시각화
        delta_candidates = np.linspace(epsilon/2, 2*epsilon, 500)
        found_delta = None
        for delta in delta_candidates:
            x_left = np.linspace(a-delta, a, 50)
            x_right = np.linspace(a, a+delta, 50)
            x_vals = np.concatenate([x_left, x_right])
            fx_vals = np.array([f(xi) for xi in x_vals])
            valid = np.isfinite(fx_vals)
            if np.all(valid) and np.all(np.abs(fx_vals[valid] - fa) < epsilon):
                found_delta = delta
                break
        x_plot = np.linspace(domain[0], domain[1], 1200)
        def safe_f(xx):
            try:
                vals = np.array([f(xi) for xi in xx])
            except Exception:
                vals = np.full_like(xx, np.nan)
            return vals
        y_plot = safe_f(x_plot)
        mask = np.isfinite(y_plot)
        # 테마 기반 색상 설정
        try:
            theme = st.get_option("theme.base")
        except Exception:
            theme = None
        if theme == "dark":
            LINE_COLOR = '#90caf9'
            EPS_FILL = '#3a5566'
            DELTA_FILL = '#083047'
            DISC_COLOR = '#ff8a80'
            A_LINE_COLOR = '#ff5252'
            FA_LINE_COLOR = '#66bb6a'
        else:
            LINE_COLOR = '#1976d2'
            EPS_FILL = '#fffde7'
            DELTA_FILL = '#b3e5fc'
            DISC_COLOR = '#d32f2f'
            A_LINE_COLOR = '#c62828'
            FA_LINE_COLOR = '#388e3c'
        fig, ax = plt.subplots(figsize=(9,5))
        ax.plot(x_plot[mask], y_plot[mask], label="$f(x)$", color=LINE_COLOR, linewidth=2)
        if not np.all(mask):
            ax.scatter(x_plot[~mask], np.full(np.sum(~mask), 0), color=DISC_COLOR, marker='x', label='불연속/정의불가')
        ax.axvline(a, color=A_LINE_COLOR, linestyle='--', label='$a$', linewidth=2)
        ax.axhline(fa, color=FA_LINE_COLOR, linestyle='--', label='$f(a)$', linewidth=2)
        ax.fill_between(x_plot, fa-epsilon, fa+epsilon, color=EPS_FILL, alpha=0.5, label='$|f(x)-f(a)|<\\epsilon$')
        # δ 범위
        if found_delta:
            ax.axvspan(a-found_delta, a+found_delta, color=DELTA_FILL, alpha=0.4, label='$|x-a|<\\delta$')
            st.markdown(f"<div class='result-card'><b>적당한 δ 값:</b> {found_delta:.6f}<br>모든 x∈({a-found_delta:.3f}, {a+found_delta:.3f})에서 |f(x)-f(a)|&lt;{epsilon} 입니다.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-card' style='background:#ffebee;border-color:#ffcdd2;color:#c62828;'><b>해당 ε에 대해 δ를 찾을 수 없습니다.<br>함수 또는 입력값을 확인하세요.</b></div>", unsafe_allow_html=True)
        found_delta = None
    if st.button("그래프 그리기 및 δ-ε 시각화", key="draw_graph_delta_epsilon_2"):
            # 모든 ε에 대해 δ(최대 δ) 값 계산
            epsilons = np.linspace(0.01, 2.0, 30)
            deltas = []
            fa = f(a)
            for eps in epsilons:
                delta_candidates = np.linspace(eps/2, 2*eps, 500)
                found_delta = None
                for delta in delta_candidates:
                    x_left = np.linspace(a-delta, a, 50)
                    x_right = np.linspace(a, a+delta, 50)
                    x_vals = np.concatenate([x_left, x_right])
                    fx_vals = np.array([f(xi) for xi in x_vals])
                    valid = np.isfinite(fx_vals)
                    if np.all(valid) and np.all(np.abs(fx_vals[valid] - fa) < eps):
                        found_delta = delta
                        break
                deltas.append(found_delta if found_delta else np.nan)
            # 표로 δ-ε 관계 출력
            st.markdown("<div class='result-card'><b>ε-δ 관계표</b></div>", unsafe_allow_html=True)
            st.dataframe({"ε": epsilons, "δ(최대)": deltas})

            # 선택한 ε에 대한 δ 및 그래프 시각화
            delta_candidates = np.linspace(epsilon/2, 2*epsilon, 500)
            found_delta = None
            for delta in delta_candidates:
                x_left = np.linspace(a-delta, a, 50)
                x_right = np.linspace(a, a+delta, 50)
                x_vals = np.concatenate([x_left, x_right])
                fx_vals = np.array([f(xi) for xi in x_vals])
                valid = np.isfinite(fx_vals)
                if np.all(valid) and np.all(np.abs(fx_vals[valid] - fa) < epsilon):
                    found_delta = delta
                    break
            x_plot = np.linspace(domain[0], domain[1], 1200)
            def safe_f(xx):
                try:
                    vals = np.array([f(xi) for xi in xx])
                except Exception:
                    vals = np.full_like(xx, np.nan)
                return vals
            y_plot = safe_f(x_plot)
            mask = np.isfinite(y_plot)
            fig, ax = plt.subplots(figsize=(9,5))
            ax.plot(x_plot[mask], y_plot[mask], label="$f(x)$", color='#1976d2', linewidth=2)
            if not np.all(mask):
                ax.scatter(x_plot[~mask], np.full(np.sum(~mask), 0), color='#d32f2f', marker='x', label='불연속/정의불가')
            ax.axvline(a, color='#c62828', linestyle='--', label='$a$', linewidth=2)
            ax.axhline(fa, color='#388e3c', linestyle='--', label='$f(a)$', linewidth=2)
            ax.fill_between(x_plot, fa-epsilon, fa+epsilon, color='#fffde7', alpha=0.5, label='$|f(x)-f(a)|<\epsilon$')
            if found_delta:
                ax.axvspan(a-found_delta, a+found_delta, color='#b3e5fc', alpha=0.4, label='$|x-a|<\delta$')
                st.markdown(f"<div class='result-card'><b>적당한 δ 값:</b> {found_delta:.6f}<br>모든 x∈({a-found_delta:.3f}, {a+found_delta:.3f})에서 |f(x)-f(a)|&lt;{epsilon} 입니다.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='result-card' style='background:#ffebee;border-color:#ffcdd2;color:#c62828;'><b>해당 ε에 대해 δ를 찾을 수 없습니다.<br>함수 또는 입력값을 확인하세요.</b></div>", unsafe_allow_html=True)
            ax.set_xlabel('x', fontsize=13)
            ax.set_ylabel('f(x)', fontsize=13)
            if np.any(mask):
                y_min, y_max = np.nanmin(y_plot[mask]), np.nanmax(y_plot[mask])
                if y_max-y_min < 1e-6:
                    ax.set_ylim(fa-1, fa+1)
                else:
                    ax.set_ylim(y_min-(y_max-y_min)*0.2, y_max+(y_max-y_min)*0.2)
            ax.legend(fontsize=12, loc='best')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

            if found_delta:
                st.markdown(f"<div class='result-card'><b>함수는 x={a}에서 ε={epsilon}에 대해 연속입니다.</b></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='result-card' style='background:#ffebee;border-color:#ffcdd2;color:#c62828;'><b>함수는 x={a}에서 ε={epsilon}에 대해 연속이 아닐 수 있습니다.</b></div>", unsafe_allow_html=True)