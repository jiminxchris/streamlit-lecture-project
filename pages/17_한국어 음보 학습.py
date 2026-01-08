# app.py
import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(layout="wide") # 페이지를 넓게 사용

st.title("🎵 한국어 음보 학습 ")
st.info("한국 문학에서 음보 배우기")

# HTML 파일을 읽어옵니다.
try:
    with open('./data/korearhythm.html', 'r', encoding='utf-8') as f:
        html_code = f.read()
except FileNotFoundError:
    st.error("korearhythm.html 파일을 찾을 수 없습니다. app.py와 같은 폴더에 저장해주세요.")
    st.stop()


# Streamlit 앱 안에 HTML 코드를 삽입합니다.
# height를 충분히 주어야 스크롤 없이 전체 앱이 보입니다.
components.html(html_code, height=950, scrolling=False)

st.sidebar.header("Streamlit")
st.sidebar.write("""음보가 뭔가요?
음보는 우리말의 리듬 단위예요. 문장을 읽을 때 자연스럽게 끊어 읽는 덩어리라고 생각하면 됩니다.
예를 들어:

"파란 하늘 / 흰 구름이 / 떠간다"
이렇게 3개의 리듬 덩어리로 나누어 읽으면 훨씬 운율감 있게 들려요!

이 앱은 뭘 하는 앱인가요?
한국어의 리듬감을 눈으로 보고, 귀로 듣고, 직접 연습할 수 있는 교육 앱입니다.
특히 시조나 시를 읽을 때 필요한 음보 감각을 기를 수 있어요.
3단계 학습 시스템
1단계: 음보 듣기 👂

문장이 음보 단위로 구분되어 표시됩니다
"빰빰빰빰 (쉼) 빰빰빰빰 (쉼) 빰빰빰" 이런 식으로 리듬이 들려요
각 음보마다 번호가 표시되고, 재생할 때 하이라이트됩니다
반복 재생으로 리듬을 익힐 수 있어요

2단계: 음보 나누기 ✏️

띄어쓰기 부분의 회색 칸을 클릭해서 음보를 나눠보세요
클릭하면 노란색 구분선(|)이 나타납니다
"내 음보 재생"을 눌러서 나눈 대로 들어볼 수 있어요
정답이 없어서 자유롭게 연습 가능합니다

3단계: 리듬 연습 🎹

스페이스바나 화면 버튼으로 음보 리듬을 직접 연습
예시를 먼저 들어보고 따라할 수 있어요
시각적 피드백으로 리듬감을 확인""")
name = st.sidebar.text_input("이름을 입력하세요")
if name:
    st.sidebar.write(f"안녕하세요, {name}님!")