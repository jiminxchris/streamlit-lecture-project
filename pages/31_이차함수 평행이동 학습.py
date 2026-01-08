import streamlit as st
import streamlit.components.v1 as components
import os
import re

# 페이지 설정 - 컴팩트한 레이아웃
st.set_page_config(
    page_title="이차함수 완전제곱식 & 그래프 변환 학습",
    page_icon="🎯",
    layout="wide",  # 변경: centered -> wide
    initial_sidebar_state="collapsed"
)

# 강제 업데이트 트리거 (v1.1)
st.markdown("<!-- Force Update v1.1 -->", unsafe_allow_html=True)

# 사이드바에 정보 추가
st.sidebar.title("📚 이차함수 학습 도우미")
st.sidebar.markdown("""
### 🎯 학습 목표
- 완전제곱식 변환 연습
- 그래프 평행이동 이해
- 이차함수와 그래프의 관계 파악

### 📖 사용법
1. **Level 1**: x² + bx + c 형태
2. **Level 2**: ax² + bx + c 형태

### 🔧 기능
- 랜덤 문제 생성
- 단계별 피드백
- 인터랙티브 그래프
""")

# 컴팩트한 메인 타이틀
st.title("🎯 이차함수 완전제곱식 & 그래프 변환 학습")

# 페이지 폭을 넓히고 여백을 줄이는 전역 CSS
st.markdown("""
<style>
/* 전체 최대 너비를 적당히 확장 */
.block-container {
    padding-top: 0.25rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    padding-bottom: 0.25rem;
    max-width: 100%;
}

/* 폰트 크기 조정 */
html, body, .stApp, .block-container {
    font-size: 14px !important;
    line-height: 1.1 !important;
}

/* 컴포넌트 여백 최소화 */
.element-container, .stMarkdown, .stButton, .stTextInput, .stSelectbox {
    margin: 0 !important;
    padding: 0.2rem !important;
}

/* 플롯/이미지 최적화 */
img, svg, canvas {
    max-width: 100% !important;
    height: auto !important;
}

/* 헤더/사이드바 여백 최소화 */
header[data-testid="stHeader"], aside[aria-label="Sidebar"] {
    padding: 6px 12px !important;
}

/* 기본 마진/패딩 제거 */
h1, h2, h3, p, li, label { 
    margin: 0; 
    padding: 0; 
}
</style>
""", unsafe_allow_html=True)

# HTML, CSS, JavaScript 파일 읽기
try:
    # 현재 스크립트의 디렉토리 기준으로 파일 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # HTML 파일 읽기
    with open(os.path.join(current_dir, '31_index.html'), 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # CSS 파일 읽기
    with open(os.path.join(current_dir, '31_style.css'), 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # JavaScript 파일 읽기 (31_main.js 사용)
    with open(os.path.join(current_dir, '31_main.js'), 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # 최종적으로 CSS/JS를 인라인으로 삽입
    html_with_inline = html_content.replace(
        '<link rel="stylesheet" href="31_style.css">',
        f'<style>{css_content}</style>'
    ).replace(
        '<script src="31_main.js"></script>',
        f'<script>{js_content}</script>'
    )

    # iframe 내부에서 스크롤을 없애고 전체 내용을 보여주기 위한 추가 스타일
    injection_style = """
    <style>
      /* 내부 스크롤 제거, 내부 컨테이너 자동 높이 */
      html, body, #app, .container, .root, .content {
          overflow: visible !important;
          height: auto !important;
          max-height: none !important;
      }
      /* 컨테이너 높이 제약 제거 */
      .container {
          height: auto !important;
          max-height: none !important;
          overflow: visible !important;
      }
      /* 스크롤바 숨김 */
      ::-webkit-scrollbar { display: none; }
      body { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
    """
    # 위 스타일을 <head> 직후나 <body> 최상단에 삽입
    if '<head>' in html_with_inline:
        html_with_inline = html_with_inline.replace('<head>', '<head>' + injection_style)
    else:
        html_with_inline = injection_style + html_with_inline

    # --- 변경: HTML 길이에 따라 적정 높이 계산 ---
    content_len = len(html_with_inline)
    line_count = html_with_inline.count('\n') + content_len / 200.0
    # 최소 600px, 최대 2000px 범위로 추정
    estimated_height = int(min(max(600, line_count * 15), 2000))

    # 부모 페이지(스트림릿)에서 iframe과 블록의 높이/정렬을 추정값 기준으로 적용
    st.markdown(f"""
    <style>
    /* 블록을 가로 중앙 정렬 */
    .block-container {{
        max-width: 100% !important;
        padding: 0.3rem !important;
        margin: 0 auto !important;
    }}

    /* iframe을 중앙에 고정하고 높이를 콘텐츠 기반으로 설정 */
    iframe[srcdoc], iframe {{
        height: {estimated_height}px !important;
        width: 100% !important;
        max-width: 100% !important;
        display: block;
        margin: 0 auto;
        border: none !important;
        overflow: hidden !important;
    }}

    /* 부모 페이지 스크롤 동작 안정화 */
    .main > div[role="main"] {{ overflow: auto !important; display: block; }}
    </style>
    """, unsafe_allow_html=True)

    # Streamlit에서 HTML 컴포넌트 실행 - 추정 높이 사용
    components.html(
        html_with_inline,
        height=estimated_height,    # 내용 기반 높이
        width=1600,                 # 부모에서 max-width로 제한하므로 적당한 픽셀값 사용
        scrolling=False
    )
    
except FileNotFoundError as e:
    st.error(f"파일을 찾을 수 없습니다: {e}")
    st.info("현재 디렉토리의 파일들을 확인해주세요.")
    
    # 디버깅을 위한 파일 목록 표시
    if st.checkbox("파일 목록 보기"):
        current_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                current_files.append(os.path.join(root, file))
        
        st.write("현재 디렉토리의 파일들:")
        for file in sorted(current_files):
            st.write(f"- {file}")

# 컴팩트한 푸터
st.markdown("""
<div style='text-align: center; color: #666; padding: 10px;'>
    <p>🎓 이차함수 학습 프로그램 v1.0</p>
</div>
""", unsafe_allow_html=True)