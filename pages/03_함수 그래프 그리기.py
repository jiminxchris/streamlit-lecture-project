

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# NanumGothic 폰트 경로 지정 및 예외처리
import os
font_path = './fonts/NanumGothic-Regular.ttf'
try:
	if os.path.exists(font_path):
		fontprop = fm.FontProperties(fname=font_path)
		plt.rc('font', family=fontprop.get_name())
	else:
		fontprop = None
except Exception:
	fontprop = None



st.title('함수 그래프 그리기')


st.write('아래에 함수를 입력하세요. 예: sin(x), x**2, exp(-x)')

func_str = st.text_input('함수 입력', value='sin(x)')


# 실수 전체 정의역 버튼 추가

# 정의역 입력 및 실수 전체 버튼 처리

if 'domain_str' not in st.session_state:
    st.session_state['domain_str'] = '-10,10'



# 입력란은 columns 바깥에서 한 번만 생성
domain_input = st.text_input('정의역 입력 (예: -10,10 또는 -3.14,3.14)', value=st.session_state['domain_str'], key='domain_input')
# 입력값이 바뀌면 session_state도 동기화
if domain_input != st.session_state['domain_str']:
    st.session_state['domain_str'] = domain_input

try:
	domain_vals = [float(v.strip()) for v in domain_input.split(',')]
	if len(domain_vals) == 2:
		x_min, x_max = domain_vals
	else:
		x_min, x_max = -10.0, 10.0
except Exception:
	x_min, x_max = -10.0, 10.0



if func_str:
	try:
		x = np.linspace(x_min, x_max, 500)
		# 안전하게 eval을 사용하기 위해 numpy 함수만 허용
		allowed_names = {k: getattr(np, k) for k in dir(np) if not k.startswith('_')}
		allowed_names['x'] = x
		y = eval(func_str, {"__builtins__": {}}, allowed_names)

		# 입력 정보 요약
		st.info(f"입력한 함수: f(x) = {func_str}\n정의역: x ∈ [{x_min}, {x_max}]")

		# 연속성 판정: np.isnan, np.isinf로 불연속점 탐색
		discontinuity = np.any(np.isnan(y)) or np.any(np.isinf(y))
		if discontinuity:
			st.warning('이 함수는 입력 구간 내에서 불연속점이 있습니다.')
		else:
			st.success('이 함수는 입력 구간 내에서 연속함수입니다.')

		# 최댓값, 최솟값 계산
		y_valid = y[~(np.isnan(y) | np.isinf(y))]
		if y_valid.size > 0:
			y_max = np.max(y_valid)
			y_min = np.min(y_valid)
			st.info(f'최댓값: {y_max:.4f}, 최솟값: {y_min:.4f}')
		else:
			st.error('유효한 함수값이 없어 최댓값/최솟값을 계산할 수 없습니다.')

		fig, ax = plt.subplots()
		ax.plot(x, y)
		# x축, y축 선 추가
		ax.axhline(0, color='gray', linewidth=1)
		ax.axvline(0, color='gray', linewidth=1)
		ax.set_xlabel('x', fontproperties=fontprop)
		ax.set_ylabel('f(x)', fontproperties=fontprop)
		ax.set_title(f'f(x) = {func_str}', fontproperties=fontprop)
		st.pyplot(fig)
	except Exception as e:
		st.error(f'그래프를 그릴 수 없습니다: {e}')