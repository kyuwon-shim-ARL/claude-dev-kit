#!/usr/bin/env python3
"""
Real Testing Quality Validator
Theater Testing을 감지하고 진짜 테스트 품질을 검증
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class TestQualityAnalyzer(ast.NodeVisitor):
    """테스트 품질을 AST 분석으로 검증"""
    
    def __init__(self):
        self.tests = []
        self.current_test = None
        self.theater_patterns = []
        self.quality_issues = []
        
    def visit_FunctionDef(self, node):
        """테스트 함수 분석"""
        if node.name.startswith('test_'):
            self.current_test = {
                'name': node.name,
                'assertions': [],
                'mocks': [],
                'has_error_case': False,
                'has_specific_values': False,
                'line': node.lineno
            }
            self.tests.append(self.current_test)
            self.generic_visit(node)
            self.current_test = None
    
    def visit_Assert(self, node):
        """Assertion 품질 분석"""
        if not self.current_test:
            return
            
        assertion_str = ast.unparse(node.test) if hasattr(ast, 'unparse') else str(node.test)
        self.current_test['assertions'].append(assertion_str)
        
        # Theater Testing 패턴 감지
        if self._is_theater_assertion(node.test):
            self.theater_patterns.append({
                'test': self.current_test['name'],
                'pattern': assertion_str,
                'line': node.lineno,
                'issue': 'Theater Testing: 너무 느슨한 검증'
            })
        
        # 구체적 값 검증 확인
        if self._has_specific_value(node.test):
            self.current_test['has_specific_values'] = True
            
        self.generic_visit(node)
    
    def visit_With(self, node):
        """에러 케이스 검증 확인"""
        if not self.current_test:
            return
            
        # pytest.raises 패턴 확인
        for item in node.items:
            if self._is_error_handling(item.context_expr):
                self.current_test['has_error_case'] = True
                
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Mock 사용 감지"""
        if not self.current_test:
            return
            
        func_name = self._get_call_name(node)
        if func_name and 'mock' in func_name.lower():
            self.current_test['mocks'].append(func_name)
            
        self.generic_visit(node)
    
    def _is_theater_assertion(self, node) -> bool:
        """Theater Testing 패턴인지 확인"""
        # assert result is not None
        if isinstance(node, ast.Compare):
            if len(node.ops) == 1 and isinstance(node.ops[0], (ast.IsNot, ast.NotEq)):
                if len(node.comparators) == 1:
                    comp = node.comparators[0]
                    if isinstance(comp, ast.Constant) and comp.value is None:
                        return True
        
        # assert len(x) > 0
        if isinstance(node, ast.Compare):
            if isinstance(node.left, ast.Call):
                func = node.left.func
                if isinstance(func, ast.Name) and func.id == 'len':
                    if isinstance(node.ops[0], ast.Gt):
                        if isinstance(node.comparators[0], ast.Constant):
                            if node.comparators[0].value == 0:
                                return True
        
        return False
    
    def _has_specific_value(self, node) -> bool:
        """구체적 값을 검증하는지 확인"""
        if isinstance(node, ast.Compare):
            # == 연산자로 구체적 값 비교
            if any(isinstance(op, ast.Eq) for op in node.ops):
                # None이 아닌 구체적 값과 비교
                for comp in node.comparators:
                    if isinstance(comp, ast.Constant) and comp.value is not None:
                        return True
                    if isinstance(comp, (ast.Str, ast.Num)):
                        return True
        return False
    
    def _is_error_handling(self, node) -> bool:
        """에러 처리 테스트인지 확인"""
        if isinstance(node, ast.Call):
            func_name = self._get_call_name(node)
            return func_name and 'raises' in func_name
        return False
    
    def _get_call_name(self, node) -> str:
        """함수 호출 이름 추출"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""

def analyze_test_file(filepath: Path) -> Dict:
    """단일 테스트 파일 분석"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
        analyzer = TestQualityAnalyzer()
        analyzer.visit(tree)
        
        # 품질 메트릭 계산
        total_tests = len(analyzer.tests)
        tests_with_specific_values = sum(1 for t in analyzer.tests if t['has_specific_values'])
        tests_with_error_cases = sum(1 for t in analyzer.tests if t['has_error_case'])
        total_mocks = sum(len(t['mocks']) for t in analyzer.tests)
        total_assertions = sum(len(t['assertions']) for t in analyzer.tests)
        
        mock_usage_rate = (total_mocks / total_assertions * 100) if total_assertions > 0 else 0
        
        return {
            'file': str(filepath),
            'total_tests': total_tests,
            'theater_patterns': analyzer.theater_patterns,
            'tests_with_specific_values': tests_with_specific_values,
            'tests_with_error_cases': tests_with_error_cases,
            'mock_usage_rate': mock_usage_rate,
            'quality_score': calculate_quality_score(analyzer)
        }
    except SyntaxError as e:
        print(f"⚠️  Syntax error in {filepath}: {e}")
        return None

def calculate_quality_score(analyzer) -> float:
    """품질 점수 계산 (0-100)"""
    if not analyzer.tests:
        return 0.0
    
    score = 0.0
    total_tests = len(analyzer.tests)
    
    # 구체적 값 검증 (40점)
    specific_ratio = sum(1 for t in analyzer.tests if t['has_specific_values']) / total_tests
    score += specific_ratio * 40
    
    # 에러 케이스 포함 (30점)
    error_ratio = sum(1 for t in analyzer.tests if t['has_error_case']) / total_tests
    score += error_ratio * 30
    
    # Theater Testing 없음 (20점)
    theater_penalty = len(analyzer.theater_patterns) / total_tests if total_tests > 0 else 0
    score += (1 - min(theater_penalty, 1)) * 20
    
    # Mock 최소 사용 (10점)
    total_assertions = sum(len(t['assertions']) for t in analyzer.tests)
    total_mocks = sum(len(t['mocks']) for t in analyzer.tests)
    mock_ratio = total_mocks / total_assertions if total_assertions > 0 else 0
    score += (1 - min(mock_ratio / 0.2, 1)) * 10  # 20% 이하면 만점
    
    return round(score, 1)

def generate_report(results: List[Dict]) -> None:
    """품질 검증 리포트 생성"""
    print("\n" + "=" * 60)
    print("🧪 Real Testing Quality Report")
    print("=" * 60)
    
    total_files = len([r for r in results if r])
    total_tests = sum(r['total_tests'] for r in results if r)
    total_theater = sum(len(r['theater_patterns']) for r in results if r)
    avg_quality = sum(r['quality_score'] for r in results if r) / total_files if total_files > 0 else 0
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Files analyzed: {total_files}")
    print(f"  Total tests: {total_tests}")
    print(f"  Average quality score: {avg_quality:.1f}/100")
    
    if total_theater > 0:
        print(f"\n🎭 Theater Testing Detected: {total_theater} patterns")
        for result in results:
            if result and result['theater_patterns']:
                print(f"\n  {result['file']}:")
                for pattern in result['theater_patterns'][:3]:  # 최대 3개만
                    print(f"    ❌ Line {pattern['line']}: {pattern['pattern']}")
                    print(f"       Issue: {pattern['issue']}")
    
    # 품질 기준 체크
    print(f"\n✅ Quality Gates:")
    mock_rates = [r['mock_usage_rate'] for r in results if r]
    avg_mock_rate = sum(mock_rates) / len(mock_rates) if mock_rates else 0
    
    print(f"  Mock usage: {avg_mock_rate:.1f}% {'✅' if avg_mock_rate < 20 else '❌'} (limit: 20%)")
    print(f"  Theater Testing: {total_theater} {'✅' if total_theater == 0 else '❌'} (should be 0)")
    print(f"  Quality Score: {avg_quality:.1f} {'✅' if avg_quality >= 70 else '❌'} (minimum: 70)")
    
    # 개선 제안
    if avg_quality < 70:
        print("\n💡 Recommendations:")
        if total_theater > 0:
            print("  1. Replace 'assert x is not None' with specific value checks")
        if avg_mock_rate > 20:
            print("  2. Reduce mock usage, use real implementations")
        print("  3. Add error case testing with pytest.raises()")
        print("  4. Use concrete assertions instead of existence checks")
    
    # 최종 판정
    if avg_quality >= 70 and avg_mock_rate < 20 and total_theater == 0:
        print("\n✅ Test Quality: PASSED")
        return 0
    else:
        print("\n❌ Test Quality: FAILED")
        return 1

def main():
    """메인 실행 함수"""
    print("🔍 Real Testing Quality Validation Starting...")
    print("-" * 60)
    
    # 테스트 파일 찾기
    test_files = []
    for pattern in ["**/test_*.py", "**/*_test.py"]:
        test_files.extend(Path(".").glob(pattern))
    
    if not test_files:
        print("⚠️  No test files found")
        return 0
    
    print(f"Found {len(test_files)} test files to analyze")
    
    # 각 파일 분석
    results = []
    for test_file in test_files:
        result = analyze_test_file(test_file)
        if result:
            results.append(result)
            quality_emoji = "✅" if result['quality_score'] >= 70 else "⚠️"
            print(f"  {quality_emoji} {test_file.name}: Quality {result['quality_score']:.1f}/100")
    
    # 리포트 생성
    return generate_report(results)

if __name__ == "__main__":
    sys.exit(main())