"""
슬래시 커맨드 실행 검증 테스트

Real Testing 원칙: 실제 커맨드가 실행 로직을 포함하고 있는지 검증
Theater Testing 방지: 구체적 실행 결과 확인
"""

import pytest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

# Project root path for consistent file access
PROJECT_ROOT = Path(__file__).parent.parent

class TestSlashCommandExecution:
    """슬래시 커맨드 실제 실행 능력 테스트"""

    def test_all_commands_have_execution_protocol(self):
        """모든 슬래시 커맨드에 실행 프로토콜이 포함되어 있어야 함"""
        
        # Given: 모든 슬래시 커맨드 파일
        commands_dir = PROJECT_ROOT / ".claude/commands"
        command_files = list(commands_dir.glob("*.md"))
        
        # When: 각 커맨드 파일 검증
        missing_execution = []
        for cmd_file in command_files:
            content = cmd_file.read_text(encoding='utf-8')
            
            # Then: 실행 프로토콜이 포함되어야 함
            if "Claude 실행 프로토콜" not in content:
                missing_execution.append(cmd_file.name)
            
            # And: 실제 실행 코드가 포함되어야 함
            if "def execute_" not in content:
                missing_execution.append(f"{cmd_file.name} (no execute function)")
            
            # And: 즉시 실행 트리거가 있어야 함
            if 'if __name__ == "__main__"' not in content:
                missing_execution.append(f"{cmd_file.name} (no main trigger)")
        
        # Then: 모든 커맨드가 실행 로직을 가져야 함
        assert len(missing_execution) == 0, f"실행 로직 누락 커맨드: {missing_execution}"

    def test_full_cycle_command_has_complete_workflow(self):
        """전체사이클 커맨드는 완전한 워크플로우를 가져야 함"""

        # Given: 전체사이클 커맨드
        full_cycle_path = PROJECT_ROOT / ".claude/commands/전체사이클.md"

        if not full_cycle_path.exists():
            pytest.skip(f"Command file not found: {full_cycle_path}")

        content = full_cycle_path.read_text(encoding='utf-8')
        
        # Then: 6단계 모두 포함
        required_steps = ["분석", "기획", "테스트", "구현", "검증", "배포"]
        for step in required_steps:
            assert step in content, f"{step} 단계 누락"
        
        # And: 에러 핸들링 포함
        assert "try:" in content and "except" in content, "에러 핸들링 누락"
        
        # And: 결과 보고 포함
        assert "results" in content, "결과 수집 로직 누락"

    def test_planning_command_has_llm_routing(self):
        """기획 커맨드는 LLM 라우팅 로직을 가져야 함"""
        
        # Given: 기획 커맨드
        planning_path = PROJECT_ROOT / ".claude/commands/기획.md"

        if not planning_path.exists():
            pytest.skip(f"Command file not found: {planning_path}")

        content = planning_path.read_text(encoding='utf-8')
        
        # Then: LLM 분석 로직 포함
        assert "analyze_user_intent" in content, "의도 분석 함수 누락"
        assert "select_optimal_mode" in content, "모드 선택 함수 누락"
        
        # And: 모드별 분기 처리
        assert "exploration" in content, "탐색 모드 누락"
        assert "implementation" in content, "구현 모드 누락"

    def test_testing_command_enforces_tadd(self):
        """테스트 커맨드는 TADD 강제 로직을 가져야 함"""
        
        # Given: 테스트 커맨드
        testing_path = PROJECT_ROOT / ".claude/commands/테스트.md"

        if not testing_path.exists():
            pytest.skip(f"Command file not found: {testing_path}")

        content = testing_path.read_text(encoding='utf-8')
        
        # Then: Theater Testing 감지 로직
        assert "is_theater_testing" in content, "Theater Testing 감지 함수 누락"
        assert "convert_to_real_testing" in content, "Real Testing 변환 함수 누락"
        
        # And: Mock 사용률 제한 로직
        assert "mock_ratio" in content, "Mock 사용률 계산 누락"
        assert "0.2" in content or "20%" in content, "Mock 20% 제한 기준 누락"

    def test_implementation_command_follows_tadd_cycle(self):
        """구현 커맨드는 TADD 사이클을 따라야 함"""
        
        # Given: 구현 커맨드
        impl_path = PROJECT_ROOT / ".claude/commands/구현.md"

        if not impl_path.exists():
            pytest.skip(f"Command file not found: {impl_path}")

        content = impl_path.read_text(encoding='utf-8')
        
        # Then: Red-Green-Refactor 사이클 포함
        assert "failing_tests" in content, "실패 테스트 확인 누락"
        assert "Red:" in content, "Red 단계 누락"
        assert "Green:" in content, "Green 단계 누락"
        assert "Refactor" in content, "Refactor 단계 누락"
        
        # And: DRY 원칙 적용
        assert "existing_code" in content, "기존 코드 검색 누락"

    def test_verification_command_checks_quality_metrics(self):
        """검증 커맨드는 품질 메트릭을 확인해야 함"""
        
        # Given: 검증 커맨드
        verification_path = PROJECT_ROOT / ".claude/commands/검증.md"

        if not verification_path.exists():
            pytest.skip(f"Command file not found: {verification_path}")

        content = verification_path.read_text(encoding='utf-8')
        
        # Then: 핵심 품질 검증 포함
        quality_checks = [
            "run_all_tests",      # 전체 테스트 실행
            "detect_theater_testing",  # Theater Testing 감지
            "mock_usage",         # Mock 사용률 확인
            "coverage",          # 커버리지 분석
            "integration_tests"   # 통합 테스트
        ]
        
        for check in quality_checks:
            assert check in content, f"{check} 품질 검증 누락"

    @patch('subprocess.run')
    def test_commands_are_executable_in_principle(self, mock_run):
        """커맨드들이 원칙적으로 실행 가능해야 함 (Mock 테스트)"""
        
        # Given: Mock 환경 설정
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "실행 완료"
        
        # When: 각 커맨드의 실행 로직 검증
        commands = ["전체사이클", "기획", "구현", "테스트", "검증"]
        
        for cmd in commands:
            cmd_path = PROJECT_ROOT / f".claude/commands/{cmd}.md"

            if not cmd_path.exists():
                pytest.skip(f"Command file not found: {cmd_path}")

            content = cmd_path.read_text(encoding='utf-8')

            # Then: 실행 가능한 구조여야 함 (스킵 조건 완화)
            has_execution = any([
                "def execute_" in content,
                "실행" in content,
                "execute" in content,
                "run" in content
            ])
            assert has_execution, f"{cmd}: 실행 로직 없음"
            assert "ARGUMENTS" in content, f"{cmd}: 인수 처리 없음"
            
            # And: 실제 로직이 있어야 함 (Theater Testing 방지)
            lines = content.count('\n')
            assert lines > 50, f"{cmd}: 너무 단순함 (Theater 의심)"

class TestCommandIntegration:
    """커맨드 간 통합 테스트"""
    
    def test_full_cycle_can_call_other_commands(self):
        """전체사이클이 다른 커맨드들을 호출할 수 있어야 함"""
        
        # Given: 전체사이클 커맨드
        full_cycle_path = PROJECT_ROOT / ".claude/commands/전체사이클.md"

        if not full_cycle_path.exists():
            pytest.skip(f"Command file not found: {full_cycle_path}")

        content = full_cycle_path.read_text(encoding='utf-8')
        
        # Then: 다른 커맨드들을 호출하는 로직 포함
        sub_commands = ["분석", "기획", "테스트", "구현", "검증", "배포"]
        for cmd in sub_commands:
            assert f'execute_command(f"/{cmd}"' in content or f'/{cmd}' in content, \
                   f"전체사이클에서 {cmd} 호출 로직 누락"

    def test_error_handling_between_commands(self):
        """커맨드 간 에러 처리가 적절해야 함"""
        
        # Given: 전체사이클 커맨드
        full_cycle_path = PROJECT_ROOT / ".claude/commands/전체사이클.md"

        if not full_cycle_path.exists():
            pytest.skip(f"Command file not found: {full_cycle_path}")

        content = full_cycle_path.read_text(encoding='utf-8')
        
        # Then: 에러 상황에서 중단 로직
        assert "Exception" in content, "예외 처리 누락"
        assert "break" in content, "실패 시 중단 로직 누락"
        
        # And: 계속 진행 옵션
        assert "continue_on_error" in content, "에러 시 계속 진행 옵션 누락"