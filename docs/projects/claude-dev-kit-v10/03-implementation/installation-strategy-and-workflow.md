<!--
@meta
id: strategy_20250905_1110_installation-strategy-and-workflow
type: strategy
scope: strategic
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: installation, installation-strategy-and-workflow.md, claude-dev-kit-v10, 03-implementation, projects
related: 
-->

# 설치 전략 및 문서화 워크플로우 결정

## 1. 현재 상황 분석

### 1.1 init.sh와 update.sh 동작
- **설치 위치**: `.claude/commands/` (프로젝트 로컬)
- **홈 폴더 아님**: `~/.claude/commands/`가 아닌 각 프로젝트별 설치
- **결과**: 프로젝트마다 독립적인 명령어 세트

### 1.2 장단점 분석
| 측면 | 프로젝트 로컬 (현재) | 글로벌 설치 (대안) |
|------|---------------------|-------------------|
| **장점** | • 프로젝트별 커스터마이징<br>• 버전 독립성<br>• 충돌 없음 | • 한 번만 설치<br>• 일관성<br>• 유지보수 용이 |
| **단점** | • 반복 설치 필요<br>• 디스크 공간<br>• 업데이트 번거로움 | • 커스터마이징 어려움<br>• 충돌 가능성<br>• 모든 프로젝트 영향 |

## 2. 권장 전략: 하이브리드 접근

### 2.1 이중 구조 제안
```bash
# 글로벌 (기본 명령어)
~/.claude/commands/
├── 기획.md          # 범용
├── 구현.md
├── 안정화.md
└── 배포.md

# 프로젝트 (특화 명령어)
project/.claude/commands/
├── rna-qc.md        # RNA-seq 특화
├── deg-analysis.md  # DEG 분석 특화
└── pathway.md       # Pathway 특화
```

### 2.2 실행 방안
```bash
# init.sh 개선안
init.sh --global     # ~/.claude/commands/에 설치
init.sh --local      # .claude/commands/에 설치 (기본값)
init.sh --project    # 프로젝트 특화 명령어만 설치
```

## 3. 문서화 워크플로우 결정

### 3.1 현재 /안정화의 Documentation Sync
```
5. Documentation Sync
   - CLAUDE.md 반영
   - README 업데이트
   - .gitignore 정리
```
**분석**: 이미 포함되어 있지만 "코드 문서화"에 초점

### 3.2 연구 문서 관리는 별도 필요
| 작업 유형 | 담당 명령어 | 이유 |
|-----------|------------|------|
| **코드 문서화** | /안정화 | 구조적 정리의 일부 |
| **연구 문서 정리** | /문서정리 (신규) | 프로젝트 문서 체계화 |
| **보고서 작성** | /보고서 | 최종 산출물 생성 |

### 3.3 새로운 /문서정리 명령어 제안
```bash
/문서정리 "프로젝트명"
```
**역할**:
1. 흩어진 문서를 프로젝트 폴더로 수집
2. 연구 단계별 자동 분류
3. 버전 정리 (중복 제거)
4. 인덱스 생성
5. 다음 단계 제안

## 4. 최적 워크플로우

### 4.1 일반 개발 프로젝트
```
/기획 → /구현 → /안정화 (문서화 포함) → /배포
```

### 4.2 연구 프로젝트
```
/프로젝트시작 → /기획 → /구현 → /분석 → /문서정리 → /보고서
                                              ↑
                                      주기적으로 실행
```

### 4.3 통합 접근
```python
def handle_documentation():
    if project_type == "development":
        # /안정화에서 처리
        sync_code_documentation()
    elif project_type == "research":
        # /문서정리로 별도 처리
        organize_research_documents()
        suggest_next_steps()
```

## 5. 실행 계획

### Phase 1: 즉시 적용 가능
- 프로젝트별 .claude/commands/ 활용 (현재 방식 유지)
- /안정화의 Documentation Sync 활용

### Phase 2: 점진적 개선
- [ ] init.sh에 --global 옵션 추가
- [ ] /문서정리 명령어 개발
- [ ] 프로젝트 타입 자동 감지

### Phase 3: 완전 통합
- [ ] 글로벌 + 로컬 명령어 자동 병합
- [ ] 연구 문서 자동 분류 시스템
- [ ] 프로젝트 라이프사이클 추적

## 6. 결론

### 6.1 설치 전략
**현재 유지 + 점진적 개선**
- 당장은 프로젝트별 설치 유지 (작동 중이므로)
- 추후 --global 옵션 추가로 선택권 제공

### 6.2 문서화 전략
**역할 분리**
- 코드 문서: /안정화에서 계속 처리
- 연구 문서: /문서정리 신규 개발
- 최종 보고서: /보고서 활용

### 핵심 원칙
> "작동하는 것을 깨뜨리지 말고, 점진적으로 개선하자"

---
*현재 시스템이 작동하므로 급격한 변경보다는 점진적 개선이 안전합니다.*