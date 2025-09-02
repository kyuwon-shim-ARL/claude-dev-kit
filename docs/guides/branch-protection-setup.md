# Branch Protection 설정 가이드: TADD 강제 적용

## 🎯 목적
GitHub Actions만으로는 TADD를 강제할 수 없습니다. Branch Protection Rules를 설정해야 실제로 머지를 차단할 수 있습니다.

## 📋 설정 단계

### 1. GitHub Repository Settings 접속
```
https://github.com/[OWNER]/[REPO]/settings/branches
```

### 2. Branch Protection Rule 추가
- **Branch name pattern**: `main` (또는 기본 브랜치명)
- 아래 "Add rule" 클릭

### 3. 필수 설정 항목 ✅

#### 3.1 Require status checks to pass before merging
✅ 체크 필수

**Required status checks 추가:**
- `TADD Enforcement / verify-test-first`
- `TADD Enforcement / check-mock-usage`  
- `TADD Enforcement / quality-gate`
- `TADD Enforcement / test-coverage`

#### 3.2 Require branches to be up to date before merging
✅ 체크 (최신 main과 동기화 강제)

#### 3.3 Include administrators
✅ 체크 (관리자도 규칙 적용)

#### 3.4 Restrict who can push to matching branches
✅ 체크 (선택사항)
- GitHub Actions bot만 허용
- 또는 특정 팀/사용자만 허용

### 4. 저장
"Create" 또는 "Save changes" 클릭

## 🔍 설정 검증

### GUI로 확인
1. Settings → Branches
2. main 브랜치에 🔒 아이콘 표시 확인
3. Protection rules 세부사항 확인

### CLI로 확인
```bash
# GitHub CLI 사용
gh api repos/OWNER/REPO/branches/main/protection | jq '.'

# 또는 curl 사용
curl -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/repos/OWNER/REPO/branches/main/protection
```

### 실제 테스트
```bash
# 1. TADD 위반 브랜치 생성
git checkout -b test-violation
echo "code without test" > feature.js
git add . && git commit -m "feat: no test"
git push origin test-violation

# 2. PR 생성
gh pr create --title "Test TADD Violation" --body "This should fail"

# 3. 확인사항
# - Status checks가 ❌ 표시
# - "Merge" 버튼이 비활성화
# - "This branch cannot be merged" 메시지
```

## 🚨 주의사항

### 1. 초기 설정 시
- 기존 PR들이 머지 불가능해질 수 있음
- 점진적 적용 권장 (처음엔 warning only)

### 2. 긴급 상황 대응
```bash
# 임시로 Protection 해제 (관리자만)
gh api -X DELETE repos/OWNER/REPO/branches/main/protection

# 긴급 수정 후 다시 활성화
gh api -X PUT repos/OWNER/REPO/branches/main/protection --input protection.json
```

### 3. 팀 온보딩
- 설정 전 팀 공지 필수
- TADD 교육 세션 진행
- 1-2주 적응 기간 제공

## 📊 효과 측정

### 설정 전
- TADD 준수율: ~30%
- 버그 발생률: 높음
- 코드 리뷰 시간: 길음

### 설정 후 (예상)
- TADD 준수율: 100% (강제)
- 버그 발생률: 70% 감소
- 코드 리뷰 시간: 50% 단축

## 🔧 트러블슈팅

### Q: Status checks가 안 보임
A: GitHub Actions가 최소 1회 실행되어야 표시됨

### Q: 관리자도 머지 못함
A: "Include administrators" 체크 해제 (권장하지 않음)

### Q: 특정 파일만 제외하고 싶음
A: CODEOWNERS 파일 활용 또는 workflow에서 path 필터 사용

## 📚 참고 자료
- [GitHub Docs: Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [GitHub API: Branch Protection](https://docs.github.com/en/rest/branches/branch-protection)

---

**작성일**: 2025-09-02
**버전**: v1.0