"""
Real Testing Template - Theater Testing 방지 예시
이 파일을 참고하여 진짜 테스트를 작성하세요.
"""

import subprocess
import tempfile
from pathlib import Path
import pytest
import json
from typing import Dict, List

# ❌ BAD: Theater Testing 패턴 (절대 사용 금지)
class BadTheaterTesting:
    """이런 테스트는 작성하지 마세요!"""
    
    def test_bad_existence_only(self):
        """나쁜 예: 존재 여부만 확인"""
        result = some_function()
        assert result  # 예시: Theater Testing 방지용 주석  # ❌ 너무 느슨함
        
    def test_bad_length_check(self):
        """나쁜 예: 길이만 확인"""
        data = get_data()
        assert len(data) > 0  # ❌ 구체적이지 않음
        
    def test_bad_mock_everything(self):
        """나쁜 예: 모든 것을 Mock"""
        with mock.patch('everything') as mock_all:
            mock_all.return_value = "success"
            result = function()
            assert result == "success"  # ❌ Mock만 테스트함
            
    def test_bad_no_error_case(self):
        """나쁜 예: Happy Path만 테스트"""
        result = process_data("valid")
        assert result == expected  # ❌ 에러 케이스 없음


# ✅ GOOD: Real Testing 패턴 (이렇게 작성하세요)
class GoodRealTesting:
    """진짜 테스트 작성 예시"""
    
    def test_korean_command_installation(self):
        """
        User Story: 사용자가 init.sh를 실행하면 한글 명령어를 사용할 수 있다
        """
        # Given: 깨끗한 환경 준비 (실제 파일시스템 사용)
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir) / "test_project"
            
            # When: 실제 명령 실행
            result = subprocess.run(
                ['bash', 'init.sh', 'test_project', 'Test Project'],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Then: 구체적 값 검증 (not just existence)
            assert result.returncode == 0, f"Init failed: {result.stderr}"
            
            # 한글 명령어 파일 검증
            korean_commands = ['기획', '구현', '안정화', '배포']
            for cmd in korean_commands:
                cmd_path = project_path / '.claude' / 'commands' / f'{cmd}.md'
                
                # 파일 존재 + 크기 + 내용 검증
                assert cmd_path.exists(), f"Missing: {cmd}.md"
                
                file_size = cmd_path.stat().st_size
                assert file_size > 1000, f"Too small: {cmd}.md ({file_size} bytes)"
                
                content = cmd_path.read_text()
                assert '404' not in content, f"Error content in {cmd}.md"
                assert '400 Bad Request' not in content, f"Error content in {cmd}.md"
                
                # 실제 명령어 내용 검증
                if cmd == '기획':
                    assert '탐색 단계' in content, "Missing planning content"
                    assert '계획 단계' in content, "Missing planning content"
    
    def test_network_error_fallback(self):
        """
        Error Case: 네트워크 오류 시 Fallback 동작 검증
        """
        # Given: 네트워크 차단 환경
        with tempfile.TemporaryDirectory() as tmpdir:
            # 네트워크 접근 차단 (iptables 또는 환경변수)
            env = os.environ.copy()
            env['NO_NETWORK'] = '1'
            
            # When: 네트워크 없이 실행
            result = subprocess.run(
                ['bash', 'init.sh', '--offline', 'test_project'],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                env=env,
                timeout=10
            )
            
            # Then: Fallback 동작 검증
            assert 'Using offline fallback' in result.stdout
            assert result.returncode == 0
            
            # Fallback 콘텐츠 검증
            project_path = Path(tmpdir) / 'test_project'
            assert (project_path / '.claude' / 'commands').exists()
            
            # 최소한의 명령어는 있어야 함
            commands = list((project_path / '.claude' / 'commands').glob('*.md'))
            assert len(commands) >= 5, f"Only {len(commands)} commands in fallback"
    
    def test_korean_url_encoding(self):
        """
        Edge Case: 한글 파일명 URL 인코딩 검증
        """
        # Given: 다양한 한글 파일명
        test_cases = [
            ('기획.md', '%EA%B8%B0%ED%9A%8D.md'),
            ('구현.md', '%EA%B5%AC%ED%98%84.md'),
            ('안정화.md', '%EC%95%88%EC%A0%95%ED%99%94.md'),
            ('한글 파일명.txt', '%ED%95%9C%EA%B8%80%20%ED%8C%8C%EC%9D%BC%EB%AA%85.txt')
        ]
        
        for korean_name, expected_encoded in test_cases:
            # When: URL 인코딩
            encoded = encode_korean_filename(korean_name)
            
            # Then: 정확한 인코딩 검증
            assert encoded == expected_encoded, f"Wrong encoding for {korean_name}"
            
            # URL 유효성 검증
            test_url = f"https://example.com/{encoded}"
            assert is_valid_url(test_url), f"Invalid URL: {test_url}"
    
    def test_concurrent_installation(self):
        """
        Load Test: 동시 설치 시나리오
        """
        import concurrent.futures
        
        # Given: 여러 사용자가 동시에 설치
        def install_project(index: int) -> Dict:
            with tempfile.TemporaryDirectory() as tmpdir:
                result = subprocess.run(
                    ['bash', 'init.sh', f'project_{index}'],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return {
                    'index': index,
                    'success': result.returncode == 0,
                    'time': result.stdout
                }
        
        # When: 10개 동시 실행
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(install_project, i) for i in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # Then: 모든 설치 성공
        success_count = sum(1 for r in results if r['success'])
        assert success_count == 10, f"Only {success_count}/10 succeeded"
        
        # 성능 검증
        times = [r.get('time', 0) for r in results if r.get('time')]
        avg_time = sum(times) / len(times) if times else 0
        assert avg_time < 5.0, f"Too slow: {avg_time:.2f}s average"
    
    @pytest.mark.parametrize("invalid_input,expected_error", [
        ("", "Project name required"),
        ("../../../etc", "Invalid path"),
        ("project with | pipe", "Invalid character"),
        ("a" * 256, "Name too long")
    ])
    def test_invalid_input_handling(self, invalid_input: str, expected_error: str):
        """
        Security Test: 잘못된 입력 처리
        """
        # When: 잘못된 입력으로 실행
        result = subprocess.run(
            ['bash', 'init.sh', invalid_input],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Then: 적절한 에러 처리
        assert result.returncode != 0
        assert expected_error in result.stderr
        
        # 시스템 파일 변경 없음 확인
        assert not Path('/etc').glob('test_*')
        assert not Path.home().glob('test_*')


# 🎯 Helper Functions for Real Testing
def encode_korean_filename(filename: str) -> str:
    """한글 파일명 URL 인코딩"""
    import urllib.parse
    return urllib.parse.quote(filename)

def is_valid_url(url: str) -> bool:
    """URL 유효성 검증"""
    from urllib.parse import urlparse
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# 📊 Test Quality Metrics
def calculate_test_quality_score(test_class) -> Dict:
    """테스트 품질 점수 계산"""
    metrics = {
        'has_given_when_then': 0,
        'has_error_cases': 0,
        'has_specific_assertions': 0,
        'mock_usage': 0,
        'has_performance_checks': 0
    }
    
    # 실제 메트릭 계산 로직
    # ...
    
    score = sum(metrics.values()) * 20  # 각 항목 20점
    return {
        'score': min(score, 100),
        'metrics': metrics,
        'grade': 'A' if score >= 90 else 'B' if score >= 70 else 'F'
    }