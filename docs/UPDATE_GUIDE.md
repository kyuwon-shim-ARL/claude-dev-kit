# 기존 프로젝트 업데이트 가이드

## 🚀 빠른 업데이트 (1분)

```bash
# 프로젝트 루트에서 실행
curl -s https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/update.sh | bash
```

## 📋 수동 업데이트 (선택적)

### 1. 핵심 파일만 업데이트

```bash
# 배포 명령어만 업데이트 (컨텍스트 관리 포함)
curl -o .claude/commands/배포.md \
  https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/.claude/commands/배포.md
```

### 2. 전체 명령어 업데이트

```bash
# 모든 슬래시 명령어 업데이트
cd .claude/commands
for cmd in 기획 구현 안정화 배포 전체사이클 문서화 배포문서 분석; do
  curl -O "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/.claude/commands/${cmd}.md"
done
cd ../..
```

### 3. 선택적 컴포넌트

```bash
# 컨텍스트 관리 가이드 추가
mkdir -p docs/development
curl -o docs/development/claude-ops-integration.md \
  https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/docs/development/claude-ops-integration.md
```

## 🔄 버전별 업데이트 내역

### v8.0.0 (2025-08-22)
- ✨ 스마트 컨텍스트 관리 시스템
- 📋 /compact 템플릿 가이드
- 🤖 Claude-Ops 텔레그램 통합 설계

### v7.1.0 (2025-08-21)
- 🔧 Git 자동 초기화 수정
- 📝 포괄적 .gitignore 템플릿

## ⚠️ 주의사항

### 유지해야 할 파일
- `project_rules.md` - 프로젝트별 고유 규칙
- `CLAUDE.md` - 프로젝트 설명서
- `docs/CURRENT/*` - 현재 작업 문서

### 백업 권장
```bash
# 업데이트 전 백업
cp -r .claude/commands .claude/commands.backup
```

## 🎯 업데이트 확인

```bash
# 버전 확인
cat .claude/.version

# 컨텍스트 관리 기능 확인
grep "compact" .claude/commands/배포.md
```

## 💡 효과적인 업데이트 전략

### A. 최소 업데이트 (안전)
- 배포.md만 업데이트
- 컨텍스트 관리 기능만 추가

### B. 표준 업데이트 (권장)
- 모든 명령어 업데이트
- 기존 설정 유지

### C. 전체 재설치 (신중)
- 백업 후 init.sh 재실행
- 모든 기능 최신화

## 📊 업데이트 후 테스트

```bash
# 1. 명령어 확인
ls -la .claude/commands/

# 2. 컨텍스트 관리 테스트
echo '/compact "테스트 완료. 문서 보존됨. 과정 제거"'

# 3. 버전 확인
cat .claude/.version
```

## 🆘 문제 해결

### 롤백 방법
```bash
# 백업에서 복원
cp -r .claude/commands.backup/* .claude/commands/
```

### 충돌 해결
- project_rules.md 충돌 시: 기존 파일 유지
- CLAUDE.md 충돌 시: 프로젝트별 내용 우선

## 📞 지원

- GitHub Issues: https://github.com/kyuwon-shim-ARL/claude-dev-kit/issues
- 최신 릴리즈: https://github.com/kyuwon-shim-ARL/claude-dev-kit/releases