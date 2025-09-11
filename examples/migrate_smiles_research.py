#!/usr/bin/env python3
"""
SMILES Research Project Migration Script
기존 SMILES_property_webapp 연구를 ResearchProjectManager로 체계화
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_manager_hybrid import HybridResearchManager


def migrate_smiles_research():
    """SMILES 연구 프로젝트를 ResearchProjectManager로 마이그레이션"""
    
    print("\n" + "=" * 70)
    print("   🔬 SMILES Research Project Migration")
    print("=" * 70)
    
    # 1. Manager 초기화
    manager = HybridResearchManager()
    print("\n✅ ResearchProjectManager 초기화 완료")
    
    # 2. 프로젝트 생성
    print("\n📁 연구 프로젝트 생성 중...")
    result = manager.init_project(
        "smiles_rgcca_chemical_space",
        "RGCCA 기반 화학물질 활성 예측 및 화학 공간 분석 연구"
    )
    
    if "error" not in result:
        project_id = result.get("project_id")
        print(f"✅ 프로젝트 생성: {project_id}")
        print(f"📁 위치: {result.get('path')}")
    else:
        print(f"⚠️ 프로젝트가 이미 존재합니다. 기존 프로젝트 사용.")
        # 기존 프로젝트로 전환
        projects = manager.list_projects()
        for p in projects:
            if "smiles" in p['name'].lower():
                manager.switch_project(p['id'])
                project_id = p['id']
                break
    
    # 3. 과거 진행사항 복원
    print("\n📝 과거 연구 기록 복원 중...")
    past_progress = [
        ("2025-08-26: 프로젝트 시작, SMILES 웹앱 기본 구조 설계"),
        ("2025-09-01: 화학물질 분석 파이프라인 초기 구현"),
        ("2025-09-03: RGCCA v1 - 118차원에서 62차원으로 축소"),
        ("2025-09-05: RGCCA v2 - Sparse L1 정규화 추가 (tau=0.7)"),
        ("2025-09-08: Chemical Space Analysis - Multi-fingerprint 전략"),
        ("2025-09-09: v4.0 완성 - Dual Pipeline (ROC-AUC 0.7144)")
    ]
    
    for progress in past_progress:
        manager.track_progress(progress)
        print(f"   ✓ {progress[:30]}...")
    
    # 4. 핵심 가설 설정
    print("\n💡 연구 가설 설정 중...")
    hypotheses = [
        "RGCCA 차원 축소가 화학적 해석가능성을 유지하면서 예측 성능 개선",
        "Multi-fingerprint (Morgan+MACCS+RDKit)가 화학 공간을 더 잘 표현",
        "Sparse L1 정규화가 과적합 방지 및 일반화 성능 향상"
    ]
    
    for hypothesis in hypotheses:
        manager.set_hypothesis(hypothesis)
        print(f"   ✓ {hypothesis[:40]}...")
    
    # 5. 실험 기록
    print("\n🧪 수행한 실험들 기록 중...")
    experiments = [
        ("baseline_rdkit", "RDKit descriptors only baseline"),
        ("rgcca_v1_basic", "Basic RGCCA 차원 축소"),
        ("rgcca_v2_sparse", "Sparse RGCCA with L1"),
        ("multi_fingerprint", "통합 fingerprint 전략"),
        ("dual_pipeline_v4", "최종 통합 dual pipeline")
    ]
    
    for exp_name, exp_desc in experiments:
        manager.start_experiment(exp_name, exp_desc)
        print(f"   ✓ {exp_name}: {exp_desc}")
        
        # 최종 실험 결과 기록
        if exp_name == "dual_pipeline_v4":
            manager.track_progress(
                f"실험 {exp_name} 완료: ROC-AUC 0.7144, 해석가능성 0.605 달성"
            )
    
    # 6. 마일스톤 설정
    print("\n🏁 주요 마일스톤 설정 중...")
    milestones = [
        ("RGCCA 구현", "차원 축소 파이프라인 구축 완료"),
        ("해석가능성 구축", "SHAP + Loading weights 통합"),
        ("Chemical Space", "Multi-fingerprint 전략 구현"),
        ("v4.0 Production", "ROC-AUC 0.7144 달성")
    ]
    
    for name, desc in milestones:
        manager.set_milestone(name, desc)
        print(f"   ✓ {name}: {desc}")
    
    # 7. 체크포인트 생성
    print("\n💾 체크포인트 생성 중...")
    checkpoint_result = manager.checkpoint(
        "SMILES 연구 ResearchProjectManager 마이그레이션 완료"
    )
    print(f"✅ 체크포인트 ID: {checkpoint_result.get('checkpoint_id')}")
    
    # 8. 현재 상태 요약
    print("\n" + "=" * 70)
    print("   📊 마이그레이션 완료 - 프로젝트 현황")
    print("=" * 70)
    
    project_info = manager.metadata["projects"][project_id]
    
    print(f"""
프로젝트: {project_info.get('name')}
상태: {project_info.get('status', 'active')}
진행사항: {len(project_info.get('progress', []))}개 기록
가설: {len(project_info.get('hypotheses', []))}개 설정
실험: {len(project_info.get('experiments', []))}개 수행
마일스톤: {len(project_info.get('milestones', []))}개 달성

📁 프로젝트 위치: research_projects/{project_id}
📄 타임라인: research_projects/{project_id}/timeline.md
""")
    
    return manager, project_id


def setup_daily_workflow(manager, project_id):
    """일일 연구 워크플로우 예시"""
    
    print("\n" + "=" * 70)
    print("   📅 일일 연구 워크플로우 설정")
    print("=" * 70)
    
    print("""
이제부터 다음과 같이 연구를 진행하세요:

# 아침: 연구 시작
manager.execute("진행", "오늘 목표: [목표 입력]")

# 실험 수행
manager.start_experiment("[실험명]", "[설명]")
manager.track_progress("[진행사항]", ["관련파일.py"])

# 결과 검증
manager.validate_results("[검증 내용]")

# 저녁: 체크포인트
manager.checkpoint("[오늘 완료 사항, 내일 계획]")
""")
    
    # 예시 워크플로우 실행
    print("\n💡 예시 실행:")
    manager.execute("진행", "오늘 목표: RGCCA 하이퍼파라미터 최적화")
    print("✅ 오늘 연구 시작 기록됨")


def create_research_dashboard_template(project_id):
    """Research Dashboard 템플릿 생성"""
    
    dashboard_code = '''import streamlit as st
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
    project_id = "''' + project_id + '''"
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
'''
    
    # Dashboard 파일 저장
    dashboard_path = Path(f"research_projects/{project_id}/dashboard.py")
    dashboard_path.write_text(dashboard_code)
    
    print(f"\n📊 Research Dashboard 템플릿 생성됨:")
    print(f"   파일: {dashboard_path}")
    print(f"   실행: streamlit run {dashboard_path}")


if __name__ == "__main__":
    print("\n🚀 SMILES Research Migration 시작\n")
    
    # 1. 마이그레이션 실행
    manager, project_id = migrate_smiles_research()
    
    # 2. 일일 워크플로우 설정
    setup_daily_workflow(manager, project_id)
    
    # 3. Dashboard 템플릿 생성
    create_research_dashboard_template(project_id)
    
    print("\n" + "=" * 70)
    print("   🎉 마이그레이션 완료!")
    print("=" * 70)
    
    print(f"""
✅ SMILES 연구가 성공적으로 체계화되었습니다!

다음 단계:
1. 타임라인 확인: cat research_projects/{project_id}/timeline.md
2. 대시보드 실행: streamlit run research_projects/{project_id}/dashboard.py
3. 일일 기록 시작: 위 워크플로우 참조

💡 Tip: 이제부터 모든 연구 활동을 ResearchProjectManager로 기록하세요!
""")