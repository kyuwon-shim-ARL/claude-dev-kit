# ZEDS와 문서정리 통합 계획

## 1. 문제 인식
- ZEDS: 개발 중 자동 문서화 (docs/CURRENT/)
- 문서정리: 프로젝트별 체계화 (projects/)
- **중복**: 두 시스템이 별개로 존재

## 2. 통합 방안: ZEDS 2.0

### 2.1 기존 ZEDS 확장
```
ZEDS (Zero-Effort Documentation System)
├── 기존: docs/CURRENT/에 자동 문서화
└── 확장: 프로젝트 구조로 자동 정리
```

### 2.2 /안정화 명령어 개선
```python
# 기존 안정화 5단계
5. Documentation Sync
   - CLAUDE.md 반영
   - README 업데이트
   - .gitignore 정리

# 개선: 프로젝트 문서 정리 추가
5. Documentation Sync & Organization
   - CLAUDE.md 반영
   - README 업데이트
   - 프로젝트별 문서 자동 정리 (신규)
   - 로드맵 기반 분류 (신규)
   - 버전별 문서 관리 (신규)
```

### 2.3 자동 트리거
```python
def stabilization_process():
    # ... 기존 안정화 단계들 ...
    
    # 5단계: Documentation Sync & Organization
    if has_project_structure():
        organize_project_documents()  # 문서정리 기능 통합
        update_roadmap_progress()
        create_version_snapshot()
    
    update_claude_md()
    update_readme()
```

## 3. 구현 계획

### 3.1 안정화 명령어 수정
- Documentation Sync 단계에 문서정리 기능 통합
- 프로젝트 감지 시 자동 실행
- 개발 버전과 문서 버전 동기화

### 3.2 ZEDS 폴더 구조 개선
```
docs/
├── CURRENT/           # 활성 작업 (기존 ZEDS)
├── projects/          # 프로젝트별 정리 (신규)
│   └── {project}/
│       ├── v1.0/      # 버전별 스냅샷
│       ├── v1.1/
│       └── latest/    # 현재 버전
└── archives/          # 아카이브 (기존)
```

### 3.3 워크플로우 통합
```
기본 워크플로우 (변경 없음):
/기획 → /구현 → /안정화 → /배포

안정화 내부 프로세스:
1. 구조 스캔
2. 구조 최적화
3. 의존성 해결
4. 테스트
5. Documentation Sync & Organization (확장)
   ├── 코드 문서화
   ├── 프로젝트 문서 정리 (통합)
   └── 버전 스냅샷 생성
6. 품질 보증
```

## 4. 장점

### 개발과 문서의 일체화
- 코드 버전 = 문서 버전
- /안정화 한 번으로 모든 정리 완료
- 중간 문서도 자동 관리

### ZEDS 철학 유지
- Zero-Effort: 추가 명령어 불필요
- 자동화: /안정화에서 자동 실행
- 체계적: 프로젝트 구조 자동 생성

## 5. 실행 예시

```bash
# 개발 진행
/기획 "RNA-seq 파이프라인"
/구현 "DEG 분석 모듈"

# 안정화 실행 시
/안정화

# 자동으로:
1. 코드 구조 정리
2. 테스트 실행
3. 문서 자동 정리:
   - docs/CURRENT/* → projects/rna-seq/latest/
   - 로드맵 단계별 분류
   - 버전 스냅샷 생성
4. CLAUDE.md 업데이트
```

## 6. 마이그레이션 계획

### Phase 1: 안정화 명령어 수정
- Documentation Sync 단계 확장
- 문서정리 로직 통합

### Phase 2: 기존 명령어 처리
- /문서정리: 독립 실행 가능 (유지)
- /주간보고: 독립 도구 (유지)
- 단, /안정화에서도 자동 실행

### Phase 3: ZEDS 2.0 완성
- 개발-문서 완전 통합
- 버전 관리 자동화
- 프로젝트 추적 강화

---
*"개발과 문서는 하나다" - ZEDS 2.0 철학*