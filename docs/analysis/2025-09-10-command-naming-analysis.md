# 슬래시 커맨드 명명 혼란 분석 및 해결책

## 📅 분석 정보
- **날짜**: 2025-09-10 08:50
- **요청**: 연구.md, research.md, research-simple.md 혼란 해결
- **유형**: command organization

## 📊 현재 상황 분석

### 문제점: 3개의 유사한 명령어 파일

| 파일명 | 생성 시점 | 목적 | 실제 구현 |
|--------|-----------|------|-----------|
| **연구.md** | 초기 | 한글 명령어, 연구 관리 아이디어 | 미구현 (개념만) |
| **research.md** | 중간 | 영어 버전, Python 통합 | Python 모듈 호출 |
| **research-simple.md** | 최근 | Bash 전용 간소화 버전 | 순수 Bash 구현 |

### 혼란의 원인

1. **점진적 개발**: 아이디어 → Python 구현 → Bash 대안
2. **요구사항 변화**: "Python 없이도 가능하게"
3. **명확한 정리 부재**: 기존 파일 유지한 채 새 파일 추가

## 🎯 해결책: 통합 명령어 시스템

### Option 1: 단일 파일로 통합 (권장) ✅

```markdown
# /연구 (별칭: /research) - 지능형 연구 관리 시스템

## 자동 모드 선택
- Python 있음 → 고급 기능 모드
- Python 없음 → Bash 기본 모드

## 실행 프로토콜
[지능형 분기 로직]
```

**장점:**
- 사용자는 하나의 명령어만 기억
- 환경에 따라 자동 최적화
- 유지보수 간편

### Option 2: 명확한 구분 유지

```
/연구-고급    → Python 필수, 모든 기능
/연구-기본    → Bash만, 핵심 기능
/연구        → 자동 선택 (wrapper)
```

**장점:**
- 명시적 선택 가능
- 디버깅 용이

**단점:**
- 사용자가 3개 명령어 구분 필요

### Option 3: 삭제 및 재구성

```bash
# 정리 작업
1. research.md → 삭제 (research-unified.md로 대체)
2. research-simple.md → 삭제 (통합됨)
3. 연구.md → research-unified.md로 개명 및 업데이트
```

## 📋 권장 액션 플랜

### Phase 1: 즉시 실행
```bash
# 1. 백업
cp .claude/commands/연구.md .claude/commands/연구.md.bak
cp .claude/commands/research.md .claude/commands/research.md.bak
cp .claude/commands/research-simple.md .claude/commands/research-simple.md.bak

# 2. 통합 파일 생성
cat > .claude/commands/research-unified.md << 'EOF'
[통합된 내용]
EOF

# 3. 기존 파일 아카이브
mkdir -p .claude/commands/archive
mv .claude/commands/research*.md.bak .claude/commands/archive/
```

### Phase 2: 테스트
```bash
# 각 모드 테스트
/research-unified init test_project  # Python 모드
unset PYTHONPATH
/research-unified init test_bash     # Bash 모드
```

### Phase 3: 문서 업데이트
```markdown
# CLAUDE.md 업데이트
## 슬래시 커맨드
- /연구 (research) - 통합 연구 관리 시스템
  - Python 있으면 고급 기능
  - 없으면 Bash 기본 기능
```

## 🔍 근본 원인 분석

### 왜 이런 혼란이 발생했나?

1. **Iterative Development**
   - v1: 아이디어 (연구.md)
   - v2: Python 구현 (research.md)
   - v3: Bash 대안 (research-simple.md)

2. **Backwards Compatibility 우려**
   - 기존 파일 삭제 주저
   - "혹시 필요할까봐" 유지

3. **Clear Migration Path 부재**
   - 언제 어떤 버전 사용할지 불명확
   - 문서화 미흡

## 💡 향후 방지 전략

### 1. 버전 관리 규칙
```
command.md          # 현재 버전
command.v1.md       # 이전 버전 (archive/)
command-dev.md      # 개발 중
```

### 2. 명령어 생명주기
```
idea → dev → beta → stable → deprecated → archive
```

### 3. 자동 정리 시스템
```bash
# 주기적 정리 스크립트
find .claude/commands -name "*.deprecated.md" -mtime +30 -delete
```

## 🎯 최종 권장사항

### 즉시 실행 사항
1. **통합 파일 생성**: `research-unified.md`
2. **기존 파일 아카이브**: `archive/` 폴더로 이동
3. **별칭 설정**: `/연구`, `/research` → 동일 명령어

### 장기 개선 사항
1. **명령어 관리 시스템 구축**
2. **자동 버전 관리**
3. **사용 통계 수집**

## 📊 예상 효과

### Before (혼란)
```
사용자: "어떤 명령어 써야 하지?"
- /연구? /research? /research-simple?
- 차이가 뭐지?
- Python 필요한가?
```

### After (명확)
```
사용자: "/연구"
시스템: [자동으로 최적 모드 선택]
- Python 있음 → 풀 기능
- Python 없음 → 기본 기능
```

## 🔄 마이그레이션 체크리스트

- [ ] 통합 명령어 파일 생성
- [ ] 기존 파일 백업
- [ ] 테스트 실행
- [ ] 문서 업데이트
- [ ] 사용자 공지
- [ ] 기존 파일 아카이브
- [ ] 모니터링 (1주일)
- [ ] 최종 정리