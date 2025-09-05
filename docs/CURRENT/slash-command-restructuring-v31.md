<!--
@meta
id: planning_20250905_1115_slash_command_restructuring
type: planning
status: draft
scope: strategic
created: 2025-09-05
updated: 2025-09-05
tags: slash-commands, restructuring, TADD, automation
related: project_rules.md, CLAUDE.md
-->

# 슬래시 커맨드 구조화 프로젝트 v31.0

## 🎯 프로젝트 목표

**현황**: 25개 슬래시 커맨드, 약 60% 중복률로 사용자 혼란 가중
**목표**: TADD 철학 기반 9개 핵심 커맨드로 64% 간소화하여 인지 부하 최소화

## 🏗️ 최종 아키텍처 설계

### **2-Track 하이브리드 시스템**

```
🔍 탐색 트랙 (Understanding) - 3개
├── /분석     → 5단계 완전 분석 사이클 (탐색→수렴→정제→보고서→정리)
├── /찾기     → 문서찾기 + 컨텍스트 통합  
└── /보고     → 주간보고 + 보고서작업 통합

🛠️ TADD 실행 트랙 (Implementation) - 4개  
├── /기획     → LLM 지능형 라우팅 (5개 모드: 분석/기획/비전/전략/로드맵)
├── /테스트   → Failing Tests 우선 생성 (TADD 강제)
├── /구현     → 테스트 통과 구현 (Red→Green)
└── /배포     → 검증 + 배포 + 자동 정리 (6개 통합)

⚡ 특수 트랙 (Special) - 2개
├── /실험     → 실험시작 + 실험완료 통합
└── /전체사이클 → 기존 유지 (TADD 4단계 자동 진행)
```

## 🧠 핵심 혁신 포인트

### **1. LLM 기반 지능형 라우팅**
**기존**: 키워드 매칭 (너무 단순)
```
"비전" → 비전수립 (80% 자동) // 안일함
```

**신규**: 컨텍스트 기반 LLM 판단
```markdown
# /기획 실행 시 자동 분석
**🤖 LLM이 다음을 종합 분석:**
- 프로젝트 현재 단계 (초기/개발/운영)
- 요청의 시간 범위 (즉시/단기/장기)  
- 영향 범위 (기능/시스템/비즈니스)
- 구체성 수준 (아이디어/요구사항/구현계획)
- 의사결정 필요도 (정보수집/전략결정/실행계획)

**자동 라우팅 예시:**
"우리 서비스를 해외에 출시하려면..." 
→ LLM 분석: 장기적 + 비즈니스 레벨 → 비전수립 모드

"로그인 버튼 색깔 바꿔줘"
→ LLM 분석: 즉시 + 기능 레벨 → 기능 기획 모드
```

### **2. 분석 완전체 복원**
**기존**: 탐색만 (불완전)

**신규**: `/분석` 커맨드 5단계 풀 워크플로우
```markdown
# /분석 커맨드 (완전체)
**🔄 5단계 자동 진행:**

1. **탐색** → 현황 파악, 데이터 수집
2. **수렴** → 패턴 식별, 핵심 이슈 도출  
3. **정제** → 분석 결과 구조화, 검증
4. **보고서** → docs/analysis/ 자동 저장
5. **정리** → 컨텍스트 아카이빙, 액션 아이템 추출

**최종 산출물:**
- 분석 보고서 (시각화 포함)
- 액션 아이템 리스트 
- 다음 단계 추천 (/기획 or /구현 제안)
```

### **3. 3-Layer 자동 문서화 시스템**
**기존 문제**: 안정화/레포정리/세션마감/문서정리 → 중복 + 부담

**신규 해결책**:
```markdown
# 📚 지능형 문서화 시스템

**Layer 1: 실시간 자동화** (무의식적)
├── 모든 작업 → docs/CURRENT/ 실시간 기록
├── Git hook → 커밋마다 CLAUDE.md 자동 동기화
└── TodoWrite → active-todos.md 실시간 업데이트

**Layer 2: 주기별 스마트 정리** (semi-auto)
├── 5번째 커밋마다 → 자동 문서 분류 트리거
├── 완료 작업 → docs/archive/ 자동 이관
└── 중요 결정사항 → docs/decisions/ 자동 추출

**Layer 3: 세션 종료 시점** (/배포 내장)
├── 전체 세션 요약 → weekly-summary.md 생성
├── 미완료 TODO → 다음 세션으로 이관
└── 컨텍스트 최적화 → .claudeignore 자동 업데이트
```

### **4. TADD 강제 시스템**
**핵심**: 테스트 우선 작성 → 구현 → 검증 순서 철저히 준수

```markdown
# TADD 워크플로우
1. /기획 → PRD + 실패하는 테스트 생성
2. /테스트 → Theater Testing 자동 차단, Real Testing 강제
3. /구현 → 테스트 통과 목표로 최소 구현
4. /배포 → 전체 검증 + 자동 정리
```

## 📊 커맨드 통합 매핑

### **기존 25개 → 신규 9개 매핑**

| 신규 커맨드 | 통합되는 기존 커맨드들 | 통합 개수 |
|------------|---------------------|----------|
| `/분석` | 분석 | 1개 |
| `/기획` | 기획, 기획구현, 비전수립, 전략기획, 로드맵관리 | 5개 |
| `/테스트` | 검증, 극한검증, 품질보증, TADD강화, 테스트강화 | 5개 |
| `/구현` | 구현 | 1개 |
| `/배포` | 안정화, 문서정리, 레포정리, 개발완료, 배포, 세션마감 | 6개 |
| `/찾기` | 문서찾기, 컨텍스트 | 2개 |
| `/보고` | 주간보고, 보고서작업 | 2개 |
| `/실험` | 실험시작, 실험완료 | 2개 |
| `/전체사이클` | 전체사이클 | 1개 |
| **합계** | **25개** | **25개** |

## 🎯 예상 효과

| 항목 | 현재 | 최적화 후 | 개선율 |
|------|------|-----------|--------|
| 커맨드 수 | 25개 | 9개 | **64% 감소** |
| 중복 기능 | 15개 | 0개 | **100% 제거** |
| 학습 비용 | 높음 | 낮음 | **75% 감소** |
| 사용 효율 | 60% | 95% | **35% 향상** |
| TADD 준수율 | 60% | 95% | **35% 향상** |

## 🚀 구현 계획

### **Phase 1: 핵심 4개 커맨드 리팩토링** (우선순위 1)
1. `/분석` → 5단계 완전 사이클 + 메타데이터 자동 생성
2. `/기획` → LLM 지능형 라우팅 + 메타데이터 자동 생성  
3. `/테스트` → TADD 강제 시스템 + Theater Testing 차단
4. `/배포` → 자동 정리 통합 + 3-Layer 문서화

### **Phase 2: 통합 커맨드 구현** (우선순위 2)
1. `/찾기` → 문서찾기 + 컨텍스트 기능 통합
2. `/보고` → 주간보고 + 보고서작업 통합
3. `/실험` → 실험시작 + 실험완료 통합

### **Phase 3: 별칭 처리 및 마이그레이션** (우선순위 3)
- 25개 기존 커맨드 → 새로운 커맨드로 리디렉트
- 점진적 마이그레이션 메시지 표시
- 사용자 가이드 자동 생성

## 🔧 메타데이터 시스템 강화

**기존 메타데이터 완전 보존 + 자동화 강화:**
```markdown
<!--
@meta
id: [type]_[timestamp]_[feature]
type: [implementation|test_report|documentation|analysis|planning]
status: draft|review|published|archived
created: [date]
updated: [date]
scope: strategic|tactical|operational
tags: [relevant-tags]
related: [linked-documents]
-->
```

**자동화 기능:**
1. **자동 타입 감지**: 커맨드별 자동 type 할당
2. **지능형 상태 관리**: 생성→완료→아카이빙 자동 전환
3. **자동 연관 관계**: PRD↔requirements.md 자동 링크

## 🧪 테스트 전략

### **Real Testing 강제 기준:**
```python
# ❌ Theater Testing (자동 거부)
def test_installation():
    assert os.path.exists('file')  # REJECTED: 너무 추상적
    print("✅ Pass")  # REJECTED: 의미없는 출력

# ✅ Real Testing (필수 포함)
def test_korean_command_installation():
    """사용자가 init.sh 실행 시 한글 명령어 사용 가능"""
    # Given: 구체적 초기 상태
    with tempfile.TemporaryDirectory() as tmpdir:
        # When: 실제 행동 실행
        result = subprocess.run(['./init.sh', 'test'], 
                              capture_output=True, timeout=30)
        
        # Then: 구체적 검증
        cmd_path = Path(f'{tmpdir}/test/.claude/commands/기획.md')
        assert cmd_path.exists(), "파일 미생성"
        assert cmd_path.stat().st_size > 1000, f"크기 부족: {cmd_path.stat().st_size}"
        assert '404' not in cmd_path.read_text(), "에러 콘텐츠"
        
        # And: 에러 케이스
        with mock.patch('urllib.request.urlopen', side_effect=Exception):
            fallback_result = run_with_network_error()
            assert 'fallback' in fallback_result
```

### **품질 게이트:**
- 테스트 통과율: 100%
- Mock 사용률: < 20%
- Coverage: > 15% (프로젝트 기준)
- Theater Testing: 0개

## 🎉 성공 기준

1. **기능적 요구사항:**
   - ✅ 9개 커맨드로 25개 기능 완전 대체
   - ✅ TADD 워크플로우 100% 준수
   - ✅ 메타데이터 자동 생성 100%
   - ✅ 3-Layer 문서화 시스템 작동

2. **품질 요구사항:**
   - ✅ 모든 테스트 통과
   - ✅ GitHub Actions 100% 통과
   - ✅ Real Testing 비율 > 80%
   - ✅ Theater Testing 0개

3. **사용성 요구사항:**
   - ✅ 기존 사용자 워크플로우 100% 보존
   - ✅ 별칭을 통한 백워드 호환성
   - ✅ 학습 비용 75% 감소 달성

## 🔄 지속적 개선

**모니터링 지표:**
- 커맨드 사용 빈도 분석
- 사용자 피드백 수집
- 에러 발생률 추적
- TADD 준수율 측정

**정기 검토:**
- 월간 사용성 리뷰
- 분기별 아키텍처 최적화
- 반기별 전체 구조 재평가

---

**이것이 25개→9개 슬래시 커맨드 구조화의 마스터 플랜입니다. TADD 철학과 사용자 경험을 모두 만족하는 혁신적 설계로 프로젝트 복잡성을 64% 감소시킵니다.**