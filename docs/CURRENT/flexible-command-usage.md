# 🌐 Research Project Manager - 유연한 명령어 사용법

## ✨ 핵심 답변: 영어/한글 모두 사용 가능!

**질문**: "서브커맨드들은 정확하게 영어로 써야 하는거?"

**답변**: **아니요! 한글, 영어, 심지어 축약어도 모두 사용 가능합니다.**

## 📚 3가지 사용 방법

### 1️⃣ 기본 영어 인터페이스 (Original)
```python
from research_project_manager import ResearchProjectManager

manager = ResearchProjectManager()
manager.init_project("my_research", "Description")
manager.track_progress("Work completed")
manager.set_milestone("Phase 1", "Complete")
```

### 2️⃣ 완전 한글 인터페이스 (Korean)
```python
from research_manager_korean import 연구프로젝트관리자

관리자 = 연구프로젝트관리자()
관리자.프로젝트_생성("내_연구", "설명")
관리자.진행사항_기록("작업 완료")
관리자.마일스톤_설정("1단계", "완료")
```

### 3️⃣ 하이브리드 인터페이스 (Flexible) ⭐ 추천!
```python
from research_manager_hybrid import HybridResearchManager

manager = HybridResearchManager()

# 모든 형태의 명령어 사용 가능!
manager.execute("생성", "프로젝트1", "설명")      # 한글
manager.execute("init", "project2", "desc")       # 영어
manager.execute("create", "project3", "desc")     # 별칭

# 또는 직접 메서드 호출
manager.프로젝트_생성("한글프로젝트", "설명")     # 한글 메서드
manager.init_project("english_project", "desc")   # 영어 메서드
```

## 🔄 명령어 대응표

| 기능 | 영어 명령어 | 한글 명령어 | 축약어/별칭 |
|------|------------|------------|------------|
| **프로젝트 생성** | init_project | 프로젝트_생성 | 생성, 초기화, 시작, create, new |
| **진행사항 기록** | track_progress | 진행사항_기록 | 진행, 기록, track, log |
| **마일스톤 설정** | set_milestone | 마일스톤_설정 | 마일스톤, 목표, 달성 |
| **프로젝트 목록** | list_projects | 프로젝트_목록 | 목록, 리스트, all, show |
| **프로젝트 전환** | switch_project | 프로젝트_전환 | 전환, 변경, change, goto |
| **프로젝트 보관** | archive_project | 프로젝트_보관 | 보관, 완료, 종료, finish |
| **데이터 탐색** | explore_data | 데이터_탐색 | 탐색, 분석, eda, analyze |
| **가설 설정** | set_hypothesis | 가설_설정 | 가설, 이론, theory |
| **실험 시작** | start_experiment | 실험_시작 | 실험, 테스트, test, trial |
| **결과 검증** | validate_results | 결과_검증 | 검증, 확인, verify, check |
| **체크포인트** | checkpoint | 체크포인트 | 저장, 백업, save |
| **복원** | resume_from_checkpoint | 체크포인트_복원 | 복원, 재개, restore, continue |
| **결과 공유** | share_results | 결과_공유 | 공유, 배포, export, publish |
| **도구 목록** | list_tools | 도구_목록 | 도구, 툴, utilities |

## 💡 실제 사용 예시

### 예시 1: 한국 연구자용 (완전 한글)
```python
from research_manager_korean import 연구관리자

관리자 = 연구관리자()

# 신약 개발 프로젝트
관리자.프로젝트_생성("신약개발", "코로나19 치료제 개발")
관리자.진행사항_기록("화합물 1000개 스크리닝 완료")
관리자.가설_설정("화합물 X가 바이러스 증식을 억제할 것")
관리자.실험_시작("세포실험", "Vero 세포주 사용")
관리자.마일스톤_설정("전임상 완료", "세포 실험 성공")
```

### 예시 2: 국제 협업용 (영어)
```python
from research_project_manager import ResearchProjectManager

manager = ResearchProjectManager()

# Drug discovery project
manager.init_project("drug_discovery", "COVID-19 therapeutic")
manager.track_progress("Screened 1000 compounds")
manager.set_hypothesis("Compound X inhibits viral replication")
manager.start_experiment("cell_assay", "Using Vero cells")
manager.set_milestone("Preclinical complete", "Cell assay success")
```

### 예시 3: 편한대로 섞어서 (하이브리드)
```python
from research_manager_hybrid import HybridResearchManager

m = HybridResearchManager()

# 편한 언어로 자유롭게!
m.execute("생성", "ai_drug", "AI 신약 개발")     # 한글로 시작
m.track_progress("Dataset prepared")              # 영어로 기록
m.execute("실험", "ml_model", "딥러닝 모델")     # 다시 한글
m.checkpoint("모델 학습 완료")                    # 한글 메서드
m.validate_results("Cross validation")            # 영어 메서드
```

## 🎯 Claude Code와 사용하기

Claude Code에서는 자연어로 요청하면 자동으로 적절한 인터페이스를 선택합니다:

```
You: "연구 프로젝트 시작해줘"
Claude: [한글 인터페이스로 프로젝트 생성]

You: "Start a new research project"
Claude: [영어 인터페이스로 프로젝트 생성]

You: "진행사항 track 해줘: 데이터 수집 완료"
Claude: [하이브리드로 처리]
```

## 🔧 설치 및 Import

```python
# 영어만
from research_project_manager import ResearchProjectManager

# 한글만
from research_manager_korean import 연구프로젝트관리자
# 또는 짧게
from research_manager_korean import 연구관리자

# 하이브리드 (추천!)
from research_manager_hybrid import HybridResearchManager
```

## 📋 빠른 참조

### 가장 자주 쓰는 명령어
```python
# 하이브리드 매니저 사용 시
m = HybridResearchManager()

# 5개 핵심 명령어 (한/영 모두 가능)
m.execute("생성", "프로젝트명", "설명")     # 프로젝트 시작
m.execute("진행", "오늘 작업 완료")         # 진행사항 기록
m.execute("마일스톤", "1단계", "완료")      # 중요 지점 표시
m.execute("실험", "실험1", "테스트")        # 실험 시작
m.execute("체크포인트", "백업 메모")        # 상태 저장

# 영어도 OK
m.execute("init", "project", "desc")
m.execute("track", "Work done")
m.execute("milestone", "Phase 1", "Done")
m.execute("experiment", "exp1", "test")
m.execute("checkpoint", "Backup note")
```

## ❓ FAQ

**Q: 한글과 영어를 섞어서 써도 되나요?**
```python
# 네! 하이브리드 매니저는 모두 이해합니다
m.프로젝트_생성("project", "프로젝트 설명")  # OK
m.track_progress("데이터 분석 완료")          # OK
```

**Q: 축약어나 별칭도 사용 가능한가요?**
```python
# 네! execute() 메서드로 다양한 별칭 사용 가능
m.execute("new", "프로젝트", "설명")     # new = init
m.execute("log", "작업 완료")            # log = track_progress
m.execute("save", "체크포인트")          # save = checkpoint
```

**Q: 어떤 인터페이스를 추천하나요?**
- **한국 팀 전용**: `연구프로젝트관리자` (완전 한글)
- **국제 협업**: `ResearchProjectManager` (영어)
- **유연함 원할 때**: `HybridResearchManager` (추천!)

## 🎉 결론

**서브커맨드는 영어로 정확하게 쓸 필요 없습니다!**

- ✅ 한글 명령어 완벽 지원
- ✅ 영어/한글 자유롭게 혼용 가능
- ✅ 축약어와 별칭도 사용 가능
- ✅ 본인에게 편한 방식으로 사용하세요!

```python
# 가장 간단한 시작
from research_manager_hybrid import HybridResearchManager
m = HybridResearchManager()
m.execute("생성", "내프로젝트", "편하게 한글로!")
print("🎉 성공!")
```

---
**Version**: 2.0.0 (Multilingual Support)  
**Last Updated**: 2025-09-10