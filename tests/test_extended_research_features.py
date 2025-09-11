#!/usr/bin/env python3
"""
Extended Research Features Tests
새로 추가된 연구 서브커맨드들에 대한 테스트
"""
import pytest
import sys
import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_project_manager import ResearchProjectManager


class TestExtendedResearchCommands:
    """확장 연구 커맨드 테스트"""
    
    def setup_method(self):
        """테스트 환경 설정"""
        import tempfile
        self.temp_root = Path(tempfile.mkdtemp())
        self.test_dir = self.temp_root / "test_extended_research"
        
        self.manager = ResearchProjectManager(base_dir=str(self.test_dir))
        self.manager.init_project("test_extended", "Extended features test")
    
    def teardown_method(self):
        """테스트 정리"""
        if hasattr(self, 'temp_root') and self.temp_root.exists():
            shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def test_explore_data_creates_eda_notebook(self):
        """데이터 탐색이 EDA 노트북을 생성하는가?"""
        # When: 데이터 탐색 실행
        result = self.manager.explore_data("Initial data exploration")
        
        # Then: 성공 및 노트북 생성 확인
        assert result["success"] is True
        assert "EDA notebook created" in result["message"]
        
        notebook_path = Path(result["notebook_path"])
        assert notebook_path.exists()
        
        # 노트북 내용 확인
        with open(notebook_path, 'r') as f:
            notebook_content = json.load(f)
        
        assert "cells" in notebook_content
        assert len(notebook_content["cells"]) >= 2
        assert "Initial data exploration" in notebook_content["cells"][0]["source"]
    
    def test_set_hypothesis_records_properly(self):
        """가설 설정이 올바르게 기록되는가?"""
        # When: 가설 설정
        hypothesis_text = "분자량이 클수록 독성이 높다"
        result = self.manager.set_hypothesis(hypothesis_text)
        
        # Then: 성공 확인
        assert result["success"] is True
        assert hypothesis_text in result["message"]
        
        # 메타데이터 확인
        project_id = self.manager.metadata["active_project"]
        hypotheses = self.manager.metadata["projects"][project_id]["hypotheses"]
        
        assert len(hypotheses) == 1
        assert hypotheses[0]["hypothesis"] == hypothesis_text
        assert hypotheses[0]["status"] == "active"
    
    def test_start_experiment_creates_structure(self):
        """실험 시작이 올바른 구조를 생성하는가?"""
        # When: 실험 시작
        result = self.manager.start_experiment("baseline_model", "Random forest baseline")
        
        # Then: 성공 확인
        assert result["success"] is True
        assert "baseline_model" in result["message"]
        assert "experiment_id" in result
        
        # 실험 디렉토리 확인
        project_id = self.manager.metadata["active_project"]
        project_dir = self.test_dir / project_id
        experiments_dir = project_dir / "experiments"
        
        assert experiments_dir.exists()
        
        # 실험 노트북 확인
        notebook_path = Path(result["notebook_path"])
        assert notebook_path.exists()
        
        with open(notebook_path, 'r') as f:
            notebook_content = json.load(f)
        
        assert "baseline_model" in notebook_content["cells"][0]["source"]
    
    def test_validate_results_creates_script(self):
        """결과 검증이 검증 스크립트를 생성하는가?"""
        # When: 결과 검증
        result = self.manager.validate_results("Model performance validation")
        
        # Then: 성공 확인
        assert result["success"] is True
        assert "validation script" in result["message"].lower()
        
        script_path = Path(result["script_path"])
        assert script_path.exists()
        
        # 스크립트 내용 확인
        content = script_path.read_text()
        assert "validate_model_performance" in content
        assert "validate_statistical_significance" in content
        assert "validate_reproducibility" in content
        
        # 실행 권한 확인
        assert os.access(script_path, os.X_OK)
    
    def test_analyze_results_creates_report(self):
        """결과 분석이 분석 보고서를 생성하는가?"""
        # When: 결과 분석
        result = self.manager.analyze_results("Comprehensive analysis")
        
        # Then: 성공 확인
        assert result["success"] is True
        assert "analysis report" in result["message"].lower()
        
        report_path = Path(result["report_path"])
        assert report_path.exists()
        
        # 보고서 내용 확인
        content = report_path.read_text()
        assert "# Analysis Report" in content
        assert "Comprehensive analysis" in content
        assert "## Summary" in content
        assert "## Results" in content
        assert "## Conclusions" in content
    
    def test_compare_experiments_creates_notebook(self):
        """실험 비교가 비교 노트북을 생성하는가?"""
        # When: 실험 비교
        result = self.manager.compare_experiments("exp1", "exp2")
        
        # Then: 성공 확인
        assert result["success"] is True
        assert "comparison notebook" in result["message"].lower()
        
        notebook_path = Path(result["notebook_path"])
        assert notebook_path.exists()
        
        # 노트북 내용 확인
        with open(notebook_path, 'r') as f:
            notebook_content = json.load(f)
        
        comparison_text = notebook_content["cells"][0]["source"]
        assert "exp1 vs exp2" in comparison_text
    
    def test_checkpoint_resume_workflow(self):
        """체크포인트 생성 및 재개 워크플로우가 작동하는가?"""
        # When: 체크포인트 생성
        checkpoint_result = self.manager.checkpoint("Need new analysis tool")
        
        # Then: 체크포인트 생성 성공
        assert checkpoint_result["success"] is True
        assert "checkpoint_id" in checkpoint_result
        
        checkpoint_id = checkpoint_result["checkpoint_id"]
        
        # When: 체크포인트에서 재개
        resume_result = self.manager.resume_from_checkpoint(checkpoint_id)
        
        # Then: 재개 성공
        assert resume_result["success"] is True
        assert resume_result["checkpoint_id"] == checkpoint_id
    
    def test_share_results_creates_package(self):
        """결과 공유가 공유 패키지를 생성하는가?"""
        # When: 결과 공유 준비
        result = self.manager.share_results()
        
        # Then: 성공 확인
        assert result["success"] is True
        assert "share package" in result["message"].lower()
        
        share_path = Path(result["share_path"])
        assert share_path.exists()
        
        # 공유 패키지 내용 확인
        readme_file = share_path / "README.md"
        requirements_file = share_path / "requirements.txt"
        
        assert readme_file.exists()
        assert requirements_file.exists()
        
        readme_content = readme_file.read_text()
        assert "# test_extended" in readme_content


class TestDirectoryBasedDetection:
    """디렉토리 기반 프로젝트 감지 테스트"""
    
    def setup_method(self):
        """테스트 환경 설정"""
        import tempfile
        self.temp_root = Path(tempfile.mkdtemp())
        self.test_dir = self.temp_root / "test_directory_detection"
        
        self.manager = ResearchProjectManager(base_dir=str(self.test_dir))
        
        # 여러 프로젝트 생성
        self.manager.init_project("project_a", "Project A")
        self.manager.init_project("project_b", "Project B")
    
    def teardown_method(self):
        """테스트 정리"""
        if hasattr(self, 'temp_root') and self.temp_root.exists():
            shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def test_detects_project_from_directory_path(self):
        """디렉토리 경로에서 프로젝트를 감지하는가?"""
        # Given: 디렉토리 기반 감지 테스트를 위해 실제 디렉토리 구조 생성
        original_cwd = os.getcwd()
        
        # project_a ID 찾기
        project_a_id = None
        for proj_id in self.manager.metadata["projects"]:
            if "project_a" in proj_id:
                project_a_id = proj_id
                break
        
        assert project_a_id is not None and "project_a" in project_a_id, f"project_a not found in metadata. Available: {list(self.manager.metadata['projects'].keys())}"
        
        try:
            # 실제 디렉토리 구조 생성
            notebooks_dir = self.test_dir / "research_projects" / project_a_id / "notebooks"
            notebooks_dir.mkdir(parents=True, exist_ok=True)
            
            # 메타데이터 파일 복사
            import shutil
            metadata_source = self.test_dir / "research_projects" / ".research_metadata.json"
            metadata_target = self.test_dir / "research_projects" / ".research_metadata.json"
            
            # 현재 메타데이터를 임시 위치에 저장
            with open(metadata_target, 'w') as f:
                json.dump(self.manager.metadata, f, indent=2)
            
            # 해당 디렉토리로 이동하여 테스트
            os.chdir(str(notebooks_dir))
            
            # 새로운 manager로 테스트 (현재 디렉토리에서 감지)
            test_manager = ResearchProjectManager()
            detected_project = test_manager.detect_current_project()
            
            # Then: project_a 감지
            assert detected_project == project_a_id
            
        finally:
            os.chdir(original_cwd)  # 원래 디렉토리로 복원
    
    def test_auto_switch_project_functionality(self):
        """자동 프로젝트 전환 기능이 작동하는가?"""
        # Given: 특정 프로젝트가 활성 상태
        project_b_id = None
        for proj_id in self.manager.metadata["projects"]:
            if "project_b" in proj_id:
                project_b_id = proj_id
                break
        
        self.manager.switch_project(project_b_id)
        
        # When: 자동 전환 시도 (이미 활성인 경우)
        result = self.manager.auto_switch_project()
        
        # Then: 변경 없음 확인
        assert result["success"] is True
        assert result.get("no_change") is True
        assert self.manager.metadata["active_project"] == project_b_id
    
    def test_handles_multiple_projects_scenario(self):
        """여러 프로젝트 시나리오를 올바르게 처리하는가?"""
        # Given: 활성 프로젝트 제거 (애매한 상황)
        self.manager.metadata["active_project"] = None
        self.manager.save_metadata()
        
        # When: 자동 전환 시도
        result = self.manager.auto_switch_project()
        
        # Then: 선택 옵션 제공
        if "error" in result and "Multiple projects" in result["error"]:
            assert "projects" in result
            assert len(result["projects"]) == 2
        else:
            # 또는 자동으로 하나 선택됨
            assert result["success"] is True
    
    def test_recent_activity_detection(self):
        """최근 활동 기반 프로젝트 감지가 작동하는가?"""
        # Given: 프로젝트 A에서 최근 체크포인트 생성
        project_a_id = None
        for proj_id in self.manager.metadata["projects"]:
            if "project_a" in proj_id:
                project_a_id = proj_id
                break
        
        self.manager.switch_project(project_a_id)
        self.manager.checkpoint("Recent activity test")
        
        # 활성 프로젝트 제거
        self.manager.metadata["active_project"] = None
        
        # When: 최근 활동 감지
        recent_project = self.manager._get_recent_activity_project(minutes=5)
        
        # Then: 최근 활동한 프로젝트 감지
        assert recent_project == project_a_id


class TestToolIntegration:
    """도구 통합 테스트"""
    
    def setup_method(self):
        """테스트 환경 설정"""
        import tempfile
        self.temp_root = Path(tempfile.mkdtemp())
        self.test_dir = self.temp_root / "test_tool_integration"
        
        self.manager = ResearchProjectManager(base_dir=str(self.test_dir))
        self.manager.init_project("tool_test", "Tool integration test")
    
    def teardown_method(self):
        """테스트 정리"""
        if hasattr(self, 'temp_root') and self.temp_root.exists():
            shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def test_list_tools_handles_missing_inventory(self):
        """도구 인벤토리가 있을 때와 없을 때를 모두 처리하는가?"""
        # When: 도구 목록 조회
        result = self.manager.list_tools()
        
        # Then: 성공하거나 적절한 오류 처리
        if result.get("success"):
            # 도구 인벤토리가 있는 경우
            assert "tools" in result
            assert "count" in result
            assert "categories" in result
        else:
            # 도구 인벤토리가 없는 경우
            assert "error" in result
            assert "Tool inventory not available" in result["error"]
            assert "message" in result
    
    def test_tool_categorization_logic(self):
        """도구 분류 로직이 올바르게 작동하는가?"""
        # Given: 가상 도구 데이터
        mock_tools = {
            "analyze_molecules": {"file": "src/chemistry/analyzer.py"},
            "plot_data": {"file": "src/visualization/plotter.py"},
            "load_csv": {"file": "src/io/csv_loader.py"}
        }
        
        # When: 도구 분류
        categories = self.manager._categorize_tools(mock_tools)
        
        # Then: 올바른 분류
        assert "chemistry" in categories
        assert "visualization" in categories  
        assert "io" in categories
        
        assert "analyze_molecules" in categories["chemistry"]
        assert "plot_data" in categories["visualization"]
        assert "load_csv" in categories["io"]


if __name__ == "__main__":
    # 확장 기능 테스트 실행
    print("🧪 Extended Research Features 테스트 시작")
    pytest.main([__file__, "-v", "--tb=short"])