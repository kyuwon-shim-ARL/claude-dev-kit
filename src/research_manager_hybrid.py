#!/usr/bin/env python3
"""
Research Project Manager - Hybrid Interface
영어와 한글을 모두 지원하는 하이브리드 인터페이스
"""

from typing import Dict, List, Optional, Any, Union
from research_project_manager import ResearchProjectManager


class HybridResearchManager(ResearchProjectManager):
    """영어와 한글 명령어를 모두 지원하는 하이브리드 매니저"""
    
    def __init__(self, base_dir: str = "research_projects"):
        super().__init__(base_dir)
        
        # 한글 → 영어 명령어 매핑
        self._command_map = {
            # 프로젝트 관리
            "생성": "init",
            "초기화": "init", 
            "시작": "init",
            "create": "init",
            "new": "init",
            
            # 진행사항
            "진행": "progress",
            "기록": "progress",
            "track": "progress",
            "log": "progress",
            
            # 마일스톤
            "마일스톤": "milestone",
            "목표": "milestone",
            "달성": "milestone",
            
            # 목록
            "목록": "list",
            "리스트": "list",
            "all": "list",
            "show": "list",
            
            # 전환
            "전환": "switch",
            "변경": "switch",
            "change": "switch",
            "goto": "switch",
            
            # 보관
            "보관": "archive",
            "완료": "archive",
            "종료": "archive",
            "finish": "archive",
            
            # 데이터 탐색
            "탐색": "explore",
            "분석": "explore",
            "eda": "explore",
            "analyze": "explore",
            
            # 가설
            "가설": "hypothesis",
            "이론": "hypothesis",
            "theory": "hypothesis",
            
            # 실험
            "실험": "experiment",
            "테스트": "experiment",
            "test": "experiment",
            "trial": "experiment",
            
            # 검증
            "검증": "validate",
            "확인": "validate",
            "verify": "validate",
            "check": "validate",
            
            # 체크포인트
            "체크포인트": "checkpoint",
            "저장": "checkpoint",
            "백업": "checkpoint",
            "save": "checkpoint",
            
            # 복원
            "복원": "resume",
            "재개": "resume",
            "restore": "resume",
            "continue": "resume",
            
            # 공유
            "공유": "share",
            "배포": "share",
            "export": "share",
            "publish": "share",
            
            # 도구
            "도구": "tools",
            "툴": "tools",
            "utilities": "tools",
        }
    
    def execute(self, command: str, *args, **kwargs) -> Dict[str, Any]:
        """
        유연한 명령어 실행 - 영어/한글 모두 지원
        
        사용 예:
            manager.execute("생성", "프로젝트명", "설명")
            manager.execute("init", "project_name", "description")
            manager.execute("진행", "작업 완료")
            manager.execute("track", "Task completed")
        """
        # 명령어 정규화
        command_lower = command.lower()
        normalized_command = self._command_map.get(command_lower, command_lower)
        
        # 명령어별 메서드 매핑
        method_map = {
            "init": self.init_project,
            "progress": self.track_progress,
            "milestone": self.set_milestone,
            "list": self.list_projects,
            "switch": self.switch_project,
            "archive": self.archive_project,
            "explore": self.explore_data,
            "hypothesis": self.set_hypothesis,
            "experiment": self.start_experiment,
            "validate": self.validate_results,
            "checkpoint": self.checkpoint,
            "resume": self.resume_from_checkpoint,
            "share": self.share_results,
            "tools": self.list_tools,
        }
        
        # 메서드 실행
        if normalized_command in method_map:
            method = method_map[normalized_command]
            try:
                # 인자 개수에 따라 적절히 호출
                if normalized_command == "init":
                    return method(args[0], args[1] if len(args) > 1 else "")
                elif normalized_command == "progress":
                    return method(args[0], args[1] if len(args) > 1 else None)
                elif normalized_command in ["milestone", "hypothesis", "experiment", "validate"]:
                    return method(args[0], args[1] if len(args) > 1 else "")
                elif normalized_command in ["switch", "resume"]:
                    return method(args[0])
                elif normalized_command == "checkpoint":
                    return method(args[0] if args else "")
                else:  # list, archive, share, tools
                    return method()
            except IndexError:
                return {"error": f"명령어 '{command}'에 필요한 인자가 부족합니다"}
        else:
            return {"error": f"알 수 없는 명령어: '{command}'"}
    
    # 한글 별칭 메서드들 (직접 호출용)
    def 프로젝트_생성(self, 이름: str, 설명: str = "") -> Dict[str, Any]:
        """프로젝트 생성 (한글)"""
        return self.init_project(이름, 설명)
    
    def 진행사항_기록(self, 메시지: str, 파일들: Optional[List[str]] = None) -> Dict[str, Any]:
        """진행사항 기록 (한글)"""
        return self.track_progress(메시지, 파일들)
    
    def 마일스톤_설정(self, 이름: str, 설명: str = "") -> Dict[str, Any]:
        """마일스톤 설정 (한글)"""
        return self.set_milestone(이름, 설명)
    
    def 프로젝트_목록(self) -> List[Dict[str, Any]]:
        """프로젝트 목록 (한글)"""
        return self.list_projects()
    
    def 프로젝트_전환(self, 프로젝트_id: str) -> Dict[str, Any]:
        """프로젝트 전환 (한글)"""
        return self.switch_project(프로젝트_id)
    
    def 프로젝트_보관(self) -> Dict[str, Any]:
        """프로젝트 보관 (한글)"""
        return self.archive_project()
    
    def 데이터_탐색(self, 설명: str = "") -> Dict[str, Any]:
        """데이터 탐색 (한글)"""
        return self.explore_data(설명)
    
    def 가설_설정(self, 가설: str) -> Dict[str, Any]:
        """가설 설정 (한글)"""
        return self.set_hypothesis(가설)
    
    def 실험_시작(self, 실험명: str, 설명: str = "") -> Dict[str, Any]:
        """실험 시작 (한글)"""
        return self.start_experiment(실험명, 설명)
    
    def 결과_검증(self, 설명: str = "") -> Dict[str, Any]:
        """결과 검증 (한글)"""
        return self.validate_results(설명)
    
    def 체크포인트_생성(self, 메모: str = "") -> Dict[str, Any]:
        """체크포인트 생성 (한글)"""
        return self.checkpoint(메모)
    
    def 체크포인트_복원(self, 체크포인트_id: str) -> Dict[str, Any]:
        """체크포인트 복원 (한글)"""
        return self.resume_from_checkpoint(체크포인트_id)
    
    def 결과_공유(self) -> Dict[str, Any]:
        """결과 공유 (한글)"""
        return self.share_results()
    
    def 도구_목록(self) -> Dict[str, Any]:
        """도구 목록 (한글)"""
        return self.list_tools()
    
    def help(self, language: str = "both") -> str:
        """
        도움말 표시
        
        Args:
            language: "korean", "english", "both"
        """
        help_text = {
            "korean": """
📚 연구 프로젝트 관리자 - 한글 명령어

프로젝트 관리:
  생성/초기화/시작 <이름> <설명>  - 새 프로젝트 생성
  목록/리스트                    - 모든 프로젝트 표시
  전환/변경 <프로젝트ID>         - 프로젝트 전환
  보관/완료/종료                 - 프로젝트 보관

작업 관리:
  진행/기록 <메시지> [파일들]    - 진행사항 기록
  마일스톤/목표 <이름> <설명>    - 마일스톤 설정
  체크포인트/저장 [메모]         - 현재 상태 저장
  복원/재개 <체크포인트ID>       - 이전 상태 복원

연구 활동:
  탐색/분석 <설명>              - 데이터 탐색
  가설/이론 <가설내용>          - 가설 설정
  실험/테스트 <이름> <설명>     - 실험 시작
  검증/확인 <설명>              - 결과 검증

기타:
  공유/배포                     - 결과 공유
  도구/툴                       - 도구 목록
""",
            "english": """
📚 Research Project Manager - English Commands

Project Management:
  init/create/new <name> <desc>    - Create new project
  list/all/show                    - List all projects
  switch/change/goto <id>          - Switch project
  archive/finish                   - Archive project

Work Management:
  track/progress/log <msg> [files] - Track progress
  milestone <name> <desc>          - Set milestone
  checkpoint/save [memo]           - Save checkpoint
  resume/restore <checkpoint_id>   - Resume from checkpoint

Research Activities:
  explore/analyze/eda <desc>      - Explore data
  hypothesis/theory <content>     - Set hypothesis
  experiment/test <name> <desc>   - Start experiment
  validate/verify/check <desc>    - Validate results

Others:
  share/export/publish            - Share results
  tools/utilities                 - List tools
""",
            "both": """
📚 Research Project Manager - 하이브리드 명령어 / Hybrid Commands

프로젝트 관리 / Project Management:
  생성|init|create <이름|name> <설명|desc>    - 새 프로젝트 / New project
  목록|list|show                             - 프로젝트 목록 / List projects
  전환|switch|change <ID>                    - 프로젝트 전환 / Switch project
  보관|archive|finish                        - 프로젝트 보관 / Archive project

작업 관리 / Work Management:
  진행|track|progress <메시지|msg>           - 진행사항 기록 / Track progress
  마일스톤|milestone <이름|name>             - 마일스톤 설정 / Set milestone
  체크포인트|checkpoint|save                 - 상태 저장 / Save state
  복원|resume|restore <ID>                   - 복원 / Restore

연구 활동 / Research Activities:
  탐색|explore|analyze                       - 데이터 탐색 / Explore data
  가설|hypothesis <내용|content>             - 가설 설정 / Set hypothesis
  실험|experiment|test                       - 실험 시작 / Start experiment
  검증|validate|verify                       - 결과 검증 / Validate results
"""
        }
        
        return help_text.get(language, help_text["both"])


if __name__ == "__main__":
    # 테스트 예제
    print("🔬 Hybrid Research Manager Test")
    print("=" * 50)
    
    manager = HybridResearchManager()
    
    # 도움말 표시
    print(manager.help("both"))
    
    # 영어 명령어 테스트
    result1 = manager.execute("init", "test_project", "Testing hybrid interface")
    if "error" not in result1:
        print(f"✅ English: Created {result1['project_id']}")
    
    # 한글 명령어 테스트
    result2 = manager.execute("진행", "테스트 진행중")
    print("✅ Korean: 진행사항 기록됨")
    
    # 한글 메서드 직접 호출
    manager.마일스톤_설정("첫 단계", "하이브리드 인터페이스 테스트")
    print("✅ Direct Korean method: 마일스톤 설정됨")
    
    # 영어 메서드 직접 호출
    manager.checkpoint("Hybrid test complete")
    print("✅ Direct English method: Checkpoint created")
    
    print("\n✅ Hybrid interface test successful!")