# 연구 관리 방법 비교: Python vs Bash

## 방법 1: Python ResearchProjectManager (기능 풍부)

```python
# Python 모듈 필요
from research_manager_hybrid import HybridResearchManager

m = HybridResearchManager()
m.switch_project("2025-09-10_smiles_rgcca_chemical_space")
m.track_progress("RGCCA 하이퍼파라미터 최적화 완료")
m.set_milestone("최적화 완료", "최적 파라미터 발견")
```

**장점:**
- 복잡한 데이터 처리 가능
- JSON 메타데이터 관리
- 자동 백업 및 복원
- 프로젝트 간 전환 편리

**단점:**
- Python 설치 필요
- 사용자 레포에 스크립트 추가
- 의존성 관리 필요

## 방법 2: 슬래시 커맨드 + Bash (간단함)

```bash
# /research-simple 슬래시 커맨드 사용
/research-simple track "RGCCA 하이퍼파라미터 최적화 완료"
/research-simple milestone "최적화 완료" "최적 파라미터 발견"
/research-simple status
```

**장점:**
- Python 불필요
- 사용자 레포에 추가 파일 없음
- 시스템 독립적
- Git 친화적 (텍스트 파일만)

**단점:**
- 고급 기능 제한
- 프로젝트 전환 수동
- 복잡한 쿼리 어려움

## 실제 사용 예시: SMILES 연구 프로젝트

### 1. 오늘의 연구 시작
```bash
# Bash 방식
/research-simple track "$(date +%Y-%m-%d) 연구 시작"
/research-simple hypothesis "Attention mechanism이 RGCCA보다 효과적일 것"
```

### 2. 실험 진행
```bash
# 실험 시작
/research-simple experiment attention_v1 "Self-attention layer 추가"

# 결과 기록 (파일에 직접)
echo "## Results" >> research_projects/*/experiments/*attention_v1/README.md
echo "- Accuracy: 0.8234" >> research_projects/*/experiments/*attention_v1/README.md
echo "- ROC-AUC: 0.7892" >> research_projects/*/experiments/*attention_v1/README.md
```

### 3. 마일스톤 달성
```bash
/research-simple milestone "Attention 구현" "Self-attention 메커니즘 완성"
```

### 4. 체크포인트 생성
```bash
/research-simple checkpoint "오늘 작업 완료, 내일 하이퍼파라미터 튜닝"
```

### 5. 진행 상황 확인
```bash
/research-simple status
```

### 6. 검색
```bash
# 특정 키워드 검색
/research-simple search "attention"
/research-simple search "RGCCA"
```

### 7. 백업
```bash
# 전체 연구 프로젝트 백업
/research-simple backup
```

## 권장 사용 시나리오

### Python이 적합한 경우:
- 데이터 분석이 많은 연구
- 자동화가 중요한 프로젝트
- 여러 프로젝트 동시 관리
- 복잡한 메타데이터 추적

### Bash가 적합한 경우:
- 간단한 진행 기록
- 일회성 연구 프로젝트
- Python 설치 불가 환경
- 최소한의 의존성 선호

## 하이브리드 접근법

```bash
# 1. 기본 관리는 Bash로
/research-simple init my_research "연구 설명"
/research-simple track "진행사항"

# 2. 복잡한 분석이 필요할 때만 Python
python -c "
import json
from pathlib import Path

# 타임라인 분석
timeline = Path('research_projects/2025-09-10_smiles_rgcca_chemical_space/timeline.md').read_text()
entries = timeline.count('##') - 1  # 헤더 제외
print(f'총 {entries}개 진행사항 기록')

# 실험 통계
exp_dir = Path('research_projects/2025-09-10_smiles_rgcca_chemical_space/experiments')
experiments = list(exp_dir.glob('*'))
print(f'총 {len(experiments)}개 실험 완료')
"
```

## 결론

- **80% 사용 사례**: Bash로 충분
- **20% 고급 기능**: Python 선택적 사용
- **핵심**: 파일 시스템이 데이터베이스 역할
- **장점**: 사용자 레포 깔끔 유지