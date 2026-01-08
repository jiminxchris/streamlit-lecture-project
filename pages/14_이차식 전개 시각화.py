import streamlit as st
import plotly.graph_objects as go

# --- 페이지 설정 ---
st.set_page_config(page_title="이차식 전개 시각화", layout="wide")
st.title("이차식 (x+a)(x+b) 전개 시각화 🧩")
st.info("사이드바에서 a와 b의 길이를 조정한 후, '사각형 합치기' 체크박스를 선택해 어떻게 (x+a)(x+b)가 만들어지는지 확인해보세요!")

# --- 'x'의 길이를 상수로 고정 ---
# x는 변수가 아니므로, 여기에서 고정된 값으로 설정합니다.
x = 7
st.sidebar.info(f"x의 길이는 '{x}'로 고정되어 있습니다.")

# --- 사이드바 설정 ---
st.sidebar.header("a, b 값 조정")
a = st.sidebar.slider("🔴 a 의 길이", min_value=1, max_value=10, value=3)
b = st.sidebar.slider("🟢 b 의 길이", min_value=1, max_value=10, value=4)

# --- 상호작용 위젯 ---
combine = st.checkbox("✅ 사각형 합치기")

# --- 데이터 및 좌표 설정 ---
if combine:
    # 합쳐진 상태의 좌표: 가로 (x+b), 세로 (x+a)
    shapes = [
        # x² (파란색)
        dict(type="rect", x0=0, y0=a, x1=x, y1=a+x, line=dict(color="RoyalBlue"), fillcolor="rgba(65,105,225,0.7)"),
        # ax (초록색)
        dict(type="rect", x0=0, y0=0, x1=x, y1=a, line=dict(color="SeaGreen"), fillcolor="rgba(46,139,87,0.7)"),
        # bx (주황색)
        dict(type="rect", x0=x, y0=a, x1=x+b, y1=a+x, line=dict(color="Orange"), fillcolor="rgba(255,165,0,0.7)"),
        # ab (빨간색)
        dict(type="rect", x0=x, y0=0, x1=x+b, y1=a, line=dict(color="Crimson"), fillcolor="rgba(220,20,60,0.7)"),
    ]
    # 합쳐진 상태의 텍스트 레이블 위치
    texts = [
        dict(x=x/2, y=a+x/2, text=f"x²<br>({x}×{x})"),
        dict(x=x/2, y=a/2, text=f"ax<br>({a}×{x})"),
        dict(x=x+b/2, y=a+x/2, text=f"bx<br>({b}×{x})"),
        dict(x=x+b/2, y=a/2, text=f"ab<br>({a}×{b})"),
    ]
    x_range = [-1, x + b + 1]
    y_range = [-1, x + a + 1]

else:
    # 분리된 상태의 좌표
    gap = 2  # 사각형 사이의 간격
    shapes = [
        # x² (파란색)
        dict(type="rect", x0=0, y0=a + gap, x1=x, y1=a + gap + x, line=dict(color="RoyalBlue"), fillcolor="rgba(65,105,225,0.7)"),
        # ax (초록색)
        dict(type="rect", x0=0, y0=0, x1=x, y1=a, line=dict(color="SeaGreen"), fillcolor="rgba(46,139,87,0.7)"),
        # bx (주황색)
        dict(type="rect", x0=x + gap, y0=0, x1=x + gap + b, y1=x, line=dict(color="Orange"), fillcolor="rgba(255,165,0,0.7)"),
        # ab (빨간색)
        dict(type="rect", x0=x + gap, y0=x + gap, x1=x + gap + b, y1=x + gap + a, line=dict(color="Crimson"), fillcolor="rgba(220,20,60,0.7)"),
    ]
    # 분리된 상태의 텍스트 레이블 위치
    texts = [
        dict(x=x/2, y=a + gap + x/2, text=f"x²<br>({x}×{x})"),
        dict(x=x/2, y=a/2, text=f"ax<br>({a}×{x})"),
        dict(x=x+b/2, y=x/2, text=f"bx<br>({b}×{x})"),
        dict(x=x+b/2, y=x+gap+a/2, text=f"ab<br>({a}×{b})"),
    ]
    # x, y축 범위 동적 조정
    x_range = [-1, x + b + gap + 1]
    y_range = [-1, x + a + gap + 1]


# --- Plotly Figure 생성 ---
fig = go.Figure()

# 도형 추가
for shape in shapes:
    fig.add_shape(**shape)

# 텍스트 레이블 추가
for t in texts:
    fig.add_annotation(
        x=t['x'], y=t['y'], text=t['text'],
        showarrow=False,
        font=dict(size=16, color="white")
    )

# 레이아웃 업데이트
fig.update_layout(
    width=700,
    height=700,
    xaxis=dict(range=x_range, showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(range=y_range, showgrid=False, showticklabels=False, zeroline=False, scaleanchor="x", scaleratio=1),
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor='rgba(240,240,240,0.95)' # 배경색
)

# --- Streamlit에 차트 및 수식 표시 ---
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 이차식 표시
st.markdown(f"""
### 전개식
- **변수**: $a = {a}$, $b = {b}$ (단, $x$는 기호)
- **결과**:
$$
(x + a)(x + b) = x^2 + (a+b)x + ab
$$
$$
(x + {a})(x + {b}) = x^2 + ({a}+{b})x + {a*b}
$$
""")