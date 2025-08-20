#!/usr/bin/env python3
"""
컨텍스트 관리 A/B 테스트 프레임워크
"""
import json
import random
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Literal, Optional
from dataclasses import dataclass, asdict

TestGroup = Literal["control", "treatment"]

@dataclass
class TestSession:
    """테스트 세션 데이터"""
    session_id: str
    group: TestGroup
    start_time: str
    task_description: str
    task_type: str  # strategic, tactical, operational
    
    # 결과 메트릭 (완료 시 업데이트)
    completion_time_minutes: Optional[float] = None
    success_achieved: bool = False
    context_management_used: bool = False
    duplicate_work_detected: bool = False
    consistency_maintained: bool = True
    user_satisfaction: Optional[int] = None  # 1-5 scale

class ABTestFramework:
    """A/B 테스트 관리 클래스"""
    
    def __init__(self, test_file: str = "docs/CURRENT/ab_test_results.json"):
        self.test_file = Path(test_file)
        self.test_file.parent.mkdir(parents=True, exist_ok=True)
        
    def assign_test_group(self, user_id: str, task_description: str) -> TestGroup:
        """사용자를 테스트 그룹에 할당"""
        # 일관된 그룹 할당을 위한 해시 기반 분배
        hash_input = f"{user_id}_{task_description}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest()[:8], 16)
        
        # 50-50 분배
        return "treatment" if hash_value % 2 == 0 else "control"
    
    def start_test_session(
        self,
        user_id: str,
        task_description: str,
        task_type: str
    ) -> Dict[str, str]:
        """테스트 세션 시작"""
        group = self.assign_test_group(user_id, task_description)
        session_id = f"{group}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id[:8]}"
        
        session = TestSession(
            session_id=session_id,
            group=group,
            start_time=datetime.now().isoformat(),
            task_description=task_description,
            task_type=task_type
        )
        
        self._save_session(session)
        
        return {
            "session_id": session_id,
            "group": group,
            "recommendation": self._get_group_recommendation(group, task_type)
        }
    
    def _get_group_recommendation(self, group: TestGroup, task_type: str) -> str:
        """그룹별 권장사항"""
        if group == "control":
            return "기존 방식 사용: 전체 컨텍스트 유지"
        else:
            # 치료군 - 작업 유형별 차별화된 컨텍스트 관리
            if task_type == "strategic":
                return "치료군: Strategic 수준 컨텍스트 관리 적용"
            elif task_type == "tactical":
                return "치료군: Tactical 수준 컨텍스트 관리 적용"
            else:
                return "치료군: Operational 수준 컨텍스트 관리 적용"
    
    def complete_test_session(
        self,
        session_id: str,
        completion_time_minutes: float,
        success_achieved: bool,
        **kwargs
    ) -> None:
        """테스트 세션 완료"""
        sessions = self._load_sessions()
        
        if session_id in sessions:
            session_data = sessions[session_id]
            session_data.update({
                "completion_time_minutes": completion_time_minutes,
                "success_achieved": success_achieved,
                **kwargs
            })
            sessions[session_id] = session_data
            self._save_all_sessions(sessions)
    
    def analyze_results(self) -> Dict:
        """결과 분석"""
        sessions = self._load_sessions()
        
        if not sessions:
            return {"error": "No test data available"}
        
        control_sessions = [s for s in sessions.values() if s["group"] == "control"]
        treatment_sessions = [s for s in sessions.values() if s["group"] == "treatment"]
        
        if not control_sessions or not treatment_sessions:
            return {"error": "Insufficient data for comparison"}
        
        control_stats = self._calculate_group_stats(control_sessions)
        treatment_stats = self._calculate_group_stats(treatment_sessions)
        
        return {
            "control_group": control_stats,
            "treatment_group": treatment_stats,
            "comparison": {
                "completion_time_improvement": self._calculate_improvement(
                    control_stats["avg_completion_time"],
                    treatment_stats["avg_completion_time"],
                    reverse=True  # 더 빠른 것이 좋음
                ),
                "success_rate_improvement": self._calculate_improvement(
                    control_stats["success_rate"],
                    treatment_stats["success_rate"]
                ),
                "consistency_improvement": self._calculate_improvement(
                    control_stats["consistency_rate"],
                    treatment_stats["consistency_rate"]
                )
            },
            "statistical_significance": self._check_significance(control_sessions, treatment_sessions)
        }
    
    def _calculate_group_stats(self, sessions: List[Dict]) -> Dict:
        """그룹 통계 계산"""
        completed_sessions = [s for s in sessions if s.get("completion_time_minutes") is not None]
        
        if not completed_sessions:
            return {"error": "No completed sessions"}
        
        return {
            "total_sessions": len(sessions),
            "completed_sessions": len(completed_sessions),
            "avg_completion_time": sum(s["completion_time_minutes"] for s in completed_sessions) / len(completed_sessions),
            "success_rate": sum(1 for s in completed_sessions if s.get("success_achieved")) / len(completed_sessions) * 100,
            "consistency_rate": sum(1 for s in completed_sessions if s.get("consistency_maintained")) / len(completed_sessions) * 100,
            "duplicate_work_rate": sum(1 for s in completed_sessions if s.get("duplicate_work_detected")) / len(completed_sessions) * 100
        }
    
    def _calculate_improvement(self, control_value: float, treatment_value: float, reverse: bool = False) -> float:
        """개선율 계산"""
        if control_value == 0:
            return 0.0
        
        improvement = (treatment_value - control_value) / control_value * 100
        return -improvement if reverse else improvement
    
    def _check_significance(self, control_sessions: List[Dict], treatment_sessions: List[Dict]) -> Dict:
        """통계적 유의성 검정 (간단한 버전)"""
        # 실제로는 t-test 등을 사용해야 하지만, 여기서는 간단한 체크
        control_size = len([s for s in control_sessions if s.get("completion_time_minutes") is not None])
        treatment_size = len([s for s in treatment_sessions if s.get("completion_time_minutes") is not None])
        
        return {
            "sample_size_adequate": control_size >= 10 and treatment_size >= 10,
            "control_sample_size": control_size,
            "treatment_sample_size": treatment_size,
            "note": "실제 프로덕션에서는 적절한 통계 검정 필요"
        }
    
    def _load_sessions(self) -> Dict:
        """세션 로드"""
        if not self.test_file.exists():
            return {}
        try:
            with open(self.test_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_session(self, session: TestSession) -> None:
        """세션 저장"""
        sessions = self._load_sessions()
        sessions[session.session_id] = asdict(session)
        self._save_all_sessions(sessions)
    
    def _save_all_sessions(self, sessions: Dict) -> None:
        """전체 세션 저장"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, indent=2, ensure_ascii=False)

def main():
    """CLI 인터페이스"""
    import sys
    
    framework = ABTestFramework()
    
    if len(sys.argv) < 2:
        print("Usage: python ab_test_framework.py [start|complete|analyze] [args...]")
        return
    
    command = sys.argv[1]
    
    if command == "start":
        if len(sys.argv) < 5:
            print("Usage: start <user_id> <task_description> <task_type>")
            return
        result = framework.start_test_session(sys.argv[2], sys.argv[3], sys.argv[4])
        print(f"Test session started: {result}")
        
    elif command == "complete":
        if len(sys.argv) < 5:
            print("Usage: complete <session_id> <completion_time_minutes> <success_achieved>")
            return
        framework.complete_test_session(
            sys.argv[2], 
            float(sys.argv[3]), 
            sys.argv[4].lower() == 'true'
        )
        print("Session completed")
        
    elif command == "analyze":
        results = framework.analyze_results()
        print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()