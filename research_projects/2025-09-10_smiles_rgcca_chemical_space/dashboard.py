import streamlit as st
from pathlib import Path
import sys
sys.path.append("../src")
from research_manager_hybrid import HybridResearchManager

st.set_page_config(page_title="SMILES Research Dashboard", layout="wide")
st.title("🔬 SMILES Research Dashboard")

# Manager 초기화
manager = HybridResearchManager()

# 사이드바
with st.sidebar:
    st.header("프로젝트 정보")
    project_id = "2025-09-10_smiles_rgcca_chemical_space"
    manager.switch_project(project_id)
    
    if st.button("진행사항 새로고침"):
        st.rerun()

# 메인 대시보드
col1, col2, col3, col4 = st.columns(4)

project_info = manager.metadata["projects"][project_id]

with col1:
    st.metric("진행사항", len(project_info.get("progress", [])))
    
with col2:
    st.metric("실험 수", len(project_info.get("experiments", [])))
    
with col3:
    st.metric("마일스톤", len(project_info.get("milestones", [])))
    
with col4:
    st.metric("가설", len(project_info.get("hypotheses", [])))

# 타임라인
st.header("📅 연구 타임라인")
timeline_file = Path(f"research_projects/{project_id}/timeline.md")
if timeline_file.exists():
    with st.expander("타임라인 보기", expanded=True):
        st.markdown(timeline_file.read_text())

# 빠른 입력
st.header("✍️ 빠른 기록")
col1, col2 = st.columns([3, 1])

with col1:
    note = st.text_input("진행사항 입력")
    
with col2:
    if st.button("기록", type="primary"):
        if note:
            manager.track_progress(note)
            st.success("기록 완료!")
            st.rerun()

# 실험 섹션
st.header("🧪 실험 관리")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    exp_name = st.text_input("실험명")
    
with col2:
    exp_desc = st.text_input("실험 설명")
    
with col3:
    if st.button("실험 시작"):
        if exp_name:
            manager.start_experiment(exp_name, exp_desc)
            st.success(f"실험 '{exp_name}' 시작됨!")
            st.rerun()
