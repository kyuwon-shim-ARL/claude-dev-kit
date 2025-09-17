#!/usr/bin/env python3
"""
@meta: tool-automation | 2025-09-17 | keep
@purpose: 테스트/검증/분석 파일에 메타데이터 자동 추가
@io: Python files → metadata insertion → updated files
"""

import re
import sys
from pathlib import Path
from datetime import date
from typing import Optional, Dict, List

class ArtifactMetadataManager:
    """부산물 파일 메타데이터 관리 도구"""

    # 파일 패턴별 타입 매핑
    TYPE_PATTERNS = {
        'test_': 'test-unit',
        'test_integration': 'test-integration',
        'test_e2e': 'test-e2e',
        'test_perf': 'test-performance',
        'verify_': 'verify-data',
        'validate_': 'verify-data',
        'check_': 'verify-compatibility',
        'analyze_': 'analysis-code',
        'analysis_': 'analysis-code',
        'profile_': 'analysis-performance',
        'benchmark_': 'analysis-performance',
        'scan_': 'analysis-security',
        'migrate_': 'tool-migration',
        'convert_': 'tool-migration',
        'generate_': 'tool-helper',
        'create_': 'tool-helper',
        'setup_': 'tool-helper'
    }

    # 기본 lifecycle 설정
    DEFAULT_LIFECYCLES = {
        'test-unit': 'keep',
        'test-integration': 'keep',
        'test-e2e': 'keep',
        'test-performance': 'temp',
        'verify-data': 'temp',
        'verify-compatibility': 'archive',
        'analysis-code': 'archive',
        'analysis-performance': 'archive',
        'analysis-security': 'keep',
        'tool-migration': 'archive',
        'tool-helper': 'keep'
    }

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.stats = {
            'processed': 0,
            'skipped': 0,
            'updated': 0,
            'failed': 0
        }

    def detect_file_type(self, filepath: Path) -> Optional[str]:
        """파일 이름과 내용을 기반으로 타입 자동 감지"""

        filename = filepath.name.lower()

        # 파일명 패턴 매칭
        for pattern, file_type in self.TYPE_PATTERNS.items():
            if pattern in filename:
                return file_type

        # 내용 기반 추가 감지
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # 처음 1000자만 확인

            # pytest, unittest 등 테스트 프레임워크 감지
            if 'import pytest' in content or 'import unittest' in content:
                return 'test-unit'

            # 분석 도구 import 감지
            if 'import pandas' in content or 'import numpy' in content:
                return 'analysis-code'

            # 성능 분석 도구 감지
            if 'import cProfile' in content or 'import timeit' in content:
                return 'analysis-performance'

        except Exception:
            pass

        return None

    def extract_purpose(self, filepath: Path) -> str:
        """파일 내용에서 목적 자동 추출"""

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # docstring에서 첫 줄 추출
            for i, line in enumerate(lines[:20]):  # 처음 20줄만 확인
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    if len(line.strip()) > 3:  # 같은 줄에 설명이 있는 경우
                        purpose = line.strip()[3:].strip('"\'')
                        if purpose:
                            return purpose[:80]  # 최대 80자
                    elif i + 1 < len(lines):  # 다음 줄에 설명이 있는 경우
                        purpose = lines[i + 1].strip()
                        if purpose:
                            return purpose[:80]

            # 함수/클래스 이름에서 추출
            for line in lines[:50]:
                if line.startswith('def test_'):
                    func_name = line.split('(')[0].replace('def test_', '').replace('_', ' ')
                    return f"Test: {func_name.title()}"
                elif line.startswith('class Test'):
                    class_name = line.split('(')[0].replace('class Test', '').replace('_', ' ')
                    return f"Test Suite: {class_name.title()}"

        except Exception:
            pass

        # 기본값: 파일명 기반
        return f"Auto-detected {filepath.stem} artifact"

    def detect_io_relationships(self, filepath: Path) -> Dict[str, str]:
        """Input-Process-Output 관계 자동 감지"""

        io_info = {
            'input': 'TBD',
            'process': 'TBD',
            'output': 'TBD'
        }

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Import 문에서 input 추론
            imports = re.findall(r'from\s+(\S+)\s+import|import\s+(\S+)', content)
            if imports:
                modules = [imp[0] or imp[1] for imp in imports[:3]]
                io_info['input'] = ', '.join(m for m in modules if not m.startswith('test'))

            # 함수 이름에서 process 추론
            functions = re.findall(r'def\s+(\w+)\s*\(', content)
            if functions:
                main_funcs = [f for f in functions if not f.startswith('_')][:2]
                if main_funcs:
                    io_info['process'] = ' → '.join(main_funcs)

            # Assert/return 문에서 output 추론
            if 'assert' in content:
                io_info['output'] = 'test assertions'
            elif 'return' in content:
                returns = re.findall(r'return\s+([^\n]+)', content)
                if returns:
                    io_info['output'] = returns[0][:50]

        except Exception:
            pass

        return io_info

    def generate_metadata(self, filepath: Path) -> str:
        """파일에 적합한 메타데이터 생성"""

        file_type = self.detect_file_type(filepath)
        if not file_type:
            return None

        lifecycle = self.DEFAULT_LIFECYCLES.get(file_type, 'temp')
        purpose = self.extract_purpose(filepath)
        io_info = self.detect_io_relationships(filepath)

        # 간단 버전 또는 상세 버전 결정
        if io_info['input'] != 'TBD' or io_info['output'] != 'TBD':
            # 상세 버전
            metadata = f'''"""
@meta
type: {file_type}
date: {date.today()}
lifecycle: {lifecycle}
purpose: {purpose}

@io
input: {io_info['input']}
process: {io_info['process']}
output: {io_info['output']}
"""
'''
        else:
            # 간단 버전
            metadata = f'''"""
@meta: {file_type} | {date.today()} | {lifecycle}
@purpose: {purpose}
"""
'''

        return metadata

    def add_metadata_to_file(self, filepath: Path) -> bool:
        """파일에 메타데이터 추가"""

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 이미 메타데이터가 있는지 확인
            if '@meta' in content[:1000]:
                print(f"⏭️  Skipped (has metadata): {filepath}")
                self.stats['skipped'] += 1
                return False

            # 메타데이터 생성
            metadata = self.generate_metadata(filepath)
            if not metadata:
                print(f"❓ Cannot detect type: {filepath}")
                self.stats['failed'] += 1
                return False

            # 파일 시작 부분에 메타데이터 삽입
            # shebang이 있으면 그 다음에 삽입
            if content.startswith('#!'):
                lines = content.split('\n', 1)
                new_content = lines[0] + '\n' + metadata + '\n' + (lines[1] if len(lines) > 1 else '')
            else:
                new_content = metadata + '\n' + content

            if not self.dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

            print(f"✅ Added metadata: {filepath}")
            self.stats['updated'] += 1
            return True

        except Exception as e:
            print(f"❌ Failed: {filepath} - {e}")
            self.stats['failed'] += 1
            return False

    def process_directory(self, directory: Path = Path('.'),
                         patterns: List[str] = None,
                         recursive: bool = True) -> None:
        """디렉토리 내 파일들 일괄 처리"""

        # 기본 패턴
        if not patterns:
            patterns = ['test_*.py', 'verify_*.py', 'analyze_*.py',
                       'check_*.py', 'validate_*.py', 'profile_*.py',
                       'benchmark_*.py', 'migrate_*.py']

        # 파일 수집
        files = []
        for pattern in patterns:
            if recursive:
                files.extend(directory.rglob(pattern))
            else:
                files.extend(directory.glob(pattern))

        # 중복 제거 및 정렬
        files = sorted(set(files))

        if not files:
            print("📭 No matching files found")
            return

        print(f"🔍 Found {len(files)} files to process")
        if self.dry_run:
            print("🧪 DRY RUN MODE - No files will be modified\n")
        else:
            print("✍️  WRITE MODE - Files will be modified\n")

        # 각 파일 처리
        for filepath in files:
            self.stats['processed'] += 1
            self.add_metadata_to_file(filepath)

        # 통계 출력
        self.print_statistics()

    def update_existing_metadata(self, filepath: Path) -> bool:
        """기존 메타데이터 업데이트"""

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 기존 메타데이터 찾기
            meta_match = re.search(r'(@meta.*?)(?=\n[^@\s]|\n\n|\Z)', content, re.DOTALL)
            if not meta_match:
                return False

            old_metadata = meta_match.group(1)

            # IO 정보 업데이트
            io_info = self.detect_io_relationships(filepath)

            # 새 메타데이터 생성
            new_metadata = old_metadata
            if '@io' not in old_metadata and io_info['input'] != 'TBD':
                new_metadata += f"\n\n@io\ninput: {io_info['input']}\nprocess: {io_info['process']}\noutput: {io_info['output']}"

            if new_metadata != old_metadata:
                new_content = content.replace(old_metadata, new_metadata)

                if not self.dry_run:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                print(f"📝 Updated metadata: {filepath}")
                return True

        except Exception as e:
            print(f"❌ Update failed: {filepath} - {e}")

        return False

    def print_statistics(self) -> None:
        """처리 통계 출력"""

        print(f"\n📊 Processing Statistics:")
        print(f"  • Total processed: {self.stats['processed']}")
        print(f"  • Added metadata: {self.stats['updated']}")
        print(f"  • Skipped (has metadata): {self.stats['skipped']}")
        print(f"  • Failed: {self.stats['failed']}")

        if self.dry_run:
            print(f"\n💡 This was a DRY RUN. Use --write to apply changes.")
        else:
            print(f"\n✅ Metadata has been added to {self.stats['updated']} files.")

def main():
    """메인 실행 함수"""

    import argparse

    parser = argparse.ArgumentParser(
        description='Add metadata to test/verification/analysis artifacts'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Directory path to process (default: current directory)'
    )
    parser.add_argument(
        '--write',
        action='store_true',
        help='Actually modify files (default: dry run)'
    )
    parser.add_argument(
        '--pattern',
        action='append',
        help='File pattern to match (can use multiple times)'
    )
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Do not process subdirectories'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Update existing metadata with IO relationships'
    )

    args = parser.parse_args()

    # Manager 생성
    manager = ArtifactMetadataManager(dry_run=not args.write)

    # 경로 확인
    directory = Path(args.path)
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        sys.exit(1)

    # 처리 실행
    if args.update:
        # 기존 메타데이터 업데이트 모드
        print("📝 Updating existing metadata...")
        # TODO: 구현 필요
    else:
        # 새 메타데이터 추가 모드
        manager.process_directory(
            directory=directory,
            patterns=args.pattern,
            recursive=not args.no_recursive
        )

if __name__ == "__main__":
    main()