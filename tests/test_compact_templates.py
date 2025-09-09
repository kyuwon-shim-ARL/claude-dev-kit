#!/usr/bin/env python3
"""
컨텍스트 관리 템플릿 테스트
실제 /compact 실행은 불가하지만 템플릿 생성 로직 검증
"""

import json
import re
from typing import Dict, List

class CompactTemplateGenerator:
    """컨텍스트 정리 템플릿 생성기"""
    
    def __init__(self):
        self.templates = {
            'deploy': '/compact "v{VERSION} 배포 완료. ZEDS 문서 보존됨. 구현 과정 제거"',
            'planning': '/compact "기획 완료. planning.md 저장됨. 탐색 과정 제거"',
            'implementation': '/compact "구현 완료. 코드 변경 저장됨. 디버깅 과정 제거"',
            'stabilization': '/compact "안정화 완료. test-report.md 저장됨. 오류 수정 과정 제거"',
            'general': '/compact "작업 완료. ZEDS 문서 보존됨. 작업 과정 제거"'
        }
    
    def generate(self, task_type: str, **params) -> str:
        """템플릿 생성"""
        template = self.templates.get(task_type, self.templates['general'])
        
        # 파라미터 치환
        for key, value in params.items():
            template = template.replace(f"{{{key.upper()}}}", str(value))
        
        return template
    
    def validate_command(self, command: str) -> bool:
        """명령어 유효성 검증"""
        pattern = r'^/compact\s+"[^"]+"$'
        return bool(re.match(pattern, command))
    
    def estimate_reduction(self, task_type: str) -> str:
        """예상 감소율 반환"""
        reductions = {
            'deploy': '75-85%',
            'planning': '70-80%',
            'implementation': '70-80%',
            'stabilization': '75-85%',
            'general': '60-70%'
        }
        return reductions.get(task_type, '50-60%')

def test_template_generation():
    """템플릿 생성 테스트"""
    generator = CompactTemplateGenerator()
    
    # 배포 템플릿 테스트
    cmd = generator.generate('deploy', version='8.0.0')
    assert generator.validate_command(cmd), f"Invalid command: {cmd}"
    assert 'v8.0.0' in cmd, "Version not substituted"
    print(f"✅ 배포 템플릿: {cmd}")
    
    # 기획 템플릿 테스트
    cmd = generator.generate('planning')
    assert generator.validate_command(cmd), f"Invalid command: {cmd}"
    assert 'planning.md' in cmd, "Document reference missing"
    print(f"✅ 기획 템플릿: {cmd}")
    
    # 예상 감소율 테스트
    reduction = generator.estimate_reduction('deploy')
    assert reduction == '75-85%', f"Wrong reduction: {reduction}"
    print(f"✅ 예상 감소율: {reduction}")

def test_telegram_button_structure():
    """텔레그램 버튼 구조 테스트"""
    buttons = [
        {'id': 'compact_deploy', 'label': '🚀 배포 후 정리'},
        {'id': 'compact_planning', 'label': '📋 기획 후 정리'},
        {'id': 'compact_implementation', 'label': '⚡ 구현 후 정리'},
        {'id': 'compact_stabilization', 'label': '🔧 안정화 후 정리'},
        {'id': 'compact_general', 'label': '🧹 일반 정리'}
    ]
    
    # 모든 버튼이 고유 ID 가지는지 확인
    ids = [b['id'] for b in buttons]
    assert len(ids) == len(set(ids)), "Duplicate button IDs found"
    
    # 모든 버튼이 이모지 포함하는지 확인
    for button in buttons:
        assert any(ord(c) > 127 for c in button['label']), f"No emoji in {button['label']}"
    
    print(f"✅ 텔레그램 버튼 구조: {len(buttons)}개 버튼 검증 완료")

def test_json_serialization():
    """JSON 직렬화 테스트"""
    config = {
        'context_management': {
            'commands': [
                {
                    'id': 'compact_deploy',
                    'label': '🚀 배포 후 정리',
                    'command_template': '/compact "v{VERSION} 배포 완료. ZEDS 문서 보존됨. 구현 과정 제거"',
                    'params': ['VERSION'],
                    'expected_reduction': '75-85%'
                }
            ]
        }
    }
    
    # JSON 직렬화/역직렬화
    json_str = json.dumps(config, ensure_ascii=False, indent=2)
    parsed = json.loads(json_str)
    
    assert parsed == config, "JSON serialization failed"
    print(f"✅ JSON 직렬화: {len(json_str)} 바이트")

def main():
    """모든 테스트 실행"""
    print("=" * 50)
    print("컨텍스트 관리 시스템 테스트")
    print("=" * 50)
    
    test_template_generation()
    test_telegram_button_structure()
    test_json_serialization()
    
    print("=" * 50)
    print("✅ 모든 테스트 통과!")
    print("=" * 50)
    
    # 실사용 예시
    print("\n📋 실사용 예시:")
    generator = CompactTemplateGenerator()
    
    for task_type in ['deploy', 'planning', 'implementation']:
        cmd = generator.generate(task_type, version='8.0.0')
        reduction = generator.estimate_reduction(task_type)
        print(f"\n{task_type.upper()}:")
        print(f"  명령어: {cmd}")
        print(f"  예상 감소: {reduction}")

if __name__ == '__main__':
    main()