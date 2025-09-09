#!/usr/bin/env python3
"""
Research Project Manager Tests
TADD 방식으로 실제 기능 검증
"""
import pytest
import sys
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_project_manager import ResearchProjectManager, ResearchTimeline


class TestResearchProjectInitialization:
    """연구 프로젝트 초기화 테스트"""
    
    def setup_method(self):
        """각 테스트 전 실행"""
        import tempfile
        self.temp_root = Path(tempfile.mkdtemp())
        self.test_dir = self.temp_root / "test_research_projects"
    
    def teardown_method(self):
        """각 테스트 후 정리"""
        if hasattr(self, 'temp_root') and self.temp_root.exists():
            shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def test_creates_project_structure(self):
        """프로젝트 구조가 올바르게 생성되는가?"""
        # Given: Research Project Manager
        manager = ResearchProjectManager(base_dir=str(self.test_dir))
        
        # When: 새 프로젝트 초기화
        result = manager.init_project(
            "test_project",
            "Test research project for validation"
        )
        
        # Then: 성공 및 구조 확인
        assert result["success"] is True
        assert "test_project" in result["project_id"]
        
        project_dir = Path(result["path"])
        assert project_dir.exists()
        
        # 모든 필수 디렉토리 확인
        required_dirs = ["notebooks", "data", "results", "figures", "docs", "scripts"]
        for dir_name in required_dirs:
            dir_path = project_dir / dir_name
            assert dir_path.exists()
            assert (dir_path / "README.md").exists()
    
    def test_creates_timeline_file(self):
        """타임라인 파일이 생성되고 초기화되는가?"""
        # Given: Research Project Manager
        manager = ResearchProjectManager(base_dir=str(self.test_dir))
        
        # When: 프로젝트 생성
        result = manager.init_project("timeline_test", "Testing timeline")
        
        # Then: 타임라인 파일 확인
        project_dir = Path(result["path"])
        timeline_file = project_dir / "timeline.md"
        
        assert timeline_file.exists()
        content = timeline_file.read_text()
        assert "Research Timeline" in content
        assert "timeline_test" in content
        assert "Testing timeline" in content
    
    def test_saves_environment_info(self):
        """환경 정보가 저장되는가?"""
        # Given: Research Project Manager
        manager = ResearchProjectManager(base_dir=str(self.test_dir))
        
        # When: 프로젝트 생성
        result = manager.init_project("env_test", "Environment test")
        
        # Then: 환경 정보 파일 확인
        project_dir = Path(result["path"])
        env_file = project_dir / "environment.json"
        
        assert env_file.exists()
        env_data = json.loads(env_file.read_text())
        assert "python_version" in env_data
        assert "packages" in env_data


class TestProgressTracking:
    """진행사항 추적 테스트"""
    
    def setup_method(self):
        """테스트 환경 설정"""
        import tempfile
        self.temp_root = Path(tempfile.mkdtemp())
        self.test_dir = self.temp_root / "test_research_projects"
        
        self.manager = ResearchProjectManager(base_dir=str(self.test_dir))
        self.manager.init_project("tracking_test", "Progress tracking test")
    
    def teardown_method(self):
        """테스트 후 정리"""
        if hasattr(self, 'temp_root') and self.temp_root.exists():
            shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def test_tracks_progress_notes(self):
        """진행사항이 타임라인에 기록되는가?"""
        # When: 진행사항 추적
        result = self.manager.track_progress("Loaded dataset with 1000 samples")
        
        # Then: 성공 확인
        assert result["success"] is True
        assert "timestamp" in result
        
        # 타임라인 파일 확인
        project_id = self.manager.metadata["active_project"]
        timeline_file = self.test_dir / project_id / "timeline.md"
        content = timeline_file.read_text()
        
        assert "Loaded dataset with 1000 samples" in content
        assert result["timestamp"] in content
    
    def test_tracks_related_files(self):
        """관련 파일이 함께 기록되는가?"""
        # When: 파일과 함께 진행사항 추적
        files = ["notebooks/01_analysis.ipynb", "data/processed.csv"]
        result = self.manager.track_progress("Completed initial analysis", files)
        
        # Then: 파일 정보 확인
        project_id = self.manager.metadata["active_project"]
        timeline_file = self.test_dir / project_id / "timeline.md"
        content = timeline_file.read_text()
        
        assert "notebooks/01_analysis.ipynb" in content
        assert "data/processed.csv" in content


class TestMilestoneManagement:
    """마일스톤 관리 테스트"""
    
    def setup_method(self):
        """테스트 환경 설정"""
        import tempfile
        self.temp_root = Path(tempfile.mkdtemp())
        self.test_dir = self.temp_root / "test_research_projects"
        
        self.manager = ResearchProjectManager(base_dir=str(self.test_dir))
        self.manager.init_project("milestone_test", "Milestone management test")
    
    def teardown_method(self):
        """테스트 후 정리"""
        if hasattr(self, 'temp_root') and self.temp_root.exists():
            shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def test_sets_milestone_successfully(self):
        """마일스톤이 설정되고 기록되는가?"""
        # When: 마일스톤 설정
        result = self.manager.set_milestone(
            "Data Preparation Complete",
            "All data cleaned and features extracted"
        )
        
        # Then: 성공 확인
        assert result["success"] is True
        
        # 메타데이터 확인
        project_id = self.manager.metadata["active_project"]
        milestones = self.manager.metadata["projects"][project_id]["milestones"]
        assert len(milestones) == 1
        assert milestones[0]["name"] == "Data Preparation Complete"
        
        # 타임라인 확인
        timeline_file = self.test_dir / project_id / "timeline.md"
        content = timeline_file.read_text()
        assert "🎯 MILESTONE" in content
        assert "Data Preparation Complete" in content


class TestProjectManagement:
    """프로젝트 관리 기능 테스트"""
    
    def setup_method(self):
        """테스트 환경 설정"""
        import tempfile
        self.temp_root = Path(tempfile.mkdtemp())
        self.test_dir = self.temp_root / "test_research_projects"
        
        self.manager = ResearchProjectManager(base_dir=str(self.test_dir))
    
    def teardown_method(self):
        """테스트 후 정리"""
        if hasattr(self, 'temp_root') and self.temp_root.exists():
            shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def test_lists_all_projects(self):
        """모든 프로젝트가 올바르게 나열되는가?"""
        # Given: 여러 프로젝트 생성
        self.manager.init_project("project1", "First project")
        self.manager.init_project("project2", "Second project")
        
        # When: 프로젝트 목록 조회
        projects = self.manager.list_projects()
        
        # Then: 두 프로젝트 모두 존재
        assert len(projects) == 2
        names = [p["name"] for p in projects]
        assert "project1" in names
        assert "project2" in names
    
    def test_switches_between_projects(self):
        """프로젝트 간 전환이 작동하는가?"""
        # Given: 두 프로젝트
        result1 = self.manager.init_project("project1", "First")
        project1_id = result1["project_id"]
        result2 = self.manager.init_project("project2", "Second")
        project2_id = result2["project_id"]
        
        # When: 첫 번째 프로젝트로 전환
        switch_result = self.manager.switch_project(project1_id)
        
        # Then: 전환 성공
        assert switch_result["success"] is True
        assert self.manager.metadata["active_project"] == project1_id
    
    def test_archives_project(self):
        """프로젝트 아카이빙이 작동하는가?"""
        # Given: 활성 프로젝트
        result = self.manager.init_project("archive_test", "To be archived")
        project_id = result["project_id"]
        
        # When: 아카이빙
        archive_result = self.manager.archive_project()
        
        # Then: 성공 및 상태 확인
        assert archive_result["success"] is True
        assert self.manager.metadata["active_project"] is None
        assert self.manager.metadata["projects"][project_id]["status"] == "archived"
        
        # 최종 보고서 생성 확인
        final_report = self.test_dir / project_id / "FINAL_REPORT.md"
        assert final_report.exists()


class TestTimelineSystem:
    """타임라인 시스템 테스트"""
    
    def setup_method(self):
        """테스트 환경 설정"""
        import tempfile
        self.temp_root = Path(tempfile.mkdtemp())
        self.test_dir = self.temp_root / "test_timeline"
        self.test_dir.mkdir()
        
        self.timeline = ResearchTimeline(self.test_dir)
    
    def teardown_method(self):
        """테스트 후 정리"""
        if hasattr(self, 'temp_root') and self.temp_root.exists():
            shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def test_adds_timeline_entries(self):
        """타임라인 엔트리가 추가되는가?"""
        # When: 엔트리 추가
        self.timeline.add_entry(
            "ANALYSIS",
            "Performed PCA on feature matrix",
            {"dimensions": 50, "variance_explained": 0.95}
        )
        
        # Then: 파일에 기록 확인
        content = self.timeline.timeline_file.read_text()
        assert "ANALYSIS" in content
        assert "Performed PCA on feature matrix" in content
        assert "dimensions: 50" in content
        assert "variance_explained: 0.95" in content
    
    def test_creates_checkpoints(self):
        """체크포인트가 생성되고 저장되는가?"""
        # When: 체크포인트 생성
        checkpoint_id = self.timeline.create_checkpoint("Initial analysis complete")
        
        # Then: 체크포인트 디렉토리 확인
        checkpoint_dir = self.timeline.checkpoints_dir / checkpoint_id
        assert checkpoint_dir.exists()
        
        snapshot_file = checkpoint_dir / "snapshot.json"
        assert snapshot_file.exists()
        
        snapshot = json.loads(snapshot_file.read_text())
        assert snapshot["name"] == "Initial analysis complete"
        assert "timestamp" in snapshot
        assert "environment" in snapshot


if __name__ == "__main__":
    # 실제 테스트 실행
    pytest.main([__file__, "-v", "--tb=short"])