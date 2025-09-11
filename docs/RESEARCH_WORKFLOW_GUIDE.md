# 🔬 연구-개발 통합 워크플로우 가이드

## 🎯 명확한 역할 분리

### 개발 작업 (도구 만들기)
**사용 커맨드**: `/구현`, `/테스트`, `/검증`
**작업 위치**: `src/` 디렉토리
**목적**: 재사용 가능한 기능/API/라이브러리 구현

```bash
# 예시: SMILES 분석 도구 개발
/구현 "SMILES 유효성 검증 함수"
/테스트 "validate_smiles 함수"
```

### 연구 작업 (도구 사용하기)
**사용 커맨드**: `/연구` (모든 연구 활동)
**작업 위치**: `research_projects/` 디렉토리
**목적**: 특정 연구 질문에 답하기 위한 실험/분석

```bash
# 예시: 약물 독성 예측 연구
/연구 init "drug_toxicity" "약물 독성 예측 모델 개발"
/연구 track "10,000개 분자 분석 완료"
/연구 milestone "Model v1.0" "초기 모델 완성"
```

## 🔄 다중 연구 프로젝트 관리

### 1. 프로젝트 구조
```
research_projects/
├── .research_metadata.json          # 전체 메타데이터
├── 2025-09-09_drug_toxicity/       # 연구 1
│   ├── timeline.md                 # 자동 추적
│   ├── notebooks/                  # Jupyter 분석
│   └── tools@ -> ../../src/        # 개발 도구 링크
│
├── 2025-09-10_molecular_similarity/ # 연구 2
│   └── ...
│
└── 2025-09-11_protein_binding/     # 연구 3
    └── ...
```

### 2. 활성 프로젝트 자동 감지

#### 방법 1: 메타데이터 기반 (기본)
```bash
# 현재 활성 프로젝트 확인
/연구 status
# → 🔬 Active: drug_toxicity

# 작업은 자동으로 활성 프로젝트에 기록
/연구 track "새로운 발견"
# → drug_toxicity/timeline.md에 기록
```

#### 방법 2: 디렉토리 기반 (자동 감지)
```bash
# 특정 연구 디렉토리에서 작업
cd research_projects/2025-09-10_molecular_similarity/
/연구 track "분자 유사도 계산"
# → 현재 디렉토리 감지하여 molecular_similarity에 기록
```

#### 방법 3: 명시적 전환
```bash
# 프로젝트 목록 확인
/연구 list
# 📚 Research Projects:
# 🟢 drug_toxicity (활성)
# ⚪ molecular_similarity
# ⚪ protein_binding

# 프로젝트 전환
/연구 switch "molecular_similarity"
# → ✅ Switched to molecular_similarity
```

### 3. 프로젝트별 컨텍스트 격리

각 연구는 독립적으로 관리됨:
- **타임라인**: 각 프로젝트별 timeline.md
- **체크포인트**: 프로젝트별 .checkpoints/
- **환경**: 각 프로젝트별 environment.json
- **결과**: 독립적인 results/ 디렉토리

## 📋 실전 시나리오

### 시나리오 1: 새로운 연구 시작
```bash
# 1. 새 연구 프로젝트 초기화
/연구 init "covid_drug_repurposing" "코로나 치료제 재창출"

# 2. 자동으로 활성화됨
/연구 status
# → Active: covid_drug_repurposing

# 3. 연구 진행
/연구 track "FDA 승인 약물 DB 로드"
/연구 track "분자 도킹 시뮬레이션 시작"
```

### 시나리오 2: 여러 연구 병행
```bash
# 오전: 약물 독성 연구
/연구 switch "drug_toxicity"
/연구 track "Random Forest 모델 학습"

# 오후: 분자 유사도 연구
/연구 switch "molecular_similarity"
/연구 track "Tanimoto 계수 계산 완료"

# 각 연구의 타임라인은 독립적으로 관리됨
```

### 시나리오 3: 연구에서 개발 필요 발견
```bash
# 연구 중 새로운 도구 필요
/연구 track "기존 도구로 처리 불가능한 3D 구조 발견"

# 개발 모드로 전환
/구현 "3D 분자 구조 분석 함수"
# → src/molecular/structure_3d.py 생성

# 개발 완료 후 연구로 복귀
/연구 track "새 3D 분석 도구로 재분석 시작"
```

## 🤖 지능형 자동 감지 메커니즘

### 우선순위 (높은 순)
1. **명시적 지정**: `/연구 --project "project_name"`
2. **현재 디렉토리**: `pwd`가 research_projects/xxx 내부
3. **최근 활동**: 최근 5분 내 작업한 프로젝트
4. **메타데이터**: .research_metadata.json의 active_project
5. **유일한 프로젝트**: 프로젝트가 1개만 있을 때

### 충돌 해결
```python
def detect_target_project():
    # 1. 현재 디렉토리 확인
    if is_inside_research_project():
        return extract_project_from_path()
    
    # 2. 최근 활동 확인
    if recent_activity := get_recent_activity(minutes=5):
        return recent_activity.project_id
    
    # 3. 활성 프로젝트 사용
    if active := metadata.get("active_project"):
        return active
    
    # 4. 애매한 경우 확인 요청
    projects = list_all_projects()
    if len(projects) > 1:
        print("🤔 어느 프로젝트에 기록할까요?")
        for i, p in enumerate(projects):
            print(f"{i+1}. {p.name}")
        choice = input("선택: ")
        return projects[int(choice)-1]
    
    return projects[0] if projects else None
```

## 💡 베스트 프랙티스

### DO ✅
- 연구 시작 시 명확한 이름으로 프로젝트 생성
- 주요 진전마다 milestone 설정
- 프로젝트 전환 시 명시적 switch
- 완료된 연구는 archive로 정리

### DON'T ❌
- 여러 연구를 하나의 프로젝트에 혼합
- 개발 코드를 research_projects/에 작성
- 연구 데이터를 src/에 저장
- 프로젝트 전환 없이 다른 연구 작업

## 📊 상태 확인 명령어

```bash
# 전체 연구 프로젝트 현황
/연구 list

# 현재 활성 프로젝트
/연구 status  

# 특정 프로젝트 타임라인
cat research_projects/[project_id]/timeline.md

# 프로젝트 메타데이터
cat research_projects/.research_metadata.json
```

## 🔮 향후 개선 계획

1. **자동 분류**: 연구 주제별 자동 태깅
2. **협업 지원**: 여러 연구자 동시 작업
3. **시각화**: 연구 진행 대시보드
4. **통합 검색**: 모든 연구 결과 통합 검색