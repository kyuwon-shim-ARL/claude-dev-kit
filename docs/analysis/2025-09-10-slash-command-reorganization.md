# 슬래시 커맨드 재구성 계획

## 📅 분석 정보
- **날짜**: 2025-09-10 09:05
- **목적**: 슬래시 커맨드 체계 재정립
- **원칙**: Simple is Better

## 🎯 재구성 원칙

### 1. 핵심 철학
- **KISS (Keep It Simple, Stupid)**
- **Do One Thing Well**
- **Convention over Configuration**

### 2. 명령어 분류

#### 🔵 핵심 워크플로우 (유지)
```
/기획    → 요구사항 분석, 설계
/구현    → 코드 작성, 개발
/테스트  → 검증, 품질 확인
/배포    → 커밋, 푸시, 태깅
```

#### 🟢 보조 명령어 (유지)
```
/분석    → 현황 파악, 문제 분석
/찾기    → 코드/파일 검색
/보고    → 주간/월간 보고서
```

#### 🔴 통합 대상 (정리 필요)
```
/연구         → 
/research     → /연구 (통합)
/research-simple →

/실험    → /연구의 서브커맨드로
/검증    → /테스트와 통합
/전체사이클 → 메타 커맨드 (유지)
```

## 📋 새로운 명령어 체계

### 1. 개발 사이클 (4 Core)
```bash
/기획 [주제]          # 계획 및 설계
/구현 [기능]          # 코드 작성
/테스트 [범위]        # 검증 (검증 통합)
/배포 [메시지]        # 커밋 및 푸시
```

### 2. 분석 도구 (3 Tools)
```bash
/분석 [대상]          # 문제 분석, 현황 파악
/찾기 [키워드]        # 코드/파일 검색
/보고 [기간]          # 진행 상황 보고
```

### 3. 연구 관리 (1 Unified)
```bash
/연구 [서브커맨드]    # 통합 연구 관리
  init               # 프로젝트 시작
  track              # 진행 기록
  experiment         # 실험 (구 /실험)
  hypothesis         # 가설 설정
  milestone          # 마일스톤
  status             # 현황
  backup             # 백업
```

### 4. 메타 커맨드 (1 Meta)
```bash
/전체사이클           # 전체 워크플로우 실행
```

## 🔄 마이그레이션 계획

### Phase 1: 백업 (즉시)
```bash
# 기존 명령어 백업
mkdir -p .claude/commands/archive/2025-09-10
cp .claude/commands/*.md .claude/commands/archive/2025-09-10/
```

### Phase 2: 통합 (오늘)
```bash
# 연구 명령어 통합
mv .claude/commands/연구.md .claude/commands/연구.md.unified
rm .claude/commands/research.md
rm .claude/commands/research-simple.md

# 검증 통합
cat .claude/commands/검증.md >> .claude/commands/테스트.md
rm .claude/commands/검증.md

# 실험 통합
# (연구의 서브커맨드로 이동)
rm .claude/commands/실험.md
```

### Phase 3: 구현 (내일)
```bash
# 통합된 /연구 명령어 구현
cat > .claude/commands/연구.md << 'EOF'
# /연구 - 통합 연구 관리 시스템
# Bash 기반, Python 선택적 사용
[새로운 구현]
EOF
```

## 🎯 최종 명령어 구조 (9개)

```
.claude/commands/
├── 기획.md        # Planning
├── 구현.md        # Implementation  
├── 테스트.md      # Testing (검증 통합)
├── 배포.md        # Deployment
├── 분석.md        # Analysis
├── 찾기.md        # Search
├── 보고.md        # Reporting
├── 연구.md        # Research (통합)
└── 전체사이클.md   # Full Cycle
```

## 💡 기대 효과

### Before (13개, 혼란)
- 중복: 연구 vs research vs research-simple
- 모호: 테스트 vs 검증
- 산만: 실험이 독립 명령어

### After (9개, 명확)
- 통합: /연구 하나로
- 명확: 각 명령어 역할 분명
- 체계: 서브커맨드로 계층 구조

## 📊 사용 통계 예상

| 명령어 | 예상 사용률 | 용도 |
|--------|------------|------|
| /구현 | 30% | 일상 개발 |
| /분석 | 20% | 문제 해결 |
| /테스트 | 15% | 품질 검증 |
| /연구 | 15% | 연구 관리 |
| /기획 | 10% | 새 기능 |
| /배포 | 5% | 릴리즈 |
| 기타 | 5% | 보고, 찾기 등 |

## ✅ 액션 아이템

1. **즉시**: 현재 명령어 백업
2. **오늘**: 중복 명령어 정리
3. **내일**: 통합 /연구 구현
4. **주말**: 문서 업데이트
5. **다음주**: 사용성 평가

## 🎯 핵심 메시지

> **"적은 것이 많은 것이다 (Less is More)"**

- 13개 → 9개로 축소
- 중복 제거, 역할 명확화
- 사용자 혼란 최소화
- 유지보수 용이성 증대