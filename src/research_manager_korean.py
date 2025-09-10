#!/usr/bin/env python3
"""
Research Project Manager - 한글 인터페이스
한글 메서드명으로 편하게 사용할 수 있는 래퍼 클래스
"""

from typing import Dict, List, Optional, Any
from research_project_manager import ResearchProjectManager


class 연구프로젝트관리자:
    """ResearchProjectManager의 한글 인터페이스"""
    
    def __init__(self, 기본_디렉토리: str = "research_projects"):
        """
        연구 프로젝트 관리자 초기화
        
        Args:
            기본_디렉토리: 프로젝트들을 저장할 기본 디렉토리
        """
        self._manager = ResearchProjectManager(base_dir=기본_디렉토리)
        
        # 속성 직접 접근을 위한 프록시
        self.메타데이터 = self._manager.metadata
        self.기본디렉토리 = self._manager.base_dir
    
    def 프로젝트_생성(self, 이름: str, 설명: str = "") -> Dict[str, Any]:
        """
        새 연구 프로젝트 생성
        
        사용 예:
            관리자 = 연구프로젝트관리자()
            관리자.프로젝트_생성("신약개발", "AI 기반 신약 후보 물질 발굴")
        """
        return self._manager.init_project(이름, 설명)
    
    def 진행사항_기록(self, 메시지: str, 파일들: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        프로젝트 진행사항 기록
        
        사용 예:
            관리자.진행사항_기록("데이터 전처리 완료", ["data/processed.csv"])
        """
        return self._manager.track_progress(메시지, 파일들)
    
    def 마일스톤_설정(self, 이름: str, 설명: str = "") -> Dict[str, Any]:
        """
        중요 마일스톤 설정
        
        사용 예:
            관리자.마일스톤_설정("1단계 완료", "데이터 수집 및 정제 완료")
        """
        return self._manager.set_milestone(이름, 설명)
    
    def 프로젝트_목록(self) -> List[Dict[str, Any]]:
        """
        모든 프로젝트 목록 조회
        
        사용 예:
            프로젝트들 = 관리자.프로젝트_목록()
            for 프로젝트 in 프로젝트들:
                print(프로젝트["name"])
        """
        return self._manager.list_projects()
    
    def 프로젝트_전환(self, 프로젝트_id: str) -> Dict[str, Any]:
        """
        다른 프로젝트로 전환
        
        사용 예:
            관리자.프로젝트_전환("2025-09-10_genomics")
        """
        return self._manager.switch_project(프로젝트_id)
    
    def 프로젝트_보관(self) -> Dict[str, Any]:
        """
        현재 프로젝트를 보관(아카이브)
        
        사용 예:
            관리자.프로젝트_보관()
        """
        return self._manager.archive_project()
    
    def 데이터_탐색(self, 설명: str = "") -> Dict[str, Any]:
        """
        탐색적 데이터 분석(EDA) 시작
        
        사용 예:
            관리자.데이터_탐색("유전자 발현 데이터 초기 분석")
        """
        return self._manager.explore_data(설명)
    
    def 가설_설정(self, 가설: str) -> Dict[str, Any]:
        """
        연구 가설 설정
        
        사용 예:
            관리자.가설_설정("BRCA1 유전자 발현이 약물 저항성과 연관됨")
        """
        return self._manager.set_hypothesis(가설)
    
    def 실험_시작(self, 실험명: str, 설명: str = "") -> Dict[str, Any]:
        """
        새로운 실험 시작
        
        사용 예:
            관리자.실험_시작("rf_모델", "랜덤포레스트 기준 모델")
        """
        return self._manager.start_experiment(실험명, 설명)
    
    def 결과_검증(self, 설명: str = "") -> Dict[str, Any]:
        """
        실험 결과 검증
        
        사용 예:
            관리자.결과_검증("교차 검증을 통한 모델 성능 평가")
        """
        return self._manager.validate_results(설명)
    
    def 체크포인트(self, 메모: str = "") -> Dict[str, Any]:
        """
        현재 상태를 체크포인트로 저장
        
        사용 예:
            체크포인트_id = 관리자.체크포인트("모델 학습 완료, 하이퍼파라미터 튜닝 예정")
        """
        return self._manager.checkpoint(메모)
    
    def 체크포인트_복원(self, 체크포인트_id: str) -> Dict[str, Any]:
        """
        이전 체크포인트로 복원
        
        사용 예:
            관리자.체크포인트_복원("20250910_123456")
        """
        return self._manager.resume_from_checkpoint(체크포인트_id)
    
    def 결과_공유(self) -> Dict[str, Any]:
        """
        프로젝트 결과를 공유 가능한 형태로 패키징
        
        사용 예:
            관리자.결과_공유()
        """
        return self._manager.share_results()
    
    def 도구_목록(self) -> Dict[str, Any]:
        """
        사용 가능한 분석 도구 목록 조회
        
        사용 예:
            도구들 = 관리자.도구_목록()
        """
        return self._manager.list_tools()
    
    def 현재_프로젝트(self) -> Optional[str]:
        """현재 활성 프로젝트 ID 반환"""
        return self._manager.metadata.get("active_project")
    
    def 프로젝트_정보(self, 프로젝트_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        특정 프로젝트의 상세 정보 조회
        
        Args:
            프로젝트_id: 조회할 프로젝트 ID (None이면 현재 프로젝트)
        
        Returns:
            프로젝트 정보 딕셔너리
        """
        if 프로젝트_id is None:
            프로젝트_id = self.현재_프로젝트()
        
        if 프로젝트_id and 프로젝트_id in self._manager.metadata["projects"]:
            return self._manager.metadata["projects"][프로젝트_id]
        return None


# 편의를 위한 별칭 클래스
class 연구관리자(연구프로젝트관리자):
    """더 짧은 이름의 별칭 클래스"""
    pass


# 함수형 인터페이스 (선택적)
def 새_프로젝트(이름: str, 설명: str = "") -> Dict[str, Any]:
    """빠른 프로젝트 생성을 위한 헬퍼 함수"""
    관리자 = 연구프로젝트관리자()
    return 관리자.프로젝트_생성(이름, 설명)


def 진행_기록(메시지: str, 파일들: Optional[List[str]] = None) -> Dict[str, Any]:
    """빠른 진행사항 기록을 위한 헬퍼 함수"""
    관리자 = 연구프로젝트관리자()
    return 관리자.진행사항_기록(메시지, 파일들)


if __name__ == "__main__":
    # 사용 예제
    print("🔬 연구프로젝트관리자 한글 인터페이스 예제")
    print("=" * 50)
    
    # 한글 메서드 사용
    관리자 = 연구프로젝트관리자()
    
    # 프로젝트 생성
    결과 = 관리자.프로젝트_생성("한글테스트", "한글 인터페이스 테스트")
    if "error" not in 결과:
        print(f"✅ 프로젝트 생성: {결과['project_id']}")
        
        # 진행사항 기록
        관리자.진행사항_기록("한글로 진행사항을 기록합니다")
        print("✅ 진행사항 기록 완료")
        
        # 마일스톤 설정
        관리자.마일스톤_설정("첫 마일스톤", "한글 인터페이스 테스트 완료")
        print("✅ 마일스톤 설정 완료")
        
        # 프로젝트 목록
        프로젝트들 = 관리자.프로젝트_목록()
        print(f"📋 전체 프로젝트: {len(프로젝트들)}개")
        
        print("\n✅ 한글 인터페이스 테스트 성공!")
    else:
        print("⚠️ 프로젝트가 이미 존재합니다")