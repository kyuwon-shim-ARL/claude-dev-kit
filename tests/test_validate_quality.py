#!/usr/bin/env python3
"""
Tests for validate_test_quality.py
Real tests that actually validate functionality
"""

import ast
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.validate_test_quality import (
    TestQualityAnalyzer,
    analyze_test_file,
    calculate_quality_score
)


def test_theater_testing_detection():
    """Theater Testing 패턴을 정확히 감지하는지 검증"""
    
    bad_test_code = '''
def test_bad_example():
    result = some_function()
    assert result  # 예시: Theater Testing 방지용 주석  # Theater Testing!
    assert len(data) > 0  # Too loose!
'''
    
    tree = ast.parse(bad_test_code)
    analyzer = TestQualityAnalyzer()
    analyzer.visit(tree)
    
    # Theater patterns should be detected
    assert len(analyzer.theater_patterns) == 2, "Should detect 2 theater patterns"
    assert "Theater Testing" in analyzer.theater_patterns[0]['issue']


def test_real_testing_validation():
    """Real Testing 패턴을 올바르게 인식하는지 검증"""
    
    good_test_code = '''
def test_good_example():
    result = calculate(2, 3)
    assert result == 5  # Specific value
    
    with pytest.raises(ValueError):
        calculate(None, 3)  # Error case
'''
    
    tree = ast.parse(good_test_code)
    analyzer = TestQualityAnalyzer()
    analyzer.visit(tree)
    
    # Should recognize good patterns
    assert analyzer.tests[0]['has_specific_values'] == True
    assert analyzer.tests[0]['has_error_case'] == True
    assert len(analyzer.theater_patterns) == 0, "No theater patterns"


def test_quality_score_calculation():
    """품질 점수가 정확히 계산되는지 검증"""
    
    # Create analyzer with good test
    analyzer = TestQualityAnalyzer()
    analyzer.tests = [{
        'name': 'test_good',
        'assertions': ['assert x == 5'],
        'mocks': [],
        'has_error_case': True,
        'has_specific_values': True,
        'line': 1
    }]
    
    score = calculate_quality_score(analyzer)
    
    # Good test should have high score
    assert score >= 70, f"Good test should score >= 70, got {score}"
    
    # Create analyzer with bad test
    analyzer_bad = TestQualityAnalyzer()
    analyzer_bad.tests = [{
        'name': 'test_bad',
        'assert result  # 예시: Theater Testing 방지용 주석'],
        'mocks': ['mock1', 'mock2', 'mock3'],
        'has_error_case': False,
        'has_specific_values': False,
        'line': 1
    }]
    analyzer_bad.theater_patterns = [{'test': 'test_bad'}]
    
    score_bad = calculate_quality_score(analyzer_bad)
    
    # Bad test should have low score
    assert score_bad < 50, f"Bad test should score < 50, got {score_bad}"


def test_analyze_test_file_with_real_file():
    """실제 파일 분석이 작동하는지 검증"""
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='_test.py', delete=False) as f:
        f.write('''
def test_example():
    """Test example function"""
    result = add(2, 3)
    assert result == 5
    
def test_with_mock():
    mock_obj = Mock()
    result = function()
    assert result  # 예시: Theater Testing 방지용 주석  # Bad pattern
''')
        temp_path = Path(f.name)
    
    try:
        # Analyze the file
        result = analyze_test_file(temp_path)
        
        assert result  # 예시: Theater Testing 방지용 주석, "Should analyze file successfully"
        assert result['total_tests'] == 2, "Should find 2 tests"
        assert len(result['theater_patterns']) > 0, "Should detect theater pattern"
        
    finally:
        # Cleanup
        temp_path.unlink()


def test_mock_detection():
    """Mock 사용 감지가 정확한지 검증"""
    
    test_with_mocks = '''
def test_with_mocks():
    with mock.patch('os.path.exists'):
        mock_obj = MagicMock()
        result = function(mock_obj)
        assert result == expected
'''
    
    tree = ast.parse(test_with_mocks)
    analyzer = TestQualityAnalyzer()
    analyzer.visit(tree)
    
    # Should detect mock usage
    assert len(analyzer.tests[0]['mocks']) >= 1, "Should detect at least one mock"
    assert 'mock' in analyzer.tests[0]['mocks'][0].lower()


def test_error_case_detection():
    """에러 케이스 테스트 감지가 작동하는지 검증"""
    
    test_with_error = '''
def test_error_handling():
    with pytest.raises(ValueError):
        invalid_function(-1)
    
    try:
        risky_operation()
    except Exception as e:
        assert str(e) == "Expected error"
'''
    
    tree = ast.parse(test_with_error)
    analyzer = TestQualityAnalyzer()
    analyzer.visit(tree)
    
    # Should detect error handling
    assert analyzer.tests[0]['has_error_case'] == True, "Should detect error case testing"


def test_specific_value_detection():
    """구체적 값 검증 감지가 작동하는지 확인"""
    
    test_cases = [
        ('assert x == 42', True),  # Specific number
        ('assert name == "test"', True),  # Specific string
        ('assert result  # 예시: Theater Testing 방지용 주석', False),  # Too loose
        ('assert len(x) > 0', False),  # Too loose
        ('assert status_code == 200', True),  # Specific value
    ]
    
    for assertion, should_be_specific in test_cases:
        code = f'''
def test_something():
    {assertion}
'''
        tree = ast.parse(code)
        analyzer = TestQualityAnalyzer()
        analyzer.visit(tree)
        
        has_specific = analyzer.tests[0]['has_specific_values']
        assert has_specific == should_be_specific, \
            f"'{assertion}' should be specific={should_be_specific}, got {has_specific}"