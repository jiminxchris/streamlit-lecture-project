import os
from matplotlib import font_manager
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 페이지 설정 ---
st.set_page_config(
    page_title="뷔퐁의 바늘 시뮬레이션",
    page_icon="🪡",
    layout="centered"
)


# --- 함수 정의 ---
def run_simulation(num_needles):
    """
    뷔퐁의 바늘 시뮬레이션을 실행하고 결과를 반환합니다.
    """
    # 시뮬레이션 상수 (바늘 길이 l, 선 간격 d)
    # 계산 편의를 위해 l=1, d=2로 설정 (l <= d 만족)
    needle_length = 1.0
    line_spacing = 2.0
    
    crosses = 0
    needle_coords = [] # 시각화를 위한 바늘 좌표 저장

    # 진행 상태 바
    progress_bar = st.progress(0, text="시뮬레이션을 진행 중입니다...")
    
    for i in range(num_needles):
        # 1. 바늘의 중심점 y좌표를 무작위로 생성 (0과 d/2 사이)
        #    대칭성을 이용해 0 ~ d/2 범위에서만 계산하여 효율을 높임
        y_center = np.random.uniform(0, line_spacing / 2)
        
        # 2. 바늘의 각도 θ를 무작위로 생성 (0과 π/2 사이)
        #    역시 대칭성을 이용
        theta = np.random.uniform(0, np.pi / 2)
        
        # 3. 교차 조건 확인
        #    y_center가 (l/2) * sin(θ) 보다 작으면 선과 교차
        if y_center <= (needle_length / 2) * np.sin(theta):
            crosses += 1
            is_crossed = True
        else:
            is_crossed = False
            
        # 시각화를 위해 바늘 정보 저장 (화면에 골고루 보이도록 x좌표도 무작위로 설정)
        x_center = np.random.uniform(0, line_spacing * 4)
        needle_coords.append((x_center, y_center, theta, is_crossed))

        # 진행 상태 업데이트
        progress_bar.progress((i + 1) / num_needles, text=f"시뮬레이션 진행 중... ({i+1}/{num_needles})")
    
    progress_bar.empty() # 시뮬레이션 완료 후 진행 바 제거
    return crosses, needle_coords, needle_length, line_spacing

def plot_needles(needle_coords, needle_length, line_spacing):
    """
    시뮬레이션 결과를 Matplotlib으로 시각화합니다.
    """
    fig, ax = plt.subplots(figsize=(12, 12))

    # 한글 폰트 적용
    font_path = os.path.join(os.path.dirname(__file__), '../fonts/NanumGothic-Regular.ttf')
    font_prop = font_manager.FontProperties(fname=font_path)

    # 평행선 그리기
    for i in range(5):
        ax.axhline(y=i * line_spacing, color='black', linestyle='-', linewidth=2)

    # 바늘 그리기
    for x_center, y_center, theta, is_crossed in needle_coords:
        y_center_display = y_center + np.random.randint(0, 5) * line_spacing
        half_l = needle_length / 2
        x_start = x_center - half_l * np.cos(theta)
        x_end = x_center + half_l * np.cos(theta)
        y_start = y_center_display - half_l * np.sin(theta)
        y_end = y_center_display + half_l * np.sin(theta)
        color = 'red' if is_crossed else 'blue'
        ax.plot([x_start, x_end], [y_start, y_end], color=color, alpha=0.7)

    ax.set_title('뷔퐁의 바늘 시뮬레이션 결과', fontsize=20, fontproperties=font_prop)
    ax.set_xlim(0, line_spacing * 4)
    ax.set_ylim(-1, line_spacing * 5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal', adjustable='box')
    
    # 범례 추가 (폰트 적용)
    red_patch = plt.Line2D([0], [0], color='red', lw=4, label='선에 걸친 바늘')
    blue_patch = plt.Line2D([0], [0], color='blue', lw=4, label='선에 걸치지 않은 바늘')
    ax.legend(handles=[red_patch, blue_patch], loc='upper right', prop=font_prop)
    return fig

# --- Streamlit UI 구성 ---

st.title("🪡 뷔퐁의 바늘 시뮬레이션")
st.markdown("""
이 웹 앱은 **뷔퐁의 바늘 문제**를 시뮬레이션하여 원주율($\pi$)의 근삿값을 계산합니다.
바늘을 평행선이 그어진 평면에 무작위로 던졌을 때, 바늘이 선과 교차할 확률을 이용합니다.
- 확률 공식: $P = \\frac{2l}{\pi d}$ (여기서 $l$: 바늘 길이, $d$: 선 간격)
- $\pi$ 추정 공식: $\pi \\approx \\frac{2l \\times (\\text{총 던진 횟수})}{d \\times (\\text{교차 횟수})}$
""")

st.info("여기서는 계산 편의를 위해 **바늘 길이(l) = 1**, **선 간격(d) = 2**로 고정합니다.")

# --- 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    num_needles_input = st.slider(
        "던질 바늘의 개수 (시행 횟수)", 
        min_value=100, 
        max_value=50000, 
        value=1000, 
        step=100,
        help="시행 횟수가 많을수록 $\pi$ 값에 더 근접하지만, 계산 시간이 오래 걸립니다."
    )
    
    run_button = st.button("시뮬레이션 시작", type="primary")

# --- 메인 화면 ---
if run_button:
    with st.spinner('열심히 바늘을 던지고 있습니다... 잠시만 기다려주세요.'):
        cross_count, needles, l, d = run_simulation(num_needles_input)

    st.header("📊 시뮬레이션 결과")

    # 결과 계산
    probability = cross_count / num_needles_input if num_needles_input > 0 else 0
    
    if cross_count == 0:
        pi_estimate = "N/A (교차 횟수가 0입니다)"
        error_percent = "N/A"
    else:
        pi_estimate = (2 * l * num_needles_input) / (d * cross_count)
        error = abs((pi_estimate - np.pi) / np.pi) * 100
        error_percent = f"{error:.4f}%"

    # 결과 출력
    col1, col2, col3 = st.columns(3)
    col1.metric("총 던진 횟수", f"{num_needles_input}개")
    col2.metric("선에 걸친 횟수", f"{cross_count}개")
    col3.metric("계산된 확률", f"{probability:.4f}")
    
    st.divider()

    col1, col2 = st.columns(2)
    col1.metric(
        label="실제 π 값",
        value=f"{np.pi:.6f}"
    )
    col2.metric(
        label="추정된 π 값",
        value=f"{pi_estimate:.6f}" if isinstance(pi_estimate, float) else pi_estimate,
        delta=f"오차: {error_percent}" if isinstance(pi_estimate, float) else None,
        delta_color="inverse"
    )

    st.header("🎨 시각화")
    st.markdown("시뮬레이션이 끝난 후 바늘들의 최종 배치 모습입니다.")
    
    # 시각화 그래프 표시
    # 많은 바늘을 모두 그리면 속도가 느려지므로, 최대 3000개까지만 시각화
    if len(needles) > 3000:
        st.warning(f"시각화 성능을 위해 {len(needles)}개의 바늘 중 3000개만 무작위로 표시합니다.")
        vis_needles = np.random.permutation(needles)[:3000]
    else:
        vis_needles = needles
        
    fig = plot_needles(vis_needles, l, d)
    st.pyplot(fig)
else:
    st.info("사이드바에서 바늘 개수를 설정하고 '시뮬레이션 시작' 버튼을 눌러주세요.")