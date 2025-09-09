<!--
@meta
id: document_20250905_1110_test_analysis_autosave
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: analysis, test, tests, autosave, test_analysis_autosave.md
related: 
-->

# 분석 자동 저장 테스트 시나리오

## 테스트 목적
`/분석` 명령어가 실제로 분석 결과를 파일로 자동 저장하는지 검증

## 테스트 케이스

### TC1: 기본 분석 자동 저장
- **입력**: `/분석 "테스트 분석 요청"`
- **예상 결과**: 
  - docs/analysis/YYYY-MM-DD-테스트분석요청.md 파일 생성
  - 파일 내용에 분석 결과 포함
  - 사용자에게 저장 경로 알림

### TC2: 바이오인포 분석 자동 저장
- **입력**: `/분석 "RNA-seq 샘플 품질 체크"`
- **예상 결과**:
  - docs/analysis/YYYY-MM-DD-RNAseq샘플품질체크.md 파일 생성
  - 연구 분석 템플릿 적용
  - 관련 분석 링크 포함

### TC3: 인덱스 자동 업데이트
- **입력**: 여러 분석 수행 후
- **예상 결과**:
  - docs/analysis/index.md 자동 생성/업데이트
  - 최근 분석 목록 포함
  - 카테고리별 분류

## 실제 테스트 수행 필요 사항

⚠️ **현재 상태**: 테스트 불가능
- **이유**: /분석 명령어의 실제 구현체가 없음
- **필요 조건**: 
  1. Claude가 실제로 /분석 명령을 받았을 때 자동 저장 코드 실행
  2. Write 도구를 사용한 파일 저장 로직 구현
  3. 실제 분석 데이터 필요

## 테스트 가능한 부분

✅ **파일 구조 검증**:
- docs/analysis/ 폴더 존재 확인
- 템플릿 파일 존재 확인
- 설정 파일 유효성 검증

❌ **자동 저장 기능**:
- 실제 /분석 명령 실행 시 동작 확인 불가
- Mock 데이터로는 의미 없음