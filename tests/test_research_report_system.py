"""
연구 보고서 생성 시스템 테스트 스위트
TADD 방식으로 실패하는 테스트를 먼저 작성
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import shutil


class TestResearchReportSystem:
    """연구 보고서 시스템 테스트"""
    
    def test_research_data_collection_finds_all_entries(self):
        """연구 데이터 수집이 모든 항목을 올바르게 찾는지 검증"""
        # Given: 테스트용 연구 데이터가 있는 임시 디렉토리
        temp_dir = Path(tempfile.mkdtemp())
        projects_dir = temp_dir / ".research_projects"
        projects_dir.mkdir()
        
        test_data = {
            "project_name": "test_project",
            "description": "테스트 프로젝트",
            "history": [
                {
                    "type": "track",
                    "content": "첫 번째 진행사항",
                    "timestamp": "2024-09-01T10:00:00",
                    "metadata": {}
                },
                {
                    "type": "hypothesis", 
                    "content": "테스트 가설",
                    "timestamp": "2024-09-02T11:00:00",
                    "metadata": {"confidence": "high"}
                },
                {
                    "type": "experiment",
                    "content": "실험 A",
                    "timestamp": "2024-09-03T12:00:00", 
                    "metadata": {"description": "첫 번째 실험"}
                }
            ]
        }
        
        project_file = projects_dir / "test_project.json"
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)
        
        # When: 연구 데이터를 수집
        from src.research_report_generator import ResearchReportGenerator
        generator = ResearchReportGenerator(str(temp_dir))
        collected_data = generator.collect_research_data("test_project")
        
        # Then: 모든 데이터가 정확히 수집되어야 함
        assert "track" in collected_data
        assert "hypothesis" in collected_data
        assert "experiment" in collected_data
        
        assert len(collected_data["track"]) == 1
        assert len(collected_data["hypothesis"]) == 1
        assert len(collected_data["experiment"]) == 1
        
        # And: 내용이 정확해야 함
        track_entry = collected_data["track"][0]
        assert track_entry.content == "첫 번째 진행사항"
        assert track_entry.project_name == "test_project"
        
        hypothesis_entry = collected_data["hypothesis"][0]
        assert hypothesis_entry.content == "테스트 가설"
        assert hypothesis_entry.metadata["confidence"] == "high"
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_academic_report_generation_includes_all_sections(self):
        """학술 보고서가 모든 필수 섹션을 포함하는지 검증"""
        # Given: 완전한 연구 데이터
        from src.research_report_generator import ResearchReportGenerator, ResearchEntry
        temp_dir = Path(tempfile.mkdtemp())
        generator = ResearchReportGenerator(str(temp_dir))
        
        research_data = {
            "metadata": [{
                "project_name": "comprehensive_test",
                "description": "포괄적 테스트 프로젝트",
                "version": "1.0.0",
                "status": "active",
                "key_achievements": ["성과 1", "성과 2"],
                "current_experiments": ["실험 1", "실험 2"],
                "next_milestones": ["계획 1", "계획 2"]
            }],
            "hypothesis": [
                ResearchEntry(
                    timestamp=datetime(2024, 9, 1),
                    command="hypothesis",
                    content="주요 가설",
                    project_name="comprehensive_test",
                    metadata={}
                )
            ],
            "track": [
                ResearchEntry(
                    timestamp=datetime(2024, 9, 2),
                    command="track", 
                    content="중요한 진전",
                    project_name="comprehensive_test",
                    metadata={}
                )
            ],
            "experiment": [
                ResearchEntry(
                    timestamp=datetime(2024, 9, 3),
                    command="experiment",
                    content="핵심 실험", 
                    project_name="comprehensive_test",
                    metadata={"description": "실험 설명"}
                )
            ]
        }
        
        # When: 학술 보고서를 생성
        report = generator.generate_academic_report("comprehensive_test", research_data)
        
        # Then: 모든 필수 섹션이 포함되어야 함
        required_sections = [
            "# comprehensive_test", # 제목
            "## 📋 연구 개요",
            "## 🎯 연구 목적 및 배경", 
            "## 🔬 연구 방법론",
            "### 연구 가설",
            "### 실험 설계",
            "## 📈 연구 진행 과정",
            "## 🏆 주요 연구 성과",
            "## 📊 연구 통계",
            "## 🎯 결론 및 제언"
        ]
        
        for section in required_sections:
            assert section in report, f"필수 섹션 '{section}'이 보고서에 누락됨"
        
        # And: 구체적 데이터가 포함되어야 함
        assert "주요 가설" in report
        assert "중요한 진전" in report
        assert "핵심 실험" in report
        assert "성과 1" in report
        assert "실험 1" in report
        assert "계획 1" in report
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_report_file_creation_and_storage(self):
        """보고서 파일이 올바른 위치에 생성되고 저장되는지 검증"""
        # Given: 임시 프로젝트 디렉토리
        temp_dir = Path(tempfile.mkdtemp())
        projects_dir = temp_dir / ".research_projects"
        projects_dir.mkdir()
        
        # 기본 연구 데이터 생성
        test_data = {
            "project_name": "file_test_project",
            "description": "파일 테스트 프로젝트",
            "history": [
                {
                    "type": "track",
                    "content": "파일 테스트 진행",
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {}
                }
            ]
        }
        
        project_file = projects_dir / "file_test_project.json"
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)
        
        # When: 보고서를 생성
        from src.research_report_generator import ResearchReportGenerator
        generator = ResearchReportGenerator(str(temp_dir))
        report_path = generator.generate_comprehensive_report("file_test_project")
        
        # Then: 보고서 파일이 정확한 위치에 생성되어야 함
        assert not report_path.startswith("❌"), f"보고서 생성 실패: {report_path}"
        
        report_file = Path(report_path)
        assert report_file.exists(), "보고서 파일이 생성되지 않음"
        assert report_file.suffix == ".md", "보고서가 마크다운 형식이 아님"
        
        # And: 파일 이름 패턴이 올바라야 함
        expected_pattern = "file_test_project_research_report_"
        assert expected_pattern in report_file.name
        
        # And: 최신 보고서 심볼릭 링크가 생성되어야 함
        latest_link = report_file.parent / "file_test_project_latest_report.md"
        assert latest_link.exists(), "최신 보고서 링크가 생성되지 않음"
        assert latest_link.is_symlink(), "최신 보고서가 심볼릭 링크가 아님"
        
        # And: 보고서 내용이 유효해야 함
        content = report_file.read_text(encoding='utf-8')
        assert "file_test_project" in content
        assert "파일 테스트 진행" in content
        assert "연구" in content
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_multiple_projects_report_generation(self):
        """여러 프로젝트의 보고서가 독립적으로 생성되는지 검증"""
        # Given: 두 개의 서로 다른 연구 프로젝트
        temp_dir = Path(tempfile.mkdtemp())
        projects_dir = temp_dir / ".research_projects"
        projects_dir.mkdir()
        
        # 프로젝트 A
        project_a_data = {
            "project_name": "project_a",
            "description": "프로젝트 A",
            "history": [{"type": "track", "content": "프로젝트 A 진행", "timestamp": datetime.now().isoformat(), "metadata": {}}]
        }
        
        # 프로젝트 B  
        project_b_data = {
            "project_name": "project_b", 
            "description": "프로젝트 B",
            "history": [{"type": "hypothesis", "content": "프로젝트 B 가설", "timestamp": datetime.now().isoformat(), "metadata": {}}]
        }
        
        with open(projects_dir / "project_a.json", 'w', encoding='utf-8') as f:
            json.dump(project_a_data, f, ensure_ascii=False)
            
        with open(projects_dir / "project_b.json", 'w', encoding='utf-8') as f:
            json.dump(project_b_data, f, ensure_ascii=False)
        
        # When: 각 프로젝트의 보고서를 생성
        from src.research_report_generator import ResearchReportGenerator
        generator = ResearchReportGenerator(str(temp_dir))
        
        report_a_path = generator.generate_comprehensive_report("project_a")
        report_b_path = generator.generate_comprehensive_report("project_b")
        
        # Then: 두 보고서가 모두 생성되어야 함
        assert not report_a_path.startswith("❌")
        assert not report_b_path.startswith("❌")
        
        report_a_file = Path(report_a_path)
        report_b_file = Path(report_b_path)
        
        assert report_a_file.exists()
        assert report_b_file.exists()
        
        # And: 보고서 내용이 서로 다르고 정확해야 함
        content_a = report_a_file.read_text(encoding='utf-8')
        content_b = report_b_file.read_text(encoding='utf-8')
        
        assert "프로젝트 A 진행" in content_a
        assert "프로젝트 B" not in content_a
        
        assert "프로젝트 B 가설" in content_b
        assert "프로젝트 A" not in content_b
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_empty_project_handling(self):
        """빈 프로젝트나 존재하지 않는 프로젝트 처리 검증"""
        # Given: 빈 임시 디렉토리
        temp_dir = Path(tempfile.mkdtemp())
        
        # When: 존재하지 않는 프로젝트의 보고서 생성 시도
        from src.research_report_generator import ResearchReportGenerator
        generator = ResearchReportGenerator(str(temp_dir))
        result = generator.generate_comprehensive_report("nonexistent_project")
        
        # Then: 적절한 에러 메시지가 반환되어야 함
        assert result.startswith("❌"), "존재하지 않는 프로젝트에 대해 에러가 발생해야 함"
        assert "nonexistent_project" in result
        assert "연구 데이터를 찾을 수 없습니다" in result
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_report_statistics_accuracy(self):
        """보고서 통계가 정확한지 검증"""
        # Given: 정확한 개수의 각 유형별 데이터
        from src.research_report_generator import ResearchReportGenerator, ResearchEntry
        temp_dir = Path(tempfile.mkdtemp())
        generator = ResearchReportGenerator(str(temp_dir))
        
        research_data = {
            "metadata": [{"description": "통계 테스트"}],
            "track": [
                ResearchEntry(datetime.now(), "track", f"진행{i}", "test", {}) 
                for i in range(5)
            ],
            "hypothesis": [
                ResearchEntry(datetime.now(), "hypothesis", f"가설{i}", "test", {})
                for i in range(3)  
            ],
            "experiment": [
                ResearchEntry(datetime.now(), "experiment", f"실험{i}", "test", {})
                for i in range(2)
            ],
            "milestone": [
                ResearchEntry(datetime.now(), "milestone", f"마일스톤{i}", "test", {})
                for i in range(4)
            ]
        }
        
        # When: 보고서 생성
        report = generator.generate_academic_report("stats_test", research_data)
        
        # Then: 통계가 정확해야 함
        assert "**총 연구 기록**: 14" in report  # 5+3+2+4 = 14
        assert "**가설 수**: 3" in report
        assert "**실험 수**: 2" in report  
        assert "**마일스톤**: 4" in report
        
        # And: 각 항목이 보고서에 포함되어야 함
        for i in range(5):
            assert f"진행{i}" in report
        for i in range(3):
            assert f"가설{i}" in report
        for i in range(2):
            assert f"실험{i}" in report
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_chronological_ordering_in_report(self):
        """보고서에서 시간순 정렬이 올바른지 검증"""
        # Given: 시간이 다른 여러 항목들
        from src.research_report_generator import ResearchReportGenerator, ResearchEntry
        temp_dir = Path(tempfile.mkdtemp())
        generator = ResearchReportGenerator(str(temp_dir))
        
        base_time = datetime(2024, 9, 1)
        research_data = {
            "metadata": [{"description": "시간순 테스트"}],
            "track": [
                ResearchEntry(base_time + timedelta(days=3), "track", "세 번째 진행", "test", {}),
                ResearchEntry(base_time + timedelta(days=1), "track", "첫 번째 진행", "test", {}),
                ResearchEntry(base_time + timedelta(days=2), "track", "두 번째 진행", "test", {})
            ]
        }
        
        # When: 보고서 생성
        report = generator.generate_academic_report("chronology_test", research_data)
        
        # Then: 시간순으로 정렬되어야 함
        first_pos = report.find("첫 번째 진행")
        second_pos = report.find("두 번째 진행") 
        third_pos = report.find("세 번째 진행")
        
        assert first_pos < second_pos < third_pos, "진행 사항이 시간순으로 정렬되지 않음"
        
        # And: 날짜가 올바르게 표시되어야 함
        assert "09-02" in report  # 첫 번째 (base_time + 1일)
        assert "09-03" in report  # 두 번째 (base_time + 2일)  
        assert "09-04" in report  # 세 번째 (base_time + 3일)
        
        # Cleanup
        shutil.rmtree(temp_dir)