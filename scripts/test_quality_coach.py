#!/usr/bin/env python3
"""
테스트 품질 코치 시스템
실시간 피드백과 구체적 개선 제안 제공
"""

import ast
from pathlib import Path
from typing import Dict, List
from intent_matching_validator import IntentMatchingValidator

class TestQualityCoach:
    """테스트 품질 실시간 코치"""
    
    def __init__(self):
        self.intent_validator = IntentMatchingValidator()
        
        self.improvement_templates = {
            'theater_testing': {
                'pattern': r'assert.*is not None',
                'message': '❌ Theater Testing 감지',
                'suggestion': 'assert result.{specific_field} == {expected_value}',
                'example': '''
# 현재 (Theater Testing)
assert result  # Theater Testing 예시 (실제로는 사용하지 마세요)

# 개선안 (Real Testing)  
assert result.status == "success"
assert result.user_id == 123
assert len(result.items) == 5
                '''
            },
            'missing_error_cases': {
                'pattern': 'no_exception_handling',
                'message': '⚠️ 에러 케이스 누락',
                'suggestion': 'with pytest.raises({ExpectedError}):',
                'example': '''
# 추가 권장
with pytest.raises(ValidationError):
    login_user({"username": "", "password": "test"})

with pytest.raises(AuthenticationError):
    login_user({"username": "user", "password": "wrong"})
                '''
            },
            'vague_assertions': {
                'pattern': r'assert.*in.*',
                'message': '🎯 더 구체적 검증 권장',
                'suggestion': 'assert {actual} == {specific_expected}',
                'example': '''
# 현재 (모호함)
assert "success" in response.text

# 개선안 (구체적)
assert response.json()["status"] == "success"
assert response.json()["message"] == "Login successful"
                '''
            }
        }
    
    def analyze_and_coach(self, filepath: Path) -> Dict:
        """파일 분석 및 코칭 제공"""
        analysis = self.intent_validator.validate_file(filepath)
        
        if 'error' in analysis:
            return analysis
        
        coaching_report = {
            'file': str(filepath),
            'overall_grade': analysis['summary']['grade'],
            'overall_score': analysis['summary']['score'],
            'coaching_sessions': []
        }
        
        for test in analysis['tests']:
            session = self._generate_coaching_session(test)
            if session['improvements']:  # 개선사항이 있는 경우만
                coaching_report['coaching_sessions'].append(session)
        
        return coaching_report
    
    def _generate_coaching_session(self, test_analysis: Dict) -> Dict:
        """개별 테스트 코칭 세션"""
        test_name = test_analysis['name']
        score = test_analysis['matching_score']
        
        session = {
            'test_name': test_name,
            'current_score': round(score * 100),
            'target_score': min(100, round(score * 100) + 20),
            'improvements': [],
            'priority': self._calculate_priority(score)
        }
        
        # 구체적 개선사항 식별
        improvements = self._identify_improvements(test_analysis)
        session['improvements'] = improvements
        
        return session
    
    def _identify_improvements(self, test_analysis: Dict) -> List[Dict]:
        """구체적 개선사항 식별"""
        improvements = []
        assertions = test_analysis['assertions']
        
        # 1. Theater Testing 감지
        theater_assertions = [
            a for a in assertions 
            if 'is not none' in a['text'].lower()
        ]
        
        if theater_assertions:
            improvements.append({
                'type': 'theater_testing',
                'severity': 'high',
                'message': f'{len(theater_assertions)}개 Theater Testing 패턴 발견',
                'specific_lines': [a['line'] for a in theater_assertions],
                'fix_template': self.improvement_templates['theater_testing']
            })
        
        # 2. 구체성 부족
        low_specificity = [
            a for a in assertions
            if a['specificity_score'] < 0.3
        ]
        
        if low_specificity:
            improvements.append({
                'type': 'low_specificity',
                'severity': 'medium',
                'message': f'{len(low_specificity)}개 assertion이 너무 모호함',
                'specific_lines': [a['line'] for a in low_specificity],
                'fix_template': self.improvement_templates['vague_assertions']
            })
        
        # 3. 에러 케이스 부족
        has_error_handling = any(
            'raises' in a['text'].lower() or 'exception' in a['text'].lower()
            for a in assertions
        )
        
        if not has_error_handling and test_analysis['intent']['category'] != 'error_handling':
            improvements.append({
                'type': 'missing_error_cases', 
                'severity': 'medium',
                'message': '에러 케이스 테스트 부족',
                'specific_lines': [],
                'fix_template': self.improvement_templates['missing_error_cases']
            })
        
        # 우선순위별 정렬
        improvements.sort(key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['severity']])
        
        return improvements
    
    def _calculate_priority(self, score: float) -> str:
        """개선 우선순위 계산"""
        if score < 0.3:
            return 'urgent'  # 즉시 수정 필요
        elif score < 0.6:
            return 'high'    # 높은 우선순위
        elif score < 0.8:
            return 'medium'  # 중간 우선순위
        else:
            return 'low'     # 낮은 우선순위
    
    def generate_coaching_report(self, coaching_data: Dict) -> str:
        """사람이 읽기 쉬운 코칭 리포트 생성"""
        report = []
        
        report.append("🧑‍🏫 Test Quality Coaching Report")
        report.append("=" * 50)
        
        file_name = Path(coaching_data['file']).name
        report.append(f"📄 File: {file_name}")
        report.append(f"📊 Overall: {coaching_data['overall_grade']} ({coaching_data['overall_score']}/100)")
        report.append("")
        
        if not coaching_data['coaching_sessions']:
            report.append("🎉 모든 테스트가 좋은 품질입니다!")
            return "\n".join(report)
        
        # 우선순위별 그룹화
        urgent_sessions = [s for s in coaching_data['coaching_sessions'] if s['priority'] == 'urgent']
        high_sessions = [s for s in coaching_data['coaching_sessions'] if s['priority'] == 'high']
        
        if urgent_sessions:
            report.append("🚨 긴급 개선 필요:")
            for session in urgent_sessions:
                report.extend(self._format_session(session))
                report.append("")
        
        if high_sessions:
            report.append("⚠️ 높은 우선순위:")
            for session in high_sessions:
                report.extend(self._format_session(session))
                report.append("")
        
        return "\n".join(report)
    
    def _format_session(self, session: Dict) -> List[str]:
        """개별 세션 포맷팅"""
        lines = []
        
        lines.append(f"   🎯 {session['test_name']}")
        lines.append(f"      현재: {session['current_score']}점 → 목표: {session['target_score']}점")
        
        for improvement in session['improvements']:
            lines.append(f"      • {improvement['message']}")
            
            if improvement['specific_lines']:
                lines.append(f"        라인: {', '.join(map(str, improvement['specific_lines']))}")
            
            # 개선 예시 (처음 1개만)
            if improvement == session['improvements'][0]:
                example = improvement['fix_template']['example'].strip()
                lines.append("        개선 예시:")
                for example_line in example.split('\n'):
                    if example_line.strip():
                        lines.append(f"        {example_line}")
        
        return lines

class TestQualityDashboard:
    """테스트 품질 대시보드"""
    
    def __init__(self):
        self.coach = TestQualityCoach()
    
    def run_quality_check(self, target_dir: str = ".") -> None:
        """전체 프로젝트 품질 체크 실행"""
        print("🏃‍♂️ Running comprehensive test quality check...")
        print()
        
        test_files = list(Path(target_dir).glob('**/test*.py'))
        
        if not test_files:
            print("❌ 테스트 파일을 찾을 수 없습니다.")
            return
        
        total_score = 0
        file_count = 0
        urgent_count = 0
        
        for test_file in test_files:
            coaching_data = self.coach.analyze_and_coach(test_file)
            
            if 'error' not in coaching_data:
                file_count += 1
                total_score += coaching_data['overall_score']
                
                urgent_sessions = [
                    s for s in coaching_data['coaching_sessions'] 
                    if s['priority'] == 'urgent'
                ]
                urgent_count += len(urgent_sessions)
                
                # 품질이 낮은 파일만 리포트 출력
                if coaching_data['overall_score'] < 70 or urgent_sessions:
                    report = self.coach.generate_coaching_report(coaching_data)
                    print(report)
                    print()
        
        # 전체 요약
        if file_count > 0:
            avg_score = total_score / file_count
            print("📊 전체 요약")
            print("=" * 30)
            print(f"평균 품질: {avg_score:.1f}/100")
            print(f"분석된 파일: {file_count}개")
            print(f"긴급 개선 필요: {urgent_count}개")
            
            if avg_score >= 80:
                print("🎉 전체적으로 좋은 품질입니다!")
            elif avg_score >= 60:
                print("⚠️ 일부 개선이 필요합니다.")
            else:
                print("🚨 상당한 개선이 필요합니다.")

def main():
    """메인 실행 함수"""
    dashboard = TestQualityDashboard()
    dashboard.run_quality_check()

if __name__ == '__main__':
    main()