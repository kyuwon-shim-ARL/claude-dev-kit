#!/usr/bin/env python3
"""
의도 매칭 검증 시스템
테스트가 실제 의도(User Story)에 부합하는지 검증
"""

import ast
import re
from typing import Dict, List, Tuple
from pathlib import Path

class IntentMatcher:
    """의도와 테스트 매칭 분석기"""
    
    def __init__(self):
        self.intent_patterns = {
            'user_action': [
                'user can', '사용자가', '사용자는', 'when user', 'given user'
            ],
            'system_behavior': [
                'system should', '시스템이', '시스템은', 'should return', 'should display'  
            ],
            'error_handling': [
                'when invalid', '잘못된', '오류가', 'should fail', 'should reject'
            ],
            'edge_cases': [
                'boundary', '경계', '극한', 'edge case', 'limit'
            ]
        }
    
    def extract_intent_from_test_name(self, test_name: str) -> Dict:
        """테스트 이름에서 의도 추출"""
        intent = {
            'action': None,
            'subject': None,
            'expected_outcome': None,
            'category': 'unknown'
        }
        
        # Given-When-Then 패턴 감지
        if 'given' in test_name.lower():
            parts = re.split(r'given|when|then', test_name.lower())
            if len(parts) >= 3:
                intent['action'] = parts[1].strip()
                intent['expected_outcome'] = parts[2].strip()
        
        # 사용자 액션 패턴 감지
        for pattern in self.intent_patterns['user_action']:
            if pattern in test_name.lower():
                intent['category'] = 'user_action'
                break
        
        # 에러 처리 패턴 감지  
        for pattern in self.intent_patterns['error_handling']:
            if pattern in test_name.lower():
                intent['category'] = 'error_handling'
                break
                
        return intent
    
    def analyze_test_assertions(self, test_node: ast.FunctionDef) -> List[Dict]:
        """테스트의 assertion 분석"""
        assertions = []
        
        for node in ast.walk(test_node):
            if isinstance(node, ast.Assert):
                assertion_text = ast.unparse(node.test) if hasattr(ast, 'unparse') else str(node.test)
                
                assertion_info = {
                    'text': assertion_text,
                    'type': self._categorize_assertion(assertion_text),
                    'specificity_score': self._calculate_specificity(assertion_text),
                    'line': node.lineno
                }
                assertions.append(assertion_info)
        
        return assertions
    
    def _categorize_assertion(self, assertion_text: str) -> str:
        """Assertion 유형 분류"""
        assertion_lower = assertion_text.lower()
        
        if 'status_code' in assertion_lower or 'response' in assertion_lower:
            return 'api_response'
        elif 'len(' in assertion_lower or 'count' in assertion_lower:
            return 'quantity_check'
        elif 'is not none' in assertion_lower:
            return 'existence_check'
        elif '==' in assertion_lower and any(char.isdigit() for char in assertion_text):
            return 'specific_value'
        elif 'in' in assertion_lower:
            return 'content_check'
        else:
            return 'other'
    
    def _calculate_specificity(self, assertion_text: str) -> float:
        """Assertion의 구체성 점수 (0.0-1.0)"""
        score = 0.0
        
        # 구체적 값 체크
        if re.search(r'==\s*["\'][\w\s]+["\']', assertion_text):
            score += 0.4
        elif re.search(r'==\s*\d+', assertion_text):
            score += 0.3
        
        # 범위 체크
        if any(op in assertion_text for op in ['>', '<', '>=', '<=']):
            score += 0.2
        
        # 내용 검증
        if 'in' in assertion_text and '"' in assertion_text:
            score += 0.2
        
        # 복합 조건
        if 'and' in assertion_text or 'or' in assertion_text:
            score += 0.1
            
        # Theater testing 패널티
        if 'is not none' in assertion_text.lower():
            score -= 0.5
        
        return max(0.0, min(1.0, score))

class IntentMatchingValidator:
    """의도 매칭 검증 시스템"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.matcher = IntentMatcher()
        
    def validate_file(self, filepath: Path) -> Dict:
        """단일 테스트 파일 검증"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {'error': 'Syntax error'}
        
        results = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                test_analysis = self._analyze_single_test(node)
                results.append(test_analysis)
        
        return {
            'file': str(filepath),
            'tests': results,
            'summary': self._calculate_file_summary(results)
        }
    
    def _analyze_single_test(self, test_node: ast.FunctionDef) -> Dict:
        """단일 테스트 분석"""
        test_name = test_node.name
        docstring = ast.get_docstring(test_node) or ""
        
        # 의도 추출
        intent = self.matcher.extract_intent_from_test_name(test_name)
        if docstring:
            intent['description'] = docstring
        
        # Assertion 분석
        assertions = self.matcher.analyze_test_assertions(test_node)
        
        # 의도-구현 매칭 점수 계산
        matching_score = self._calculate_matching_score(intent, assertions)
        
        return {
            'name': test_name,
            'intent': intent,
            'assertions': assertions,
            'matching_score': matching_score,
            'recommendations': self._generate_recommendations(intent, assertions)
        }
    
    def _calculate_matching_score(self, intent: Dict, assertions: List[Dict]) -> float:
        """의도-구현 매칭 점수 (0.0-1.0)"""
        if not assertions:
            return 0.0
        
        score = 0.0
        
        # 기본 점수: assertion 구체성 평균
        specificity_avg = sum(a['specificity_score'] for a in assertions) / len(assertions)
        score += specificity_avg * 0.4
        
        # 의도 카테고리별 가점
        if intent['category'] == 'user_action':
            # 사용자 액션은 결과 검증이 중요
            result_assertions = [a for a in assertions if a['type'] in ['api_response', 'specific_value']]
            score += (len(result_assertions) / len(assertions)) * 0.3
        
        elif intent['category'] == 'error_handling':
            # 에러 처리는 예외 검증이 중요
            error_indicators = any('raise' in str(a) or 'exception' in str(a).lower() for a in assertions)
            score += 0.3 if error_indicators else 0.0
        
        # 테스트 이름과 assertion 일관성
        consistency_score = self._check_name_assertion_consistency(intent, assertions)
        score += consistency_score * 0.3
        
        return min(1.0, score)
    
    def _check_name_assertion_consistency(self, intent: Dict, assertions: List[Dict]) -> float:
        """테스트 이름과 assertion의 일관성 체크"""
        # 간단한 키워드 매칭으로 일관성 점수 계산
        # 실제로는 더 정교한 NLP 분석 필요
        return 0.7  # 임시값
    
    def _generate_recommendations(self, intent: Dict, assertions: List[Dict]) -> List[str]:
        """개선 권장사항 생성"""
        recommendations = []
        
        # 구체성 부족
        low_specificity = [a for a in assertions if a['specificity_score'] < 0.3]
        if low_specificity:
            recommendations.append(
                f"구체적 값 검증 부족: {len(low_specificity)}개 assertion을 더 구체적으로 만들어주세요"
            )
        
        # 에러 케이스 부족
        if intent['category'] != 'error_handling' and not any('exception' in str(a).lower() for a in assertions):
            recommendations.append("에러 케이스 테스트 추가를 고려해보세요")
        
        # Theater testing 감지
        theater_assertions = [a for a in assertions if 'is not none' in a['text'].lower()]
        if theater_assertions:
            recommendations.append(
                f"Theater testing 감지: {len(theater_assertions)}개 assertion을 구체적 값 검증으로 변경"
            )
        
        return recommendations
    
    def _calculate_file_summary(self, test_results: List[Dict]) -> Dict:
        """파일 전체 요약"""
        if not test_results:
            return {'score': 0.0, 'grade': 'F'}
        
        avg_score = sum(t['matching_score'] for t in test_results) / len(test_results)
        
        grade = 'A' if avg_score >= 0.8 else 'B' if avg_score >= 0.6 else 'C' if avg_score >= 0.4 else 'D' if avg_score >= 0.2 else 'F'
        
        return {
            'score': round(avg_score, 2),
            'grade': grade,
            'total_tests': len(test_results),
            'high_quality_tests': len([t for t in test_results if t['matching_score'] >= 0.7])
        }

def main():
    """메인 실행"""
    validator = IntentMatchingValidator()
    
    # 모든 테스트 파일 검증
    test_files = list(Path('.').glob('**/test*.py'))
    
    print("🎯 Intent Matching Validation Report")
    print("=" * 50)
    
    for test_file in test_files[:5]:  # 처음 5개 파일만
        result = validator.validate_file(test_file)
        
        if 'error' not in result:
            summary = result['summary']
            print(f"\n📄 {test_file}")
            print(f"   Grade: {summary['grade']} (Score: {summary['score']})")
            print(f"   Tests: {summary['total_tests']} total, {summary['high_quality_tests']} high-quality")
            
            # 낮은 점수 테스트 개선 제안
            low_score_tests = [t for t in result['tests'] if t['matching_score'] < 0.5]
            if low_score_tests:
                print(f"   ⚠️ {len(low_score_tests)} tests need improvement:")
                for test in low_score_tests[:2]:
                    print(f"      - {test['name']}: {test['recommendations'][0] if test['recommendations'] else 'No specific recommendations'}")

if __name__ == '__main__':
    main()