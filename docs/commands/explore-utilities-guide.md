# /탐구 커맨드 사용 가이드

> **마이그레이션 노트**: 이 문서는 2025-09-13에 simple_smiles_PCA 프로젝트에서 claude-dev-kit으로 이전되었습니다.
> - 원본 위치: `docs/commands/explore-command-guide.md`
> - 새 위치: `docs/commands/explore-utilities-guide.md`
> - 핵심 기능은 `scripts/explore_utilities.py`에 구현됨


## 개요
`/탐구` 커맨드는 데이터 분석 과정을 투명하게 기록하고 추적하는 도구입니다. 단순히 결과만 보여주는 것이 아니라, 그 결과에 도달하는 모든 과정과 기준을 투명하게 공개합니다.

## 핵심 철학
**"Show the Journey, Not Just the Destination"** 🔍

- **투명성**: 모든 분석 과정이 추적 가능
- **설명성**: 모든 결정에 이유 포함
- **재현성**: 100% 재현 가능한 연구

## 사용법

### 기본 사용
```python
from scripts.explore_utilities import explore_main

# 데이터 준비
data = {
    "dataset": "compounds.csv",
    "type": "SMILES",
    "compounds": ["CCO", "CC(C)O", "c1ccccc1"],
    "objective": "Find chemical patterns",
    "seed": 42  # 재현성을 위한 시드
}

# 탐구 실행
result = explore_main(data)

# 결과 확인
print(f"발견된 패턴: {result['patterns_found']}개")
print(f"최종 신뢰도: {result['confidence']:.2f}")
print(f"보고서 위치: {result['report_path']}")
```

### 상세 사용
```python
from scripts.explore_utilities import (
    ExploreCommand,
    ConvergenceEngine,
    ConfidenceTracker,
    DecisionEngine
)

# 1. 탐색 실행
explorer = ExploreCommand()
exploration_result = explorer.explore(data)

# 2. 수렴 과정 추적
engine = ConvergenceEngine()
convergence_result = engine.converge(data)

# 3. 신뢰도 추적
tracker = ConfidenceTracker()
for method in ["pca", "umap", "tsne"]:
    confidence = tracker.add_evidence({
        "method": method, 
        "result": f"{method} completed"
    })
    print(f"{method} 후 신뢰도: {confidence:.2f}")

# 4. 의사결정 투명화
decision_engine = DecisionEngine()
decision = decision_engine.make_decision({
    "data_quality": 0.95,
    "pattern_strength": 0.8,
    "consensus_level": 0.85
})
```

## 출력 구조

### 탐색 로그
```json
{
    "exploration_log": [
        {
            "module": "validation",
            "timestamp": "2024-01-01T10:00:00",
            "input": {...},
            "output": {"valid": true, "count": 100},
            "decision": "Proceed with valid data",
            "criteria": "Validation rate > 95%"
        }
    ]
}
```

### 수렴 과정
```json
{
    "convergence_process": {
        "iterations": [
            {
                "iteration": 1,
                "hypothesis": "5 clusters exist",
                "evidence": [...],
                "confidence": 0.85,
                "decision": "Continue for higher confidence"
            }
        ]
    }
}
```

### 의사결정 트리
```json
{
    "decision_path": [
        {
            "condition": "data_quality > 0.9",
            "evaluated_value": 0.95,
            "threshold": 0.9,
            "passed": true,
            "reasoning": "High quality data required"
        }
    ]
}
```

## 보고서 생성

탐구가 완료되면 자동으로 마크다운 형식의 보고서가 생성됩니다:
- 위치: `reports/exploration_report_[timestamp].md`
- 내용: 탐색 경로, 수렴 과정, 최종 결과, 재현 정보

## 주요 특징

### 1. 완전한 투명성
- 모든 시도와 실패가 기록됨
- 각 단계의 입력과 출력이 보존됨
- 의사결정 기준이 명시됨

### 2. 재현 가능성
- 동일한 시드로 100% 재현 가능
- 모든 파라미터가 기록됨
- 재현 스크립트 자동 생성

### 3. 신뢰도 추적
- 증거가 누적될수록 신뢰도 상승
- 각 단계별 신뢰도 변화 기록
- 최종 신뢰도 점수 제공

### 4. 의사결정 투명화
- 모든 결정 기준이 명시됨
- 통과/실패 여부와 이유 기록
- 최종 결론의 근거 제시

## 활용 예시

### 화학 물질 패턴 분석
```python
data = {
    "dataset": "drug_compounds.csv",
    "type": "SMILES",
    "size": 10000,
    "objective": "Identify drug-like patterns"
}

result = explore_main(data)
# → 5개의 약물 유사 패턴 발견 (신뢰도 92%)
```

### 데이터 품질 검증
```python
data = {
    "dataset": "screening_results.csv",
    "type": "activity_data",
    "objective": "Validate data quality"
}

result = explore_main(data)
# → 데이터 품질 95%, 3% 이상치 발견
```

## API 레퍼런스

### ExploreCommand
- `explore(data: Dict) -> Dict`: 데이터 탐구 실행

### ConvergenceEngine
- `converge(data: Dict) -> Dict`: 패턴 수렴 실행

### ConfidenceTracker
- `add_evidence(evidence: Dict) -> float`: 증거 추가 및 신뢰도 반환
- `get_progression_history() -> List[Dict]`: 진행 이력 반환

### DecisionEngine
- `make_decision(scenario: Dict) -> Dict`: 시나리오 기반 의사결정

## 문제 해결

### Q: 재현이 안 되는 경우
A: `seed` 파라미터가 동일한지 확인하세요.

### Q: 신뢰도가 낮은 경우
A: 더 많은 분석 방법을 추가하거나 데이터 품질을 개선하세요.

### Q: 보고서가 생성되지 않는 경우
A: `reports/` 디렉토리가 존재하는지 확인하세요.

## 향후 계획
- 실제 SMILES 데이터 처리 통합
- 대화형 HTML 보고서 생성
- 실시간 진행 상황 모니터링
- 다중 데이터셋 비교 분석