<!--
@meta
id: document_20250905_1110_document_tracking_system
type: document
scope: operational
status: active
created: 2025-09-05
updated: 2025-09-09
tags: CURRENT, document, tracking, document_tracking_system.md, system
related: 
-->

---
meta:
  context_hash: 220b45b4c048
  created: '2025-09-01T20:05:18.900699'
  file_path: docs/CURRENT/document_tracking_system.md
  id: doc_20250901_200518_document_tracking_sy
  keywords:
  - "\uBB38\uC11C \uCD94\uC801 \uC2DC\uC2A4\uD15C \uC124\uACC4 (document tracking\
    \ system)"
  - "\U0001F3AF \uD575\uC2EC \uBB38\uC81C\uC640 \uD574\uACB0\uCC45"
  - "\uBB38\uC81C: \"\uD504\uB86C\uD504\uD2B8\uB9C8\uB2E4 \uC0C8\uB85C\uC6B4 \uB9E5\
    \uB77D\uC73C\uB85C \uBB38\uC11C\uAC00 \uC790\uC720\uB86D\uAC8C \uC0DD\uC131\""
  - "\uD574\uACB0: 3\uB2E8\uACC4 \uC790\uB3D9 \uCD94\uC801 \uC2DC\uC2A4\uD15C"
  - "\U0001F4CB 1\uB2E8\uACC4: \uC0DD\uC131 \uC2DC\uC810 \uBA54\uD0C0\uB370\uC774\uD130\
    \ \uC790\uB3D9 \uC0BD\uC785"
  - "\U0001F4CA 2\uB2E8\uACC4: \uC2E4\uC2DC\uAC04 \uCC38\uC870 \uADF8\uB798\uD504\
    \ \uAD6C\uCD95"
  - "\U0001F504 3\uB2E8\uACC4: \uC0C1\uD0DC \uC804\uD658 \uC790\uB3D9\uD654"
  - "\U0001F3A8 4\uB2E8\uACC4: \uC9C0\uB2A5\uD615 \uBB38\uC11C \uAC80\uC0C9"
  - "\U0001F680 5\uB2E8\uACC4: git hooks \uD1B5\uD569"
  - .git/hooks/pre-commit
  parent: null
  references: []
  session: git_commit_@1756724787 +0900
  status: draft
  triggers:
  - docs/CURRENT/document_tracking_system.md
  type: tutorial
  updated: 2025-09-09
---

# 문서 추적 시스템 설계 (Document Tracking System)

## 🎯 핵심 문제와 해결책

### 문제: "프롬프트마다 새로운 맥락으로 문서가 자유롭게 생성"
- 매번 다른 파일명과 위치
- 상태나 참조 관계 파악 불가
- 위계 구조 파악 어려움

### 해결: 3단계 자동 추적 시스템

## 📋 1단계: 생성 시점 메타데이터 자동 삽입

```python
def create_document_with_metadata(content, doc_type, references=[]):
    """모든 문서 생성 시 자동 호출"""
    
    metadata = {
        "id": generate_unique_id(),           # doc_20240901_143022_auth_guide
        "type": detect_document_type(content), # tutorial/planning/research/api
        "status": "draft",                     # draft→review→published→archived
        "parent": find_parent_document(),      # PRD나 상위 문서 자동 탐지
        "triggers": get_current_context(),     # 현재 작업 중인 코드/문서
        "created": datetime.now(),
        "session": get_session_id(),          # Claude 세션 ID
        "context_hash": hash(current_prompt)  # 프롬프트 컨텍스트 해시
    }
    
    # 문서 상단에 YAML front matter로 삽입
    return f"""---
meta: {yaml.dump(metadata)}
---

{content}"""
```

## 📊 2단계: 실시간 참조 그래프 구축

```python
class DocumentGraph:
    """문서 간 관계를 실시간으로 추적"""
    
    def __init__(self):
        self.graph = nx.DiGraph()  # 방향성 그래프
        self.load_existing_documents()
    
    def add_document(self, doc_id, metadata):
        """새 문서 추가 시 자동으로 그래프 업데이트"""
        self.graph.add_node(doc_id, **metadata)
        
        # 부모 문서와 연결
        if metadata.get('parent'):
            self.graph.add_edge(metadata['parent'], doc_id, 
                               relation='generates')
        
        # 트리거된 코드와 연결
        for trigger in metadata.get('triggers', []):
            self.graph.add_edge(trigger, doc_id, 
                               relation='documents')
    
    def find_related_documents(self, doc_id, depth=2):
        """특정 문서와 관련된 모든 문서 찾기"""
        return nx.ego_graph(self.graph, doc_id, radius=depth)
    
    def get_document_lineage(self, doc_id):
        """문서의 전체 계보 추적"""
        ancestors = nx.ancestors(self.graph, doc_id)
        descendants = nx.descendants(self.graph, doc_id)
        return {
            'ancestors': list(ancestors),
            'descendants': list(descendants)
        }
```

## 🔄 3단계: 상태 전환 자동화

```python
class DocumentLifecycle:
    """문서 생명주기 자동 관리"""
    
    TRANSITIONS = {
        'draft': ['review', 'archived'],
        'review': ['published', 'draft'],
        'published': ['deprecated', 'updated'],
        'deprecated': ['archived'],
        'archived': []  # 종료 상태
    }
    
    def auto_transition(self, doc_id):
        """조건에 따른 자동 상태 전환"""
        doc = self.get_document(doc_id)
        
        # 30일 이상 수정 없음 → deprecated
        if doc.status == 'published' and doc.age > 30:
            self.transition_to(doc_id, 'deprecated')
        
        # 관련 코드 삭제됨 → archived
        if not self.check_triggers_exist(doc.triggers):
            self.transition_to(doc_id, 'archived')
        
        # PRD 업데이트 → 하위 문서들 review 상태로
        if doc.type == 'PRD' and doc.updated:
            for child in self.get_children(doc_id):
                self.transition_to(child, 'review')
```

## 🎨 4단계: 지능형 문서 검색

```python
class SmartDocumentSearch:
    """컨텍스트 기반 지능형 검색"""
    
    def find_by_context(self, current_work):
        """현재 작업과 관련된 문서 자동 검색"""
        
        # 1. 현재 수정 중인 파일 기반
        if editing_file := get_current_file():
            related = self.graph.neighbors(editing_file)
        
        # 2. 최근 대화 컨텍스트 기반
        context_keywords = extract_keywords(recent_messages)
        semantic_matches = self.semantic_search(context_keywords)
        
        # 3. 시간적 근접성 (최근 작업한 문서)
        recent_docs = self.get_recent_documents(hours=24)
        
        # 4. 종합 점수 계산
        return self.rank_documents(
            related + semantic_matches + recent_docs
        )
```

## 🚀 5단계: Git Hooks 통합

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 문서 메타데이터 자동 업데이트
python scripts/update_document_metadata.py

# 문서 참조 그래프 재구축
python scripts/rebuild_document_graph.py

# 상태 전환 체크
python scripts/check_document_transitions.py

# 변경사항을 스테이징에 추가
git add docs/.metadata/
git add docs/.graph/
```

## 📈 실제 사용 예시

### 자동 추적 시나리오:
```
1. 사용자: "인증 시스템 구현해줘"
   → auth.py 생성
   → auth-guide.md 자동 생성 (메타데이터 포함)
   → 그래프에 auth.py → auth-guide.md 연결

2. 사용자: "테스트 추가해줘"  
   → auth.test.py 생성
   → auth-test-plan.md 생성
   → 그래프에 auth.py → auth.test.py → auth-test-plan.md 연결

3. 사용자: "문서 정리해줘"
   → 시스템이 자동으로 그래프 분석
   → auth 관련 문서들을 하나의 클러스터로 인식
   → 적절한 디렉토리 구조 제안
```

### 검색 시나리오:
```python
# 사용자가 "인증 버그 수정" 요청 시
related_docs = system.find_by_context("authentication bug")
# 자동으로 찾아지는 문서들:
# - auth-guide.md (type: tutorial, status: published)
# - auth-test-plan.md (type: test, status: review)  
# - auth-troubleshooting.md (type: knowledge, status: draft)
# - PRD_v3.2.md (section: authentication requirements)
```

## 🎯 ZED와의 통합

**기존 ZED(/문서정리)**: 사후 정리 도구
**신규 추적 시스템**: 실시간 메타데이터 기록

### 통합 워크플로우:
```bash
# 1. 개발 중 - 자동 추적
/구현  → 메타데이터 자동 생성 → 그래프 자동 구축

# 2. 정리 시점 - ZED 활용
/문서정리 → 메타데이터 기반 스마트 정리 → 그래프 기반 구조화

# 3. 보고 시점 - 종합 분석
/주간보고 → 그래프 분석 → 문서 관계도 포함 보고
```

## 💡 핵심 이점

1. **완전 자동화**: 문서 생성 시점부터 자동 추적
2. **관계 파악**: 문서 간 참조 관계 실시간 구축
3. **상태 관리**: 생명주기 자동 관리
4. **스마트 검색**: 컨텍스트 기반 지능형 검색
5. **ZED 연동**: 기존 도구와 시너지

이제 "프롬프트마다 새로운 맥락"이어도 시스템이 자동으로 추적하고 관리합니다.