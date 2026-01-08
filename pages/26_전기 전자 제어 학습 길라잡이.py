import streamlit as st
import base64
from pathlib import Path
import re

# --- Page settings and custom CSS ---
st.set_page_config(
    page_title="자동차 전기전자 학습",
    page_icon="🚗",
    layout="centered" 
)

# CSS code to change the app's color theme and font
def load_css():
    # Load local fonts from the fonts/ directory and embed them as base64 so Streamlit uses them.
    fonts_dir = Path(__file__).parent / "fonts"

    font_face_css = ""
    discovered_families = []
    primary_family = None

    # 폰트 Base64 인코딩 함수 (로컬 파일 접근 실패 시 무시됨)
    def font_data_uri(font_path: Path):
        try:
            font_bytes = font_path.read_bytes()
            b64 = base64.b64encode(font_bytes).decode()
            suffix = font_path.suffix.lower().lstrip('.')
            fmt = 'truetype' if suffix == 'ttf' else ('opentype' if suffix == 'otf' else suffix)
            return f"data:font/{suffix};base64,{b64}", fmt
        except Exception:
            return None, None

    # 로컬 폰트 검색 및 Base64 인코딩 시도
    if fonts_dir.exists() and fonts_dir.is_dir():
        font_files = list(fonts_dir.glob('*.ttf')) + list(fonts_dir.glob('*.otf'))
        font_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        for font_path in font_files:
            uri, fmt = font_data_uri(font_path)
            if not uri:
                continue
            
            stem = font_path.stem
            name_with_spaces = re.sub(r'[_\-]+', ' ', stem).strip()
            family = re.sub(r'(?i)\b(?:regular|bold|extrabold|heavy|black|semibold|demi|light|italic|oblique)\b', '', name_with_spaces).strip()
            family = re.sub(r'\s{2,}', ' ', family)
            
            weight = 400
            lower = stem.lower()
            if 'extrabold' in lower or 'heavy' in lower or 'black' in lower:
                weight = 800
            elif 'bold' in lower:
                weight = 700
            elif 'semibold' in lower or 'demi' in lower:
                weight = 600
            elif 'light' in lower:
                weight = 300

            font_face_css += (
                f"@font-face {{font-family: '{family}'; src: url('{uri}') format('{fmt}'); "
                f"font-weight: {weight}; font-style: normal; font-display: swap;}}\n"
            )

            if family not in discovered_families:
                discovered_families.append(family)
                if primary_family is None:
                    primary_family = family

    # Google font를 Fallback 또는 주력으로 사용
    google_import = "@import url('https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;700&display=swap');"

    # 폰트 패밀리 리스트 구성
    if discovered_families:
        ordered = []
        if primary_family:
            ordered.append(primary_family)
        for f in discovered_families:
            if f not in ordered:
                ordered.append(f)
        # 💡 안정화: 로컬 폰트 -> Gothic A1 -> sans-serif 순서
        css_font_family = ', '.join([f"'{f}'" for f in ordered]) + ", 'Gothic A1', sans-serif"
    else:
        # 💡 웹 환경에서 로컬 폰트 로드 실패 시: Gothic A1이 주력
        css_font_family = "'Gothic A1', sans-serif"
        
    if primary_family:
        primary_css_family = f"'{primary_family}'"
    else:
        primary_css_family = "'Gothic A1'" # Gothic A1을 타이틀 기본 폰트로 설정

    st.markdown(f"""
    <style>
        {google_import}
        {font_face_css}

        /* Apply the font to the entire app (broad selectors to cover all elements) */
        html, body, [class*="st-"], [data-testid], div, span, p, li, a, button, input, textarea, label {{
            font-family: {css_font_family} !important;
        }}

        /* Force title and subheader elements to use the primary (newest) font first */
        h1, h2, h3, .stTitle, .stSubheader {{
            font-family: {primary_css_family}, {css_font_family} !important;
        }}
        
        /* Widen the main content area */
        .block-container {{
            max-width: 1100px !important;
        }}

        /* Full app background and default text color */
        .stApp {{
            background: linear-gradient(to bottom, #001f3f, #003366); /* Navy gradient */
            color: white; /* Default text color to white */
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: #001f3f; /* Dark Navy */
        }}
        /* All text inside sidebar to white and adjusted size */
        [data-testid="stSidebar"] * {{
            color: white !important;
            font-size: 20px !important; 
        }}
        /* Sidebar title specific size */
        [data-testid="stSidebar"] h1 {{
             font-size: 26px !important;
        }}
        
        /* Main title (h1) - Keep large */
        h1 {{
            font-size: 3.0em !important;
            color: #FFFFFF; /* White */
        }}

        /* Subtitles (h2, h3) - Keep large */
        h2 {{
            font-size: 2.4em !important;
            color: #FFFFFF !important;
        }}
        h3 {{
            font-size: 2.0em !important;
            color: #FFFFFF !important;
        }}
        
        h5 {{
            font-size: 1.5em !important; /* Slightly larger for info boxes */
        }}

        /* General text (paragraphs, lists, etc.) - Make larger */
        body, p, li, div.stMarkdown, div.stText, span, label, input, textarea {{
            font-size: 24px !important;
            line-height: 1.6 !important;
        }}
        
        /* Ensure specific Streamlit containers also get the larger font size and consistent font */
        .st-emotion-cache-1r6slb0, .st-emotion-cache-zt5igj, .st-emotion-cache-1y4p8pa, .st-emotion-cache-ue6h4q, .st-emotion-cache-1g6gooi {{
            font-size: 24px !important;
            font-family: {css_font_family} !important;
        }}

        /* Tab style - larger font */
        .st-emotion-cache-19rxj06 {{
            border-color: #0074D9;
        }}
        .st-emotion-cache-1hb1d5i {{
            color: white !important; /* Tab title color to white */
            font-size: 24px !important;
        }}
        
        /* Button style - larger font */
        .stButton>button {{
            background-color: #007BFF; /* Blue */
            color: white;
            border-radius: 8px;
            border: 1px solid #007BFF;
            font-size: 20px !important;
            padding: 10px 16px;
        }}
        .stButton>button:hover {{
            background-color: #0056b3; /* Darker Blue */
            border: 1px solid #0056b3;
        }}

        /* Info box styling (covers quiz explanation) */
        .st-emotion-cache-1wivap2 div, .st-emotion-cache-1wivap2 p {{
             color: white !important;
             font-size: 22px !important;
        }}
        .st-emotion-cache-1wivap2 {{
            background-color: rgba(0, 116, 217, 0.2); /* Translucent Blue */
        }}
        
        /* Alert box styling (covers success/error) */
        .stAlert p {{
            color: white !important;
            font-size: 22px !important;
        }}

    </style>
    """, unsafe_allow_html=True)

load_css()


# --- Initialize session state (이미지 로딩 로직 수정) ---
# Collect local images (use them in-order to replace remote examples)
images_dir = Path(__file__).parent / "../images"
_local_images = []

# 💡 수정된 부분: Path 객체를 받아 파일명(숫자)으로 정렬하는 함수로 재정의
def sort_key(p: Path):
    try:
        # 파일 이름(stem)에서 숫자만 추출하여 정수로 변환 후 정렬
        match = re.search(r'\d+', p.stem)
        if match:
            return int(match.group(0))
        # 숫자가 없는 파일은 무한대로 처리하여 순서 맨 뒤로 보냄
        return float('inf') 
    except Exception:
        return float('inf')


if images_dir.exists() and images_dir.is_dir():
    # Path 객체 리스트를 생성
    path_objects = [p for p in images_dir.iterdir() if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif')]
    # Path 객체 리스트를 정렬 키를 이용해 정렬한 후, 문자열 경로로 변환하여 저장
    # st.image는 문자열 경로를 잘 처리합니다.
    _local_images = sorted([str(p) for p in path_objects], key=lambda p: sort_key(Path(p)))


_image_state = {"index": 0}

def get_image(default_url: str):
    """Return the next local image path if available, otherwise the provided default_url."""
    idx = _image_state["index"]
    if idx < len(_local_images):
        result = _local_images[idx]
        _image_state["index"] = idx + 1
        return result
    return default_url

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered_correctly = False

# --- Sidebar Menu ---
with st.sidebar:
    st.title('🚗 학습 메뉴')
    menu = st.radio(
        "메뉴를 선택하세요.",
        ('홈', '개념 학습', '개념 확인 퀴즈', '전기 장치 찾아보기', '단원 마무리'),
        label_visibility="collapsed"
    )

# --- Quiz Data ---
quiz_data = [
    {
        "type": "multiple_choice",
        "question": "1. 옴의 법칙(V=IR)에 대한 설명으로 올바른 것은 무엇인가요?",
        "options": [
            "전류는 전압에 반비례하고 저항에 비례한다.",
            "전압은 전류와 저항의 곱과 같다.",
            "저항은 전압과 전류에 비례한다.",
            "전류의 단위는 볼트(V)이다."
        ],
        "answer": "전압은 전류와 저항의 곱과 같다.",
        "explanation": "옴의 법칙은 V = I x R 입니다. 즉, 전압(V)은 전류(I)와 저항(R)을 곱한 값과 같습니다. 따라서 전류(I)는 전압(V)에 비례하고 저항(R)에 반비례합니다."
    },
    {
        "type": "multiple_choice",
        "question": "2. 다음 중 자동차의 '전기 장치'에 속하지 **않는** 것은 무엇인가요?",
        "options": [
            "시동 모터 (Starting Motor)",
            "발전기 (Alternator)",
            "브레이크 (Brake)",
            "전조등 (Headlight)"
        ],
        "answer": "브레이크 (Brake)",
        "explanation": "브레이크는 자동차를 멈추게 하는 제동 장치로, '섀시(Chassis)' 장치에 속합니다. 시동 모터, 발전기, 전조등은 모두 전기를 사용하는 핵심 전기 장치입니다."
    },
    {
        "type": "multiple_choice",
        "question": "3. 자동차 엔진이 작동하는 동안 전기를 생산하여 배터리를 충전하는 역할을 하는 장치는 무엇인가요?",
        "options": [
            "점화 플러그",
            "시동 모터",
            "발전기",
            "연료 펌프"
        ],
        "answer": "발전기",
        "explanation": "발전기(알터네이터)는 엔진의 회전력을 이용하여 전기를 만들어내고, 이 전기로 배터리를 충전하며 다른 전기 장치에도 전원을 공급합니다."
    },
    {
        "type": "multiple_choice",
        "question": "4. 다음 중 자동차의 동력을 발생시키는 '기관(엔진) 장치'의 핵심 부품은 무엇인가요?",
        "options": [
            "조향 장치 (Steering System)",
            "현가 장치 (Suspension System)",
            "점화 플러그 (Spark Plug)",
            "라디에이터 그릴 (Radiator Grille)"
        ],
        "answer": "점화 플러그 (Spark Plug)",
        "explanation": "점화 플러그는 엔진 연소실에서 연료와 공기의 혼합기에 불꽃을 일으켜 폭발시켜 동력을 얻는 핵심 '기관' 부품입니다. 조향 장치와 현가 장치는 '섀시'에 속합니다."
    },
    {
        "type": "multiple_choice",
        "question": "5. 전기의 흐름인 '전류'에 대한 설명으로 틀린 것은 무엇인가요?",
        "options": [
            "단위는 암페어(A)를 사용한다.",
            "전자의 이동 방향과 반대 방향으로 흐른다고 약속했다.",
            "전류를 흐르게 하는 힘을 '저항'이라고 한다.",
            "전류가 흐르면 빛이나 열이 발생할 수 있다."
        ],
        "answer": "전류를 흐르게 하는 힘을 '저항'이라고 한다.",
        "explanation": "전류를 흐르게 하는 힘(전기적 압력)은 '전압'입니다. '저항'은 오히려 전류의 흐름을 방해하는 요소입니다."
    },
    {
        "type": "short_answer",
        "question": "6. 전압, 전류, 저항의 관계를 나타내는 법칙의 이름은 무엇인가요? (OOO 법칙)",
        "answer": "옴의 법칙",
        "explanation": "전압(V), 전류(I), 저항(R) 사이의 관계 V=IR을 '옴의 법칙'이라고 합니다."
    },
    {
        "type": "short_answer",
        "question": "7. 자동차의 엔진을 처음 가동시키기 위해 배터리의 전기를 이용해 강력한 회전력을 만들어주는 전기 장치의 이름은 무엇인가요? (OO OO)",
        "answer": "시동 모터",
        "explanation": "'시동 모터' 또는 '시동 전동기'는 엔진을 맨 처음 돌려주는 중요한 전기 장치입니다."
    }
]


# --- Page implementations ---

# 1. Home Page
if menu == '홈':
    st.title('자동차 전기전자제어 학습 길라잡이')
    st.divider() 
    st.subheader('1단원: 자동차 전기전자 개요에 대해 알아봅시다.')
    
    st.write("""
    이 앱은 '자동차 전기전자제어' 교과의 첫 단원인 **'자동차 전기전자 개요'**의 내용을 학습하는 데 도움을 주기 위해 만들어졌습니다.  
    왼쪽 사이드바에서 원하는 학습 메뉴를 선택하여 진행해 주세요.
    """)
    
    st.info("##### 📖 개념 학습\n전기, 전류, 전압 등 기초 개념을 시각 자료와 함께 배워봅니다.", icon="ℹ️")
    st.info("##### ✍️ 개념 확인 퀴즈\n객관식 퀴즈를 풀며 학습한 내용을 점검해 보세요.", icon="ℹ️")
    st.info("##### 🔍 전기 장치 찾아보기\n실제 자동차 사진을 보고 전기 장치의 종류와 명칭을 맞춰봅니다.", icon="ℹ️")


# 2. Concept Learning Page
elif menu == '개념 학습':
    # 💡 수정된 부분: 이미지 인덱스를 다시 0으로 초기화
    _image_state["index"] = 0 
    
    st.title('📖 개념 학습: 자동차 전기전자 개요')
    st.divider()

    tab1, tab2, tab3 = st.tabs(["⚡ 전기와 전류의 기초", "💡 옴의 법칙 (V=IR)", "🚗 자동차 전기 장치"])

    with tab1:
        st.subheader("1. 전기(Electricity)와 전류(Current)")
        st.write(
            """
            전기는 우리 생활과 자동차에 없어서는 안 될 중요한 에너지입니다. 
            모든 물질은 **원자**로 이루어져 있고, 원자는 원자핵(+)과 그 주위를 도는 **전자(-)**로 구성됩니다.
            
            **전기**란 바로 이 '전자'가 이동하면서 발생하는 에너지 현상을 의미합니다.
            """
        )
        st.image(get_image("https://i.postimg.cc/9F4Zt6H0/atom.jpg"), caption="[그림 1] 원자의 구조", width=400) # 0번째 이미지
        
        st.markdown(
            """
            ---
            #### 전류: 전기의 흐름
            **전류**는 물이 높은 곳에서 낮은 곳으로 흐르는 것처럼, 전하(전자)가 한 방향으로 이동하는 흐름을 말합니다.
            - **전류의 방향:** 전자가 이동하는 방향과 **반대** 방향 (양극(+) → 음극(-))
            - **단위:** **A (암페어)**
            
            회로에 전구와 같은 부하(일을 하는 장치)가 연결되어 있으면, 전류가 흐르면서 빛이나 열을 발생시킵니다.
            """
        )
        st.image(get_image("https://i.postimg.cc/tJn4h0zZ/current-flow.jpg"), caption="[그림 2] 전류와 전자의 이동 방향") # 1번째 이미지

        st.markdown("---")

        st.subheader("🧐 잠깐 퀴즈!")
        st.write("일상생활의 예시를 통해 교류와 직류를 구분해 봅시다.")

        question = st.radio(
            "**Q. 우리가 가정에서 사용하는 콘센트의 전기와 자동차에서 사용하는 배터리 전기는 각각 무엇일까요?**",
            ('둘 다 직류(DC)입니다.', 
             '둘 다 교류(AC)입니다.', 
             '가정용은 교류(AC), 자동차용은 직류(DC)입니다.', 
             '가정용은 직류(DC), 자동차용은 교류(AC)입니다.'),
            index=None,
        )

        if st.button('정답 확인'):
            if question == '가정용은 교류(AC), 자동차용은 직류(DC)입니다.':
                st.success('정답입니다! 짝짝짝 👏')
                st.info(
                    """
                    **해설:**
                    - **가정용 전기(교류, AC):** 발전소에서 만들어진 전기는 먼 거리를 효율적으로 보내기 위해 교류 형태를 사용합니다.
                    - **자동차 배터리(직류, DC):** 배터리는 화학 에너지를 전기 에너지로 저장하는데, 이때는 한 방향으로만 흐르는 직류 형태를 띱니다.
                    """
                )
            elif question is None:
                st.warning("답을 선택해주세요!")
            else:
                st.error('아쉽지만 틀렸어요. 다시 한번 생각해 보세요! 🤔')

    with tab2:
        st.subheader("2. 전압, 전류, 저항의 관계: 옴의 법칙")
        st.write(
            """
            전기 회로에서는 전압, 전류, 저항 세 가지 요소가 서로 밀접한 관계를 맺고 있습니다. 이 관계를 설명하는 것이 바로 **옴의 법칙**입니다.
            - **전압(V):** 전류를 흐르게 하는 힘 (전기적인 압력). 단위는 **V(볼트)**.
            - **전류(I):** 전하의 흐름. 단위는 **A(암페어)**.
            - **저항(R):** 전류의 흐름을 방해하는 정도. 단위는 **Ω(옴)**.
            """
        )
        
        st.image(get_image("https://i.postimg.cc/Jn3J37sf/ohms-law.png"), caption="[그림 3] 옴의 법칙 (E는 전압 V와 같음)") # 2번째 이미지

        st.success(
            """
            **"회로에 흐르는 전류(I)는 전압(V)에 비례하고, 저항(R)에 반비례한다."**
            #### $I = V / R$
            """
        )
        
        st.markdown("---")
        
        st.subheader("🔢 옴의 법칙 계산기")
        st.write("슬라이더를 조절하여 전압과 저항의 변화에 따른 전류의 변화를 직접 확인해보세요.")
        
        col1, col2 = st.columns(2)
        with col1:
            voltage = st.slider('전압 (V) 선택', 1, 24, 12, 1)
        with col2:
            resistance = st.slider('저항 (R) 선택', 1, 100, 10, 1)

        if resistance > 0:
            current = voltage / resistance
            st.metric(label="계산된 전류 (I)", value=f"{current:.2f} A")
        else:
            st.error("저항은 0보다 커야 합니다.")


    with tab3:
        st.subheader("3. 자동차의 주요 전기 장치")
        st.write("자동차에는 다양한 전기 장치들이 있으며, 크게 다음과 같이 분류할 수 있습니다.")

        col1, col2 = st.columns(2)
        with col1:
            st.info("#### 시동 장치 (Starting System)")
            st.write("엔진을 처음 가동시키기 위해 크랭크축에 회전력을 공급하는 장치입니다. (예: 시동 모터)")
            st.image(get_image("https://i.postimg.cc/6p2L9f3P/starter-motor.png"), caption="시동 모터") # 3번째 이미지

            st.info("#### 등화 장치 (Lighting System)")
            st.write("야간 주행 시 시야를 확보하고, 다른 차에게 신호를 보내는 장치입니다. (예: 전조등, 방향지시등)")
            st.image(get_image("https://i.postimg.cc/Hxb1T53z/headlight.png"), caption="전조등") # 4번째 이미지
        
        with col2:
            st.info("#### 충전 장치 (Charging System)")
            st.write("엔진이 작동하는 동안 전기를 생산하여 배터리를 충전하고, 각 부품에 전원을 공급하는 장치입니다. (예: 발전기)")
            st.image(get_image("https://i.postimg.cc/tCTw1g2C/alternator.png"), caption="발전기 (알터네이터)") # 5번째 이미지

            st.info("#### 점화 장치 (Ignition System)")
            st.write("가솔린 엔진의 연소실 내 압축된 혼합기에 전기 불꽃을 일으켜 점화하는 장치입니다. (예: 점화 코일, 점화 플러그)")
            st.image(get_image("https://i.postimg.cc/k4GkYqw9/spark-plug.png"), caption="점화 플러그") # 6번째 이미지


# 3. Concept Check Quiz Page
elif menu == '개념 확인 퀴즈':
    st.title('✍️ 개념 확인 퀴즈')
    st.divider()

    def reset_quiz():
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered_correctly = False

    if st.session_state.current_question >= len(quiz_data):
        st.success(f"🎉 모든 퀴즈를 완료했습니다! 당신의 점수는: {st.session_state.score} / {len(quiz_data)}")
        st.balloons()
        if st.button("다시 풀기"):
            reset_quiz()
            st.rerun()
    else:
        question_data = quiz_data[st.session_state.current_question]
        
        # 퀴즈 문제 번호를 h3 스타일로 크게 표시
        st.subheader(f"문제 {st.session_state.current_question + 1} / {len(quiz_data)}")
        
        # 질문 텍스트를 st.write로 별도 출력하여 24px의 일반 텍스트 스타일을 적용
        st.write(f"**{question_data['question']}**")

        if not st.session_state.get('answered_correctly', False):
            user_answer = None
            if question_data["type"] == "multiple_choice":
                # 라벨을 빈 문자열로 설정하여 질문 텍스트가 중복되거나 작게 나오는 것을 방지
                user_answer = st.radio(
                    "", 
                    question_data["options"],
                    index=None,
                    key=f"q_{st.session_state.current_question}"
                )
            elif question_data["type"] == "short_answer":
                 # 라벨을 빈 문자열로 설정하여 질문 텍스트가 중복되거나 작게 나오는 것을 방지
                user_answer = st.text_input(
                    "", 
                    placeholder="정답을 입력하세요.",
                    key=f"q_{st.session_state.current_question}"
                )

            if st.button("제출하기"):
                correct_answer = question_data["answer"]
                
                is_correct = False
                if user_answer is not None and user_answer != "": 
                    if question_data["type"] == "short_answer":
                        # 단답형은 공백 제거 및 소문자 비교 (혹시 모를 대소문자 문제 방지)
                        is_correct = user_answer.strip().lower() == correct_answer.lower()
                    else:
                        is_correct = user_answer == correct_answer

                if is_correct:
                    st.session_state.score += 1
                    st.session_state.answered_correctly = True
                    st.rerun() 
                
                elif user_answer is None or (question_data["type"] == "short_answer" and user_answer.strip() == ""):
                    st.warning("답을 입력하거나 선택해주세요.")
                else:
                    st.error("오답입니다. 다시 한번 생각해 보세요. 💡")

        if st.session_state.get('answered_correctly', False):
            st.success("정답입니다! 👍")
            st.info(f"**해설:** {question_data['explanation']}")
            
            if st.button("다음 문제로 이동"):
                st.session_state.current_question += 1
                st.session_state.answered_correctly = False
                st.rerun()


# 4. Find Electrical Components Page
elif menu == '전기 장치 찾아보기':
    # 💡 수정된 부분: 이미지 인덱스를 7로 설정 (마지막 이미지를 사용)
    _image_state["index"] = 7
    
    st.title('🔍 전기 장치 찾아보기')
    st.divider()
    st.write("아래 엔진룸 사진에서 번호가 가리키는 부품의 이름을 맞춰보세요!")

    st.image(get_image("https://i.postimg.cc/qR13x0Yw/engine-bay-labels.jpg"), caption="엔진룸 주요 부품") # 7번째 이미지

    st.markdown("---")

    answers = {
        "①": "배터리 (Battery)",
        "②": "퓨즈 박스 (Fuse Box)",
        "③": "워셔액 주입구 (Washer Fluid Inlet)",
        "④": "엔진 커버 (Engine Cover)"
    }
    
    options = ["배터리 (Battery)", "퓨즈 박스 (Fuse Box)", "엔진 커버 (Engine Cover)", "워셔액 주입구 (Washer Fluid Inlet)", "브레이크액 저장소 (Brake Fluid Reservoir)", "라디에이터 (Radiator)"]

    col1, col2 = st.columns(2)

    with col1:
        st.write("1. 사진 속 ①번 부품의 이름은 무엇일까요?")
        q1_answer = st.selectbox(
            "_", 
            options,
            index=None,
            placeholder="부품 이름을 선택하세요.",
            key="q1_device",
            label_visibility="collapsed" 
        )

    with col2:
        st.write("2. 사진 속 ②번 부품의 이름은 무엇일까요?")
        q2_answer = st.selectbox(
            "__", 
            options,
            index=None,
            placeholder="부품 이름을 선택하세요.",
            key="q2_device",
            label_visibility="collapsed" 
        )
    
    col3, col4 = st.columns(2)
    with col3:
        st.write("3. 사진 속 ③번 부품의 이름은 무엇일까요?")
        q3_answer = st.selectbox(
            "___", 
            options,
            index=None,
            placeholder="부품 이름을 선택하세요.",
            key="q3_device",
            label_visibility="collapsed" 
        )

    with col4:
        st.write("4. 사진 속 ④번 부품은 '전기 장치'일까요?")
        q4_answer = st.selectbox(
            "____", 
            ("예", "아니오"),
            index=None,
            placeholder="예/아니오를 선택하세요.",
            key="q4_device",
            label_visibility="collapsed" 
        )


    st.markdown("---")

    if st.button("결과 확인하기"):
        score = 0
        
        st.subheader("채점 결과")

        if q1_answer == answers["①"]:
            st.success("✅ 1번 정답! **배터리**는 시동을 걸고, 각종 전기 장치에 전원을 공급하는 핵심 '전기 장치'입니다.")
            score += 1
        else:
            st.error(f"❌ 1번 오답! 정답은 **{answers['①']}** 입니다. ①번은 배터리입니다.")

        if q2_answer == answers["②"]:
            st.success("✅ 2번 정답! **퓨즈 박스**는 과전류로부터 전기 회로와 부품을 보호하는 중요한 '전기 장치'입니다.")
            score += 1
        else:
            st.error(f"❌ 2번 오답! 정답은 **{answers['②']}** 입니다. ②번은 퓨즈 박스입니다.")
            
        if q3_answer == answers["③"]:
            st.success("✅ 3번 정답! **워셔액 주입구** 자체는 전기 장치가 아니지만, 전기를 사용하는 '워셔액 펌프'와 연결됩니다.")
            score += 1
        else:
            st.error(f"❌ 3번 오답! 정답은 **{answers['③']}** 입니다. ③번은 워셔액 주입구입니다.")

        if q4_answer == "아니오":
            st.success("✅ 4번 정답! 맞습니다. **엔진 커버**는 엔진을 보호하는 '기관 장치'의 일부로, 전기 장치가 아닙니다.")
            score += 1
        else:
            st.error("❌ 4번 오답! 엔진은 동력을 만드는 '기관 장치'입니다. 전기 장치가 아닙니다.")
        
        st.divider()
        st.header(f"총 {score} / 4 점 입니다!")

        if score == 4:
            st.balloons()

# 5. Unit Summary Page
elif menu == '단원 마무리':
    st.title('✅ 단원 마무리')
    st.divider()

    st.subheader('📌 1단원 핵심 내용 요약')
    st.markdown("""
    이번 단원에서는 자동차 전기전자의 가장 기초적인 개념들을 배웠습니다.
    
    - **전기와 전류:** 전자의 이동으로 발생하는 에너지 현상이며, 전류는 이러한 전기의 흐름을 의미합니다.
    - **옴의 법칙 (V=IR):** 전기 회로의 세 가지 기본 요소인 전압(V), 전류(I), 저항(R) 사이의 중요한 관계를 나타내는 법칙입니다.
    - **자동차의 주요 전기 장치:** 자동차가 움직이는 데 필수적인 시동 장치, 충전 장치, 점화 장치, 등화 장치 등의 역할과 종류를 알아보았습니다.
    
    각 개념들이 어떻게 연결되는지 다시 한번 생각해 보세요!
    """)
    
    st.divider()

    st.subheader('📚 다음 학습 안내')
    st.info("""
    **다음 시간에는 2단원, '자동차 전기·전자 회로'에 대해 학습합니다.**
    
    - 자동차 전기 회로를 보호하는 **퓨즈**와 **릴레이**의 역할에 대해 배웁니다.
    - 전기 회로에 문제가 생겼을 때 어떻게 진단하고 해결하는지에 대한 기초적인 **고장 진단 방법**을 알아봅니다.
    
    오늘 배운 기초 개념이 다음 단원 학습의 중요한 발판이 될 것입니다.
    """, icon="📖")