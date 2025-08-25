# 분석 문서화 체계 v3.0 (Balanced)

## 📊 균형잡힌 구조

```
docs/analysis/
├── index.md               # 📋 분석 색인 (자동 생성/업데이트)
├── 2024/                 # 연도별
│   ├── 01-dev/           # 월-카테고리
│   │   ├── 15-API성능분석.md
│   │   └── 28-코드리뷰.md
│   ├── 01-bio/           # 바이오인포
│   │   └── 12-RNA-seq-DEG.md
│   └── 01-business/      # 비즈니스
│       └── 30-Q1계획.md
└── templates/            # 템플릿 모음
    ├── dev.md           # 개발 분석
    ├── research.md      # 연구 분석
    └── business.md      # 비즈니스 분석
```

## 🎯 자동 분류 시스템

### 사용법 (변경 없음)
```bash
/분석 "RNA-seq 결과 pathway 분석해줘"
```

### Claude의 자동 처리
1. **키워드 감지**: "RNA-seq" → bio 카테고리
2. **날짜 폴더**: 2024/01-bio/ 확인/생성
3. **파일 저장**: 15-RNA-seq-pathway.md
4. **인덱스 업데이트**: index.md에 자동 추가

## 📋 자동 생성 인덱스

### docs/analysis/index.md 예시
```markdown
# 분석 보고서 색인 (Auto-generated)

## 최근 분석 (Recent)
- 2024-01-15: [RNA-seq Pathway 분석](2024/01-bio/15-RNA-seq-pathway.md) #bio #research
- 2024-01-12: [API 성능 병목 분석](2024/01-dev/12-API성능분석.md) #dev #performance
- 2024-01-10: [Q1 매출 분석](2024/01-business/10-Q1매출분석.md) #business

## 카테고리별 (By Category)
### 🧬 Bio/Research (3)
- RNA-seq 분석: 2건
- 유전체 분석: 1건

### 💻 Development (5)
- 성능 분석: 3건
- 코드 리뷰: 2건

### 📊 Business (2)
- 매출 분석: 1건
- 사용자 분석: 1건

## 검색 태그
#performance #rna-seq #api #business #코드리뷰 #매출
```

## 🔍 스마트 검색

### 파일명 기반 검색
```bash
find docs/analysis -name "*API*"          # API 관련
find docs/analysis -name "*RNA*"          # RNA 관련
grep -r "성능" docs/analysis              # 내용 검색
```

### 태그 기반 검색 (metadata)
```markdown
각 분석 파일에 자동 추가:
---
date: 2024-01-15
category: bio
tags: [rna-seq, pathway, deg]
duration: 2h
impact: high
---
```

## 🧹 자동 정리 규칙

### 월별 정리
- 매월 말: 해당 월 분석 개수 확인
- 3개 이상이면 유지, 1-2개면 misc/ 폴더로 이동

### 연말 정리
- 중요 분석: 별도 highlights/ 폴더로 복사
- 임시 분석: archive/ 폴더로 이동
- 연간 보고서 자동 생성

## 💡 관리 vs 유연성 밸런스

### 자동 관리 (AI가 처리)
- ✅ 카테고리 분류 (키워드 기반)
- ✅ 파일명 생성 (날짜-핵심키워드)
- ✅ 인덱스 업데이트
- ✅ 메타데이터 추가
- ✅ 주기적 정리

### 수동 관리 (필요시만)
- 📝 중요 분석 하이라이트 표시
- 📝 관련 분석끼리 연결
- 📝 연간 리뷰 및 아카이빙

## 🎪 실제 사용 시나리오

### 1. 일상적 분석
```bash
/분석 "어제 배포한 기능 모니터링 결과"
# → 2024/01-dev/16-배포모니터링.md
# → index.md 자동 업데이트
```

### 2. 연구 분석
```bash
/분석 "샘플 10개 RNA-seq DEG 분석, pathway enrichment 포함"
# → 2024/01-bio/16-RNA-seq-DEG-10samples.md
# → research 템플릿 자동 적용
# → 통계, 방법론 섹션 포함
```

### 3. 월말 정리
```bash
# Claude가 자동으로:
- index.md 통계 업데이트
- 카테고리별 요약 생성
- 다음달 폴더 준비
```

## 📈 장점

1. **자동 분류**: 키워드로 적절한 카테고리 판단
2. **검색 가능**: 파일명, 태그, 내용 검색 지원
3. **적절한 구조**: 너무 복잡하지도, 단순하지도 않음
4. **확장 가능**: 새 카테고리 자동 생성
5. **관리 부담 최소**: 대부분 자동화

## 🔧 설정 파일

### analysis_config.yaml
```yaml
categories:
  dev: [api, 성능, 코드, 리뷰, 버그]
  bio: [rna, dna, 유전자, 단백질, 샘플]
  business: [매출, 사용자, 비용, roi, 분기]
  
auto_cleanup:
  monthly: true
  archive_threshold: 90days
  
templates:
  dev: templates/dev.md
  bio: templates/research.md
  business: templates/business.md
```

이렇게 하면 관리와 유연성의 균형을 맞출 수 있습니다!