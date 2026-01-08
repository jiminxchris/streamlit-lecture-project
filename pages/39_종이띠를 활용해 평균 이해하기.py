import streamlit as st

# 기본 데이터
default_data = {
    '수현': 6,
    '은정': 5,
    '서진': 2,
    '재희': 3
}

# 색상 리스트
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

# Session state 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {'수현': 6, '은정': 5, '서진': 2, '재희': 3}

# 사이드바: 데이터 입력
st.sidebar.header("📝 학생 데이터 설정")
st.session_state.data = {}
default_names = ['수현', '은정', '서진', '재희']
default_values = [6, 5, 2, 3]
for i in range(4):
    name = st.sidebar.text_input(f"학생 {i+1} 이름", value=default_names[i], key=f"name_{i}")
    value = st.sidebar.number_input(f"{name}의 값", value=default_values[i], min_value=0, key=f"value_{i}")
    st.session_state.data[name] = value

# 메인 타이틀
st.title("📏 평균(Mean) 이해하기 - 종이띠 활동 🎉")

# 단계 버튼
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("1단계: 초기 상태", key="step1"):
        st.session_state.step = 1
with col2:
    if st.button("2단계: 종이띠 잇기", key="step2"):
        st.session_state.step = 2
with col3:
    if st.button("3단계: 똑같이 나누기", key="step3"):
        st.session_state.step = 3
with col4:
    if st.button("4단계: 평균 확인", key="step4"):
        st.session_state.step = 4

# 데이터 계산
values = list(st.session_state.data.values())
names = list(st.session_state.data.keys())
total = sum(values)
average = total / len(values) if values else 0

# 종이띠 생성 함수 (한 칸마다 구분, 지구 아이콘 추가)
def create_strip(value, color):
    boxes = ''.join([f'<div style="width:20px; height:20px; background-color:{color}; border:1px solid black; display:inline-block; text-align:center; line-height:18px; font-size:14px;">🌍</div>' for _ in range(int(value))])
    return f'<div style="overflow-x: auto; white-space: nowrap; border:2px solid black; display: inline-block;">{boxes}</div>'

# 단계별 표시
if st.session_state.step == 1:
    st.header("1단계: 각 친구가 가진 환경 카드의 수입니다. 🌟")
    st.write("각 친구마다 가지고 있는 카드의 수만큼 종이띠를 준비했어요!")
    cols = st.columns(len(names))
    for i, (name, value) in enumerate(zip(names, values)):
        with cols[i]:
            st.write(f"**{name}**: {value}장")
            st.markdown(create_strip(value, colors[i]), unsafe_allow_html=True)

elif st.session_state.step == 2:
    st.header("2단계: 종이띠를 이어 붙여요! 🔗")
    st.write("모든 종이띠를 하나로 이어 붙이면 이렇게 돼요!")
    st.write(f"수식: ({' + '.join(map(str, values))}) = {total}")
    combined_boxes_list = []
    for i, value in enumerate(values):
        combined_boxes_list.extend([f'<div style="width:20px; height:20px; background-color:{colors[i]}; border:1px solid black; display:inline-block; text-align:center; line-height:18px; font-size:14px;">🌍</div>' for _ in range(int(value))])
    combined_boxes = ''.join(combined_boxes_list)
    st.markdown(f'<div style="overflow-x: auto; white-space: nowrap; border:2px solid black; display: inline-block;">{combined_boxes}</div>', unsafe_allow_html=True)
    st.write("합계가 되었어요! 🎊")

elif st.session_state.step == 3:
    st.header("3단계: 똑같이 나누어요! ✂️")
    st.write("긴 종이띠를 친구 수만큼 똑같이 나누면...")
    st.write(f"수식: ({' + '.join(map(str, values))}) ÷ {len(values)} = {average:.0f}")
    if average == int(average):
        cols = st.columns(len(names))
        avg_int = int(average)
        combined_boxes_list = []
        for i, value in enumerate(values):
            combined_boxes_list.extend([f'<div style="width:20px; height:20px; background-color:{colors[i]}; border:1px solid black; display:inline-block; text-align:center; line-height:18px; font-size:14px;">🌍</div>' for _ in range(int(value))])
        start = 0
        for i, name in enumerate(names):
            boxes = ''.join(combined_boxes_list[start:start + avg_int])
            with cols[i]:
                st.write(f"**{name}**: {avg_int}장")
                st.markdown(f'<div style="overflow-x: auto; white-space: nowrap; border:2px solid black; display: inline-block;">{boxes}</div>', unsafe_allow_html=True)
            start += avg_int
    else:
        st.error("똑같이 나눌 수 없어요!")

elif st.session_state.step == 4:
    st.header("4단계: 평균 확인! 🎯")
    st.write("최종 평균 값을 확인해보세요!")
    if average == int(average):
        st.markdown(f"<h2 style='text-align: center; color: #FF6B6B;'>평균: {average:.0f}</h2>", unsafe_allow_html=True)
        st.success(f"친구들 모두가 똑같이 가질 수 있는 공평한 양은 {average:.0f}입니다. 🎉")
    else:
        st.error("똑같이 나눌 수 없어요!")
    if st.button("초기화", key="reset4"):
        st.session_state.data = default_data.copy()
        st.session_state.step = 1
        st.rerun()

# 추가 설명
st.markdown("---")
st.write("💡 **평균이란?** 친구들 모두가 똑같이 가질 수 있는 공평한 양이에요!")