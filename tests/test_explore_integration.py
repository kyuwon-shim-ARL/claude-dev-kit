#!/usr/bin/env python3
"""
Integration Test: /탐구 Command with claude-dev-kit
Tests the integration of explore utilities with existing systems
Created: 2025-09-13
"""
import unittest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from explore_utilities import (
    ExploreCommand, ConvergenceEngine, ConfidenceTracker, 
    DecisionEngine, ReportGenerator, explore_main, quick_explore
)


class TestExploreIntegration(unittest.TestCase):
    """claude-dev-kit 통합 테스트"""
    
    def setUp(self):
        self.test_data = {
            "dataset": "test_compounds.csv",
            "compounds": ["CCO", "CC(C)O", "c1ccccc1"],
            "type": "SMILES",
            "seed": 42
        }
        
    def test_explore_main_integration(self):
        """전체 탐구 워크플로우 통합 테스트"""
        result = explore_main(self.test_data)
        
        # 기본 결과 구조 확인
        self.assertIn("status", result)
        self.assertEqual(result["status"], "completed")
        self.assertIn("patterns_found", result)
        self.assertIn("confidence", result)
        self.assertIn("report_path", result)
        
        # 투명성 요소 확인
        self.assertIn("full_exploration_log", result)
        self.assertIn("convergence_history", result)
        self.assertIn("decision_tree", result)
        self.assertIn("reproducibility_info", result)
        
    def test_quick_explore_convenience(self):
        """빠른 탐구 편의 함수 테스트"""
        result = quick_explore("test_dataset.csv", "test_project")
        
        self.assertIn("status", result)
        self.assertEqual(result["status"], "completed")
        
    def test_report_generation_claude_dev_kit_structure(self):
        """claude-dev-kit 구조에서 보고서 생성 테스트"""
        generator = ReportGenerator(".")
        
        # 보고서 디렉토리가 올바르게 생성되는지 확인
        self.assertTrue(generator.report_dir.exists())
        self.assertEqual(generator.report_dir.name, "exploration")
        
    def test_transparency_scoring(self):
        """투명성 점수 계산 테스트"""
        result = explore_main(self.test_data)
        
        # 투명성 점수가 높은지 확인
        self.assertIn("transparency_score", result)
        self.assertGreater(result["transparency_score"], 0.8)
        
    def test_reproducibility_integration(self):
        """재현성 시스템 통합 테스트"""
        result1 = explore_main(self.test_data)
        result2 = explore_main(self.test_data)
        
        # 동일한 시드로 재현 가능한지 확인
        self.assertEqual(
            result1["reproducibility_info"]["data_hash"],
            result2["reproducibility_info"]["data_hash"]
        )


if __name__ == "__main__":
    unittest.main()
