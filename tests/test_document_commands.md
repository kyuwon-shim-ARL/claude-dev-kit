<!--
@meta
id: document_20250905_1110_test_document_commands
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: document, test_document_commands.md, commands, test, tests
related: 
-->

# 문서 관리 명령어 테스트 시나리오

## 테스트 대상
- /문서정리: 프로젝트별 문서 체계화
- /주간보고: 전체 프로젝트 진행 보고

## 테스트 케이스

### TC1: /문서정리 기본 동작
**시나리오**:
1. 흩어진 문서가 있는 프로젝트에서 실행
2. `/문서정리 "프로젝트명"`

**예상 결과**:
- projects/{프로젝트명}/ 폴더 구조 생성
- 문서들이 로드맵 단계별로 분류
- README.md 자동 생성/업데이트

### TC2: /주간보고 기본 동작
**시나리오**:
1. 여러 프로젝트가 있는 상태에서 실행
2. `/주간보고`

**예상 결과**:
- 모든 프로젝트 스캔
- PRD 기반 진행률 계산
- docs/CURRENT/weekly_report_{날짜}.md 생성

### TC3: 워크플로우 통합
**시나리오**:
1. `/문서정리` 실행 (개별 프로젝트)
2. `/주간보고` 실행 (전체 조망)

**예상 결과**:
- 문서정리 결과가 주간보고에 반영
- 로드맵 위계에 따른 정확한 진행률

## 테스트 제한사항

⚠️ **실제 테스트 불가 항목**:
- 슬래시 명령어 직접 실행 (사용자만 가능)
- PRD가 없는 프로젝트에서의 동작
- 실제 프로젝트 데이터 필요

✅ **검증 완료 항목**:
- 명령어 파일 생성
- 구조적 무결성
- 워크플로우 논리

## 권장 테스트 방법

사용자가 직접 테스트:
```bash
# 1. 테스트 프로젝트 생성
mkdir -p projects/test-project
echo "# Test PRD" > projects/test-project/PRD.md

# 2. 일부 문서 생성
echo "# Analysis" > docs/analysis/test-analysis.md
echo "# Report" > docs/reports/test-report.md

# 3. 문서정리 실행
/문서정리 "test-project"

# 4. 결과 확인
ls -la projects/test-project/

# 5. 주간보고 실행
/주간보고

# 6. 보고서 확인
cat docs/CURRENT/weekly_report_*.md
```