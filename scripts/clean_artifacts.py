#!/usr/bin/env python3
"""
@meta: tool-automation | 2025-09-17 | keep
@purpose: 메타데이터 기반 부산물 파일 자동 정리
@io: artifact files → lifecycle analysis → organized structure
"""

import re
import sys
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple
from collections import defaultdict

class ArtifactCleaner:
    """메타데이터 기반 자동 정리 도구"""

    # Lifecycle 별 보존 기간 (일)
    RETENTION_DAYS = {
        'temp': 7,       # 7일 후 archive
        'archive': 30,   # 30일 후 .archive 폴더로
        'deprecated': 0, # 즉시 삭제 대상
        'wip': -1,      # 무제한 (경고만)
        'keep': -1      # 무제한
    }

    def __init__(self, dry_run: bool = True, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.stats = defaultdict(int)
        self.actions = []

    def parse_metadata(self, filepath: Path) -> Optional[Dict]:
        """파일에서 메타데이터 추출"""

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(2000)  # 처음 2000자만 확인

            # 간단 형식: @meta: type | date | lifecycle
            simple_pattern = r'@meta:\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^\n]+)'
            match = re.search(simple_pattern, content)

            if match:
                return {
                    'type': match.group(1).strip(),
                    'date': match.group(2).strip(),
                    'lifecycle': match.group(3).strip(),
                    'format': 'simple'
                }

            # 상세 형식
            if '@meta' in content:
                metadata = {}

                # type 추출
                type_match = re.search(r'type:\s*([^\n]+)', content)
                if type_match:
                    metadata['type'] = type_match.group(1).strip()

                # date 추출
                date_match = re.search(r'date:\s*([^\n]+)', content)
                if date_match:
                    metadata['date'] = date_match.group(1).strip()

                # lifecycle 추출
                lifecycle_match = re.search(r'lifecycle:\s*([^\n]+)', content)
                if lifecycle_match:
                    metadata['lifecycle'] = lifecycle_match.group(1).strip()

                # status 추출 (optional)
                status_match = re.search(r'status:\s*([^\n]+)', content)
                if status_match:
                    metadata['status'] = status_match.group(1).strip()

                if 'lifecycle' in metadata and 'date' in metadata:
                    metadata['format'] = 'detailed'
                    return metadata

        except Exception as e:
            if self.verbose:
                print(f"⚠️  Error reading {filepath}: {e}")

        return None

    def calculate_age(self, date_str: str) -> int:
        """날짜 문자열로부터 경과 일수 계산"""

        try:
            file_date = datetime.strptime(date_str, '%Y-%m-%d')
            age = (datetime.now() - file_date).days
            return age
        except ValueError:
            # 다른 날짜 형식 시도
            try:
                file_date = datetime.strptime(date_str, '%Y/%m/%d')
                age = (datetime.now() - file_date).days
                return age
            except ValueError:
                return -1  # 날짜 파싱 실패

    def determine_action(self, filepath: Path, metadata: Dict) -> Tuple[str, str]:
        """메타데이터 기반 처리 액션 결정"""

        lifecycle = metadata.get('lifecycle', 'unknown')
        age = self.calculate_age(metadata.get('date', ''))

        if age == -1:
            return 'skip', 'Invalid date format'

        retention = self.RETENTION_DAYS.get(lifecycle, -1)

        # deprecated는 즉시 삭제
        if lifecycle == 'deprecated':
            return 'delete', f'Deprecated ({age}d old)'

        # temp는 7일 후 archive로
        if lifecycle == 'temp' and retention > 0 and age > retention:
            return 'to_archive', f'Temp expired ({age}d > {retention}d)'

        # archive는 30일 후 .archive 폴더로
        if lifecycle == 'archive' and retention > 0 and age > retention:
            return 'to_archive_dir', f'Archive expired ({age}d > {retention}d)'

        # wip는 경고만
        if lifecycle == 'wip' and age > 30:
            return 'warn', f'WIP for {age} days'

        # keep은 유지
        if lifecycle == 'keep':
            return 'keep', f'Permanent ({age}d old)'

        return 'keep', f'{lifecycle} ({age}d old)'

    def get_archive_path(self, filepath: Path) -> Path:
        """아카이브 경로 생성"""

        # 날짜 기반 폴더 구조
        today = datetime.now()
        archive_base = Path('.archive') / f"{today.year:04d}-{today.month:02d}"

        # 원본 디렉토리 구조 유지
        relative_path = filepath.relative_to(Path.cwd())
        archive_path = archive_base / relative_path.parent

        return archive_path / filepath.name

    def execute_action(self, filepath: Path, action: str, reason: str) -> bool:
        """액션 실행"""

        try:
            if action == 'delete':
                if not self.dry_run:
                    filepath.unlink()
                self.actions.append(f"🗑️  Deleted: {filepath} - {reason}")
                self.stats['deleted'] += 1
                return True

            elif action == 'to_archive':
                # lifecycle를 archive로 변경
                if not self.dry_run:
                    self.update_lifecycle(filepath, 'archive')
                self.actions.append(f"📝 Updated: {filepath} - temp → archive")
                self.stats['updated'] += 1
                return True

            elif action == 'to_archive_dir':
                # .archive 폴더로 이동
                archive_path = self.get_archive_path(filepath)

                if not self.dry_run:
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(filepath), str(archive_path))

                self.actions.append(f"📦 Archived: {filepath} → {archive_path}")
                self.stats['archived'] += 1
                return True

            elif action == 'warn':
                self.actions.append(f"⚠️  Warning: {filepath} - {reason}")
                self.stats['warned'] += 1
                return True

            elif action == 'keep':
                if self.verbose:
                    self.actions.append(f"✅ Keeping: {filepath} - {reason}")
                self.stats['kept'] += 1
                return True

        except Exception as e:
            self.actions.append(f"❌ Failed: {filepath} - {e}")
            self.stats['failed'] += 1
            return False

        return False

    def update_lifecycle(self, filepath: Path, new_lifecycle: str) -> bool:
        """파일 내 lifecycle 메타데이터 업데이트"""

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 간단 형식 업데이트
            pattern = r'(@meta:\s*[^|]+\s*\|\s*[^|]+\s*\|)\s*[^\n]+'
            if re.search(pattern, content):
                new_content = re.sub(pattern, r'\1 ' + new_lifecycle, content)
            # 상세 형식 업데이트
            elif 'lifecycle:' in content:
                new_content = re.sub(r'lifecycle:\s*[^\n]+', f'lifecycle: {new_lifecycle}', content)
            else:
                return False

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return True

        except Exception:
            return False

    def find_artifacts(self, directory: Path = Path('.')) -> List[Path]:
        """정리 대상 artifact 파일 찾기"""

        artifacts = []
        patterns = [
            'test_*.py', 'verify_*.py', 'analyze_*.py',
            'check_*.py', 'validate_*.py', 'profile_*.py',
            'benchmark_*.py', 'migrate_*.py', 'scan_*.py'
        ]

        for pattern in patterns:
            artifacts.extend(directory.rglob(pattern))

        # .archive 폴더 제외
        artifacts = [f for f in artifacts if '.archive' not in str(f)]

        return sorted(set(artifacts))

    def generate_report(self) -> str:
        """정리 결과 리포트 생성"""

        report = []
        report.append("\n" + "=" * 60)
        report.append("📊 ARTIFACT CLEANUP REPORT")
        report.append("=" * 60)

        # 액션별 그룹화
        action_groups = defaultdict(list)
        for action in self.actions:
            if action.startswith('🗑️'):
                action_groups['Deleted'].append(action)
            elif action.startswith('📦'):
                action_groups['Archived'].append(action)
            elif action.startswith('📝'):
                action_groups['Updated'].append(action)
            elif action.startswith('⚠️'):
                action_groups['Warnings'].append(action)
            elif action.startswith('✅'):
                action_groups['Kept'].append(action)

        # 각 그룹 출력
        for group_name, items in action_groups.items():
            if items:  # verbose가 아니면 Kept은 제외
                if group_name == 'Kept' and not self.verbose:
                    continue
                report.append(f"\n### {group_name} ({len(items)})")
                report.append("-" * 40)
                for item in items:
                    report.append(item)

        # 통계 요약
        report.append("\n" + "=" * 60)
        report.append("📈 SUMMARY")
        report.append("-" * 40)
        report.append(f"  • Files scanned: {sum(self.stats.values())}")
        report.append(f"  • Kept: {self.stats['kept']}")
        report.append(f"  • Updated: {self.stats['updated']}")
        report.append(f"  • Archived: {self.stats['archived']}")
        report.append(f"  • Deleted: {self.stats['deleted']}")
        report.append(f"  • Warnings: {self.stats['warned']}")
        report.append(f"  • Failed: {self.stats['failed']}")

        if self.dry_run:
            report.append("\n⚠️  DRY RUN - No actual changes were made")
            report.append("💡 Use --execute to apply these changes")
        else:
            report.append("\n✅ Changes have been applied successfully")

        report.append("=" * 60 + "\n")

        return '\n'.join(report)

    def clean(self, directory: Path = Path('.')) -> None:
        """메인 정리 실행"""

        print(f"🔍 Scanning for artifacts in {directory}...")

        artifacts = self.find_artifacts(directory)

        if not artifacts:
            print("📭 No artifact files found")
            return

        print(f"📁 Found {len(artifacts)} artifact files\n")

        if self.dry_run:
            print("🧪 DRY RUN MODE - Simulating cleanup...\n")
        else:
            print("⚡ EXECUTE MODE - Applying cleanup...\n")

        # 각 파일 처리
        for filepath in artifacts:
            metadata = self.parse_metadata(filepath)

            if not metadata:
                if self.verbose:
                    print(f"⏭️  No metadata: {filepath}")
                self.stats['no_metadata'] += 1
                continue

            action, reason = self.determine_action(filepath, metadata)
            self.execute_action(filepath, action, reason)

        # 리포트 출력
        print(self.generate_report())

        # 추가 권장사항
        if self.stats.get('no_metadata', 0) > 0:
            print(f"💡 TIP: {self.stats['no_metadata']} files have no metadata")
            print("   Run 'python scripts/add_metadata_to_artifacts.py' to add metadata\n")

def main():
    """메인 실행 함수"""

    import argparse

    parser = argparse.ArgumentParser(
        description='Clean up test/verification/analysis artifacts based on metadata'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Directory path to clean (default: current directory)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually perform cleanup (default: dry run)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed information including kept files'
    )

    args = parser.parse_args()

    # Cleaner 생성 및 실행
    cleaner = ArtifactCleaner(
        dry_run=not args.execute,
        verbose=args.verbose
    )

    # 경로 확인
    directory = Path(args.path)
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        sys.exit(1)

    # 정리 실행
    cleaner.clean(directory)

if __name__ == "__main__":
    main()