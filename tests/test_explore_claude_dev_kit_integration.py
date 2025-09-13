#!/usr/bin/env python3
"""
Comprehensive Integration Test: /탐구 Command in claude-dev-kit Environment
Tests the full integration with claude-dev-kit project structure and workflows
"""
import unittest
import sys
import tempfile
import shutil
import os
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from explore_utilities import (
    ExploreCommand, ConvergenceEngine, ConfidenceTracker, 
    DecisionEngine, ReportGenerator, explore_main, quick_explore
)


class TestClaudeDevKitIntegration(unittest.TestCase):
    """claude-dev-kit 환경에서의 완전한 통합 테스트"""
    
    def setUp(self):
        """테스트 환경 설정"""
        self.test_dir = Path(__file__).parent.parent
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        self.test_data = {
            "dataset": "claude_dev_kit_test.csv",
            "compounds": ["CCO", "CC(C)O", "c1ccccc1", "CC(=O)O"],
            "type": "SMILES",
            "seed": 42,
            "project": "claude-dev-kit-integration-test"
        }
        
    def tearDown(self):
        """테스트 후 정리"""
        os.chdir(self.original_cwd)
        
    def test_reports_directory_structure(self):
        """claude-dev-kit 보고서 디렉토리 구조 확인"""
        reports_dir = self.test_dir / "reports" / "exploration"
        self.assertTrue(reports_dir.exists(), "Exploration reports directory should exist")
        
        # 보고서 생성 테스트
        generator = ReportGenerator(str(self.test_dir))
        self.assertEqual(generator.report_dir, reports_dir)
        
    def test_scripts_directory_integration(self):
        """scripts 디렉토리 통합 확인"""
        scripts_dir = self.test_dir / "scripts"
        explore_utilities = scripts_dir / "explore_utilities.py"
        
        self.assertTrue(scripts_dir.exists())
        self.assertTrue(explore_utilities.exists())
        
    def test_full_workflow_integration(self):
        """전체 워크플로우 통합 테스트"""
        # 1. 탐구 실행
        result = explore_main(self.test_data)
        
        # 2. 기본 구조 확인
        self.assertIn("status", result)
        self.assertEqual(result["status"], "completed")
        self.assertIn("patterns_found", result)
        self.assertIn("confidence", result)
        self.assertIn("report_path", result)
        
        # 3. claude-dev-kit 구조에서 보고서 생성 확인
        report_path = Path(result["report_path"])
        if not report_path.is_absolute():
            report_path = self.test_dir / report_path
        self.assertTrue(report_path.exists())
        self.assertIn("reports/exploration", str(result["report_path"]))
        
        # 4. 보고서 내용 확인
        report_content = report_path.read_text()
        self.assertIn("투명한 탐구 보고서", report_content)
        self.assertIn("탐색 경로", report_content)
        self.assertIn("수렴 과정", report_content)
        self.assertIn("투명성 메타데이터", report_content)
        
    def test_quick_explore_convenience_function(self):
        """빠른 탐구 편의 함수 테스트"""
        result = quick_explore("test_dataset.csv", "quick_test_project")
        
        self.assertEqual(result["status"], "completed")
        self.assertGreater(result["patterns_found"], 0)
        self.assertGreater(result["confidence"], 0.8)
        
        # 보고서 경로가 올바른 구조인지 확인
        report_path = Path(result["report_path"])
        self.assertTrue("reports/exploration" in str(report_path))
        
    def test_transparency_and_reproducibility(self):
        """투명성 및 재현성 테스트"""
        # 같은 데이터로 두 번 실행
        result1 = explore_main(self.test_data)
        result2 = explore_main(self.test_data)
        
        # 재현성 확인 (데이터 해시가 동일해야 함)
        self.assertEqual(
            result1["reproducibility_info"]["data_hash"],
            result2["reproducibility_info"]["data_hash"]
        )
        
        # 투명성 점수 확인
        self.assertIn("transparency_score", result1)
        self.assertGreater(result1["transparency_score"], 0.9)
        
    def test_slash_command_integration_readiness(self):
        """슬래시 명령어 통합 준비도 확인"""
        slash_command_file = self.test_dir / ".claude" / "commands" / "탐구.md"
        self.assertTrue(slash_command_file.exists(), "/탐구 slash command should exist")
        
        # 슬래시 명령어 내용 확인
        content = slash_command_file.read_text()
        self.assertIn("explore_utilities", content)
        self.assertIn("scripts", content)
        self.assertIn("투명한 수렴", content)
        
    def test_research_command_integration(self):
        """연구 명령어와의 통합 확인"""
        research_command_file = self.test_dir / ".claude" / "commands" / "연구.md"
        self.assertTrue(research_command_file.exists())
        
        # 연구 명령어에 탐구가 통합되었는지 확인
        content = research_command_file.read_text()
        self.assertIn("explore", content)
        self.assertIn("탐구", content)
        self.assertIn("투명한 수렴", content)
        
    def test_archive_and_migration_records(self):
        """마이그레이션 기록 및 아카이브 확인"""
        # 마이그레이션 보고서 존재 확인
        reports_dir = self.test_dir / "reports"
        migration_reports = list(reports_dir.glob("migration_report_*.md"))
        self.assertGreater(len(migration_reports), 0, "Migration report should exist")
        
        # 아카이브 디렉토리 확인
        archive_dir = self.test_dir / "archive" / "migration"
        if archive_dir.exists():
            explore_archives = list(archive_dir.glob("explore_command_*"))
            self.assertGreater(len(explore_archives), 0, "Explore command archive should exist")
            
    def test_test_files_integration(self):
        """테스트 파일 통합 확인"""
        tests_dir = self.test_dir / "tests"
        
        # 기본 테스트 파일
        test_explore_utilities = tests_dir / "test_explore_utilities.py"
        self.assertTrue(test_explore_utilities.exists())
        
        # 통합 테스트 파일
        test_explore_integration = tests_dir / "test_explore_integration.py"
        self.assertTrue(test_explore_integration.exists())
        
        # 현재 파일
        test_claude_dev_kit = tests_dir / "test_explore_claude_dev_kit_integration.py"
        self.assertTrue(test_claude_dev_kit.exists())
        
    def test_documentation_completeness(self):
        """문서화 완성도 확인"""
        docs_dir = self.test_dir / "docs"
        
        # 사용자 가이드
        user_guide = docs_dir / "commands" / "explore-utilities-guide.md"
        if user_guide.exists():
            content = user_guide.read_text()
            self.assertIn("claude-dev-kit", content.lower())
            
        # PRD 문서
        prd_doc = docs_dir / "specs" / "PRD-explore-utilities-v1.0.md"
        if prd_doc.exists():
            content = prd_doc.read_text()
            self.assertIn("마이그레이션", content)
            
    def test_python_path_compatibility(self):
        """Python 경로 호환성 테스트"""
        # scripts 디렉토리에서 직접 import 테스트
        original_path = sys.path[:]
        try:
            sys.path.insert(0, str(self.test_dir / "scripts"))
            
            # 동적 import 테스트
            import explore_utilities
            self.assertTrue(hasattr(explore_utilities, 'explore_main'))
            self.assertTrue(hasattr(explore_utilities, 'quick_explore'))
            
        finally:
            sys.path[:] = original_path
            
    def test_performance_and_scalability(self):
        """성능 및 확장성 테스트"""
        import time
        
        # 큰 데이터셋 시뮬레이션
        large_dataset = {
            "dataset": "large_compounds.csv",
            "compounds": [f"C{i}CO" for i in range(100)],  # 100개 화합물
            "type": "SMILES",
            "seed": 42,
            "project": "performance_test"
        }
        
        start_time = time.time()
        result = explore_main(large_dataset)
        end_time = time.time()
        
        # 성능 확인 (5초 이내 완료)
        self.assertLess(end_time - start_time, 5.0, "Should complete within 5 seconds")
        self.assertEqual(result["status"], "completed")
        
    def test_error_handling_and_recovery(self):
        """오류 처리 및 복구 테스트"""
        # 잘못된 데이터 형식
        invalid_data = {
            "dataset": None,
            "compounds": [],
            "type": "INVALID",
        }
        
        # 오류가 발생해도 시스템이 중단되지 않아야 함
        try:
            result = explore_main(invalid_data)
            # 결과가 반환되면 상태 확인
            if "status" in result:
                self.assertIn(result["status"], ["completed", "error", "partial"])
        except Exception as e:
            # 예외가 발생해도 시스템이 복구 가능해야 함
            self.assertIsInstance(e, (ValueError, TypeError, KeyError))


if __name__ == "__main__":
    print("🧪 claude-dev-kit /탐구 명령어 통합 테스트 시작...")
    unittest.main(verbosity=2)