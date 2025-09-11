# 🔬 Research Project Manager 사용 가이드

## 📖 Overview
ResearchProjectManager는 바이오인포매틱스 및 연구 프로젝트를 체계적으로 관리하기 위한 도구입니다. 
재귀적 디렉토리 감지 기능으로 프로젝트의 어느 하위 디렉토리에서도 자동으로 프로젝트를 인식합니다.

## 🚀 Quick Start

### 1. Python에서 직접 사용

```python
from research_project_manager import ResearchProjectManager

# Manager 초기화
manager = ResearchProjectManager()

# 새 프로젝트 시작
result = manager.init_project(
    name="drug_discovery", 
    description="Novel drug target identification using ML"
)
print(f"Project created: {result['project_id']}")
```

### 2. Claude Code와 함께 사용 (권장)

Claude Code 세션에서 다음과 같이 요청하세요:

```
"신약 개발 연구 프로젝트를 시작해줘. 
머신러닝을 사용한 타겟 발굴이 목적이야."
```

## 📋 주요 기능 (11개 서브커맨드)

### 1. 프로젝트 초기화 (`init`)
```python
# 새 연구 프로젝트 생성
result = manager.init_project(
    "protein_analysis",
    "단백질 구조 예측 및 기능 분석"
)

# 생성되는 구조:
# research_projects/
#   └── 2025-09-09_protein_analysis/
#       ├── notebooks/     # Jupyter 노트북
#       ├── data/          # 데이터 파일
#       ├── results/       # 분석 결과
#       ├── figures/       # 시각화
#       ├── docs/          # 문서
#       └── scripts/       # 스크립트
```

### 2. 프로젝트 상태 확인 (`status`)
```python
# 현재 활성 프로젝트 상태 조회
current_project = manager.metadata.get("active_project")
if current_project:
    project_info = manager.metadata["projects"][current_project]
    print(f"Active project: {project_info['name']}")
    print(f"Status: {project_info.get('status', 'active')}")
    print(f"Milestones: {len(project_info.get('milestones', []))}")
```

### 3. 진행사항 추적 (`progress`)
```python
# 진행사항 기록
manager.track_progress(
    "Completed data preprocessing: 10,000 samples cleaned",
    files=["notebooks/01_preprocessing.ipynb", "data/cleaned_data.csv"]
)

# 타임라인에 자동 기록됨
```

### 4. 마일스톤 설정 (`milestone`)
```python
# 중요 마일스톤 설정
manager.set_milestone(
    "Data Collection Complete",
    "All required datasets downloaded and validated"
)

# 마일스톤 달성률 자동 계산
```

### 5. 프로젝트 목록 (`list`)
```python
# 모든 프로젝트 나열
projects = manager.list_projects()
for project in projects:
    print(f"- {project['name']}: {project['status']} ({project['created']})")
```

### 6. 프로젝트 전환 (`switch`)
```python
# 다른 프로젝트로 전환
manager.switch_project("2025-09-08_protein_analysis")
# 이제 모든 작업이 해당 프로젝트에서 수행됨
```

### 7. 프로젝트 아카이빙 (`archive`)
```python
# 완료된 프로젝트 아카이빙
archive_result = manager.archive_project()
# 최종 보고서 자동 생성 + 상태를 'archived'로 변경
```

### 8. 데이터 탐색 (`explore`)
```python
# EDA 노트북 자동 생성
result = manager.explore_data("Initial exploration of gene expression data")
# notebooks/에 EDA 템플릿 노트북 생성
```

### 9. 가설 설정 (`hypothesis`)
```python
# 연구 가설 기록
manager.set_hypothesis(
    "High expression of BRCA1 correlates with drug resistance"
)
# 가설 검증 추적 시스템 활성화
```

### 10. 실험 시작 (`experiment`)
```python
# 새 실험 세션 시작
result = manager.start_experiment(
    "rf_baseline",
    "Random Forest baseline model for prediction"
)
# experiments/ 디렉토리에 실험 환경 구성
```

### 11. 결과 검증 (`validate`)
```python
# 결과 검증 스크립트 생성
result = manager.validate_results("Cross-validation of model performance")
# 자동 검증 스크립트 생성 및 실행
```

## 🎯 실제 사용 시나리오

### 시나리오 1: 신약 개발 프로젝트
```python
# 1. 프로젝트 시작
manager = ResearchProjectManager()
manager.init_project("drug_discovery", "COVID-19 antiviral development")

# 2. 데이터 탐색
manager.explore_data("Analyzing compound library")

# 3. 진행사항 추적
manager.track_progress("Screened 10,000 compounds", 
                       ["notebooks/screening.ipynb"])

# 4. 마일스톤 설정
manager.set_milestone("Lead compounds identified", 
                     "Top 10 candidates selected")

# 5. 실험 시작
manager.start_experiment("in_vitro_validation", 
                        "Cell-based assay validation")

# 6. 결과 검증
manager.validate_results("Statistical validation of IC50 values")
```

### 시나리오 2: 디렉토리 자동 감지
```python
# 깊은 하위 디렉토리에서 작업 중이어도 자동 감지
os.chdir("research_projects/2025-09-09_drug_discovery/notebooks/experiments/ml/")

# Manager가 자동으로 프로젝트 감지
manager = ResearchProjectManager()
print(manager.metadata["active_project"])  # "2025-09-09_drug_discovery"

# 바로 작업 가능
manager.track_progress("Completed deep learning model training")
```

### 시나리오 3: 여러 프로젝트 관리
```python
manager = ResearchProjectManager()

# 프로젝트 A 작업
manager.switch_project("2025-09-09_proteomics")
manager.track_progress("Mass spec data analyzed")

# 프로젝트 B로 전환
manager.switch_project("2025-09-08_genomics")  
manager.track_progress("Variant calling completed")

# 전체 프로젝트 상태 확인
for project in manager.list_projects():
    print(f"{project['name']}: {project['progress']}%")
```

## 🔒 보안 기능

### 입력 검증
```python
# 위험한 문자 자동 제거
manager.init_project("../../etc/passwd", "hack")
# → "2025-09-09_etcpasswd" (안전하게 정규화됨)

# 한글 지원
manager.init_project("신약개발/프로젝트", "의약품 연구")
# → "2025-09-09_신약개발프로젝트" (특수문자만 제거)
```

## 📊 고급 기능

### 체크포인트 시스템
```python
# 중요 시점 저장
checkpoint_id = manager.checkpoint("Need to install new analysis tool")

# 나중에 복원
manager.resume_from_checkpoint(checkpoint_id)
```

### 도구 인벤토리
```python
# 사용 가능한 분석 도구 확인
tools = manager.list_tools()
for category, tool_list in tools["categories"].items():
    print(f"{category}: {', '.join(tool_list)}")
```

### 결과 공유
```python
# 공유 패키지 생성
result = manager.share_results()
# share/ 디렉토리에 README, requirements.txt, 주요 결과 포함
```

## 💡 Best Practices

1. **프로젝트명 규칙**
   - 영문, 숫자, 한글 사용 가능
   - 특수문자는 자동 제거됨
   - 날짜가 자동으로 prefix로 추가됨

2. **진행사항 추적**
   - 매일 주요 작업 기록
   - 관련 파일 함께 기록
   - 마일스톤으로 큰 성과 표시

3. **디렉토리 구조**
   - notebooks/: 분석 노트북
   - data/raw/: 원본 데이터 (수정 금지)
   - data/processed/: 처리된 데이터
   - results/: 최종 결과물
   - figures/: 발표용 그림

4. **협업**
   - Git과 함께 사용 권장
   - .research_metadata.json은 공유
   - checkpoint로 동기화 지점 생성

## 🐛 문제 해결

### Q: 프로젝트가 감지되지 않음
```python
# 수동으로 프로젝트 루트 지정
manager = ResearchProjectManager(base_dir="/path/to/research_projects")
```

### Q: 권한 오류 발생
```bash
# 디렉토리 권한 확인
chmod 755 research_projects/
```

### Q: 메타데이터 손상
```python
# 메타데이터 재구성
manager.rebuild_metadata()  # 모든 프로젝트 다시 스캔
```

## 📚 추가 자료

- [BDD 시나리오](tests/scenarios/directory_detection_redesign.md)
- [테스트 예제](tests/test_research_project_manager.py)
- [API 문서](docs/api/research_project_manager.md)

## 🎉 시작하기

```python
# 가장 간단한 시작
from research_project_manager import ResearchProjectManager

manager = ResearchProjectManager()
manager.init_project("my_research", "My awesome research project")
print("🚀 연구 프로젝트가 시작되었습니다!")
```

---

**Version**: 1.0.0  
**Last Updated**: 2025-09-09  
**Author**: Claude Code with ResearchProjectManager