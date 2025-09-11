"""
기획 라우팅 시스템 - LLM 지능형 모드 선택
"""

from typing import Dict, List, Any


class PlanningRouter:
    """기획 요청을 분석하여 적절한 모드와 실행 계획을 생성"""
    
    def __init__(self):
        self.report_keywords = [
            "보고서", "리포트", "대시보드", "차트", "그래프", 
            "HTML", "Astro", "시각화", "분석 결과"
        ]
        
    def detect_intent(self, user_input: str) -> str:
        """사용자 입력에서 의도를 감지"""
        input_lower = user_input.lower()
        
        # 보고서 관련 키워드 감지
        if any(keyword in input_lower for keyword in self.report_keywords):
            return "report_generation"
        
        # 다른 모드들
        if any(word in input_lower for word in ["분석", "이해", "설명"]):
            return "analysis"
        elif any(word in input_lower for word in ["구현", "개발", "만들"]):
            return "implementation"
        else:
            return "general"
    
    def create_execution_plan(self, mode: str, user_input: str) -> Dict[str, Any]:
        """감지된 모드에 따라 실행 계획 생성"""
        if mode == "report_generation":
            return {
                "mode": "report_generation",
                "phases": [
                    "data_loading",
                    "template_selection", 
                    "astro_build",
                    "deployment"
                ],
                "template_type": self._select_template_type(user_input),
                "estimated_duration": "5-10 minutes"
            }
        
        # 기본 실행 계획
        return {
            "mode": mode,
            "phases": ["planning", "implementation", "testing"],
            "template_type": "default",
            "estimated_duration": "varies"
        }
    
    def _select_template_type(self, user_input: str) -> str:
        """사용자 입력에서 템플릿 타입 선택"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["과학", "연구", "학회", "scientific"]):
            return "scientific"
        elif any(word in input_lower for word in ["경영진", "임원", "ceo", "브리핑", "executive"]):
            return "executive"  
        elif any(word in input_lower for word in ["대시보드", "dashboard", "실시간"]):
            return "dashboard"
        else:
            return "scientific"  # 기본값