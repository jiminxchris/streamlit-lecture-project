import streamlit as st
import random
import math

# ----------------------------------------------------
# 0. 데이터 및 상수 정의
# ----------------------------------------------------

COLOR_CODES = {
    "Black": {"digit": 0, "multiplier": 1e0, "tolerance": None, "temp_coeff": None, "hex": "#000000"},
    "Brown": {"digit": 1, "multiplier": 1e1, "tolerance": 0.01, "temp_coeff": 100, "hex": "#8B4513"},
    "Red": {"digit": 2, "multiplier": 1e2, "tolerance": 0.02, "temp_coeff": 50, "hex": "#FF0000"},
    "Orange": {"digit": 3, "multiplier": 1e3, "tolerance": None, "temp_coeff": 15, "hex": "#FFA500"},
    "Yellow": {"digit": 4, "multiplier": 1e4, "tolerance": None, "temp_coeff": 25, "hex": "#FFFF00"},
    "Green": {"digit": 5, "multiplier": 1e5, "tolerance": 0.005, "temp_coeff": None, "hex": "#008000"},
    "Blue": {"digit": 6, "multiplier": 1e6, "tolerance": 0.0025, "temp_coeff": 10, "hex": "#0000FF"},
    "Violet": {"digit": 7, "multiplier": 1e7, "tolerance": 0.001, "temp_coeff": 5, "hex": "#EE82EE"},
    "Grey": {"digit": 8, "multiplier": 1e8, "tolerance": 0.0005, "temp_coeff": None, "hex": "#808080"},
    "White": {"digit": 9, "multiplier": 1e9, "tolerance": None, "temp_coeff": None, "hex": "#FFFFFF"},
    "Gold": {"digit": None, "multiplier": 1e-1, "tolerance": 0.05, "temp_coeff": None, "hex": "#FFD700"},
    "Silver": {"digit": None, "multiplier": 1e-2, "tolerance": 0.10, "temp_coeff": None, "hex": "#C0C0C0"},
    "None": {"digit": None, "multiplier": None, "tolerance": 0.20, "temp_coeff": None, "hex": "#FFFFFF00"} # 4색띠 전용 (투명 처리)
}

# 4색띠와 5색띠에서 사용 가능한 색상 목록을 분리
DIGIT_COLORS = ["Black", "Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "Grey", "White"]
MULTIPLIER_COLORS = ["Black", "Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "Gold", "Silver"]
TOLERANCE_COLORS = ["Brown", "Red", "Green", "Blue", "Violet", "Gold", "Silver", "None"]

# ----------------------------------------------------
# 1. 계산 함수 정의
# ----------------------------------------------------

def calculate_resistance(colors, band_count):
    """선택된 색상으로 저항값을 계산합니다. (반환값: res_str, tol_str, range_str)"""
    try:
        if band_count == 4:
            # 1, 2번째 띠: 숫자, 3번째 띠: 승수, 4번째 띠: 허용 오차
            digit1 = COLOR_CODES[colors[0]]["digit"]
            digit2 = COLOR_CODES[colors[1]]["digit"]
            multiplier = COLOR_CODES[colors[2]]["multiplier"]
            tolerance = COLOR_CODES[colors[3]]["tolerance"]

            # 첫 번째 띠는 Black(0)이 될 수 없습니다. (저항 표기법)
            if digit1 is None or digit2 is None or multiplier is None or digit1 == 0:
                return "오류: 잘못된 색상 조합입니다.", None, None

            value = (digit1 * 10 + digit2) * multiplier

        elif band_count == 5:
            # 1, 2, 3번째 띠: 숫자, 4번째 띠: 승수, 5번째 띠: 허용 오차
            digit1 = COLOR_CODES[colors[0]]["digit"]
            digit2 = COLOR_CODES[colors[1]]["digit"]
            digit3 = COLOR_CODES[colors[2]]["digit"]
            multiplier = COLOR_CODES[colors[3]]["multiplier"]
            tolerance = COLOR_CODES[colors[4]]["tolerance"]

            # 첫 번째 띠는 Black(0)이 될 수 없습니다.
            if digit1 is None or digit2 is None or digit3 is None or multiplier is None or digit1 == 0:
                return "오류: 잘못된 색상 조합입니다.", None, None

            value = (digit1 * 100 + digit2 * 10 + digit3) * multiplier
        
        else:
            return "오류: 띠 개수가 유효하지 않습니다.", None, None

        # 단위 변환 함수 (Ω, kΩ, MΩ)
        if value >= 1e6:
            res_str = f"{value / 1e6:.2f} MΩ"
        elif value >= 1e3:
            res_str = f"{value / 1e3:.2f} kΩ"
        else:
            res_str = f"{value:.2f} Ω"

        # 허용 오차 문자열
        if tolerance is not None:
            tol_str = f"±{tolerance * 100:.2g}%"
            range_min = value * (1 - tolerance)
            range_max = value * (1 + tolerance)
            range_str = "" # 퀴즈에서 오차 범위 문자열은 제거
        else:
            tol_str = "허용 오차 없음"
            range_str = ""

        return res_str, tol_str, range_str

    except Exception as e:
        return f"계산 오류: {e}", None, None

# ----------------------------------------------------
# 2. Streamlit 레이아웃 및 탭 정의
# ----------------------------------------------------

st.set_page_config(layout="wide", page_title="저항 컬러 코드 마스터")

st.title("💡 저항 컬러 코드 마스터")
st.caption("공업계 특성화고 학생들을 위한 4색/5색띠 저항 학습 및 실습 앱")

tab1, tab2, tab3 = st.tabs(["1. 학습 (이론)", "2. 실습 (계산기)", "3. 퀴즈 (평가)"])

# ----------------------------------------------------
# 탭 1: 학습 모듈 (이론)
# ----------------------------------------------------

with tab1:
    st.header("1단계: 저항 컬러 코드 이론 학습")
    
    st.subheader("색상 코드표")
    # 필요한 정보만 추출하여 데이터프레임으로 표시
    data = []
    for color, info in COLOR_CODES.items():
        if color == "None": continue
        data.append({
            "색상": color,
            "1,2,3번째 띠 (숫자)": info['digit'] if info['digit'] is not None else '-',
            "승수 (Multiplier)": f"x {info['multiplier']}" if info['multiplier'] is not None else '-',
            "허용 오차 (Tolerance)": f"±{info['tolerance']*100:.2g}%" if info['tolerance'] else '-'
        })
    st.dataframe(data, hide_index=True, use_container_width=True)

    st.subheader("4색띠와 5색띠의 구조")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**4색띠 저항**")
        st.markdown(
            """
            1. **첫 번째 띠:** 첫 번째 유효 숫자
            2. **두 번째 띠:** 두 번째 유효 숫자
            3. **세 번째 띠 (승수):** 저항값에 곱하는 값 (10의 거듭제곱)
            4. **네 번째 띠 (허용 오차):** 실제 저항값이 공칭값으로부터 벗어날 수 있는 오차 범위
            """
        )
        # 

    with col2:
        st.markdown("**5색띠 저항**")
        st.markdown(
            """
            1. **첫 번째 띠:** 첫 번째 유효 숫자
            2. **두 번째 띠:** 두 번째 유효 숫자
            3. **세 번째 띠:** 세 번째 유효 숫자
            4. **네 번째 띠 (승수):** 저항값에 곱하는 값 (10의 거듭제곱)
            5. **다섯 번째 띠 (허용 오차):** 실제 저항값이 공칭값으로부터 벗어날 수 있는 오차 범위 (더 정밀함)
            """
        )
        # 

    st.subheader("저항값 계산 공식")
    st.latex(r'''
    R_{\text{4-band}} = (D_1 \times 10 + D_2) \times M \pm T
    ''')
    st.latex(r'''
    R_{\text{5-band}} = (D_1 \times 100 + D_2 \times 10 + D_3) \times M \pm T
    ''')
    st.markdown("* $D$: 숫자 띠(Digit), $M$: 승수(Multiplier), $T$: 허용 오차(Tolerance)")

# ----------------------------------------------------
# 탭 2: 실습 모듈 (계산 시뮬레이터)
# ----------------------------------------------------

with tab2:
    st.header("2단계: 저항값 계산 시뮬레이터")
    
    band_type = st.radio("저항 띠 종류 선택", ["4색띠 저항", "5색띠 저항"], horizontal=True)
    band_count = 4 if band_type == "4색띠 저항" else 5
    
    st.subheader("색상 선택")
    
    # 선택된 색상을 저장할 딕셔너리 초기화
    selected_colors = {}
    
    cols = st.columns(band_count)
    
    for i in range(band_count):
        with cols[i]:
            if i < band_count - 2: # 1, 2, 3번째 띠 (4색띠의 경우 1, 2번째)
                label = f"띠 {i+1} (숫자)"
                options = DIGIT_COLORS
            elif i == band_count - 2: # 승수 띠 (4색띠의 3번째, 5색띠의 4번째)
                label = f"띠 {i+1} (승수)"
                options = MULTIPLIER_COLORS
            else: # 허용 오차 띠 (4색띠의 4번째, 5색띠의 5번째)
                label = f"띠 {i+1} (허용 오차)"
                options = TOLERANCE_COLORS
            
            # None 색상 처리 (4색띠 마지막 띠의 ±20%)
            default_color = "Brown" if i == 0 else "Black"
            if band_type == "4색띠 저항" and i == 3:
                options = ["Gold", "Silver", "None", "Brown", "Red", "Green", "Blue", "Violet"] # 주로 사용되는 오차부터 배치
                default_color = "Gold" if "Gold" in options else options[0]
            elif default_color not in options:
                default_color = options[0]
            
            color_key = f'band_{i+1}'
            selected_colors[color_key] = st.selectbox(label, options, index=options.index(default_color), key=color_key)
            
    # 저항 시각화를 위한 HTML/CSS
    resistor_bands_html = []
    for i, color_name in enumerate(selected_colors.values()):
        hex_color = COLOR_CODES[color_name]["hex"]
        band_class = ""
        # 4색띠의 3번째 띠 (승수)와 4번째 띠 (허용 오차) 사이에 간격
        if band_count == 4 and i == 2: # 0-indexed: 2는 3번째 띠 (multiplier)
            band_class = "band-spacing-4"
        # 5색띠의 4번째 띠 (승수)와 5번째 띠 (허용 오차) 사이에 간격
        elif band_count == 5 and i == 3: # 0-indexed: 3은 4번째 띠 (multiplier)
            band_class = "band-spacing-5"
        
        resistor_bands_html.append(f'<div class="resistor-band {band_class}" style="background-color: {hex_color};"></div>')

    resistor_full_html = f"""
    <style>
    .resistor-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin: 30px 0;
    }}
    .resistor-lead {{
        width: 50px; /* 리드의 길이 */
        height: 2px;
        background-color: #A0A0A0; /* 금속 리드 색상 */
        border-radius: 1px;
    }}
    .resistor-body-actual {{
        display: flex;
        align-items: center;
        justify-content: flex-start; /* 띠를 왼쪽부터 정렬 */
        min-width: 150px; /* 저항 몸통 최소 너비 */
        height: 40px;
        background-color: #d1b281; /* 저항 몸체 색상 (베이지/황갈색) */
        border-radius: 10px;
        padding: 0 10px; /* 띠와 몸체 끝 사이 여백 */
        box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.3);
        position: relative; /* 띠 위치 지정을 위해 */
    }}
    .resistor-band {{
        width: 8px; /* 띠의 너비 */
        height: 35px; /* 띠의 높이 */
        border-radius: 2px;
        margin: 0 3px; /* 띠들 사이의 간격 */
        border: 1px solid rgba(0,0,0,0.1);
    }}
    /* 허용 오차 띠 앞의 추가 간격 */
    .band-spacing-4 {{
        margin-right: 15px !important; /* 4색띠의 3번 띠 후 간격 */
    }}
    .band-spacing-5 {{
        margin-right: 15px !important; /* 5색띠의 4번 띠 후 간격 */
    }}
    </style>

    <div class="resistor-container">
        <div class="resistor-lead"></div>
        <div class="resistor-body-actual">
            {''.join(resistor_bands_html)}
        </div>
        <div class="resistor-lead"></div>
    </div>
    """
    
    st.markdown(resistor_full_html, unsafe_allow_html=True)

    # 계산 결과 표시
    colors_list = list(selected_colors.values())
    res_str, tol_str, range_str_dummy = calculate_resistance(colors_list, band_count) # range_str은 여기서 사용 안 함

    st.subheader("계산 결과")
    if res_str.startswith("오류"):
        st.error(res_str)
    else:
        # 탭2의 range_str 다시 사용하도록 수정
        tolerance_val = COLOR_CODES[colors_list[-1]].get('tolerance')
        range_str_display = ""
        if tolerance_val is not None and not res_str.startswith("오류"):
            value_str, unit_str = res_str.split()
            value = float(value_str)
            if 'MΩ' in unit_str:
                value *= 1e6
            elif 'kΩ' in unit_str:
                value *= 1e3
            
            range_min = value * (1 - tolerance_val)
            range_max = value * (1 + tolerance_val)

            def format_range_value(val):
                if val >= 1e6:
                    return f"{val / 1e6:.2g} MΩ"
                elif val >= 1e3:
                    return f"{val / 1e3:.2g} kΩ"
                else:
                    return f"{val:.2g} Ω"

            range_str_display = f"({format_range_value(range_min)} ~ {format_range_value(range_max)})"
        
        st.success(f"**저항값 (공칭값):** {res_str}")
        st.info(f"**허용 오차:** {tol_str} {range_str_display}")


# ----------------------------------------------------
# 탭 3: 퀴즈 모듈 (평가) - 폭죽(confetti) 추가됨
# ----------------------------------------------------

def format_ohm_value(value):
    """Ω 값을 읽기 쉬운 단위 (Ω, kΩ, MΩ)로 변환하고 문자열로 반환합니다."""
    if value >= 1e6:
        return f"{value / 1e6:.2f} MΩ"
    elif value >= 1e3:
        return f"{value / 1e3:.2f} kΩ"
    else:
        return f"{value:.2f} Ω"

def get_ohm_value(res_str):
    """저항값 문자열을 Ω 단위 실수 값으로 변환합니다."""
    try:
        value_str, unit_str = res_str.split()
        value = float(value_str)
        if 'MΩ' in unit_str:
            value *= 1e6
        elif 'kΩ' in unit_str:
            value *= 1e3
        return value
    except:
        return None

def generate_quiz_problem(band_count, num_options=4):
    """퀴즈 문제(색상 -> 저항값)를 생성합니다. (오류 처리 강화)"""
    
    while True:
        colors = []
        
        colors.append(random.choice([c for c in DIGIT_COLORS if COLOR_CODES[c]['digit'] != 0]))
        for _ in range(band_count - 3):
             colors.append(random.choice(DIGIT_COLORS))
            
        colors.append(random.choice([c for c in MULTIPLIER_COLORS if c not in ["Gold", "Silver"]]))
        
        colors.append(random.choice([c for c in TOLERANCE_COLORS if c != "None"]))
        
        res_str, tol_str, _ = calculate_resistance(colors, band_count)
        
        if not res_str.startswith("오류") and tol_str is not None:
            break

    correct_answer = f"{res_str} {tol_str}"
    correct_value_ohm = get_ohm_value(res_str)
    
    options = {correct_answer}
    while len(options) < num_options:
        
        wrong_tolerance_color = random.choice([t for t in TOLERANCE_COLORS if t != colors[-1] and COLOR_CODES[t]['tolerance'] is not None])
        wrong_tol_str = f"±{COLOR_CODES[wrong_tolerance_color]['tolerance'] * 100:.2g}%"
        options.add(f"{res_str} {wrong_tol_str}")

        wrong_value_ohm = correct_value_ohm * random.choice([0.1, 10])
        if correct_value_ohm > 10:
             wrong_value_ohm = correct_value_ohm + random.randint(1, 9) * 10**(math.floor(math.log10(correct_value_ohm)) - 1)

        wrong_res_str = format_ohm_value(wrong_value_ohm)
        options.add(f"{wrong_res_str} {tol_str}")
            
    options = list(options)[:num_options]
    random.shuffle(options)
    
    return {
        "band_count": band_count,
        "colors": colors,
        "question": f"다음 {band_count}색띠 저항의 저항값과 허용 오차는 얼마입니까?",
        "correct_answer": correct_answer,
        "options": options
    }

def display_quiz_resistor(colors, band_count):
    """퀴즈에 사용할 저항 그림을 표시합니다."""
    quiz_bands_html = []
    for i, color_name in enumerate(colors):
        hex_color = COLOR_CODES[color_name]["hex"]
        band_class = ""
        if band_count == 4 and i == 2: 
            band_class = "band-spacing-4"
        elif band_count == 5 and i == 3:
            band_class = "band-spacing-5"
        
        quiz_bands_html.append(f'<div class="resistor-band {band_class}" style="background-color: {hex_color};"></div>')
            
    quiz_resistor_full_html = f"""
    <div class="resistor-container">
        <div class="resistor-lead"></div>
        <div class="resistor-body-actual">
            {''.join(quiz_bands_html)}
        </div>
        <div class="resistor-lead"></div>
    </div>
    """
    st.markdown(quiz_resistor_full_html, unsafe_allow_html=True)
    
    
def next_quiz_problem():
    """다음 퀴즈 문제를 생성하고 세션 상태를 업데이트합니다."""
    if "초급" in st.session_state.quiz_level:
        band_count = 4
    elif "중급" in st.session_state.quiz_level:
        band_count = random.choice([4, 5])
    else: 
        band_count = 5

    st.session_state.current_quiz = generate_quiz_problem(band_count)
    st.session_state.quiz_submitted = False
    st.session_state.user_answer = None
    st.session_state.quiz_feedback = None # 다음 문제로 넘어갈 때 피드백 상태 초기화!

def check_quiz_answer(user_selection):
    """사용자 답을 체크합니다."""
    st.session_state.quiz_submitted = True
    st.session_state.user_answer = user_selection
    
    st.session_state.total_count += 1
    
    # 정답/오답 여부를 세션 상태에 저장하여 UI에서 사용하도록 변경
    if user_selection == st.session_state.current_quiz['correct_answer']:
        st.session_state.score += 1
        st.session_state.correct_count += 1
        st.session_state.quiz_feedback = "correct"
        st.balloons() # 🎉 정답 시 폭죽 효과 추가
    else:
        st.session_state.quiz_feedback = "wrong"
    
def start_quiz():
    """퀴즈를 시작합니다."""
    st.session_state.quiz_active = True
    st.session_state.score = 0
    st.session_state.correct_count = 0
    st.session_state.total_count = 0
    st.session_state.quiz_feedback = None # 퀴즈 시작 시 피드백 초기화
    next_quiz_problem() # 첫 문제 생성

with tab3:
    st.header("3단계: 저항 컬러 코드 퀴즈")
    
    if 'quiz_active' not in st.session_state:
        st.session_state.quiz_active = False
        st.session_state.quiz_level = "초급 (4색띠)"
        st.session_state.score = 0
        st.session_state.total_count = 0
        st.session_state.correct_count = 0
        st.session_state.current_quiz = None
        st.session_state.quiz_submitted = False
        st.session_state.user_answer = None
        st.session_state.quiz_feedback = None # 피드백 상태 추가

    if st.session_state.quiz_active:
        st.subheader(f"총점: {st.session_state.correct_count} / {st.session_state.total_count} 문제")
        
        quiz_data = st.session_state.current_quiz
        
        st.markdown("---")
        # 현재 문제 번호 계산: 이미 제출한 문제 개수 + 1
        current_problem_num = st.session_state.total_count + (0 if st.session_state.quiz_submitted else 1)
        st.markdown(f"**{current_problem_num}번 문제 (난이도: {st.session_state.quiz_level.split(' ')[0]})**")
        
        display_quiz_resistor(quiz_data['colors'], quiz_data['band_count'])
        
        st.markdown(quiz_data['question'])

        default_index = quiz_data['options'].index(st.session_state.user_answer) if st.session_state.user_answer in quiz_data['options'] else 0

        user_selection = st.radio("정답을 고르세요:", quiz_data['options'], index=default_index, key="quiz_options", disabled=st.session_state.quiz_submitted)
        
        # 퀴즈 제출 후 결과 피드백을 탭3 내에 명확히 표시
        if st.session_state.quiz_submitted:
            if st.session_state.quiz_feedback == "correct":
                st.success("✅ 정답입니다! 축하합니다!")
            elif st.session_state.quiz_feedback == "wrong":
                st.error(f"❌ 오답입니다. 정답은: **{st.session_state.current_quiz['correct_answer']}**")


        col_quiz1, col_quiz2 = st.columns(2)
        
        with col_quiz1:
            if not st.session_state.quiz_submitted:
                # 제출 전: 선택된 답으로 체크 함수 호출
                # st.radio의 반환 값(user_selection)을 on_click에서 사용하기 위해 args에 전달
                st.button("답안 제출", on_click=check_quiz_answer, args=(user_selection,), use_container_width=True)
            else:
                # 제출 후: 다음 문제 버튼 활성화
                st.button("다음 문제", on_click=next_quiz_problem, use_container_width=True)
        
        with col_quiz2:
             st.button("퀴즈 종료", on_click=lambda: st.session_state.update(quiz_active=False), use_container_width=True)

    else:
        st.info("퀴즈를 시작하여 저항값 계산 실력을 평가해보세요!")
        st.session_state.quiz_level = st.selectbox("난이도 선택:", ["초급 (4색띠)", "중급 (4색/5색띠 혼합)", "고급 (5색띠 위주)"], index=0, key="level_select")
        
        st.button("퀴즈 시작하기", on_click=start_quiz, use_container_width=True)