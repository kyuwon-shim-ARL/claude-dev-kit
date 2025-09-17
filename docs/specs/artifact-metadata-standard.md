<!--
@meta
id: spec_20250917_artifact_metadata
type: specification
status: draft
created: 2025-09-17
updated: 2025-09-17
tags: metadata, testing, analysis, artifact-management
-->

# 🏷️ Artifact Metadata Standard v1.0
*테스트, 검증, 분석 파일을 위한 메타데이터 표준*

## 📋 핵심 목표
**"생성 시점 3초 투자로, 정리 시점 30분 절약"**

모든 부산물 코드에 Input-Process-Output 관계와 생명주기를 명시하여:
- 자동 분류 및 아카이빙 가능
- 의존성 추적 가능
- 재사용성 판단 가능
- 중복 방지 가능

## 🎯 메타데이터 표준 구조

### 1️⃣ **최소 필수 메타데이터 (3초 버전)**
```python
"""
@meta: [type] | [date] | [lifecycle]
@purpose: [한 줄 설명]
"""
```

**예시:**
```python
"""
@meta: test-unit | 2025-09-17 | keep
@purpose: User authentication 단위 테스트
"""
```

### 2️⃣ **표준 메타데이터 (30초 버전)**
```python
"""
@meta
type: [artifact-type]
date: [YYYY-MM-DD]
lifecycle: [keep|temp|archive]
purpose: [설명]

@io
input: [입력 데이터/파일]
process: [처리 내용]
output: [결과물]
"""
```

### 3️⃣ **전체 메타데이터 (2분 버전 - 중요 파일용)**
```python
"""
@meta
id: [type]_[timestamp]_[feature]
type: [artifact-type]
date: [YYYY-MM-DD]
lifecycle: [keep|temp|archive|deprecated]
purpose: [설명]
status: [draft|active|completed|failed]

@io
input: [입력 데이터/파일/조건]
process: [처리 로직/알고리즘]
output: [결과물/리포트/메트릭]
side_effects: [파일 생성, DB 변경 등]

@dependencies
requires: [필요 모듈/파일 목록]
used_by: [이 파일을 사용하는 곳]

@results
conclusion: [결론/발견사항]
metrics: [측정값]
next_steps: [후속 액션]
"""
```

## 📁 Artifact Type 분류 체계

### **테스트 관련 (test-*)**
```python
# 단위 테스트
"""
@meta: test-unit | 2025-09-17 | keep
@purpose: Auth module 단위 테스트
@io: auth.py → pytest → 100% coverage
"""

# 통합 테스트
"""
@meta: test-integration | 2025-09-17 | keep
@purpose: API-DB 통합 테스트
@io: API endpoints → E2E test → response validation
"""

# 성능 테스트
"""
@meta: test-performance | 2025-09-17 | temp
@purpose: Load testing for /api/users
@io: 1000 requests → locust → response_time < 100ms
@results: p95=87ms, p99=145ms (FAIL)
"""

# 임시 테스트
"""
@meta: test-experiment | 2025-09-17 | temp
@purpose: OAuth 라이브러리 동작 확인
@io: google-auth → test script → works with v2.1
"""
```

### **분석 관련 (analysis-*)**
```python
# 코드 분석
"""
@meta: analysis-code | 2025-09-17 | archive
@purpose: 순환 참조 의존성 분석
@io: src/ → AST analysis → circular_deps.json
@results: 3 circular dependencies found
"""

# 성능 분석
"""
@meta: analysis-performance | 2025-09-17 | archive
@purpose: API 응답시간 병목점 분석
@io: logs/*.log → profiler → bottleneck_report.md
@results: DB query N+1 problem in get_users()
"""

# 보안 분석
"""
@meta: analysis-security | 2025-09-17 | keep
@purpose: OWASP Top 10 취약점 스캔
@io: *.py → bandit → security_report.json
@results: 2 medium severity issues
"""
```

### **검증 관련 (verify-*)**
```python
# 데이터 검증
"""
@meta: verify-data | 2025-09-17 | temp
@purpose: 마이그레이션 데이터 무결성 검증
@io: old_db + new_db → compare → diff_report.csv
@results: 100% match, safe to proceed
"""

# 배포 검증
"""
@meta: verify-deployment | 2025-09-17 | archive
@purpose: Production 배포 후 헬스체크
@io: prod endpoints → smoke test → all green
"""

# 호환성 검증
"""
@meta: verify-compatibility | 2025-09-17 | keep
@purpose: Python 3.12 호환성 검증
@io: src/ → py312 test → compatibility_matrix.md
"""
```

### **도구/유틸리티 (tool-*)**
```python
# 일회성 스크립트
"""
@meta: tool-migration | 2025-09-17 | archive
@purpose: v1 to v2 데이터 마이그레이션
@io: data_v1.json → transform → data_v2.json
@side_effects: backup created at backups/
"""

# 헬퍼 유틸리티
"""
@meta: tool-helper | 2025-09-17 | keep
@purpose: 테스트 fixture 생성 유틸리티
@io: schema.json → generate → fixtures/*.json
"""
```

## 🔄 Lifecycle 상태 정의

| 상태 | 의미 | 자동 처리 |
|-----|------|----------|
| **keep** | 영구 보존 필요 | 유지 |
| **temp** | 임시 파일 | 7일 후 archive로 이동 |
| **archive** | 완료된 작업 | 30일 후 .archive/로 이동 |
| **deprecated** | 더 이상 사용 안 함 | 확인 후 삭제 |
| **wip** | 작업 중 | 경고 후 유지 |

## 🤖 자동화 도구

### 1. **메타데이터 자동 삽입 (Git Hook)**
```python
#!/usr/bin/env python3
# .git/hooks/pre-commit-metadata

import re
from datetime import date
from pathlib import Path

def add_metadata(filepath):
    """테스트/분석 파일에 자동으로 메타데이터 삽입"""

    # 파일 타입 추론
    if 'test_' in filepath.name:
        file_type = 'test-unit'
    elif 'verify_' in filepath.name:
        file_type = 'verify-data'
    elif 'analyze_' in filepath.name:
        file_type = 'analysis-code'
    else:
        return  # 메타데이터 불필요

    with open(filepath, 'r') as f:
        content = f.read()

    # 이미 메타데이터 있으면 스킵
    if '@meta' in content[:500]:
        return

    # 자동 메타데이터 생성
    metadata = f'''"""
@meta: {file_type} | {date.today()} | temp
@purpose: [AUTO-GENERATED: Please update]
"""

'''

    # 파일 시작 부분에 삽입
    with open(filepath, 'w') as f:
        f.write(metadata + content)

    print(f"✅ Added metadata to {filepath.name}")
```

### 2. **메타데이터 기반 자동 정리**
```python
#!/usr/bin/env python3
# scripts/clean_artifacts.py

import re
from pathlib import Path
from datetime import datetime, timedelta

def parse_metadata(content):
    """파일에서 메타데이터 추출"""
    pattern = r'@meta:\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^\n]+)'
    match = re.search(pattern, content[:500])

    if match:
        return {
            'type': match.group(1).strip(),
            'date': match.group(2).strip(),
            'lifecycle': match.group(3).strip()
        }
    return None

def clean_artifacts(dry_run=True):
    """메타데이터 기반 자동 정리"""

    stats = {'archived': 0, 'deleted': 0, 'kept': 0}

    for file in Path('.').rglob('*.py'):
        # 테스트/분석/검증 파일만 대상
        if not any(x in file.name for x in ['test_', 'verify_', 'analyze_', 'check_']):
            continue

        with open(file) as f:
            content = f.read(500)

        meta = parse_metadata(content)
        if not meta:
            print(f"⚠️  No metadata: {file}")
            continue

        # Lifecycle 기반 처리
        file_date = datetime.strptime(meta['date'], '%Y-%m-%d')
        age_days = (datetime.now() - file_date).days

        if meta['lifecycle'] == 'temp' and age_days > 7:
            action = "→ archive"
            if not dry_run:
                archive_path = Path('.archive') / file.parent
                archive_path.mkdir(parents=True, exist_ok=True)
                file.rename(archive_path / file.name)
            stats['archived'] += 1

        elif meta['lifecycle'] == 'deprecated':
            action = "→ delete"
            if not dry_run:
                file.unlink()
            stats['deleted'] += 1

        elif meta['lifecycle'] == 'archive' and age_days > 30:
            action = "→ .archive/"
            if not dry_run:
                archive_path = Path('.archive') / file.parent
                archive_path.mkdir(parents=True, exist_ok=True)
                file.rename(archive_path / file.name)
            stats['archived'] += 1

        else:
            action = "✓ keep"
            stats['kept'] += 1

        print(f"{file}: {meta['lifecycle']} ({age_days}d) {action}")

    print(f"\n📊 Summary: {stats}")

    if dry_run:
        print("\n💡 This was a dry run. Use --execute to apply changes.")

if __name__ == "__main__":
    import sys
    dry_run = '--execute' not in sys.argv
    clean_artifacts(dry_run)
```

### 3. **의존성 그래프 생성**
```python
#!/usr/bin/env python3
# scripts/dependency_graph.py

def extract_dependencies():
    """메타데이터에서 의존성 추출하여 그래프 생성"""

    dependencies = {}

    for file in Path('.').rglob('*.py'):
        with open(file) as f:
            content = f.read()

        # @dependencies 섹션 파싱
        if '@dependencies' in content:
            deps_section = re.search(r'@dependencies.*?(?=@|\n\n|$)', content, re.DOTALL)
            if deps_section:
                requires = re.findall(r'requires:\s*([^\n]+)', deps_section.group())
                used_by = re.findall(r'used_by:\s*([^\n]+)', deps_section.group())

                dependencies[str(file)] = {
                    'requires': requires,
                    'used_by': used_by
                }

    # Mermaid 다이어그램 생성
    print("```mermaid")
    print("graph TD")
    for file, deps in dependencies.items():
        for req in deps.get('requires', []):
            print(f"  {req} --> {file}")
    print("```")
```

## 📊 효과 측정

### Before (메타데이터 없음)
```
test_auth.py          # 이게 뭐지?
test_auth_v2.py       # 새 버전인가?
test_auth_final.py    # 이게 최종?
verify_something.py   # 뭘 검증?
check_data.py         # 어떤 데이터?
analysis.py           # 무슨 분석?
```

### After (메타데이터 적용)
```
test_auth.py          # @meta: test-unit | 2025-09-15 | keep
                      # Core auth 테스트, 영구 보존

test_auth_v2.py       # @meta: test-experiment | 2025-09-10 | deprecated
                      # OAuth 실험, 삭제 예정

verify_migration.py   # @meta: verify-data | 2025-09-01 | archive
                      # 완료된 마이그레이션 검증, 아카이브
```

## 🚀 즉시 시작하기

### Step 1: Git Hook 설치
```bash
cp scripts/pre-commit-metadata .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Step 2: 기존 파일 일괄 처리
```bash
python scripts/add_metadata_bulk.py --auto-detect
```

### Step 3: 첫 정리 실행
```bash
python scripts/clean_artifacts.py --dry-run
# 확인 후
python scripts/clean_artifacts.py --execute
```

## 🎯 기대 효과

1. **즉각적 파악**: 파일 목적을 3초 안에 이해
2. **자동 정리**: 수명 주기에 따른 자동 아카이빙
3. **중복 방지**: 같은 목적의 파일 즉시 발견
4. **의존성 추적**: 어떤 파일이 연관되어 있는지 명확
5. **재사용성**: 필요한 도구/분석 빠르게 찾기

## 📝 체크리스트

### 파일 생성 시
- [ ] 메타데이터 추가 (최소 3초 버전)
- [ ] purpose 명확히 작성
- [ ] lifecycle 상태 결정 (keep/temp/archive)

### 작업 완료 시
- [ ] @results 섹션 업데이트
- [ ] lifecycle를 archive로 변경
- [ ] next_steps 기록

### 주기적 정리 (주 1회)
- [ ] `clean_artifacts.py --dry-run` 실행
- [ ] deprecated 파일 검토
- [ ] archive 폴더 정리

---

*"Small metadata, Big impact - 작은 투자로 큰 효율을"*