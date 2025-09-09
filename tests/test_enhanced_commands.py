"""
Enhanced Command System Tests
TADD 방식으로 실패하는 테스트들을 먼저 생성
"""
import pytest
from unittest.mock import Mock, patch
import os
import sys

# 테스트용 임포트
import sys
sys.path.append('src')

from enhanced_commands import (
    ImplementationCommand,
    FullCycleCommand,
    ContextAnalyzer,
    ComplexityAnalyzer,
    full_cycle
)


class TestEnhancedImplementationCommand:
    """Enhanced /구현 커맨드 테스트"""
    
    def test_context_analyzer_detects_complex_task(self):
        """복잡한 작업을 자동으로 감지할 수 있는가?"""
        # Given: 복잡한 작업 요청
        task = "/연구 커맨드 구현 - 바이오인포매틱스 워크플로우 지원"
        analyzer = ContextAnalyzer()
        
        # When: 컨텍스트 분석 실행
        result = analyzer.analyze_context_requirements(task)
        
        # Then: 복잡도가 임계값을 초과해야 함
        assert result.complexity_score > 0.7
        assert result.needs_additional_context is True
        assert result.recommended_action in ['gather_context', 'gather_extensive_context']
        assert 'existing_code_search' in result.required_steps
    
    def test_implementation_gathers_context_for_complex_tasks(self):
        """복잡한 작업에서 자동으로 컨텍스트를 수집하는가?"""
        # Given: 복잡한 구현 작업
        task = "새로운 슬래시 커맨드 시스템 구현"
        impl_cmd = ImplementationCommand()
        
        # When: 구현 실행
        result = impl_cmd.execute(task)
        
        # Then: 컨텍스트가 실제로 수집되었는지 확인
        assert result['context_gathered'] is True
        assert result['analysis'].complexity_score > 0.5
        assert result['analysis'].needs_additional_context is True
        assert 'implementation_status' in result
        assert result['implementation_status'] == 'completed'
    
    def test_implementation_runs_essential_tests(self):
        """구현 후 필수 테스트가 자동 실행되는가?"""
        # Given: 구현 작업 완료
        task = "간단한 함수 구현"
        impl_cmd = ImplementationCommand()
        
        # When: 구현 실행
        result = impl_cmd.execute(task)
        
        # Then: 테스트 결과가 실제로 포함되어야 함
        assert 'test_results' in result
        assert result['test_results']['passed'] == 5
        assert result['test_results']['failed'] == 0
        assert result['test_results']['coverage'] == 0.8
        assert result['test_results']['execution_time'] == '2.3s'
        
        # And: 에러 케이스 - 잘못된 작업에 대해서는 적절한 처리
        with pytest.raises(ValueError) as exc_info:
            impl_cmd.execute("")  # 빈 작업
        assert "empty task" in str(exc_info.value).lower()


class TestEnhancedFullCycleCommand:
    """Enhanced /전체사이클 커맨드 테스트"""
    
    def test_complexity_analyzer_categorizes_tasks(self):
        """작업 복잡도를 올바르게 분류하는가?"""
        # Given: 다양한 복잡도의 작업들
        simple_task = "버튼 색상 변경"
        medium_task = "/연구 커맨드 구현"
        complex_task = "새로운 인증 시스템 구축"
        
        analyzer = ComplexityAnalyzer()
        
        # When: 각 작업 분석
        simple_result = analyzer.analyze_complexity(simple_task)
        medium_result = analyzer.analyze_complexity(medium_task)
        complex_result = analyzer.analyze_complexity(complex_task)
        
        # Then: 올바른 복잡도 분류
        assert simple_result.level == 'simple'
        assert simple_result.recommended_approach == 'direct_implementation'
        
        assert medium_result.level == 'medium'
        assert medium_result.recommended_approach == 'selective_cycle'
        
        assert complex_result.level == 'complex'
        assert complex_result.recommended_approach == 'phased_cycle'
    
    def test_phased_cycle_separates_sessions(self):
        """복잡한 작업에서 세션을 분리하는가?"""
        # Given: 복잡한 전체사이클 작업
        task = "완전히 새로운 마이크로서비스 구축"
        full_cycle = FullCycleCommand()
        
        # When: 전체사이클 실행
        result = full_cycle.execute(task)
        
        # Then: 단계별 세션 분리가 실행되어야 함
        assert result['approach'] == 'phased_cycle'
        assert result['phase1'] == 'planning_complete'
        assert result['phase2'] == 'implementation_complete'
        assert result['phase3'] == 'deployment_complete'
        assert result['total_phases'] == 3
        assert result['session_separation'] is True
        
        # And: 복잡도 분석이 올바르게 수행됨
        assert result['complexity_analysis'].level == 'complex'
        assert result['complexity_analysis'].recommended_approach == 'phased_cycle'
    
    def test_error_recovery_mechanism(self):
        """단계 실패 시 복구 메커니즘이 작동하는가?"""
        # Given: 중간 단계에서 실패하는 시나리오
        task = "테스트 실패 시나리오"
        full_cycle = FullCycleCommand()
        
        # When: 테스트 단계에서 실패
        with patch.object(full_cycle, 'execute_step') as mock_step:
            # 테스트 단계에서 실패, 다른 단계는 성공
            mock_step.side_effect = [
                ('분석', True, 'success'),
                ('기획', True, 'success'),
                ('테스트', False, 'test_generation_failed'),
                ('구현', True, 'recovered')  # 복구 시도
            ]
            result = full_cycle.execute(task)
        
        # Then: 실패 후 복구가 시도되어야 함
        assert result['failed_step'] == '테스트'
        assert result['recovery_attempted'] is True
        assert result['final_status'] in ['recovered', 'partial_success']


class TestContextGatheringSystem:
    """컨텍스트 수집 시스템 테스트"""
    
    def test_searches_existing_similar_implementations(self):
        """기존 유사 구현을 검색하는가?"""
        # Given: 새로운 커맨드 구현 작업
        task = "/새커맨드 구현"
        context_analyzer = ContextAnalyzer()
        
        # When: 기존 코드 검색
        results = context_analyzer.gather_context(task)
        
        # Then: 유사한 구현을 실제로 찾아야 함
        assert 'similar_implementations' in results
        assert len(results['similar_implementations']) >= 1
        assert results['similar_implementations'][0]['file'] == '.claude/commands/기존커맨드.md'
        assert results['similar_implementations'][0]['similarity'] == 0.8
        assert results['similar_implementations'][1]['similarity'] == 0.6
        assert results['analysis_timestamp'] is not None
    
    def test_identifies_project_patterns(self):
        """프로젝트 패턴을 식별하는가?"""
        # Given: 프로젝트 컨텍스트 분석
        context_analyzer = ContextAnalyzer()
        
        # When: 프로젝트 패턴 분석
        with patch.object(context_analyzer, 'analyze_project_structure') as mock_analyze:
            mock_analyze.return_value = {
                'command_pattern': 'markdown_based',
                'testing_framework': 'pytest',
                'documentation_style': 'claude_md',
                'common_imports': ['pytest', 'Mock', 'os', 'sys']
            }
            patterns = context_analyzer.identify_project_patterns()
        
        # Then: 프로젝트 고유 패턴이 식별되어야 함
        assert patterns['command_pattern'] == 'markdown_based'
        assert patterns['testing_framework'] == 'pytest'
        assert 'pytest' in patterns['common_imports']


class TestErrorHandlingSystem:
    """에러 처리 시스템 테스트"""
    
    def test_handles_test_generation_failure(self):
        """테스트 생성 실패를 처리하는가?"""
        # Given: 테스트 생성이 실패하는 상황
        full_cycle = FullCycleCommand()
        
        # When: 테스트 단계에서 실패
        error_handler = full_cycle.get_error_handler()
        recovery_plan = error_handler.handle_test_failure({
            'step': 'test_generation',
            'error': 'insufficient_requirements',
            'context': 'unclear_specifications'
        })
        
        # Then: 적절한 복구 계획이 생성되어야 함
        assert recovery_plan['action'] == 'return_to_planning'
        assert recovery_plan['reason'] == 'specifications_unclear'
        assert 'gather_more_requirements' in recovery_plan['steps']
    
    def test_handles_implementation_failure(self):
        """구현 실패를 처리하는가?"""
        # Given: 구현이 실패하는 상황  
        impl_cmd = ImplementationCommand()
        
        # When: 구현 실패 처리
        with patch.object(impl_cmd, 'rollback_changes') as mock_rollback:
            recovery_result = impl_cmd.handle_implementation_failure({
                'failed_tests': ['test_complex_logic', 'test_edge_case'],
                'error_type': 'logic_error',
                'attempt_count': 2
            })
        
        # Then: 롤백 및 재시도가 이루어져야 함
        mock_rollback.assert_called_once()
        assert recovery_result['action'] == 'retry_with_simplified_approach'
        assert recovery_result['max_attempts'] == 3


class TestQualityAssurance:
    """품질 보증 시스템 테스트"""
    
    def test_detects_theater_testing(self):
        """Theater Testing을 감지하고 차단하는가?"""
        # Given: Theater Testing 패턴이 포함된 테스트 (의도적인 나쁜 예시)
        bad_test_code = '''
        def test_bad_patterns():
            # These are intentionally bad patterns for testing detection
            assert some_variable is not None  # Pattern 1: existence check
            assert len(some_list) > 0          # Pattern 2: length check  
            assert os.path.exists(file_path)   # Pattern 3: file existence
        '''
        
        quality_checker = full_cycle.get_quality_checker()
        
        # When: 품질 검사 실행
        violations = quality_checker.check_test_quality(bad_test_code)
        
        # Then: Theater Testing이 감지되어야 함
        assert len(violations) >= 3
        assert any('theater_testing' in v['type'] for v in violations)
        assert any('not_none_check' in v['pattern'] for v in violations)
        assert any('existence_only' in v['pattern'] for v in violations)
    
    def test_enforces_mock_usage_limits(self):
        """Mock 사용률 제한을 강제하는가?"""
        # Given: Mock을 과다 사용하는 테스트
        mock_heavy_test = {
            'total_assertions': 10,
            'mock_count': 8,  # 80% Mock 사용
            'real_assertions': 2
        }
        
        quality_checker = full_cycle.get_quality_checker()
        
        # When: Mock 사용률 검사
        mock_analysis = quality_checker.analyze_mock_usage(mock_heavy_test)
        
        # Then: 과다 사용이 감지되고 경고가 발생해야 함
        assert mock_analysis['usage_percentage'] > 0.2  # 20% 초과
        assert mock_analysis['violation'] is True
        assert mock_analysis['recommendation'] == 'reduce_mocks_add_real_tests'
        assert mock_analysis['suggested_real_tests'] >= 3


if __name__ == "__main__":
    # 이 테스트들은 현재 실패할 것임 (구현이 아직 없으므로)
    # TADD의 Red Phase - 먼저 실패하는 테스트를 작성
    pytest.main([__file__, "-v", "--tb=short"])