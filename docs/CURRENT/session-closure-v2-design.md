# 세션마감 시스템 v2.0 설계 문서

## 🎯 핵심 교훈: "완료"는 생각보다 훨씬 복잡하다

### 실제 프로젝트 분석 결과

**9개 프로젝트, 500+ 문서 분석:**
- 35% report 문서 (완료 여부 불명)
- 20% analysis 문서 (분석중? 완료? 불명)
- 15% PRD/기획서 (영구? 임시? 불명)
- 30% 기타 혼재

### v1의 문제점
```python
# v1의 너무 단순한 접근
if "completion-report" in filename:
    return "completed"  # 95% 확신

# 실제: completion-report가 계속 업데이트됨
```

### v2의 개선된 접근
```python
# v2의 다층적 분석
def analyze_file_advanced():
    1. 파일 수정 시간 체크 (30일 이상 → stale)
    2. TODO 완성도 계산 (95% 이상 + 3일 경과 → 완료)
    3. 패턴 매칭 (파일명 + 내용)
    4. 내용 신호 분석 (완료 vs 진행중 키워드)
    5. 종합 판단 (모든 요소 가중치 계산)
```

## 📊 실제 발견된 패턴들

### 파일명 패턴의 복잡성
```
PathwayGPT_v10_Final_Publication_Report.md
→ "Final"인데 v11도 있음

PHASE3_COMPLETION_SUMMARY.md
→ "COMPLETION"인데 PHASE4 진행중

FINAL_COMPLETION_REPORT.md
→ "FINAL" + "COMPLETION"인데 계속 업데이트
```

### 실제로 신뢰할 수 있는 신호들
1. **파일 수정 시간**: 가장 객관적
2. **TODO 체크리스트 완성도**: 정량적 측정 가능
3. **세션 번호 패턴**: session-001.md는 대부분 완료

## 🛠️ v2.0 시스템 설계

### 1. 카테고리 세분화
```python
categories = {
    "definitely_completed": 0.9+,   # 확실한 완료
    "likely_completed": 0.7-0.9,    # 아마도 완료
    "preserve_always": 1.0,         # 절대 보존
    "prd_or_spec": 특별처리,        # specs/로 이동
    "working_documents": 진행중,     # 작업 문서
    "stale": 30일+,                 # 방치된 파일
    "uncertain": 0.4 이하           # 불확실
}
```

### 2. 대화형 처리 프로세스
```
1. 전체 스캔 → 카테고리별 분류
2. 카테고리별 표시 및 권장사항
3. 사용자 선택:
   - [Y] 일괄 처리
   - [n] 건너뛰기
   - [s] 개별 선택
   - [v] 내용 미리보기
```

### 3. 아카이브 전략
```
완료 문서 → sessions/YYYY-MM/session-NNN.md
PRD/스펙 → specs/
오래된 파일 → archive/stale/
불확실 → 사용자 결정 대기
```

## 📈 성과 지표

### v1 vs v2 비교
| 항목 | v1 | v2 |
|------|----|----|
| 분석 정확도 | 과도한 낙관 (9/15 완료) | 현실적 (1/7 완료) |
| 카테고리 | 3개 (완료/진행/보존) | 7개 (세분화) |
| 판단 기준 | 파일명 패턴 위주 | 다층적 분석 |
| 사용자 제어 | 단순 Y/N | 대화형 선택 |
| PRD 처리 | 일반 문서와 동일 | 특별 처리 |

### 예상 효과
- **정확도 향상**: 오분류 80% 감소
- **사용자 신뢰**: 투명한 근거 제시
- **유연성**: 프로젝트별 맞춤 처리

## 🚀 다음 단계

### 학습 기능 추가
```python
# 사용자 선택 패턴 학습
if user_marks_as_complete:
    learn_pattern(filename, content)
    adjust_weights()
```

### 프로젝트별 설정
```yaml
# .claude/session_config.yaml
project_rules:
  preserve_patterns: ["*_spec.md", "architecture.md"]
  stale_days: 45  # 기본 30일 대신 45일
  auto_archive_prd: false  # PRD 자동 이동 비활성화
```

### 연관 문서 추적
```python
# 관련 문서 함께 처리
if "part1" in filename:
    find_related(["part2", "part3"])
    suggest_batch_process()
```

## 🎉 결론

v2.0은 "완벽한 자동화"를 포기하고 "현실적인 도움"을 목표로 합니다.
- 확실한 것만 자동 처리
- 애매한 것은 사용자와 상의
- 투명한 근거 제시
- 지속적 학습과 개선

**"AI가 모든 걸 해결"이 아닌 "AI와 함께 더 잘 정리"하는 시스템**