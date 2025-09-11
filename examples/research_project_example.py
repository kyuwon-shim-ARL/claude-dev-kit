#!/usr/bin/env python3
"""
Research Project Manager 실제 사용 예제
실제 연구 워크플로우를 시뮬레이션합니다.
"""

import sys
from pathlib import Path
from datetime import datetime
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_project_manager import ResearchProjectManager


def drug_discovery_workflow():
    """신약 개발 연구 프로젝트 전체 워크플로우 예제"""
    
    print("🔬 신약 개발 연구 프로젝트 시작")
    print("=" * 50)
    
    # 1. 프로젝트 초기화
    manager = ResearchProjectManager()
    result = manager.init_project(
        "drug_discovery_ml",
        "Machine learning for drug target identification"
    )
    
    project_id = result.get("project_id")
    print(f"✅ 프로젝트 생성: {project_id}")
    print(f"📁 위치: {result.get('path')}")
    time.sleep(1)
    
    # 2. 초기 데이터 탐색
    print("\n📊 데이터 탐색 시작...")
    explore_result = manager.explore_data(
        "Exploring ChEMBL database for compound activity data"
    )
    print(f"✅ EDA 노트북 생성: {explore_result.get('notebook_path')}")
    time.sleep(1)
    
    # 3. 연구 가설 설정
    print("\n🎯 연구 가설 설정...")
    hypothesis = "Graph neural networks can predict drug-target interactions better than traditional fingerprint methods"
    hyp_result = manager.set_hypothesis(hypothesis)
    print(f"✅ 가설 등록: {hypothesis[:50]}...")
    time.sleep(1)
    
    # 4. 데이터 수집 진행사항
    print("\n📥 데이터 수집 진행...")
    progress_updates = [
        ("Downloaded ChEMBL database: 2.1M compounds", ["data/chembl_compounds.csv"]),
        ("Extracted protein targets: 13,000 unique targets", ["data/protein_targets.csv"]),
        ("Generated molecular fingerprints", ["notebooks/02_fingerprints.ipynb"]),
    ]
    
    for message, files in progress_updates:
        result = manager.track_progress(message, files)
        print(f"  ✓ {message}")
        time.sleep(0.5)
    
    # 5. 첫 번째 마일스톤
    print("\n🏁 마일스톤 달성...")
    milestone_result = manager.set_milestone(
        "Data Preparation Complete",
        "All datasets collected, cleaned, and features extracted"
    )
    print(f"✅ 마일스톤: Data Preparation Complete")
    time.sleep(1)
    
    # 6. 실험 시작
    print("\n🧪 머신러닝 실험 시작...")
    experiments = [
        ("random_forest_baseline", "Random Forest with Morgan fingerprints"),
        ("gnn_model_v1", "Graph Neural Network initial architecture"),
        ("ensemble_model", "Ensemble of RF and GNN"),
    ]
    
    for exp_name, exp_desc in experiments:
        exp_result = manager.start_experiment(exp_name, exp_desc)
        print(f"  🔬 실험: {exp_name}")
        
        # 실험 진행사항 기록
        manager.track_progress(
            f"Training {exp_name}: accuracy=0.{85+experiments.index((exp_name, exp_desc))*3}",
            [f"experiments/{exp_name}/model.pkl"]
        )
        time.sleep(0.5)
    
    # 7. 결과 검증
    print("\n✔️ 결과 검증...")
    validation_result = manager.validate_results(
        "Cross-validation and statistical significance testing"
    )
    print(f"✅ 검증 스크립트 생성: {validation_result.get('script_path')}")
    time.sleep(1)
    
    # 8. 체크포인트 생성
    print("\n💾 체크포인트 생성...")
    checkpoint_result = manager.checkpoint("Models trained, ready for hyperparameter tuning")
    checkpoint_id = checkpoint_result.get("checkpoint_id")
    print(f"✅ 체크포인트 ID: {checkpoint_id}")
    time.sleep(1)
    
    # 9. 프로젝트 상태 확인
    print("\n📈 전체 프로젝트 상태:")
    # 현재 프로젝트 정보 직접 접근
    current_project = manager.metadata.get("active_project")
    if current_project and current_project in manager.metadata["projects"]:
        project_info = manager.metadata["projects"][current_project]
        print(f"  프로젝트: {project_info.get('name')}")
        print(f"  상태: {project_info.get('status', 'active')}")
        milestones = project_info.get('milestones', [])
        print(f"  마일스톤: {len(milestones)}개 설정")
        print(f"  실험: {len(experiments)}개 완료")
    
    # 10. 결과 공유 준비
    print("\n📤 결과 공유 패키지 준비...")
    share_result = manager.share_results()
    print(f"✅ 공유 패키지: {share_result.get('share_path')}")
    
    print("\n" + "=" * 50)
    print("🎉 신약 개발 연구 프로젝트 워크플로우 완료!")
    print(f"📁 프로젝트 위치: research_projects/{project_id}")
    

def multi_project_management():
    """여러 프로젝트 동시 관리 예제"""
    
    print("\n🔄 다중 프로젝트 관리 예제")
    print("=" * 50)
    
    manager = ResearchProjectManager()
    
    # 여러 프로젝트 생성
    projects = [
        ("genomics_study", "Whole genome sequencing analysis"),
        ("proteomics_ms", "Mass spectrometry proteomics"),
        ("metabolomics", "Metabolic pathway analysis"),
    ]
    
    created_projects = []
    for name, desc in projects:
        result = manager.init_project(name, desc)
        created_projects.append(result.get("project_id"))
        print(f"✅ Created: {result.get('project_id')}")
    
    # 프로젝트 간 전환하며 작업
    print("\n프로젝트 전환 및 작업:")
    for i, project_id in enumerate(created_projects):
        manager.switch_project(project_id)
        manager.track_progress(f"Initial setup for project {i+1}")
        print(f"  ✓ Switched to {project_id}")
    
    # 전체 프로젝트 목록 확인
    print("\n📋 전체 프로젝트 목록:")
    all_projects = manager.list_projects()
    for proj in all_projects:
        status_icon = "🟢" if proj["status"] == "active" else "⚫"
        print(f"  {status_icon} {proj['name']} - {proj['description'][:30]}...")
    
    print("\n✅ 다중 프로젝트 관리 예제 완료")


def directory_detection_demo():
    """디렉토리 자동 감지 데모"""
    
    print("\n🔍 디렉토리 자동 감지 데모")
    print("=" * 50)
    
    # 프로젝트 생성
    manager = ResearchProjectManager()
    result = manager.init_project("auto_detect_test", "Testing directory detection")
    project_id = result.get("project_id")
    project_path = Path(result.get("path"))
    
    print(f"✅ 프로젝트 생성: {project_id}")
    
    # 깊은 하위 디렉토리 생성
    deep_path = project_path / "notebooks" / "experiments" / "deep" / "nested"
    deep_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 깊은 디렉토리로 이동: {deep_path.relative_to(Path.cwd())}")
    
    # 해당 디렉토리에서 새 manager 생성 (시뮬레이션)
    # 실제로는 os.chdir()를 사용하지만, 여기서는 설명만
    print("\n시뮬레이션: 깊은 디렉토리에서 작업")
    print("  manager = ResearchProjectManager()")
    print(f"  자동 감지됨: {project_id}")
    print("  ✅ 어느 하위 디렉토리에서도 프로젝트 인식!")
    
    print("\n✅ 디렉토리 감지 데모 완료")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  Research Project Manager - 실제 사용 예제")
    print("=" * 60)
    
    # 1. 신약 개발 워크플로우
    drug_discovery_workflow()
    
    # 2. 다중 프로젝트 관리
    multi_project_management()
    
    # 3. 디렉토리 자동 감지
    directory_detection_demo()
    
    print("\n" + "=" * 60)
    print("  모든 예제 실행 완료! 🎉")
    print("=" * 60)
    print("\n💡 Tip: 실제 사용 시에는 Jupyter Notebook에서")
    print("   인터랙티브하게 사용하는 것을 권장합니다.")