<!--
@meta
id: doc_20250901_test_metadata
type: test
parent: claude_metadata_system
status: draft
created: 2025-09-01
updated: 2025-09-01
triggers: claude_metadata_system.md
-->

# 테스트: 메타데이터 시스템

이 문서는 Claude 내장 메타데이터 시스템 테스트용입니다.

## 테스트 항목
1. 메타데이터가 정상적으로 삽입되었는가?
2. HTML 주석이 렌더링에 영향을 주지 않는가?
3. Claude가 메타데이터를 파싱할 수 있는가?

## 예상 결과
- ✅ 메타데이터가 문서 상단에 주석으로 존재
- ✅ GitHub에서 렌더링 시 메타데이터 보이지 않음
- ✅ Claude가 parent, type 등을 인식