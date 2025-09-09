#!/usr/bin/env python3
"""
디렉토리 기반 프로젝트 감지 시스템 완전 재설계 테스트
TADD 방식: 실패하는 테스트 우선 생성

이 테스트들은 현재 구현에서는 모두 실패해야 하며,
재설계 구현 완료 후 통과해야 합니다.
"""
import pytest
import sys
import os
import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

# Add src to path  
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_project_manager import ResearchProjectManager


class TestDirectoryBasedProjectDetection:
    """디렉토리 기반 프로젝트 감지 핵심 시나리오"""
    
    def setup_method(self):
        """테스트 환경 설정"""
        # 임시 디렉토리에서 완전 격리된 테스트 환경 구축
        self.temp_root = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        
        # 실제 프로젝트 구조 시뮬레이션
        self.setup_realistic_project_structure()
        
    def teardown_method(self):
        """테스트 환경 정리"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def setup_realistic_project_structure(self):
        """실제 연구 프로젝트 구조 생성"""
        # 프로젝트 루트 구조
        project_root = self.temp_root / "my_research_workspace"
        project_root.mkdir(parents=True)
        
        # research_projects 디렉토리
        research_dir = project_root / "research_projects"  
        research_dir.mkdir()
        
        # 메타데이터 파일
        metadata = {
            "projects": {
                "2025-09-09_drug_discovery": {
                    "name": "drug_discovery",
                    "description": "Drug discovery analysis",
                    "created": "2025-09-09T10:00:00",
                    "status": "active"
                },
                "2025-09-08_protein_analysis": {
                    "name": "protein_analysis", 
                    "description": "Protein structure analysis",
                    "created": "2025-09-08T15:30:00",
                    "status": "completed"
                }
            },
            "active_project": "2025-09-09_drug_discovery"
        }
        
        metadata_file = research_dir / ".research_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # 실제 프로젝트 디렉토리들
        drug_project = research_dir / "2025-09-09_drug_discovery"
        drug_project.mkdir()
        
        # 깊은 서브디렉토리 구조 
        notebooks_dir = drug_project / "notebooks" / "exploratory" / "molecular_analysis"
        notebooks_dir.mkdir(parents=True)
        
        scripts_dir = drug_project / "scripts" / "preprocessing" 
        scripts_dir.mkdir(parents=True)
        
        results_dir = drug_project / "results" / "2025-09" / "week-37"
        results_dir.mkdir(parents=True)
        
        # 프로젝트 파일들 생성
        (notebooks_dir / "compound_screening.ipynb").touch()
        (scripts_dir / "data_loader.py").touch()
        (results_dir / "analysis_results.csv").touch()
        
        self.project_root = project_root
        self.research_dir = research_dir  
        self.drug_project = drug_project
        self.notebooks_deep = notebooks_dir
        self.scripts_deep = scripts_dir
        self.results_deep = results_dir
    
    def test_user_working_in_deep_notebooks_directory_gets_project_detected(self):
        """사용자가 깊은 notebooks 디렉토리에서 작업할 때 프로젝트가 감지되어야 함"""
        
        # Given: 사용자가 깊은 notebooks 서브디렉토리로 이동
        deep_work_dir = self.notebooks_deep
        os.chdir(str(deep_work_dir))
        
        # When: ResearchProjectManager로 현재 프로젝트 감지 시도
        manager = ResearchProjectManager()
        detected_project = manager.detect_current_project()
        
        # Then: 올바른 프로젝트 ID가 감지되어야 함
        assert detected_project == "2025-09-09_drug_discovery", f"Expected 'drug_discovery' project, got: {detected_project}"
        
        # And: 메타데이터가 올바른 경로에서 로드되어야 함  
        assert manager.metadata.get("active_project") == "2025-09-09_drug_discovery"
        assert "2025-09-09_drug_discovery" in manager.metadata.get("projects", {})
        
        # And: 프로젝트 정보가 정확해야 함
        project_info = manager.metadata["projects"]["2025-09-09_drug_discovery"]
        assert project_info["name"] == "drug_discovery"
        assert project_info["description"] == "Drug discovery analysis"
        assert project_info["status"] == "active"
    
    def test_user_working_in_scripts_subdirectory_gets_same_project_detected(self):
        """사용자가 scripts 서브디렉토리에서 작업해도 같은 프로젝트가 감지되어야 함"""
        
        # Given: 사용자가 scripts 서브디렉토리로 이동 
        scripts_work_dir = self.scripts_deep
        os.chdir(str(scripts_work_dir))
        
        # When: 프로젝트 감지 실행
        manager = ResearchProjectManager()
        detected_project = manager.detect_current_project()
        
        # Then: 같은 프로젝트가 감지되어야 함
        assert detected_project == "2025-09-09_drug_discovery"
        
        # And: 베이스 디렉토리가 올바르게 설정되어야 함
        expected_base = self.research_dir
        assert manager.base_dir == expected_base, f"Base dir should be {expected_base}, got {manager.base_dir}"
    
    def test_user_in_different_project_gets_correct_project_detected(self):
        """사용자가 다른 프로젝트 디렉토리에 있으면 해당 프로젝트가 감지되어야 함"""
        
        # Given: 다른 프로젝트 디렉토리 설정
        protein_project = self.research_dir / "2025-09-08_protein_analysis"
        protein_project.mkdir()
        protein_subdir = protein_project / "analysis" / "structures"
        protein_subdir.mkdir(parents=True)
        
        # When: 해당 디렉토리에서 작업
        os.chdir(str(protein_subdir))
        manager = ResearchProjectManager()
        detected_project = manager.detect_current_project()
        
        # Then: 해당 프로젝트가 감지되어야 함
        assert detected_project == "2025-09-08_protein_analysis"
        assert manager.metadata.get("active_project") == "2025-09-09_drug_discovery"  # 기본값 유지
        assert "2025-09-08_protein_analysis" in manager.metadata.get("projects", {})
    
    def test_user_outside_research_projects_gets_fallback_behavior(self):
        """연구 프로젝트 외부에서는 기존 동작 유지"""
        
        # Given: 연구 프로젝트 외부 디렉토리
        outside_dir = self.temp_root / "regular_work"
        outside_dir.mkdir()
        os.chdir(str(outside_dir))
        
        # When: 프로젝트 감지 시도
        manager = ResearchProjectManager()  
        detected_project = manager.detect_current_project()
        
        # Then: None 또는 기본 프로젝트 반환 (기존 동작)
        assert detected_project is None or isinstance(detected_project, str)
    
    def test_corrupted_metadata_file_does_not_crash_system(self):
        """메타데이터 파일 손상 시에도 시스템이 중단되지 않아야 함"""
        
        # Given: 손상된 메타데이터 파일
        metadata_file = self.research_dir / ".research_metadata.json"
        with open(metadata_file, 'w') as f:
            f.write("{ invalid json content }")
        
        os.chdir(str(self.notebooks_deep))
        
        # When: 프로젝트 감지 시도
        manager = ResearchProjectManager()
        
        # Then: 예외가 발생하지 않아야 함
        try:
            detected_project = manager.detect_current_project()
            # 결과는 None이거나 fallback 값이어야 함
            assert detected_project is None or isinstance(detected_project, str)
        except Exception as e:
            pytest.fail(f"Corrupted metadata should not crash the system: {e}")
    
    def test_missing_metadata_file_uses_fallback_logic(self):
        """메타데이터 파일이 없으면 기존 로직 사용"""
        
        # Given: 메타데이터 파일 제거
        metadata_file = self.research_dir / ".research_metadata.json"
        metadata_file.unlink()
        
        os.chdir(str(self.notebooks_deep))
        
        # When: 프로젝트 감지 시도
        manager = ResearchProjectManager()
        detected_project = manager.detect_current_project()
        
        # Then: 기존 fallback 로직 사용 (None 반환 등)
        assert detected_project is None or isinstance(detected_project, str)


class TestInputValidationAndSecurity:
    """입력 검증 및 보안 강화"""
    
    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(str(self.temp_dir))
        
    def teardown_method(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_empty_project_name_raises_validation_error(self):
        """빈 프로젝트명은 검증 오류를 발생시켜야 함"""
        
        # Given: ResearchProjectManager 인스턴스
        manager = ResearchProjectManager(base_dir=str(self.temp_dir))
        
        # When & Then: 빈 프로젝트명으로 초기화 시도
        with pytest.raises(ValueError) as exc_info:
            manager.init_project("", "Some description")
        
        assert "프로젝트명은 비어있을 수 없습니다" in str(exc_info.value)
    
    def test_project_name_with_path_separators_gets_sanitized(self):
        """경로 구분자가 포함된 프로젝트명은 정규화되어야 함"""
        
        # Given: 위험한 문자가 포함된 프로젝트명
        dangerous_name = "project/with\\backslash..and/more"
        
        manager = ResearchProjectManager(base_dir=str(self.temp_dir))
        
        # When: 프로젝트 생성
        result = manager.init_project(dangerous_name, "Test description")
        
        # Then: 안전한 형태로 정규화되어야 함
        assert result["success"] is True
        
        # And: 생성된 프로젝트 ID에 위험한 문자가 없어야 함  
        project_id = result.get("project_id", "")
        assert "/" not in project_id
        assert "\\" not in project_id  
        assert ".." not in project_id
        
        # And: 실제 디렉토리도 안전하게 생성되어야 함
        created_dirs = list(Path(self.temp_dir).glob("*"))
        for dir_path in created_dirs:
            assert "/" not in dir_path.name
            assert "\\" not in dir_path.name
    
    def test_extremely_long_project_name_gets_truncated(self):
        """매우 긴 프로젝트명은 적절히 잘려야 함"""
        
        # Given: 매우 긴 프로젝트명 (100자)
        long_name = "a" * 100 + "매우긴한글프로젝트명입니다" * 10
        
        manager = ResearchProjectManager(base_dir=str(self.temp_dir))
        
        # When: 프로젝트 생성
        result = manager.init_project(long_name, "Test description")
        
        # Then: 성공해야 함
        assert result["success"] is True
        
        # And: 생성된 프로젝트 ID가 합리적인 길이여야 함 (50자 이하)
        project_id = result.get("project_id", "")
        assert len(project_id) <= 60  # 날짜 prefix 포함하여 여유있게
    
    def test_unicode_korean_project_name_handled_safely(self):
        """유니코드 한글 프로젝트명이 안전하게 처리되어야 함"""
        
        # Given: 한글과 특수문자가 섞인 프로젝트명
        korean_name = "신약개발📊분석-프로젝트_2025"
        
        manager = ResearchProjectManager(base_dir=str(self.temp_dir))
        
        # When: 프로젝트 생성
        result = manager.init_project(korean_name, "한글 설명입니다")
        
        # Then: 성공해야 함
        assert result["success"] is True
        
        # And: 한글은 보존되고 위험한 문자만 제거되어야 함
        project_id = result.get("project_id", "")
        assert "신약개발" in project_id or "2025" in project_id  # 일부 보존
        
        # And: 실제 디렉토리 생성 확인
        created_dirs = list(Path(self.temp_dir).glob("*"))
        assert len(created_dirs) > 0


class TestRecursiveDirectorySearch:
    """재귀 디렉토리 탐색 핵심 로직"""
    
    def setup_method(self):
        self.temp_root = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        
    def teardown_method(self):  
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_root, ignore_errors=True)
    
    def test_finds_metadata_five_levels_up(self):
        """5단계 상위 디렉토리의 메타데이터도 찾아야 함"""
        
        # Given: 5단계 깊은 구조 생성
        level5 = self.temp_root / "work" / "projects" / "research_projects"  
        level5.mkdir(parents=True)
        
        # 메타데이터 생성
        metadata = {
            "projects": {"test_project": {"name": "test"}},
            "active_project": "test_project" 
        }
        metadata_file = level5 / ".research_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f)
        
        # 프로젝트 및 깊은 서브디렉토리
        project_dir = level5 / "test_project"
        project_dir.mkdir()
        deep_work = project_dir / "a" / "b" / "c" / "d" / "e"
        deep_work.mkdir(parents=True)
        
        # When: 가장 깊은 디렉토리에서 작업
        os.chdir(str(deep_work))
        manager = ResearchProjectManager()
        detected_project = manager.detect_current_project()
        
        # Then: 프로젝트가 감지되어야 함
        assert detected_project == "test_project"
        assert manager.base_dir == level5
    
    def test_stops_at_filesystem_root_if_no_metadata_found(self):
        """메타데이터를 찾지 못해도 무한루프에 빠지지 않아야 함"""
        
        # Given: 메타데이터가 없는 디렉토리 구조
        deep_dir = self.temp_root / "no" / "metadata" / "here"  
        deep_dir.mkdir(parents=True)
        
        # When: 깊은 디렉토리에서 탐색
        os.chdir(str(deep_dir))
        manager = ResearchProjectManager()
        
        # Then: 합리적인 시간 내에 완료되어야 함 (무한루프 없음)
        import time
        start_time = time.time()
        detected_project = manager.detect_current_project()
        elapsed = time.time() - start_time
        
        assert elapsed < 1.0  # 1초 이내 완료
        assert detected_project is None  # None 또는 fallback 값
    
    def test_handles_permission_denied_gracefully(self):
        """권한 거부 디렉토리도 우아하게 처리해야 함"""
        
        # Given: 제한된 권한 디렉토리 (시뮬레이션)
        restricted_dir = self.temp_root / "restricted"
        restricted_dir.mkdir()
        
        # Mock os.access to simulate permission denied
        with patch('os.access', return_value=False):
            os.chdir(str(restricted_dir))
            manager = ResearchProjectManager()
            
            # When & Then: 예외 없이 처리되어야 함
            try:
                detected_project = manager.detect_current_project()
                assert detected_project is None or isinstance(detected_project, str)
            except PermissionError:
                pytest.fail("Permission errors should be handled gracefully")


class TestPerformanceAndScalability:
    """성능 및 확장성 테스트"""
    
    def test_directory_detection_completes_within_50ms(self):
        """디렉토리 감지가 50ms 이내에 완료되어야 함"""
        
        # Given: 표준적인 프로젝트 구조
        temp_root = Path(tempfile.mkdtemp()) 
        try:
            research_dir = temp_root / "research_projects"
            research_dir.mkdir(parents=True)
            
            # 메타데이터 생성
            metadata = {"projects": {"test": {"name": "test"}}, "active_project": "test"}
            with open(research_dir / ".research_metadata.json", 'w') as f:
                json.dump(metadata, f)
            
            # 프로젝트 및 서브디렉토리
            project_dir = research_dir / "test"  
            project_dir.mkdir()
            work_dir = project_dir / "notebooks" / "analysis"
            work_dir.mkdir(parents=True)
            
            os.chdir(str(work_dir))
            
            # When & Then: 성능 측정
            import time
            start_time = time.time()
            
            manager = ResearchProjectManager()
            detected_project = manager.detect_current_project()
            
            elapsed = time.time() - start_time
            
            assert elapsed < 0.05  # 50ms 이내
            assert detected_project == "test"
            
        finally:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    # 이 테스트들은 현재 구현에서 실패해야 합니다 (TADD 방식)
    print("🧪 디렉토리 감지 재설계 테스트 - 현재 구현에서는 실패 예상")
    pytest.main([__file__, "-v", "--tb=short"])