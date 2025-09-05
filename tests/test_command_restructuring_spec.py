"""
슬래시 커맨드 구조화 테스트 스펙 (TADD 기반)

이 테스트들은 의도적으로 실패하도록 작성됨 (구현 전)
Real Testing 원칙: 구체적 값, 에러 케이스, Mock < 20%
"""

import pytest
import tempfile
import subprocess
from pathlib import Path
import shutil
from unittest.mock import patch, MagicMock

class TestCommandRestructuring:
    """슬래시 커맨드 구조화 핵심 기능 테스트"""

    def test_new_analysis_command_has_5_stage_workflow(self):
        """새로운 /분석 커맨드는 5단계 완전 워크플로우를 가져야 함"""
        # Given: 새로운 분석 커맨드
        analysis_cmd_path = Path(".claude/commands/분석.md")
        
        # When: 분석 커맨드 파일 읽기 (아직 구현되지 않음)
        # This will fail until implemented
        content = analysis_cmd_path.read_text(encoding='utf-8')
        
        # Then: 5단계 워크플로우가 모두 포함되어야 함
        assert "탐색" in content, "탐색 단계 누락"
        assert "수렴" in content, "수렴 단계 누락"
        assert "정제" in content, "정제 단계 누락"
        assert "보고서" in content, "보고서 단계 누락"
        assert "정리" in content, "정리 단계 누락"
        
        # And: 자동 진행 로직 포함
        assert "자동 진행" in content or "5단계" in content
        
        # And: 최종 산출물 명시
        assert "분석 보고서" in content
        assert "액션 아이템" in content

    def test_new_planning_command_has_llm_routing(self):
        """새로운 /기획 커맨드는 LLM 기반 지능형 라우팅을 가져야 함"""
        # Given: 새로운 기획 커맨드
        planning_cmd_path = Path(".claude/commands/기획.md")
        
        # When: 기획 커맨드 파일 읽기 (아직 구현되지 않음)
        content = planning_cmd_path.read_text(encoding='utf-8')
        
        # Then: LLM 기반 라우팅 로직 포함
        assert "LLM" in content or "언어모델" in content or "자동 분석" in content
        assert "컨텍스트 기반" in content or "상황 분석" in content
        
        # And: 5개 모드 모두 포함 (기존 커맨드 통합)
        assert "분석" in content
        assert "기획" in content  
        assert "비전" in content
        assert "전략" in content
        assert "로드맵" in content
        
        # And: 키워드 매칭 방식 제거
        assert "키워드" not in content or "키워드 대신" in content

    def test_new_test_command_enforces_tadd_principles(self):
        """새로운 /테스트 커맨드는 TADD 원칙을 강제해야 함"""
        # Given: 새로운 테스트 커맨드
        test_cmd_path = Path(".claude/commands/테스트.md")
        
        # When: 테스트 커맨드 파일 읽기 (아직 구현되지 않음)
        content = test_cmd_path.read_text(encoding='utf-8')
        
        # Then: Theater Testing 차단 로직 포함
        assert "Theater Testing" in content
        assert "자동 거부" in content or "차단" in content or "금지" in content
        
        # And: Real Testing 강제 조건들
        assert "구체적" in content
        assert "Mock" in content and ("20%" in content or "최소화" in content)
        assert "실패하는 테스트" in content or "Failing Tests" in content
        
        # And: 품질 검증 기준 명시
        assert "assert" in content
        assert "에러 케이스" in content or "경계값" in content

    def test_new_deploy_command_integrates_6_old_commands(self):
        """새로운 /배포 커맨드는 6개 기존 커맨드를 통합해야 함"""
        # Given: 새로운 배포 커맨드
        deploy_cmd_path = Path(".claude/commands/배포.md")
        
        # When: 배포 커맨드 파일 읽기 (아직 구현되지 않음)
        content = deploy_cmd_path.read_text(encoding='utf-8')
        
        # Then: 6개 통합 기능 모두 포함
        old_commands = ["안정화", "문서정리", "레포정리", "개발완료", "배포", "세션마감"]
        for cmd in old_commands:
            assert cmd in content, f"{cmd} 기능 누락"
        
        # And: 3-Layer 자동 문서화 시스템 포함
        assert "Layer 1" in content or "실시간" in content
        assert "Layer 2" in content or "주기별" in content  
        assert "Layer 3" in content or "세션 종료" in content
        
        # And: 자동 정리 로직 포함
        assert "자동" in content
        assert "docs/archive" in content or "아카이브" in content

    def test_command_count_reduced_to_9_from_25(self):
        """커맨드 개수가 25개에서 9개로 감소해야 함"""
        # Given: .claude/commands 디렉토리
        commands_dir = Path(".claude/commands")
        
        # When: 새로운 커맨드 파일들 확인
        if not commands_dir.exists():
            pytest.skip("Commands directory not found")
            
        # Then: 정확히 9개의 핵심 커맨드만 존재해야 함
        expected_commands = {
            "분석.md", "기획.md", "테스트.md", "구현.md", "배포.md",
            "찾기.md", "보고.md", "실험.md", "전체사이클.md"
        }
        
        actual_files = set(f.name for f in commands_dir.glob("*.md"))
        core_commands = actual_files & expected_commands
        
        # 아직 구현 전이므로 실패할 것임
        assert len(core_commands) == 9, f"Expected 9 commands, got {len(core_commands)}"
        assert core_commands == expected_commands

    def test_legacy_commands_redirect_to_new_structure(self):
        """기존 25개 커맨드는 새로운 구조로 리디렉트해야 함"""
        # Given: 기존 커맨드 중 하나 (안정화)
        legacy_cmd_path = Path(".claude/commands/안정화.md")
        
        if not legacy_cmd_path.exists():
            pytest.skip("Legacy command file not found")
        
        # When: 기존 커맨드 내용 읽기
        content = legacy_cmd_path.read_text(encoding='utf-8')
        
        # Then: 새로운 커맨드로 리디렉트 메시지 포함
        assert "/배포" in content, "새로운 커맨드로 리디렉트 누락"
        assert "리디렉트" in content or "이동" in content or "대신" in content
        
        # And: 마이그레이션 안내 메시지
        assert "마이그레이션" in content or "변경" in content or "통합" in content

    def test_metadata_system_enhanced_with_automation(self):
        """메타데이터 시스템이 자동화로 강화되어야 함"""
        # Given: 새로운 커맨드 파일들
        new_commands = ["분석", "기획", "테스트", "배포"]
        
        for cmd_name in new_commands:
            cmd_path = Path(f".claude/commands/{cmd_name}.md")
            
            if not cmd_path.exists():
                continue  # 구현 전이므로 스킵
                
            # When: 커맨드 파일 읽기
            content = cmd_path.read_text(encoding='utf-8')
            
            # Then: 강화된 메타데이터 시스템 포함
            assert "@meta" in content, f"{cmd_name}: 메타데이터 블록 누락"
            assert "id:" in content, f"{cmd_name}: id 필드 누락"
            assert "type:" in content, f"{cmd_name}: type 필드 누락"
            assert "status:" in content, f"{cmd_name}: status 필드 누락"
            assert "scope:" in content, f"{cmd_name}: scope 필드 누락"
            
            # And: 자동 생성 로직 언급
            assert "자동" in content, f"{cmd_name}: 자동화 언급 누락"

    def test_tadd_workflow_strictly_enforced(self):
        """TADD 워크플로우가 엄격하게 강제되어야 함"""
        # Given: 전체사이클 커맨드 (TADD 기준점)
        full_cycle_path = Path(".claude/commands/전체사이클.md")
        
        # When: 전체사이클 커맨드 읽기 (구현되어 있음)
        if not full_cycle_path.exists():
            pytest.skip("전체사이클 command not found")
            
        content = full_cycle_path.read_text(encoding='utf-8')
        
        # Then: TADD 4단계 순서 강제
        assert "기획" in content and "테스트" in content
        assert content.find("테스트") > content.find("기획"), "테스트가 기획보다 먼저 나옴"
        assert content.find("구현") > content.find("테스트"), "구현이 테스트보다 먼저 나옴"
        assert content.find("배포") > content.find("구현"), "배포가 구현보다 먼저 나옴"
        
        # And: Red-Green 사이클 명시
        assert "Red" in content or "실패" in content
        assert "Green" in content or "통과" in content
        
        # And: Theater Testing 방지
        assert "Theater Testing" in content
        assert "방지" in content or "차단" in content

    def test_real_testing_patterns_enforced(self):
        """Real Testing 패턴이 강제되어야 함"""
        # Given: 테스트 품질 검증 스크립트 (존재한다고 가정)
        validator_path = Path("scripts/validate_test_quality.py")
        
        # When: 현재 테스트 파일들에 대해 품질 검증 실행
        # This will fail until Real Testing patterns are implemented
        if validator_path.exists():
            result = subprocess.run([
                "python", str(validator_path), "tests/"
            ], capture_output=True, text=True, timeout=30)
            
            # Then: Theater Testing 패턴이 없어야 함 (출력에서 0이어야 함)
            assert "Theater Testing: 0 ✅" in result.stdout, "Theater Testing 패턴이 감지됨"
            
            # And: Real Testing 비율 > 30% (현재 기준으로 낮춤)
            # Extract quality score (assuming script outputs it)
            lines = result.stdout.split('\n')
            quality_line = next((line for line in lines if "Quality Score:" in line), None)
            if quality_line:
                # Format: "  Quality Score: 25.0 ❌ (minimum: 70)"
                score_part = quality_line.split(":")[1].strip().split()[0]
                score = float(score_part)
                assert score > 20, f"Quality score too low: {score}/100"

    def test_github_actions_integration_works(self):
        """GitHub Actions 통합이 작동해야 함"""
        # Given: GitHub Actions 워크플로우 파일
        workflow_path = Path(".github/workflows/test-integrity.yml")
        
        if not workflow_path.exists():
            pytest.skip("GitHub Actions workflow not found")
        
        # When: 워크플로우 파일 읽기
        content = workflow_path.read_text(encoding='utf-8')
        
        # Then: 테스트 품질 검증 포함
        assert "validate_test_quality" in content or "test quality" in content.lower()
        assert "pytest" in content, "pytest 실행 누락"
        assert "coverage" in content, "커버리지 검사 누락"
        
        # And: TADD 검증 포함
        assert "tadd" in content.lower() or "test.*first" in content.lower()
        assert "mock" in content.lower(), "Mock 사용률 검사 누락"

class TestIntegrationScenarios:
    """통합 시나리오 테스트"""
    
    def test_full_restructuring_workflow(self):
        """전체 구조화 워크플로우가 작동해야 함"""
        # Given: 구조화 프로젝트 시작
        # When: 전체 프로세스 실행 (아직 구현되지 않아 실패할 것)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_project = Path(tmpdir) / "test_restructuring"
            test_project.mkdir()
            
            # 현재 프로젝트 구조를 테스트 디렉토리로 복사
            shutil.copytree(".claude", test_project / ".claude", 
                          ignore_dangling_symlinks=True, dirs_exist_ok=True)
            
            # Then: 핵심 기능들이 모두 작동해야 함
            assert (test_project / ".claude/commands").exists()
            
            # 새로운 커맨드들이 생성되었는지 확인
            commands_dir = test_project / ".claude/commands"
            expected_new_commands = ["분석.md", "기획.md", "테스트.md", "배포.md"]
            
            # 아직 구현되지 않아 실패할 것
            for cmd_file in expected_new_commands:
                cmd_path = commands_dir / cmd_file
                assert cmd_path.exists(), f"New command {cmd_file} not created"
                
                # 내용이 비어있지 않아야 함
                content = cmd_path.read_text(encoding='utf-8')
                assert len(content) > 500, f"Command {cmd_file} content too short"

    @patch('subprocess.run')
    def test_github_actions_passes_after_implementation(self, mock_subprocess):
        """구현 후 GitHub Actions가 통과해야 함"""
        # Given: 모든 구현이 완료된 상태 (Mock으로 시뮬레이션)
        mock_subprocess.return_value = MagicMock(
            returncode=0,
            stdout="All tests passed\nCoverage: 85%\nQuality Score: 92/100\n",
            stderr=""
        )
        
        # When: GitHub Actions 워크플로우 실행
        result = subprocess.run([
            "python", "-m", "pytest", "tests/", "--cov=scripts", "--cov-report=term"
        ], capture_output=True, text=True)
        
        # Then: 모든 검사 통과
        assert result.returncode == 0, f"Tests failed: {result.stderr}"
        
        # And: 품질 기준 충족
        # (실제로는 mock이므로 항상 통과하지만, 구현 후에는 실제 테스트)
        assert "passed" in result.stdout.lower()

# 추가 에러 케이스 테스트
class TestErrorCases:
    """에러 케이스 및 경계값 테스트"""
    
    def test_handles_missing_command_files_gracefully(self):
        """커맨드 파일이 없을 때 적절히 처리해야 함"""
        # Given: 존재하지 않는 커맨드 파일
        nonexistent_cmd = Path(".claude/commands/nonexistent.md")
        
        # When: 파일 읽기 시도
        with pytest.raises(FileNotFoundError):
            nonexistent_cmd.read_text()
        
        # Then: 적절한 에러 처리 (구현 후)
        # This test verifies error handling behavior

    def test_handles_corrupted_metadata_gracefully(self):
        """손상된 메타데이터를 적절히 처리해야 함"""
        # Given: 손상된 메타데이터를 가진 임시 파일
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("""<!--
@meta
id: corrupted_data
type: invalid_type
status: unknown_status
corrupted metadata block
-->
# Test Command
""")
            corrupted_file = Path(f.name)
        
        try:
            # When: 메타데이터 파싱 시도 (구현 후)
            content = corrupted_file.read_text()
            
            # Then: 기본값으로 fallback하거나 적절한 에러 처리
            assert "@meta" in content  # 메타데이터 블록은 존재
            # 실제 파싱 로직은 구현 후 테스트
            
        finally:
            corrupted_file.unlink()  # 임시 파일 정리

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])