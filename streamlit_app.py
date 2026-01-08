import json
import streamlit as st
from pathlib import Path

BASE = Path(__file__).parent

st.set_page_config(page_title="Streamlit Lecture Samples", page_icon="🎈", layout="wide")

st.title("🎈 수업용 Streamlit 애플리케이션 예시 모음")

st.markdown("""
    이 페이지는 수업·실습에서 사용할 수 있는 Streamlit 예제 페이지들을 모아둔 페이지입니다.            
    Streamlit 애플리케이션을 개발할 때, **아이디어 탐색용**으로 활용하시길 바랍니다.            
    왼쪽 사이드바에서 페이지를 선택하거나 아래 링크를 통해 웹 애플리케이션 원본으로 이동할 수 있습니다.
    
    본 페이지에 저장된 각 콘텐츠의 저작권은 **원작자**(콘텐츠마다 기재)에게 있으며, 예시용 페이지로 옮겨오는 과정에서 원본과 조금 다르게 표시될 수 있습니다.
"""
    
)

def discover_pages(pages_dir: Path):
    """pages 디렉터리에서 .py 파일을 찾아 제목(파일명)과 첫 줄 설명을 추출합니다."""
    pages = []
    p_dir = pages_dir
    if not p_dir.exists():
        return pages
    for p in sorted(p_dir.glob("*.py")):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            text = ""
        # 파일에서 첫 번째 주석/문자열 설명 줄을 찾음
        desc = "(설명 없음)"
        for line in text.splitlines():
            s = line.strip()
            if s.startswith('#'):
                desc = s.lstrip('# ').strip()
                break
            if s.startswith('"') or s.startswith("'"):
                # 간단한 문자열 리터럴로 된 설명
                desc = s.strip('"').strip("'")[:200]
                break
        pages.append({"filename": p.name, "path": str(p.relative_to(BASE)), "description": desc})
    return pages


def load_meta(meta_path: Path):
    """메타파일(pages/_meta.json)을 불러옵니다. 없으면 빈 dict을 반환합니다."""
    try:
        if meta_path.exists():
            return json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {}


def save_meta(meta_path: Path, meta: dict):
    """메타파일을 저장합니다."""
    try:
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception as e:
        st.error(f"메타 저장 실패: {e}")
        return False


pages = discover_pages(BASE / "pages")
meta_path = BASE / "pages" / "_meta.json"
meta = load_meta(meta_path)

if pages:
    st.subheader("콘텐츠 목록")
    st.markdown("아래 목록을 확인하신 후, 좌측 사이드 바에서 해당 콘텐츠로 이동하세요.")
    for pg in pages:
        # 메타에서 제목/설명/제작자 가져오기(없으면 기본값)
        title = meta.get(pg['filename'], {}).get('title', pg['filename'])
        desc = meta.get(pg['filename'], {}).get('description', pg['description'])
        creator = meta.get(pg['filename'], {}).get('creator', "")

        # display_name: 숫자_제목.py -> 제목 (언더스코어와 확장자 사이의 텍스트)
        display_name = pg['filename']
        if '_' in display_name:
            try:
                display_name = display_name.split('_', 1)[1]
            except Exception:
                pass
        if '.' in display_name:
            display_name = display_name.rsplit('.', 1)[0]

        with st.expander(title, expanded=False):
            st.write(desc)
            if creator:
                st.markdown(f"**제작자:** {creator}")
            st.markdown(f"좌측 사이드 바에서 **{display_name}** 선택")
            # meta에 원본 URL(original_url)이 있으면 링크로 표시
            original = meta.get(pg['filename'], {}).get('original_url', '')
            if original:
                # 일반 마크다운 링크로 표시
                st.markdown(f"- 원본 출처: [{original}]({original})")
            st.write("---")
else:
    st.info("`pages/` 디렉터리에 예제 페이지가 없습니다. `pages/` 폴더에 `.py` 파일을 추가하세요.")

st.caption("프로젝트: streamlit-lecture-project — 교육용 Streamlit 예제 모음")
