# 디렉토리 기반 프로젝트 감지 시스템 BDD 시나리오

## 배경
연구자들이 프로젝트의 다양한 서브디렉토리에서 작업하더라도 자동으로 올바른 프로젝트가 감지되어야 합니다.

## 시나리오 1: 깊은 노트북 디렉토리에서 작업하는 연구자

**Given** 연구자가 다음 프로젝트 구조에서 작업하고 있습니다:
```
/workspace/research_projects/
  .research_metadata.json
  2025-09-09_drug_discovery/
    notebooks/exploratory/molecular_analysis/
      compound_screening.ipynb  ← 여기서 작업 중
```

**And** 메타데이터에 drug_discovery 프로젝트가 등록되어 있습니다

**When** 연구자가 `compound_screening.ipynb`가 있는 디렉토리에서 `/연구 status` 명령을 실행합니다

**Then** 시스템은 "Active project: drug_discovery"를 표시해야 합니다

**And** 연구자는 추가 설정 없이 모든 연구 명령어를 사용할 수 있어야 합니다

## 시나리오 2: 스크립트 디렉토리에서 작업하는 개발자

**Given** 연구자가 같은 프로젝트의 scripts 디렉토리로 이동했습니다:
```
/workspace/research_projects/2025-09-09_drug_discovery/
  scripts/preprocessing/
    data_loader.py  ← 여기서 작업 중
```

**When** 연구자가 이 디렉토리에서 `/연구 tools` 명령을 실행합니다

**Then** 시스템은 같은 drug_discovery 프로젝트로 인식해야 합니다

**And** 프로젝트 컨텍스트 내의 도구들을 올바르게 표시해야 합니다

## 시나리오 3: 다른 프로젝트로 전환

**Given** 연구자가 다른 프로젝트 디렉토리로 이동했습니다:
```
/workspace/research_projects/2025-09-08_protein_analysis/
  analysis/structures/
    protein_fold.py  ← 여기서 작업 중
```

**And** 메타데이터에 protein_analysis 프로젝트도 등록되어 있습니다

**When** 연구자가 이 디렉토리에서 연구 명령을 실행합니다

**Then** 시스템은 자동으로 protein_analysis 프로젝트로 전환해야 합니다

**And** 이전 프로젝트의 상태는 보존되어야 합니다

## 시나리오 4: 프로젝트 외부에서 작업

**Given** 연구자가 연구 프로젝트 외부 디렉토리에 있습니다:
```
/workspace/regular_work/
  some_script.py  ← 여기서 작업 중
```

**When** 연구자가 연구 명령을 실행합니다

**Then** 시스템은 "No active research project"를 표시해야 합니다

**And** 새 프로젝트 생성 방법을 안내해야 합니다

## 시나리오 5: 잘못된 프로젝트명으로 프로젝트 생성 시도

**Given** 연구자가 위험한 문자가 포함된 프로젝트명을 사용합니다:
```
"project/with\\dangerous..characters"
```

**When** 연구자가 이 이름으로 프로젝트를 생성하려고 시도합니다

**Then** 시스템은 프로젝트명을 안전하게 정규화해야 합니다

**And** 생성된 디렉토리는 파일시스템에 안전해야 합니다

**And** 연구자에게 정규화된 이름을 알려줘야 합니다

## 시나리오 6: 메타데이터 파일 손상 상황

**Given** 연구 프로젝트의 메타데이터 파일이 손상되었습니다

**When** 연구자가 해당 프로젝트 디렉토리에서 연구 명령을 실행합니다

**Then** 시스템은 크래시하지 않고 우아하게 처리해야 합니다

**And** 연구자에게 문제를 설명하고 해결 방법을 제시해야 합니다

## 시나리오 7: 권한 제한 환경

**Given** 일부 디렉토리에 읽기 권한이 없는 환경입니다

**When** 시스템이 상위 디렉토리를 탐색합니다

**Then** 권한 오류로 인해 중단되지 않아야 합니다

**And** 접근 가능한 경로에서 메타데이터를 계속 찾아야 합니다

## 성능 요구사항

**Given** 표준적인 프로젝트 구조 (10단계 깊이)

**When** 디렉토리 감지를 실행합니다

**Then** 50ms 이내에 완료되어야 합니다

**And** 메모리 사용량이 5MB를 초과하지 않아야 합니다

## 보안 요구사항

**Given** 사용자가 다양한 형태의 입력을 제공합니다

**When** 시스템이 파일 경로를 생성합니다

**Then** 디렉토리 순회 공격(`../../../etc/passwd`)을 방지해야 합니다

**And** 파일시스템 메타문자를 안전하게 처리해야 합니다

## 호환성 요구사항

**Given** 기존 연구 프로젝트들이 존재합니다

**When** 새로운 감지 시스템이 활성화됩니다

**Then** 기존 프로젝트들은 계속 정상 작동해야 합니다

**And** 기존 API는 변경 없이 유지되어야 합니다