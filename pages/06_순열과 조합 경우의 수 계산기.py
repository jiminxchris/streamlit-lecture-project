

import streamlit as st
import math
import matplotlib.pyplot as plt

st.title('순열과 조합 경우의 수 계산기')

option = st.radio('계산할 항목을 선택하세요', ['순열', '조합'])

import itertools
import random
def draw_colored_circles(numbers, n_total=None, size=0.28):
    fig, ax = plt.subplots(figsize=(len(numbers)*size*2, size*3.2))
    if n_total is None:
        n_total = max(numbers)
    base_colors = plt.cm.get_cmap('tab20', n_total)
    color_map = {i+1: base_colors(i) for i in range(n_total)}
    for i, num in enumerate(numbers):
        # 완전한 원: 중심에서 테두리까지 거리가 모두 같음 (plt.Circle 사용)
        circle = plt.Circle((i+1, 1), size, color=color_map[num], ec='black', lw=2, zorder=1)
        ax.add_patch(circle)
        ax.text(i+1, 1, str(num), ha='center', va='center', fontsize=int(size*30), color='white', zorder=2)
    ax.set_aspect('equal', adjustable='datalim')  # 원이 찌그러지지 않도록 비율 고정
    ax.set_xlim(0, len(numbers)+1)
    ax.set_ylim(0.5, 1.5)
    ax.axis('off')
    st.pyplot(fig)

if option == '순열':
    st.markdown('**서로 다른 n개 중 r개를 나열합니다.**')
    col1, col2 = st.columns(2)
    n = col1.number_input('n (전체 개수)', min_value=0, value=5, step=1)
    r = col2.number_input('r (나열할 개수)', min_value=0, value=3, step=1)
    if st.button('나열한다'):
        if n < r:
            st.error('경우의 수를 구할 수 없습니다.\n이유: 전체 개수(n)보다 뽑거나 나열할 개수(r)가 더 많으면, 실제로 선택할 수 있는 대상이 부족하므로 경우의 수가 정의되지 않습니다.')
        else:
            result = math.perm(n, r) if hasattr(math, 'perm') else math.factorial(n) // math.factorial(n - r)
            st.success(f'서로 다른 {n}개 중 {r}개를 나열하는 경우의 수: {result}')
            perms = list(itertools.permutations(range(n), r))
            st.markdown('**모든 순열 리스트**')
            for i in range(0, len(perms), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(perms):
                        nums = [k+1 for k in perms[i+j]]
                        with cols[j]:
                            st.write(f'{i+j+1}:')
                            draw_colored_circles(nums, n_total=n, size=0.28)

elif option == '조합':
    st.markdown('**서로 다른 n개 중 r개를 뽑습니다.**')
    col1, col2 = st.columns(2)
    n = col1.number_input('n (전체 개수)', min_value=0, value=5, step=1, key='comb_n')
    r = col2.number_input('r (뽑을 개수)', min_value=0, value=3, step=1, key='comb_r')
    if st.button('뽑는다'):
        if n < r:
            st.error('경우의 수를 구할 수 없습니다.\n이유: 전체 개수(n)보다 뽑을 개수(r)가 더 많으면, 실제로 선택할 수 있는 대상이 부족하므로 경우의 수가 정의되지 않습니다.')
        else:
            result = math.comb(n, r) if hasattr(math, 'comb') else math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
            st.success(f'서로 다른 {n}개 중 {r}개를 뽑는 경우의 수: {result}')
            combs = list(itertools.combinations(range(n), r))
            st.markdown('**모든 조합 리스트**')
            for i in range(0, len(combs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(combs):
                        nums = [k+1 for k in combs[i+j]]
                        with cols[j]:
                            st.write(f'{i+j+1}:')
                            draw_colored_circles(nums, n_total=n, size=0.28)