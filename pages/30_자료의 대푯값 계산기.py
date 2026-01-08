import streamlit as st
import numpy as np
import statistics as stats

st.title("📊 자료의 대푯값 계산기")

st.write("왼쪽 사이드바에서 예시를 선택하거나, 직접 자료를 입력해보세요.")

# 🎯 예시 데이터 세 가지
examples = {
    "예시 1️⃣": [5, 3, 28, 3, 8, 7],
    "예시 2️⃣": [72, 54, 54, 72, 54, 63, 81, 81, 63],
    "예시 3️⃣": [95, 100, 90, 95, 100, 90, 100, 95, 100, 90, 90, 5, 105, 95, 100, 110, 100, 105, 100, 105],
    "직접 입력하기": None
}

# 🔘 왼쪽 사이드바 선택
st.sidebar.header("📂 예시 선택")
choice = st.sidebar.radio("예시를 선택하세요 👇", examples.keys())

# 🧾 함수: 대표값 계산 + 출력
def show_stats(data, title):
    mean = np.mean(data)
    median = np.median(data)
    modes = stats.multimode(data)
    if len(modes) == len(set(data)):
        mode_text = "없음"
    else:
        mode_text = ", ".join(map(str, modes))

    st.markdown(f"### {title}")
    st.code(", ".join(map(str, data)))
    st.markdown(f"**평균:** {mean:.2f} &nbsp;&nbsp; **중앙값:** {median:.2f} &nbsp;&nbsp; **최빈값:** {mode_text}")
    st.divider()

# 📊 선택된 예시에 따라 다르게 표시
if choice == "예시 1️⃣":
    show_stats(examples["예시 1️⃣"], "예시 1️⃣ 결과")
elif choice == "예시 2️⃣":
    show_stats(examples["예시 2️⃣"], "예시 2️⃣ 결과")
elif choice == "예시 3️⃣":
    show_stats(examples["예시 3️⃣"], "예시 3️⃣ 결과")
else:
    st.subheader("✏️ 직접 입력하기")
    user_input = st.text_area("자료를 쉼표로 구분하여 입력하세요 (예: 150,160,155,165,170)")

    if user_input:
        try:
            data = [float(x.strip()) for x in user_input.split(",") if x.strip() != ""]
            show_stats(data, "직접 입력한 자료 결과")
        except ValueError:
            st.error("❌ 숫자만 입력하세요. (예: 150,160,155,165,170)")
    else:
        st.info("⬅️ 왼쪽에서 예시를 선택하거나 위에 자료를 입력하세요.")