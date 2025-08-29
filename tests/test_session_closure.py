#!/usr/bin/env python3
"""
Test Suite for Smart Session Closure System v20.1
지능형 세션 마감 시스템 테스트
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from session_closure import SessionClosure

class TestSessionClosure(unittest.TestCase):
    
    def setUp(self):
        """테스트를 위한 임시 디렉토리 설정"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.current_dir = self.test_dir / "docs" / "CURRENT"
        self.sessions_dir = self.test_dir / "docs" / "development" / "sessions"
        
        self.current_dir.mkdir(parents=True)
        self.sessions_dir.mkdir(parents=True)
        
        self.closure = SessionClosure(str(self.test_dir))
    
    def tearDown(self):
        """테스트 후 임시 디렉토리 정리"""
        shutil.rmtree(self.test_dir)
    
    def test_completion_detection_high_confidence(self):
        """완료 상태 감지 - 높은 신뢰도 테스트"""
        # 완성도 100% 문서
        completion_file = self.current_dir / "completion-report-test.md"
        completion_file.write_text("""# Test Completion Report
        
## 전체 완성도: 100%

### ✅ 완료 항목 (5/5)
- ✅ 기능 구현 완료
- ✅ 테스트 완료
- ✅ 문서화 완료
""", encoding='utf-8')
        
        analysis = self.closure.analyze_completion_status(completion_file)
        
        self.assertEqual(analysis['status'], 'completed')
        self.assertGreaterEqual(analysis['confidence'], 0.9)
    
    def test_progress_detection(self):
        """진행중 상태 감지 테스트"""
        active_file = self.current_dir / "active-todos.md"
        active_file.write_text("""# Active TODOs
        
## 🚀 Current Sprint
1. ⏳ 기능 구현 중
2. ⏳ 테스트 작성 중
""", encoding='utf-8')
        
        analysis = self.closure.analyze_completion_status(active_file)
        
        self.assertEqual(analysis['status'], 'preserve')  # active-todos는 보존 대상
        self.assertGreaterEqual(analysis['confidence'], 0.9)
    
    def test_filename_based_detection(self):
        """파일명 기반 완료 감지 테스트"""
        test_file = self.current_dir / "test-report-v1.0.md"
        test_file.write_text("""# Test Report v1.0
        
테스트가 성공적으로 완료되었습니다.
""", encoding='utf-8')
        
        analysis = self.closure.analyze_completion_status(test_file)
        
        self.assertEqual(analysis['status'], 'completed')
        self.assertGreaterEqual(analysis['confidence'], 0.8)
    
    def test_preserve_detection(self):
        """보존 대상 감지 테스트"""
        status_file = self.current_dir / "status.md"
        status_file.write_text("""# Current Project Status
        
현재 프로젝트 진행 상황입니다.
""", encoding='utf-8')
        
        analysis = self.closure.analyze_completion_status(status_file)
        
        self.assertEqual(analysis['status'], 'preserve')
        self.assertGreaterEqual(analysis['confidence'], 0.9)
    
    def test_directory_scan(self):
        """디렉토리 전체 스캔 테스트"""
        # 다양한 상태의 파일들 생성
        files = {
            "completion-report.md": ("completed", "전체 완성도: 100%"),
            "active-todos.md": ("preserve", "# Active TODOs\n⏳ 진행중"),
            "test-report.md": ("completed", "테스트 완료"),
            "status.md": ("preserve", "# Current Status"),
            "unknown-doc.md": ("uncertain", "내용 불명확")
        }
        
        for filename, (expected_status, content) in files.items():
            file_path = self.current_dir / filename
            file_path.write_text(content, encoding='utf-8')
        
        results = self.closure.scan_current_directory()
        
        # 결과 검증
        self.assertEqual(len(results['completed']), 2)  # completion-report, test-report
        self.assertEqual(len(results['preserve']), 2)   # active-todos, status
        self.assertEqual(len(results['uncertain']), 1)  # unknown-doc
    
    def test_archive_creation(self):
        """아카이브 생성 테스트"""
        # 완료 문서 생성
        completion_file = self.current_dir / "test-completion.md"
        completion_file.write_text("완성도: 100%", encoding='utf-8')
        
        analysis = self.closure.analyze_completion_status(completion_file)
        completed_files = [(completion_file, analysis)]
        
        # 아카이브 실행
        result = self.closure.archive_completed_documents(completed_files)
        
        # 검증
        self.assertIn("1개 문서가", result)
        self.assertFalse(completion_file.exists())  # 원본 파일 삭제됨
        
        # 아카이브 파일 생성 확인
        archive_files = list(self.sessions_dir.glob("**/*.md"))
        self.assertEqual(len(archive_files), 1)

def run_comprehensive_test():
    """포괄적 테스트 실행"""
    print("🧪 지능형 세션 마감 시스템 테스트 시작...")
    
    # 테스트 실행
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSessionClosure)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 결과 리포트
    print(f"\n📊 테스트 결과:")
    print(f"✅ 성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ 실패: {len(result.failures)}")
    print(f"🚨 오류: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 모든 테스트 통과!")
        return True
    else:
        print("⚠️ 일부 테스트 실패")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)