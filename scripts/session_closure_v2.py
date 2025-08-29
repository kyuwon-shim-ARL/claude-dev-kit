#!/usr/bin/env python3
"""
Smart Session Closure System v2.0
실제 프로젝트 패턴 기반 현실적 문서 정리 시스템
"""

import os
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re
import hashlib

class SessionClosureV2:
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.current_dir = self.project_root / "docs" / "CURRENT"
        self.sessions_dir = self.project_root / "docs" / "development" / "sessions"
        self.specs_dir = self.project_root / "docs" / "specs"
        self.archive_dir = self.project_root / "docs" / "archive"
        self.current_month = datetime.now().strftime("%Y-%m")
        self.dry_run = False  # 기본값 설정
        
        # 실제 프로젝트에서 발견된 패턴들
        self.known_patterns = self.load_known_patterns()
        
    def load_known_patterns(self) -> Dict:
        """실제 프로젝트에서 학습한 패턴들"""
        return {
            "definitely_completed": [
                # 명확한 완료 신호
                (r"FINAL_COMPLETION_REPORT", 0.95),
                (r"session-\d{3}\.md$", 0.9),  # 세션 파일
                (r"_complete\.md$", 0.9),
                (r"_done\.md$", 0.9),
                (r"completion-report-.*\.md$", 0.85),
                (r"test-report-v\d+", 0.85),
                (r"implementation-report-v\d+", 0.85),
            ],
            
            "likely_completed": [
                # 내용 확인 필요
                (r".*_v\d+_.*Final.*", 0.7),
                (r"PHASE\d+_COMPLETION", 0.7),
                (r"cycle\d+_.*report", 0.65),
                (r".*_analysis_.*\.md$", 0.6),
            ],
            
            "preserve_always": [
                # 절대 건드리면 안되는 파일들
                (r"^active-todos\.md$", 1.0),
                (r"^status\.md$", 1.0),
                (r"^planning\.md$", 0.9),
                (r"^project_rules\.md$", 1.0),
                (r"^CLAUDE\.md$", 1.0),
                (r"^README\.md$", 1.0),
            ],
            
            "prd_or_spec": [
                # PRD/스펙은 특별 처리
                (r"PRD[-_]v\d+", 0.9),
                (r"PRD[-_].*\.md$", 0.85),
                (r"requirements\.md$", 0.9),
                (r"architecture\.md$", 0.9),
                (r".*_spec\.md$", 0.85),
            ],
            
            "working_documents": [
                # 작업 중인 문서
                (r".*draft.*", 0.8),
                (r".*temp.*", 0.7),
                (r".*todo.*", 0.8),
                (r".*planning.*", 0.7),
            ]
        }
    
    def analyze_file_advanced(self, file_path: Path) -> Dict:
        """더 정교한 파일 분석"""
        content = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return {"status": "error", "confidence": 0, "reason": "파일 읽기 실패"}
        
        filename = file_path.name
        file_stats = file_path.stat()
        
        # 1. 파일 수정 시간 확인
        last_modified = datetime.fromtimestamp(file_stats.st_mtime)
        days_old = (datetime.now() - last_modified).days
        
        # 2. TODO 체크리스트 완성도 확인
        todo_completion = self.check_todo_completion(content)
        
        # 3. 패턴 매칭
        pattern_result = self.match_patterns(filename, content)
        
        # 4. 내용 기반 분석
        content_analysis = self.analyze_content_signals(content)
        
        # 5. 종합 판단
        return self.make_decision(
            filename=filename,
            days_old=days_old,
            todo_completion=todo_completion,
            pattern_result=pattern_result,
            content_analysis=content_analysis,
            file_path=file_path
        )
    
    def check_todo_completion(self, content: str) -> float:
        """TODO 체크리스트 완성도 계산"""
        todo_pattern = r'- \[([ x])\]'
        todos = re.findall(todo_pattern, content, re.IGNORECASE)
        
        if not todos:
            return -1  # TODO가 없음
        
        completed = sum(1 for t in todos if t.lower() == 'x')
        return completed / len(todos) if todos else 0
    
    def match_patterns(self, filename: str, content: str) -> Dict:
        """패턴 매칭 수행"""
        results = {}
        
        for category, patterns in self.known_patterns.items():
            for pattern, confidence in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    results[category] = max(results.get(category, 0), confidence)
                    
                # 내용에서도 패턴 찾기 (첫 100줄만)
                first_lines = '\n'.join(content.split('\n')[:100])
                if re.search(pattern, first_lines, re.IGNORECASE):
                    results[category] = max(results.get(category, 0), confidence * 0.8)
        
        return results
    
    def analyze_content_signals(self, content: str) -> Dict:
        """내용 기반 완료 신호 분석"""
        signals = {
            "completion_words": 0,
            "progress_words": 0,
            "has_next_steps": False,
            "has_conclusion": False,
            "has_results": False
        }
        
        # 완료 관련 단어
        completion_words = [
            "완료", "complete", "done", "finished", "final",
            "결론", "conclusion", "deployed", "shipped", "released"
        ]
        
        # 진행중 관련 단어
        progress_words = [
            "진행중", "in progress", "ongoing", "todo", "pending",
            "계획", "예정", "will", "to be", "draft"
        ]
        
        content_lower = content.lower()
        
        for word in completion_words:
            signals["completion_words"] += content_lower.count(word)
        
        for word in progress_words:
            signals["progress_words"] += content_lower.count(word)
        
        # 섹션 분석
        if re.search(r'(## next steps|## 다음 단계|## todo)', content, re.IGNORECASE):
            signals["has_next_steps"] = True
        
        if re.search(r'(## conclusion|## 결론|## summary|## 요약)', content, re.IGNORECASE):
            signals["has_conclusion"] = True
            
        if re.search(r'(## results|## 결과|## output|## 산출물)', content, re.IGNORECASE):
            signals["has_results"] = True
        
        return signals
    
    def make_decision(self, **kwargs) -> Dict:
        """종합적인 완료 상태 판단"""
        filename = kwargs['filename']
        days_old = kwargs['days_old']
        todo_completion = kwargs['todo_completion']
        pattern_result = kwargs['pattern_result']
        content_analysis = kwargs['content_analysis']
        file_path = kwargs['file_path']
        
        # 보존 대상 체크
        if pattern_result.get('preserve_always', 0) > 0.8:
            return {
                "status": "preserve",
                "confidence": pattern_result['preserve_always'],
                "reason": f"영구 보존 대상 파일 - {filename}",
                "category": "system"
            }
        
        # PRD/스펙 체크
        if pattern_result.get('prd_or_spec', 0) > 0.7:
            if days_old > 7:
                return {
                    "status": "move_to_specs",
                    "confidence": 0.85,
                    "reason": f"PRD/스펙 문서 - specs로 이동 권장",
                    "category": "specification"
                }
            else:
                return {
                    "status": "in_progress",
                    "confidence": 0.7,
                    "reason": f"최근 작업중인 PRD/스펙",
                    "category": "specification"
                }
        
        # 명확한 완료 체크
        if pattern_result.get('definitely_completed', 0) > 0.8:
            return {
                "status": "completed",
                "confidence": pattern_result['definitely_completed'],
                "reason": f"완료 패턴 감지 - {filename}",
                "category": "report"
            }
        
        # TODO 기반 판단
        if todo_completion >= 0.95 and days_old > 3:
            return {
                "status": "completed",
                "confidence": 0.85,
                "reason": f"TODO 95% 완료 + {days_old}일 경과",
                "category": "task"
            }
        
        # 내용 기반 판단
        completion_score = content_analysis['completion_words']
        progress_score = content_analysis['progress_words']
        
        if completion_score > progress_score * 2 and days_old > 5:
            return {
                "status": "likely_completed",
                "confidence": 0.7,
                "reason": f"완료 키워드 우세 + {days_old}일 경과",
                "category": "analysis"
            }
        
        # 오래된 파일 처리
        if days_old > 30:
            return {
                "status": "stale",
                "confidence": 0.8,
                "reason": f"{days_old}일 이상 방치된 파일",
                "category": "abandoned"
            }
        
        # 작업중 문서
        if pattern_result.get('working_documents', 0) > 0.6:
            return {
                "status": "in_progress",
                "confidence": 0.7,
                "reason": "작업 중인 문서로 판단",
                "category": "working"
            }
        
        # 불확실
        return {
            "status": "uncertain",
            "confidence": 0.4,
            "reason": "명확한 신호 없음 - 수동 확인 필요",
            "category": "unknown"
        }
    
    def scan_all_project_docs(self) -> Dict:
        """프로젝트 전체 문서 스캔 (CURRENT 외에도)"""
        results = {
            "current": {"completed": [], "in_progress": [], "preserve": [], 
                       "uncertain": [], "stale": [], "move_to_specs": []},
            "suggestions": [],
            "statistics": {}
        }
        
        # CURRENT 디렉토리 스캔 (하위 디렉토리 포함)
        if self.current_dir.exists():
            for file_path in self.current_dir.rglob("*.md"):  # rglob으로 재귀적 스캔
                # 시스템 파일 건너뛰기
                if file_path.name in ["INDEX.md", "README.md"]:
                    continue
                    
                analysis = self.analyze_file_advanced(file_path)
                status = analysis.get("status", "uncertain")
                
                if status == "likely_completed":
                    status = "completed"  # 단순화
                    
                if status in results["current"]:
                    results["current"][status].append((file_path, analysis))
        
        # 통계 생성
        total_files = sum(len(files) for files in results["current"].values())
        results["statistics"] = {
            "total_files": total_files,
            "completed": len(results["current"]["completed"]),
            "in_progress": len(results["current"]["in_progress"]),
            "preserve": len(results["current"]["preserve"]),
            "stale": len(results["current"]["stale"]),
            "move_to_specs": len(results["current"]["move_to_specs"]),
            "uncertain": len(results["current"]["uncertain"])
        }
        
        # 추천 생성
        if results["current"]["stale"]:
            results["suggestions"].append(
                f"📌 {len(results['current']['stale'])}개의 오래된 파일을 아카이브하는 것을 권장합니다."
            )
        
        if results["current"]["move_to_specs"]:
            results["suggestions"].append(
                f"📋 {len(results['current']['move_to_specs'])}개의 PRD/스펙 문서를 specs/ 디렉토리로 이동하는 것을 권장합니다."
            )
        
        return results
    
    def interactive_cleanup(self, scan_results: Dict) -> None:
        """대화형 정리 프로세스"""
        print("\n🧹 세션 마감 v2.0 - 대화형 정리 모드\n")
        print("=" * 60)
        
        # 각 카테고리별 처리
        categories = [
            ("completed", "✅ 완료 문서", "아카이브"),
            ("stale", "📅 오래된 문서", "아카이브"),
            ("move_to_specs", "📋 PRD/스펙 문서", "specs로 이동"),
            ("uncertain", "❓ 불확실한 문서", "수동 결정")
        ]
        
        for status_key, label, action in categories:
            files = scan_results["current"][status_key]
            if not files:
                continue
                
            print(f"\n{label} ({len(files)}개):")
            print("-" * 40)
            
            for i, (file_path, analysis) in enumerate(files[:10], 1):  # 최대 10개만 표시
                # 상대 경로 표시 (CURRENT/ 기준)
                try:
                    rel_path = file_path.relative_to(self.current_dir)
                except ValueError:
                    rel_path = file_path.name
                print(f"{i}. {rel_path}")
                print(f"   └─ {analysis['reason']} (신뢰도: {analysis['confidence']:.0%})")
            
            if len(files) > 10:
                print(f"   ... 외 {len(files)-10}개 더")
            
            if status_key != "uncertain":
                try:
                    response = input(f"\n이 파일들을 {action}하시겠습니까? [Y/n/개별선택(s)]: ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    response = 'n'  # 비대화형 환경에서는 안전하게 건너뜀
                    print(" → 비대화형 환경 감지, 건너뜀")
                
                if response in ['y', 'yes', '']:
                    self.process_files(files, status_key)
                elif response == 's':
                    self.selective_process(files, status_key)
                else:
                    print("⏭️  건너뜁니다.")
    
    def process_files(self, files: List[Tuple[Path, Dict]], action: str) -> None:
        """파일 일괄 처리"""
        if action == "completed" or action == "stale":
            # 세션 아카이브로 이동
            archive_file = self.create_session_archive()
            for file_path, analysis in files:
                self.add_to_archive(archive_file, file_path, analysis)
                file_path.unlink()  # 원본 삭제
            print(f"✅ {len(files)}개 파일이 {archive_file}에 아카이브되었습니다.")
            
        elif action == "move_to_specs":
            # specs 디렉토리로 이동
            self.specs_dir.mkdir(parents=True, exist_ok=True)
            for file_path, _ in files:
                target = self.specs_dir / file_path.name
                shutil.move(str(file_path), str(target))
            print(f"📋 {len(files)}개 파일이 specs/ 디렉토리로 이동되었습니다.")
    
    def selective_process(self, files: List[Tuple[Path, Dict]], action: str) -> None:
        """파일 개별 선택 처리"""
        print("\n개별 파일 선택 모드:")
        for i, (file_path, analysis) in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}] {file_path.name}")
            print(f"이유: {analysis['reason']}")
            try:
                choice = input("처리하시겠습니까? [Y/n/내용보기(v)]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                choice = 'n'
                print(" → 비대화형 환경, 건너뜀")
            
            if choice == 'v':
                # 파일 내용 일부 표시
                with open(file_path, 'r', encoding='utf-8') as f:
                    print("\n--- 파일 내용 (처음 20줄) ---")
                    for line in f.readlines()[:20]:
                        print(line.rstrip())
                    print("--- 끝 ---\n")
                try:
                    choice = input("처리하시겠습니까? [Y/n]: ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    choice = 'n'
                    print(" → 비대화형 환경, 건너뜀")
            
            if choice in ['y', 'yes', '']:
                self.process_files([(file_path, analysis)], action)
    
    def create_session_archive(self) -> Path:
        """세션 아카이브 파일 생성"""
        month_dir = self.sessions_dir / self.current_month
        month_dir.mkdir(parents=True, exist_ok=True)
        
        existing = list(month_dir.glob("session-*.md"))
        session_num = len(existing) + 1
        
        return month_dir / f"session-{session_num:03d}.md"
    
    def add_to_archive(self, archive_file: Path, source_file: Path, analysis: Dict) -> None:
        """아카이브 파일에 내용 추가"""
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        archive_content = f"""
## {source_file.name}
**카테고리**: {analysis.get('category', 'unknown')}
**아카이브 이유**: {analysis['reason']}
**신뢰도**: {analysis['confidence']:.0%}
**아카이브 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{content}

---

"""
        
        # 아카이브 파일에 추가
        with open(archive_file, 'a', encoding='utf-8') as f:
            f.write(archive_content)
    
    def generate_cleanup_report(self, scan_results: Dict) -> str:
        """정리 결과 리포트 생성"""
        stats = scan_results['statistics']
        
        report = f"""
# 📊 세션 마감 v2.0 분석 리포트

**분석 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**전체 파일**: {stats['total_files']}개

## 📈 카테고리별 분류

✅ **완료 문서** ({stats['completed']}개)
   - 아카이브 가능한 완료된 작업들

📚 **보존 문서** ({stats['preserve']}개)
   - active-todos.md, status.md 등 시스템 파일

⏳ **진행중 문서** ({stats['in_progress']}개)
   - 현재 작업 중인 문서들

📋 **PRD/스펙 문서** ({stats['move_to_specs']}개)
   - specs/ 디렉토리로 이동 권장

📅 **오래된 문서** ({stats['stale']}개)
   - 30일 이상 방치된 파일들

❓ **불확실 문서** ({stats['uncertain']}개)
   - 수동 확인이 필요한 파일들

## 💡 권장 사항
"""
        
        for suggestion in scan_results['suggestions']:
            report += f"- {suggestion}\n"
        
        # 정리 효과 예측
        cleanable = stats['completed'] + stats['stale'] + stats['move_to_specs']
        if cleanable > 0:
            reduction = (cleanable / stats['total_files']) * 100
            report += f"""
## 🎯 예상 효과

- **정리 가능 파일**: {cleanable}개
- **CURRENT 디렉토리 감소율**: {reduction:.1f}%
- **예상 정리 후**: {stats['total_files'] - cleanable}개 파일
"""
        
        return report

def main():
    """세션 마감 v2.0 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description='세션 마감 시스템 v2.0')
    parser.add_argument('--project', help='프로젝트 경로', default='.')
    parser.add_argument('--dry-run', action='store_true', help='실제 변경 없이 시뮬레이션만')
    args = parser.parse_args()
    
    # 프로젝트 경로 처리
    project_path = Path(args.project).resolve()
    if not project_path.exists():
        print(f"❌ 프로젝트 경로를 찾을 수 없습니다: {project_path}")
        return
    
    closure = SessionClosureV2(project_root=str(project_path))
    closure.dry_run = args.dry_run
    
    print("""
╔════════════════════════════════════════════════════════╗
║         🧹 세션 마감 시스템 v2.0                        ║
║         실제 프로젝트 패턴 기반 지능형 정리             ║
╚════════════════════════════════════════════════════════╝
    """)
    
    print("🔍 프로젝트 문서 분석 중...")
    scan_results = closure.scan_all_project_docs()
    
    # 분석 리포트 출력
    print(closure.generate_cleanup_report(scan_results))
    
    # 대화형 정리 시작
    if scan_results['statistics']['total_files'] > 0:
        try:
            response = input("\n정리를 시작하시겠습니까? [Y/n]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            response = 'n'  # 비대화형 환경에서는 안전하게 거부
            print("N (비대화형 환경, 건너뜀)")
        if response in ['y', 'yes', '']:
            closure.interactive_cleanup(scan_results)
            print("\n✨ 세션 마감이 완료되었습니다!")
        else:
            print("❌ 세션 마감이 취소되었습니다.")
    else:
        print("\n✅ 정리할 문서가 없습니다. CURRENT가 이미 깨끗합니다!")

if __name__ == "__main__":
    main()