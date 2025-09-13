"""
테스트: /탐구 유틸리티 - 투명한 수렴 과정 탐구 시스템
Migrated from simple_smiles_PCA project on 2025-09-13
TADD 방식: 실패하는 테스트 먼저 작성 (Red Phase)
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class TestExploreUtilities:
    """
    /탐구 커맨드의 핵심 기능 테스트
    - 투명한 수렴 과정
    - 모든 단계 기록
    - 재현 가능성
    """
    
    def test_exploration_records_all_attempts(self):
        """탐색 과정에서 시도한 모든 방법이 기록되는지 검증"""
        # Given: 샘플 데이터
        test_data = {
            "compounds": ["CCO", "CC(C)O", "c1ccccc1"],
            "type": "SMILES"
        }
        
        # When: 탐구 실행
        from scripts.explore_utilities import ExploreCommand
        explorer = ExploreCommand()
        result = explorer.explore(test_data)
        
        # Then: 모든 시도가 기록되어야 함
        assert "exploration_log" in result
        assert len(result["exploration_log"]) >= 3  # 최소 3개 모듈 실행
        
        # 각 시도에 필수 정보 포함
        for attempt in result["exploration_log"]:
            assert "module" in attempt
            assert "timestamp" in attempt
            assert "input" in attempt
            assert "output" in attempt
            assert "decision" in attempt
            assert "criteria" in attempt
    
    def test_convergence_criteria_transparent(self):
        """수렴 기준이 명시적으로 기록되는지 검증"""
        # Given: 테스트 데이터와 기준
        test_data = {"values": [1, 2, 3, 4, 5]}
        criteria = {
            "confidence_threshold": 0.85,
            "consensus_required": 2/3,
            "min_evidence": 3
        }
        
        # When: 수렴 과정 실행
        from scripts.explore_utilities import ConvergenceEngine
        engine = ConvergenceEngine(criteria)
        result = engine.converge(test_data)
        
        # Then: 모든 기준이 투명하게 기록
        assert "convergence_process" in result
        assert "criteria_applied" in result["convergence_process"]
        assert result["convergence_process"]["criteria_applied"] == criteria
        
        # 각 반복에서 신뢰도 진행 상황 기록
        assert "iterations" in result["convergence_process"]
        for iteration in result["convergence_process"]["iterations"]:
            assert "confidence" in iteration
            assert 0 <= iteration["confidence"] <= 1
            assert "evidence" in iteration
            assert "decision" in iteration
    
    def test_full_reproducibility(self):
        """동일한 입력으로 100% 재현 가능한지 검증"""
        # Given: 고정된 시드와 데이터
        test_data = {
            "data": [1, 2, 3],
            "seed": 42,
            "parameters": {"method": "pca", "n_components": 2}
        }
        
        # When: 두 번 실행
        from scripts.explore_utilities import ExploreCommand
        explorer1 = ExploreCommand()
        result1 = explorer1.explore(test_data)
        
        explorer2 = ExploreCommand()
        result2 = explorer2.explore(test_data)
        
        # Then: 결과가 완전히 동일해야 함 (타임스탬프와 start_time 제외)
        # 타임스탬프와 시간 관련 필드 제거 후 비교
        def remove_timestamps(obj):
            if isinstance(obj, dict):
                return {k: remove_timestamps(v) for k, v in obj.items() 
                       if k not in ["timestamp", "start_time"]}
            elif isinstance(obj, list):
                return [remove_timestamps(item) for item in obj]
            return obj
        
        assert remove_timestamps(result1) == remove_timestamps(result2)
        
        # 재현 스크립트 생성 확인
        assert "reproducibility" in result1
        assert "script" in result1["reproducibility"]
        assert "parameters" in result1["reproducibility"]
    
    def test_confidence_progression_tracking(self):
        """신뢰도가 점진적으로 증가하는 과정이 추적되는지 검증"""
        # Given: 여러 증거 소스
        evidence_sources = [
            {"method": "pca", "result": "5 clusters"},
            {"method": "umap", "result": "5 regions"},
            {"method": "tsne", "result": "5 islands"}
        ]
        
        # When: 증거 누적
        from scripts.explore_utilities import ConfidenceTracker
        tracker = ConfidenceTracker()
        
        progression = []
        for evidence in evidence_sources:
            confidence = tracker.add_evidence(evidence)
            progression.append(confidence)
        
        # Then: 신뢰도가 단조 증가
        assert all(progression[i] <= progression[i+1] 
                  for i in range(len(progression)-1))
        assert progression[0] > 0  # 초기 신뢰도
        assert progression[-1] <= 1  # 최대 신뢰도
        
        # 전체 진행 과정 기록
        history = tracker.get_progression_history()
        assert len(history) == len(evidence_sources)
        for i, step in enumerate(history):
            assert step["stage"] == evidence_sources[i]["method"]
            assert step["confidence"] == progression[i]
            assert "cumulative_evidence" in step
    
    def test_decision_tree_transparency(self):
        """의사결정 트리가 투명하게 기록되는지 검증"""
        # Given: 복잡한 의사결정 시나리오
        scenario = {
            "data_quality": 0.95,
            "pattern_strength": 0.7,
            "consensus_level": 0.8
        }
        
        # When: 의사결정 수행
        from scripts.explore_utilities import DecisionEngine
        engine = DecisionEngine()
        decision = engine.make_decision(scenario)
        
        # Then: 의사결정 경로 완전 기록
        assert "decision_path" in decision
        assert len(decision["decision_path"]) > 0
        
        # 각 결정 노드에 이유 포함
        for node in decision["decision_path"]:
            assert "condition" in node
            assert "evaluated_value" in node
            assert "threshold" in node
            assert "passed" in node
            assert "reasoning" in node
        
        # 최종 결론에 전체 근거 포함
        assert "final_decision" in decision
        assert "confidence" in decision["final_decision"]
        assert "supporting_evidence" in decision["final_decision"]
        assert len(decision["final_decision"]["supporting_evidence"]) >= 3
    
    def test_report_generation_with_transparency(self):
        """투명성 중심 보고서가 생성되는지 검증"""
        # Given: 완료된 탐구 세션
        exploration_data = {
            "project": "SMILES Analysis",
            "timestamp": datetime.now().isoformat(),
            "data_points": 100
        }
        
        # When: 보고서 생성
        from scripts.explore_utilities import ReportGenerator
        generator = ReportGenerator()
        report = generator.generate(exploration_data)
        
        # Then: 과정 중심 보고서 구조
        assert "exploration_path" in report
        assert "convergence_journey" in report
        assert "final_results" in report
        assert "transparency_metadata" in report
        
        # 투명성 메타데이터 검증
        metadata = report["transparency_metadata"]
        assert "all_parameters" in metadata
        assert "algorithms_used" in metadata
        assert "decision_criteria" in metadata
        assert "reproduction_script" in metadata
        
        # 보고서 파일 생성 확인
        assert "output_path" in report
        assert Path(report["output_path"]).suffix == ".md"


class TestExploreCommandIntegration:
    """통합 테스트: 전체 워크플로우"""
    
    def test_complete_exploration_workflow(self):
        """전체 탐구 워크플로우가 작동하는지 검증"""
        # Given: 실제와 유사한 데이터
        real_world_data = {
            "dataset": "compounds.csv",
            "type": "SMILES",
            "size": 1000,
            "objective": "Find chemical patterns"
        }
        
        # When: 전체 탐구 프로세스 실행
        from scripts.explore_utilities import explore_main
        result = explore_main(real_world_data)
        
        # Then: 완전한 결과 생성
        assert result["status"] == "completed"
        assert result["patterns_found"] > 0
        assert result["confidence"] >= 0.85
        
        # 투명성 보장
        assert "full_exploration_log" in result
        assert "convergence_history" in result
        assert "decision_tree" in result
        assert "reproducibility_info" in result
        
        # 보고서 생성 확인
        assert "report_path" in result
        assert Path(result["report_path"]).exists()
        
        # 재현 스크립트 실행 가능
        assert "reproduction_command" in result
        assert result["reproduction_command"].startswith("/탐구")