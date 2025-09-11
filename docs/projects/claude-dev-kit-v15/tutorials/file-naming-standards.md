<!--
@meta
id: document_20250905_1110_file-naming-standards
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-09
tags: standards, file, projects, tutorials, file-naming-standards.md
related: 
-->

# 📋 파일명 표준화 정책 (File Naming Standards)

## 🎯 목적
docs/CURRENT/ 디렉토리의 중복 파일 방지 및 일관된 문서 관리

## 📊 파일 분류 및 네이밍 규칙

### 1. 영속 파일 (Persistent Files)
항상 유지되며 업데이트만 되는 파일들:
- `status.md` - 프로젝트 현황
- `active-todos.md` - 진행중 작업
- **금지**: status-*.md, active-todos-*.md 형태 사용 금지

### 2. 표준 파일 (Standard Files)  
최신 버전만 유지되는 파일들:
- `planning.md` - 현재 계획
- `test-report.md` - 최근 테스트 결과
- `implementation.md` - 현재 구현 진행사항
- **원칙**: 항상 덮어쓰기, 이전 버전은 세션 아카이브

### 3. 세션별 파일 (Session-specific Files)
특정 작업/날짜에 종속되는 파일들:
- `planning-[topic].md` - 예: planning-darkmode.md
- `implementation-[date].md` - 예: implementation-20250820.md
- `[feature]-report-[date].md` - 예: verification-report-20250820.md
- **규칙**: 완료 후 sessions/로 아카이브

### 4. 임시 파일 (Temporary Files)
자동 삭제 대상:
- `*.tmp`, `*.bak` - 임시 백업
- `duplicate-*.md` - 중복 파일
- `old-*.md` - 구버전 파일
- **처리**: /배포시 자동 삭제

## ⚠️ 중복 방지 규칙

### 절대 금지사항:
- ❌ `test-report-final.md` (test-report.md 사용)
- ❌ `planning-v2.md` (planning.md 덮어쓰기)
- ❌ `status-updated.md` (status.md 업데이트)

### 올바른 예시:
- ✅ `test-report.md` - 항상 최신 유지
- ✅ `planning-authentication.md` - 특정 기능 기획
- ✅ `extreme-verification-report-20250820.md` - 날짜별 특수 리포트

## 🔄 자동 정리 트리거
- docs/CURRENT/ 파일 10개 이상
- 동일 접두사 파일 3개 이상
- 7일 이상 된 파일 존재

## 📦 아카이빙 정책
```
영속 파일 → 유지 (업데이트만)
표준 파일 → 최신 유지 (덮어쓰기)
세션별 파일 → sessions/로 이동
임시 파일 → 삭제
```

---
*이 정책은 자동 문서화 시스템 v2.0의 일부입니다.*