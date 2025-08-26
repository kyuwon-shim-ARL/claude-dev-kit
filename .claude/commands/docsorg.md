# /문서정리 - 프로젝트 문서 체계화

## 명령어 개요
흩어진 문서를 프로젝트 구조와 로드맵에 맞춰 체계적으로 정리

## 사용법
```
/문서정리 [프로젝트명]
/문서정리  # 현재 프로젝트 자동 감지
```

## Claude 실행 프로세스

### 1단계: 문서 수집 및 분석
```python
def collect_documents():
    # 프로젝트 관련 문서 검색
    - docs/CURRENT/*
    - docs/analysis/*
    - *.md 파일들
    - 테스트 보고서
    - 분석 결과
```

### 2단계: 로드맵 기반 분류
```python
def classify_by_roadmap():
    categories = {
        "01-hypothesis": ["기획", "가설", "배경"],
        "02-design": ["설계", "아키텍처", "인터페이스"],
        "03-implementation": ["구현", "코드", "개발"],
        "04-analysis": ["분석", "결과", "통계"],
        "05-validation": ["검증", "테스트", "품질"],
        "06-documentation": ["문서", "보고서", "논문"]
    }
    # 키워드와 내용 기반 자동 분류
```

### 3단계: 프로젝트 구조 생성/정리
```bash
projects/{프로젝트명}/
├── README.md           # 프로젝트 개요 (자동 생성/업데이트)
├── roadmap.md          # 로드맵과 현재 진행상황
├── 01-hypothesis/      
│   └── [관련 문서 이동]
├── 02-design/
│   └── [관련 문서 이동]
├── 03-implementation/
│   └── [관련 문서 이동]
├── 04-analysis/
│   └── [관련 문서 이동]
├── 05-validation/
│   └── [관련 문서 이동]
└── 06-documentation/
    └── [관련 문서 이동]
```

### 4단계: 진행 상황 분석
```python
def analyze_progress():
    return {
        "completed_phases": [],
        "current_phase": "",
        "completion_rate": "",
        "next_steps": [],
        "blockers": []
    }
```

### 5단계: 인덱스 및 상태 업데이트
```markdown
# {프로젝트명} 문서 인덱스

## 📊 진행 현황
- 전체 진행률: 65%
- 현재 단계: 04-analysis
- 다음 마일스톤: 검증 시작

## 📁 문서 구조
### 01-hypothesis (완료)
- initial-hypothesis.md
- literature-review.md

### 02-design (완료)
- experimental-design.md
- sample-preparation.md

### 03-implementation (완료)
- data-collection.md
- preprocessing.md

### 04-analysis (진행중)
- deg-analysis.md
- pathway-analysis.md

### 05-validation (대기)
### 06-documentation (대기)

## 🔗 빠른 링크
- [최근 분석 결과](04-analysis/latest-results.md)
- [주요 발견사항](04-analysis/key-findings.md)
- [다음 단계 계획](roadmap.md#next-steps)
```

## 실제 실행 예시

### 입력:
```
/문서정리 "RNA-seq-2024"
```

### Claude 실행:
1. docs/ 폴더에서 RNA-seq 관련 문서 검색
2. 각 문서의 내용과 날짜 분석
3. projects/RNA-seq-2024/ 구조 생성
4. 문서를 적절한 하위 폴더로 이동/복사
5. README.md와 roadmap.md 자동 생성/업데이트
6. 진행 상황 요약 제시

### 출력:
```
✅ RNA-seq-2024 프로젝트 문서 정리 완료

📊 정리 결과:
- 총 23개 문서 발견
- 6개 카테고리로 분류
- 현재 진행률: 65% (분석 단계)

📁 생성된 구조:
projects/RNA-seq-2024/
├── README.md (업데이트됨)
├── roadmap.md (생성됨)
├── 01-hypothesis/ (3개 문서)
├── 02-design/ (4개 문서)
├── 03-implementation/ (5개 문서)
├── 04-analysis/ (8개 문서)
├── 05-validation/ (1개 문서)
└── 06-documentation/ (2개 문서)

💡 다음 단계 제안:
- 분석 결과 검증 필요
- qPCR validation 계획 수립
- 논문 초안 작성 시작

📝 상세 내용: projects/RNA-seq-2024/README.md
```

## 주요 기능

### 자동 처리
- 문서 키워드 기반 자동 분류
- 중복 문서 감지 및 병합
- 버전 관리 (날짜 기반)
- 진행률 자동 계산

### 수동 확인
- 애매한 분류는 사용자에게 확인
- 중요 문서 우선순위 지정
- 커스텀 카테고리 추가 가능

## 연계 워크플로우

```bash
# 1. 프로젝트 시작
/프로젝트시작 "RNA-seq-2024"

# 2. 개발/분석 진행
/기획, /구현, /분석 ...

# 3. 주기적 문서 정리
/문서정리 "RNA-seq-2024"  # 매주 실행

# 4. 진행 상황 보고
/주간보고  # 전체 프로젝트 조망
```

## 효과

1. **체계화**: 로드맵에 따른 문서 구조
2. **추적성**: 프로젝트 진행 상황 한눈에 파악
3. **효율성**: 필요한 문서 빠르게 찾기
4. **일관성**: 모든 프로젝트 동일한 구조

---
*프로젝트의 현재 위치와 다음 단계를 명확히 합니다.*