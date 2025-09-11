#!/usr/bin/env python3
"""
Theater Testing 패턴 검사 스크립트
실제 test_ 함수 내부의 Theater Testing 패턴만 정확히 감지
"""

import ast
import sys
from pathlib import Path


class TheaterTestingDetector(ast.NodeVisitor):
    """Theater Testing 패턴 감지기"""
    
    def __init__(self):
        self.theater_patterns = []
        self.in_test_function = False
        self.current_test_name = None
    
    def visit_FunctionDef(self, node):
        if node.name.startswith('test_'):
            self.in_test_function = True
            self.current_test_name = node.name
            self.generic_visit(node)
            self.in_test_function = False
        else:
            self.generic_visit(node)
    
    def visit_Assert(self, node):
        if not self.in_test_function:
            return
            
        # assert True 패턴 검사
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            self.theater_patterns.append({
                'test': self.current_test_name,
                'line': node.lineno,
                'pattern': 'assert True',
                'issue': 'Theater Testing: assert True 패턴'
            })
        
        # assert ... is not None 패턴 검사
        elif isinstance(node.test, ast.Compare):
            # Compare 노드 구조 안전 체크
            if (hasattr(node.test, 'ops') and len(node.test.ops) == 1 and 
                isinstance(node.test.ops[0], ast.IsNot) and
                hasattr(node.test, 'comparators') and len(node.test.comparators) == 1 and
                isinstance(node.test.comparators[0], ast.Constant) and
                node.test.comparators[0].value is None):
                self.theater_patterns.append({
                    'test': self.current_test_name,
                    'line': node.lineno,
                    'pattern': 'assert ... is not None',
                    'issue': 'Theater Testing: vague None check'
                })


def check_file(file_path: Path) -> list:
    """단일 파일 Theater Testing 검사"""
    try:
        content = file_path.read_text(encoding='utf-8')
        tree = ast.parse(content)
        
        detector = TheaterTestingDetector()
        detector.visit(tree)
        
        return detector.theater_patterns
    except Exception as e:
        print(f"❌ Error analyzing {file_path}: {e}", file=sys.stderr)
        return []


def main():
    """메인 검사 함수"""
    test_files = list(Path('.').glob('**/test*.py'))
    
    if not test_files:
        print("✅ No test files found")
        return 0
    
    total_patterns = 0
    
    for test_file in test_files:
        patterns = check_file(test_file)
        
        if patterns:
            total_patterns += len(patterns)
            print(f"❌ Theater Testing patterns found in {test_file}:")
            for pattern in patterns:
                print(f"   Line {pattern['line']}: {pattern['issue']}")
    
    if total_patterns > 0:
        print(f"\n❌ Total: {total_patterns} Theater Testing patterns found")
        return 1
    else:
        print("✅ No Theater Testing patterns found")
        return 0


if __name__ == '__main__':
    sys.exit(main())