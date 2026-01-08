# streamlit-math-input 라이브러리에서 수식 입력 위젯을 가져옵니다.
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sympy import sympify, symbols, SympifyError
import re  # 문자열 처리를 위한 정규식 라이브러리
import os
import matplotlib.font_manager as fm

# --- 한글 폰트 설정 (루트 fonts/NanumGothic-Regular.ttf 고정) ---
@st.cache_data
def load_korean_font():
    font_path = os.path.join(os.getcwd(), "fonts", "NanumGothic-Regular.ttf")
    if not os.path.exists(font_path):
        st.warning(f"⚠️ 폰트 파일을 찾을 수 없습니다: {font_path}")
        return

    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False
    return font_name

# 폰트 로드
load_korean_font()

def parse_latex_to_sympy(latex_str: str) -> str:
    """
    LaTeX 형식의 문자열을 SymPy가 이해할 수 있는 파이썬 문자열로 변환합니다.
    예: "2n+n^{2}" -> "2*n+n**2"
    """
    # 거듭제곱 변환: n^{...} -> n**(...) or n^... -> n**...
    parsed_str = latex_str.replace('^', '**')
    parsed_str = parsed_str.replace('{', '(').replace('}', ')')
    
    # \frac{a}{b} 형태의 분수 변환
    parsed_str = re.sub(r'\\frac\((.*?)\)\((.*?)\)', r'(\1)/(\2)', parsed_str)

    # 숨겨진 곱셈기호 추가: 2n -> 2*n, (n)(n+1) -> (n)*(n+1)
    parsed_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', parsed_str)  # 숫자와 문자 사이
    parsed_str = re.sub(r'(\))([a-zA-Z\(])', r'\1*\2', parsed_str)  # 괄호와 문자/괄호 사이
    
    return parsed_str

def display_results(terms_list):
    """계산된 수열의 항들과 그래프를 화면에 출력하는 함수"""
    if not terms_list:
        st.warning("계산된 수열이 없습니다.")
        return

    st.subheader("🔢 수열의 항")
    # 한 줄에 4개씩 항을 보여주기 위해 컬럼 사용
    cols = st.columns(4)
    for i, term in enumerate(terms_list):
        with cols[i % 4]:
            st.latex(f"a_{{{i+1}}} = {term}")

    st.subheader("📈 수열 그래프")
    
    # 데이터프레임 생성
    n_values = list(range(1, len(terms_list) + 1))
    df = pd.DataFrame({
        '항 (n)': n_values,
        '값 (a_n)': terms_list
    })

    # Matplotlib을 사용한 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['항 (n)'], df['값 (a_n)'], marker='o', linestyle='-', color='b')
    ax.set_title('수열의 시각화', fontsize=16)
    ax.set_xlabel('항 (n)', fontsize=12)
    ax.set_ylabel('값 (a_n)', fontsize=12)
    ax.grid(True)
    ax.set_xticks(n_values)  # x축 눈금을 정수로 표시

    st.pyplot(fig)


# --- Streamlit 앱 UI ---
st.title("수열 학습 웹 애플리케이션 (수식 입력 개선)")
st.write("일반항 또는 점화식을 입력하여 수열의 항과 그래프를 확인해 보세요.")

tab1, tab2 = st.tabs(["일반항으로 계산하기", "점화식으로 계산하기"])

# --- 일반항 탭 ---
with tab1:
    st.header("일반항 ($a_n$)으로 수열 만들기")
    
    # 일반항 입력
    general_term_latex = st.text_input(
        "일반항을 LaTeX 수식으로 입력하세요.",
        key="general_term_latex"
    )
    
    num_terms_general = st.number_input(
        "몇 번째 항까지 구할까요?",
        min_value=1,
        max_value=100,
        value=10,
        key="num_general"
    )

    if st.button("일반항으로 계산", key="btn_general"):
        if general_term_latex:
            try:
                # LaTeX 수식을 SymPy가 계산 가능한 형태로 변환
                general_term_sympy = parse_latex_to_sympy(general_term_latex)
                st.info(f"입력된 수식: `{general_term_latex}` → 변환된 식: `{general_term_sympy}`")

                n = symbols('n')
                expr = sympify(general_term_sympy)
                
                if not expr.has(n):
                    st.error("입력하신 일반항에 변수 'n'이 포함되어 있는지 확인해 주세요.")
                else:
                    sequence = [float(expr.subs(n, i)) for i in range(1, num_terms_general + 1)]
                    display_results(sequence)

            except Exception as e:
                st.error(f"수식 오류: 올바른 형식인지 확인해 주세요. (오류: {e})")
        else:
            st.warning("일반항을 입력해 주세요.")


# --- 점화식 탭 ---
with tab2:
    st.header("점화식으로 수열 만들기")
    st.info("이전 항을 변수 $p$ 로 사용해 주세요. (예: $p+3$, $2p$)")

    col1, col2 = st.columns(2)
    with col1:
        first_term_input = st.number_input(
            "첫째항 $a_1$의 값을 입력하세요.",
            value=1.0,
            format="%.2f"
        )
    with col2:
        num_terms_recurrence = st.number_input(
            "몇 번째 항까지 구할까요?",
            min_value=2,
            max_value=100,
            value=10,
            key="num_recurrence"
        )
    
        recurrence_relation_latex = st.text_input(
            "점화식을 LaTeX 수식으로 입력하세요.",
            key="recurrence_relation_latex"
        )

    if st.button("점화식으로 계산", key="btn_recurrence"):
        if recurrence_relation_latex:
            try:
                # LaTeX 수식을 SymPy가 계산 가능한 형태로 변환
                recurrence_relation_sympy = parse_latex_to_sympy(recurrence_relation_latex)
                recurrence_relation_sympy = recurrence_relation_sympy.replace('p', 'a_prev')
                st.info(f"입력된 수식: `{recurrence_relation_latex}` → 변환된 식: `{recurrence_relation_sympy}`")

                a_prev = symbols('a_prev')
                expr = sympify(recurrence_relation_sympy)
                
                if not expr.has(a_prev):
                    st.error("입력하신 점화식에 이전 항 변수 'p'가 포함되어 있는지 확인해 주세요.")
                else:
                    sequence = [first_term_input]
                    current_val = first_term_input
                    
                    for i in range(2, num_terms_recurrence + 1):
                        current_val = expr.subs(a_prev, current_val)
                        sequence.append(float(current_val))
                    
                    display_results(sequence)

            except Exception as e:
                st.error(f"수식 오류: 올바른 형식인지 확인해 주세요. (오류: {e})")
        else:
            st.warning("점화식을 입력해 주세요.")
