import streamlit as st
import pandas as pd
import random 

# --- 1. 데이터 정의 (오류 발생 부분 간소화) ---

CAR_MODELS_EXTENDED = {
    '전기차': {
        '현대/제네시스': ['아이오닉 5', '아이오닉 6', '코나 EV', '넥쏘 (수소)', 'GV60', 'GV70 EV', 'G80 EV', '캐스퍼 EV'],
        '기아': ['EV6', 'EV9', '니로 EV', '레이 EV', '봉고 EV'],
        '테슬라': ['모델 3', '모델 Y', '모델 S', '모델 X', '사이버트럭'],
        'BMW': ['iX', 'i4', 'i5', 'i7', 'iX3'],
        '벤츠': ['EQA', 'EQB', 'EQC', 'EQE', 'EQS', 'EQV'],
        '폭스바겐/아우디': ['ID.4', 'ID.5', 'e-트론', 'e-트론 GT', 'Q4 e-트론'],
        '포르쉐': ['타이칸'],
        '기타 수입': ['쉐보레 볼트 EV', '폴스타 2', '리비안 R1S', '루시드 에어', 'BYD 씰']
    },
    '내연기관': {
        '현대/제네시스': ['아반떼', '쏘나타', '그랜저', '코나', '투싼', '싼타페', '팰리세이드', 'G70', 'G80', 'G90', 'GV80'],
        '기아': ['모닝', '레이', 'K3', 'K5', 'K8', '셀토스', '스포티지', '쏘렌토', '카니발', '스팅어'],
        'BMW': ['1시리즈', '3시리즈', '5시리즈', '7시리즈', 'M2/M3/M4/M5', 'X1~X7'],
        '벤츠': ['A클래스', 'C클래스', 'E클래스', 'S클래스', 'G바겐', 'AMG GT', 'GLA~GLS'],
        '아우디': ['A4', 'A6', 'A8', 'Q5', 'Q7', 'R8'],
        '포르쉐': ['911', '카이엔', '파나메라', '마칸'],
        '쉐보레/포드': ['트레일블레이저', '트래버스', '콜로라도', '머스탱', 'F-150', '브롱코'],
        '기타 수입': ['볼보 S60/XC90', '푸조 308', '지프 랭글러', '람보르기니 우루스', '페라리 로마']
    },
    '하이브리드': {
        '현대/제네시스': ['쏘나타 HEV', '그랜저 HEV', '투싼 HEV', '싼타페 HEV', '니로 HEV (PHEV 포함)'],
        '기아': ['K5 HEV', 'K8 HEV', '쏘렌토 HEV', '스포티지 HEV', '카니발 HEV'],
        '토요타/렉서스': ['프리우스', '캠리 HEV', '시에나 HEV', '라브4 HEV', 'ES 300h', 'RX 450h'],
        '기타 수입': ['혼다 어코드 HEV', '벤츠 C/E 클래스 PHEV', 'BMW 5시리즈 PHEV']
    }
}

DRIVING_FACTORS = {
    'A': '최고 수준의 가속력과 주행 성능',
    'B': '혁신적인 실내외 디자인',
    'C': '첨단 자율주행 및 인포테인먼트 옵션',
    'D': '탁월한 연비와 친환경성',
    'E': '안전성, 내구성, 잔고장이 적은 신뢰성',
    'F': '차량의 조립/정비 용이성'
}

JOB_ROLES = {
    '자동차 정비': {"desc": "차량 기계, 전기/전자 시스템 고장 진단 및 수리. (미래 EV 전문 정비 포함)", "need": "분석력, 꼼꼼함, 손기술"},
    '자동차 차체수리': {"desc": "사고 차량의 외형 복원, 판금 작업 및 차체 구조 안전성 확보.", "need": "정교함, 구조 이해력, 인내심"},
    '자동차 도장': {"desc": "차량 외관 색상 복원, 표면 처리, 코팅 등 최종 외형 품질 담당.", "need": "색감 감각, 미적 감각, 세밀함"},
    '자동차 튜닝': {"desc": "내/외장 드레스업 및 성능, 편의 기능 개선. (나만의 차 만들기)", "need": "창의성, 개성, 공학적 지식"},
    '서비스 어드바이저 (SA)': {"desc": "고객 정비 상담, 고장 내용 파악, 작업 지시 및 결과 설명. (기술과 소통의 연결)", "need": "소통 능력, 친화력, 기술 지식"},
    '자동차 딜러 (영업)': {"desc": "고객에게 차량을 판매하고 계약, 출고, 사후 관리를 담당. (가치와 매력을 전달)", "need": "설득력, 적극성, 자동차에 대한 열정"}
}

JOB_WEIGHTS = {
    '자동차 정비': {'A': 1, 'B': 0, 'C': 1, 'D': 1, 'E': 3, 'F': 3},
    '자동차 차체수리': {'A': 0, 'B': 2, 'C': 0, 'D': 0, 'E': 3, 'F': 1},
    '자동차 도장': {'A': 0, 'B': 3, 'C': 0, 'D': 0, 'E': 1, 'F': 0},
    '자동차 튜닝': {'A': 3, 'B': 2, 'C': 2, 'D': 0, 'E': 0, 'F': 0},
    '서비스 어드바이저 (SA)': {'A': 1, 'B': 1, 'C': 3, 'D': 2, 'E': 1, 'F': 0},
    '자동차 딜러 (영업)': {'A': 3, 'B': 2, 'C': 2, 'D': 1, 'E': 0, 'F': 0}
}

COLOR_OPTIONS = ['화이트', '블랙', '실버', '블루', '레드', '커스텀 색상']

# 3단계: 학기별 로드맵 데이터 (오류 발생 '목표' 키를 명확히 포함)
ROADMAP_ACADEMIC = {
    '고1': {
        '목표': '기초 학력 확보 및 기본 자격증 도전',
        '1학기': ['보통교과(국, 영, 수) 기초 학력 관리', '자동차 기초 이론 학습 및 안전 교육', '전공 동아리(익스플로러) 가입'],
        '2학기': ['기초 자격증 (정비/도장) 필기 집중 준비', '기본 정비 실습 심화', '진로 탐색 및 선배 멘토링']
    },
    '고2': {
        '목표': '선택 직무 심화 및 핵심 자격증 취득',
        '1학기': ['자동차 정비/도장 기능사 실기 집중 준비', '선택 직무별 심화 실습 시작', '공기업/공무원 희망 학생은 내신 성적 유지'],
        '2학기': ['자동차 정비/도장 기능사 최종 취득', '추가 자격증(용접 기능사 등) 도전', '튜닝/랩핑 등 흥미 유발 실습 참여']
    },
    '고3': {
        '목표': '최종 진로 실행 및 포트폴리오 완성',
        '1학기': ['최종 진로 결정 및 취업/진학 대비', '자격증 최종 마무리 및 포트폴리오 완성', '아우스빌둥 필기/면접 준비 (5월~6월)'],
        '2학기': ['취업: 현장 실습(10월~) 및 근로 계약', '대학: 수시/수능 전형 지원', '공기업: NCS/필기 시험 응시 및 면접 준비']
    }
}

ROADMAP_JOB_SIMULATOR = {
    '자동차 정비': {'고2_심화': ['EV 정비 기초 (전기/배터리)', '엔진/섀시 정밀 진단 실습', '특수용접 기능사 또는 피복아크용접 기능사 준비'], '고3_목표_텍스트': '자동차 정비 기능사 합격, 취업맞춤반(현대/기아 등), 아우스빌둥(벤츠/BMW/포르쉐 등) 준비'},
    '자동차 차체수리': {'고2_심화': ['차체 구조 복원 심화 실습', '판금/용접 집중 훈련', '차체수리 기능사 및 용접 기능사 준비'], '고3_목표_텍스트': '차체수리 기능사 합격, 아우스빌둥(판금 직무), 일반 우수 협력업체 취업 준비'},
    '자동차 도장': {'고2_심화': ['색상 조색 심화 교육', '스프레이 건/표면 처리 기술 집중 훈련'], '고3_목표_텍스트': '보수 도장 기능사 합격, 아우스빌둥(도장 직무), 일반 우수 협력업체 취업 준비'},
    '자동차 튜닝': {'고2_심화': ['랩핑/내장재 튜닝 실습', '기능 튜닝 (서스펜션/브레이크) 실습', 'CAD/3D 프린팅 기초'], '고3_목표_텍스트': '실무 프로젝트 포트폴리오 완성, 우수 튜닝샵 취업'},
    '서비스 어드바이저 (SA)': {'고2_심화': ['고객 응대/상담 화법 훈련', '자동차 보험/법규 이해 및 진단 보고서 작성'], '고3_목표_텍스트': 'OA 자격증, 아우스빌둥(SA 직무), 딜러사 SA 취업 준비'},
    '자동차 딜러 (영업)': {'고2_심화': ['마케팅/세일즈 기초', '신차 프리젠테이션 훈련', '다양한 브랜드 스터디'], '고3_목표_텍스트': '운전면허 필수, 우수 딜러사 취업 준비, 특성화고 재직자 전형 대비'}
}


# --- 2. Streamlit 앱 페이지 구성 함수 ---

def apply_custom_styles():
    """앱 전체의 커스텀 CSS (최소화)"""
    st.markdown(
        """
        <style>
        /* 기본 폰트 사용 및 크기 조정 */
        html, body, [class*="st-emotion"] {
            font-size: 0.95em;
        }
        
        /* 제목 글꼴 크기 조정 */
        h1 { font-size: 2.2em; }
        h2 { font-size: 1.8em; }
        h3 { font-size: 1.5em; }
        h4, h5, h6 { font-size: 1.2em; }

        /* Streamlit 버튼 스타일 (깔끔함 유지) */
        .stButton>button {
            border-radius: 15px;
            border: 1px solid #0078D4; 
            color: #0078D4;
            background-color: #e6f7ff; 
            font-weight: bold;
            font-size: 1.0em;
            padding: 5px 10px;
        }
        
        /* 정보 박스 스타일 */
        .stAlert {
            background-color: #e6f7ff;
            border-left: 5px solid #0078D4;
        }

        /* 2단계 직무 카드 스타일 (오류 방지를 위해 CSS 최소화) */
        .streamlit-expanderHeader {
            background-color: #f7f7f7;
            border-radius: 8px;
            padding: 10px;
            font-size: 1.1em !important;
        }
        
        </style>
        """,
        unsafe_allow_html=True,
    )

def page_header():
    """앱 제목 및 상태 초기화"""
    apply_custom_styles() 
    
    st.title("🚗 너는 왜 자동차과에 왔니?")
    st.subheader("고등학교 1학년, 나의 꿈을 찾는 진로 탐색 앱")
    st.divider()

    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = 1
        st.session_state.car_data = {}
        st.session_state.selected_job = None
        st.session_state.final_color = None
        st.session_state.student_name = 'OO공고 학생'

def calculate_job_scores(factors):
    """1단계 선호 동인을 기반으로 직무 추천 점수 계산"""
    scores = {job: 0 for job in JOB_WEIGHTS}
    
    factor_keys = factors if isinstance(factors, list) else [] 
    
    for factor in factor_keys:
        for job, weights in JOB_WEIGHTS.items():
            scores[job] += weights.get(factor, 0)
            
    sorted_jobs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_jobs

def stage_1_dreamcar():
    """1단계: 드림카 비전보드 및 선호 동인 분석"""
    st.header("1단계: 나의 드림카 비전보드 만들기")
    
    st.session_state.student_name = st.text_input("당신의 이름을 입력해주세요.", value=st.session_state.student_name)
    st.markdown("---")

    # 1-1. 동력원 선택
    st.markdown("##### 1. 당신이 꿈꾸는 자동차의 핵심 동력원을 선택해주세요.")
    st.session_state.car_data['engine'] = st.radio(
        "동력원 선택", list(CAR_MODELS_EXTENDED.keys()), index=None, horizontal=True, label_visibility="collapsed"
    )

    if st.session_state.car_data['engine']:
        engine_type = st.session_state.car_data['engine']
        
        # 1-2. 브랜드 및 모델 선택
        st.markdown(f"##### 2. {engine_type} 분야에서 가장 관심 있는 브랜드와 모델을 선택해주세요.")
        
        brands = list(CAR_MODELS_EXTENDED.get(engine_type, {}).keys())
        brand_col, model_col = st.columns(2)
        
        with brand_col:
            st.session_state.car_data['brand'] = st.selectbox("브랜드 선택", brands, index=None, placeholder="브랜드 선택", key="brand_select")
        
        if st.session_state.car_data['brand']:
            brand = st.session_state.car_data['brand']
            models = CAR_MODELS_EXTENDED[engine_type][brand]
            
            with model_col:
                st.session_state.car_data['model'] = st.selectbox("모델 선택 (다양한 차종 포함)", models, index=None, placeholder="모델 선택", key="model_select")

            # 1-2-1. 색상 선택
            if st.session_state.car_data['model']:
                st.markdown("##### 3. 나의 드림카 색상을 선택해주세요.")
                st.session_state.final_color = st.selectbox(
                    "색상 선택", COLOR_OPTIONS, index=0, key="color_select"
                )
                
                model = st.session_state.car_data['model']
                
                # 1-3. 드림카 비전보드 최종 화면 (시각화 강조)
                st.markdown("---")
                st.markdown("### 나의 드림카 비전보드 완성!")
                
                # 이미지 플레이스홀더 영역
                st.markdown(f"""
                <div style="background-color: #f0f2f6; height: 300px; border-radius: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center; border: 5px solid {st.session_state.final_color.lower() if st.session_state.final_color else '#ccc'};">
                    <h3 style="color:#333;">선택된 드림카 이미지 영역</h3>
                    <p style="color:#555;">[모델: {brand} {model} / 색상: {st.session_state.final_color}]</p>
                    <p style="color:red; font-weight:bold;">🚨 실제 앱에서는 고품질 이미지를 URL로 연결해야 합니다.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 1-4. 나의 드림카 코멘트
                st.session_state.car_data['comment'] = st.text_area(
                    "나의 드림카 코멘트 (이 차에 대한 나의 꿈이나 생각)", 
                    placeholder="예: '이 차를 언젠가 직접 튜닝해보고 싶어요!'",
                    key="comment_area"
                )
                
                # 1-5. 선호 동인 분석 (2단계 직무 매칭의 기초 자료)
                st.markdown("---")
                st.markdown("### 4. 이 차를 선택한 가장 결정적인 이유는 무엇인가요? (최대 3가지)")
                
                selected_factors = []
                cols = st.columns(2)
                for i, (key, desc) in enumerate(DRIVING_FACTORS.items()):
                    if cols[i % 2].checkbox(f'{key}. {desc}', key=f'factor_{key}'):
                        selected_factors.append(key)
                
                st.session_state.car_data['factors'] = selected_factors
                
                if st.button("2단계: 미래 직무 연결하기"):
                    if len(selected_factors) > 0:
                        st.session_state.current_stage = 2
                        st.rerun()
                    else:
                        st.error("결정적인 이유(선호 동인)를 최소 1가지 선택해주세요.")

def stage_2_job_matching():
    """2단계: 산업 수요 브리핑 및 6가지 직무 선택"""
    st.header("2단계: 현장 실무 중심 직무 연결")
    
    # 2-1. 산업 수요 브리핑 (강조 내용 포함)
    st.markdown("### 미래 자동차 산업, 왜 유망할까요? **(당신의 직업이 안정적인 이유)**")
    st.info("""
    **1. 지금 당장 밖에서 보이는 모든 차들이 일거리!** (안정적인 수요)
    **2. 자동차 정비/수리의 불변의 가치:** 기계가 대체할 수 없는 **사람의 숙련된 손기술**이 핵심!
    **3. 시대 변화에 적응하는 기술의 연속성:** 내연기관 경험이 미래 EV 정비의 튼튼한 기초가 됩니다.
    """)
    
    st.markdown("---")
    
    # 2-2. 직무 추천 결과 표시 및 상호작용 강화
    factors = st.session_state.car_data.get('factors', [])
    recommended_jobs_scored = calculate_job_scores(factors)
    
    st.markdown("### 나에게 맞는 직무 추천 결과")
    
    if recommended_jobs_scored:
        top_job_name = recommended_jobs_scored[0][0]
        st.warning(f"1단계 드림카 분석 결과, **'{top_job_name}'** 직무가 당신에게 가장 높은 추천 점수를 받았습니다! 👍")
    
    st.markdown("---")
    
    # 2-3. 6가지 핵심 직무 카드 제시 (Expander를 활용하여 상세 정보 제공)
    st.markdown("### 6가지 핵심 직무 카드를 눌러 자세히 알아보세요")
    
    job_choices = list(JOB_ROLES.keys())
    
    for job_name in job_choices:
        job_info = JOB_ROLES[job_name]
        
        # 추천 점수 표시 (상위 3개 직무에 '추천!' 마크 표시)
        is_top_job = any(job_name == job[0] for job in recommended_jobs_scored[:3])
        score_text = " (추천!)" if is_top_job else " (⭐)"
        
        # Expander 제목은 단순 문자열로 구성하여 오류 방지
        with st.expander(f"{job_name}{score_text}"):
            st.markdown(f"**✅ 주요 역할:** {job_info['desc']}")
            st.markdown(f"**💡 필요 역량:** **{job_info['need']}** (3단계 로드맵의 기초!)")

            
    st.markdown("---")

    # 2-4. 최종 직무 선택
    st.markdown("### ✅ 1. 이 6가지 직무 중, 당신의 꿈에 가장 가까운 직무를 **최종 선택**해주세요.")
    st.session_state.selected_job = st.selectbox(
        "최종 선택 직무", job_choices, index=None, placeholder="직무 선택", key="final_job_select"
    )
    
    if st.session_state.selected_job:
        st.success(f"최종 목표 직무: **{st.session_state.selected_job}**")
        if st.button("3단계: 3년 학습 로드맵 설계하기"):
            st.session_state.current_stage = 3
            st.rerun()
    
    if st.button("이전 단계 (1단계)로 돌아가기", key="back_to_stage1"):
        st.session_state.current_stage = 1
        st.rerun()

def stage_3_roadmap():
    """3단계: 3년 학습 로드맵 설계 및 최종 시각화"""
    st.header("3단계: 나만의 3년 학습 로드맵 만들기")
    
    selected_job = st.session_state.selected_job
    student_name = st.session_state.get('student_name', 'OO공고 학생')
    
    if selected_job:
        st.markdown(f"## 🙋‍♂️ **{student_name} 학생의 3년 맞춤형 학습 로드맵**")
        st.info(f"선택 직무: **{selected_job}** | 목표: 현장 전문가 및 미래 커리어 설계")
        st.markdown("---")
        
        # -----------------------------------------------------------
        # 최종 로드맵 요약 (한눈에 보기) - 학기별 세분화
        # -----------------------------------------------------------
        st.markdown("### 🏆 최종 로드맵 요약 (고교 3년 학기별 계획)")

        # 데이터 정리 및 병합
        roadmap_data_list = []
        for year, year_data in ROADMAP_ACADEMIC.items():
            core_goal = year_data['목표']
            
            for semester in ['1학기', '2학기']:
                activities = year_data[semester]
                
                # 고2 심화 활동 추가
                if year == '고2':
                    job_sim_activities = ROADMAP_JOB_SIMULATOR.get(selected_job, {}).get('고2_심화', [])
                    activities = activities + job_sim_activities
                
                # 고3 목표 텍스트 추가
                g3_goal_text = ""
                if year == '고3' and semester == '1학기':
                     g3_goal_text = f" (최종 목표: {ROADMAP_JOB_SIMULATOR.get(selected_job, {}).get('고3_목표_텍스트', '진로 설정 중')})"

                roadmap_data_list.append({
                    '학년/학기': f"**{year} {semester}**",
                    '핵심 목표': core_goal if semester == '1학기' else '', # 학년 시작 시점에 한 번만 표시
                    '주요 활동': "\n- " + "\n- ".join(activities) + g3_goal_text
                })

        df_academic = pd.DataFrame(roadmap_data_list)
        
        # '핵심 목표'가 비어있는 행을 이전 행의 값으로 채우기 (시각화 목적)
        df_academic['핵심 목표'] = df_academic['핵심 목표'].replace('', method='ffill')
        
        # 테이블 최종 출력 (세로 폭을 넓게 하여 깔끔하게 보이도록 마크다운 테이블 대신 st.dataframe 사용)
        st.dataframe(df_academic, hide_index=True, use_container_width=True, height=500)
        
        st.markdown("---")

        # 3. 고3 이후 최종 진로 경로 (선택의 기회) - 단순 마크다운으로 오류 방지
        st.markdown("### 🎯 고3 이후 최종 진로 경로 (선택의 기회)")
        
        st.markdown("#### 💼 아우스빌둥 (일학습 병행) - 메인 취업처")
        st.markdown("- **혜택:** 대학 등록금 지원, 매월 **100만원 지원금** + 신입 정직원 급여 지급.")
        st.markdown("- **경로:** 2년제 대학(1학기) → 군 복무(18개월) → 복학 → 회사 복귀(3년 트레이닝) → 정직원")
        
        st.markdown("#### 🏭 일반 취업 후 재직자 전형 (대학 진학 목표)")
        st.markdown("- **경로:** 고3 10월 이후 3개월 현장실습 → 1월 근로계약 체결 및 취업.")
        st.markdown("- **혜택:** **3년 근속** 시 **특성화고 재직자 전형**을 통해 서울 시내 대학 진학 가능.")
        
        st.markdown("#### 🏢 공기업 및 공무원")
        st.markdown("- **요건:** 고2까지 보통교과 평균 3.5 이상, 전문교과 50% 이상 A등급.")
        st.markdown("- **전형:** 학교장 추천 (인원 제한 있음) → **NCS 시험** 및 면접.")
        
        st.markdown("#### 🎓 기타 진학 경로")
        st.markdown("- **국내 대학 연계:** 여주대, 두원공과대 등 수시/수능 전형.")
        st.markdown("- **연계 사업:** P-TECH (폴리텍 일학습 병행), 계약학부.")

        st.success(f"**{student_name} 학생**, 이 로드맵이 당신의 성공적인 3년을 위한 지침서가 될 것입니다! 🚀")
        
    else:
        st.warning("직무 선택이 필요합니다. 2단계로 돌아가서 직무를 선택해주세요.")
        if st.button("2단계로 돌아가기"):
            st.session_state.current_stage = 2
            st.rerun()

# --- 3. 메인 앱 실행 로직 ---

page_header()

if st.session_state.current_stage == 1:
    stage_1_dreamcar()
elif st.session_state.current_stage == 2:
    stage_2_job_matching()
elif st.session_state.current_stage == 3:
    stage_3_roadmap()