#!/usr/bin/env python3
"""
Smart Session Closure System v20.1
지능형 세션 마감 시스템 - Claude 맥락 이해 기반 자동 문서 정리
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import re

class SessionClosure:
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.current_dir = self.project_root / "docs" / "CURRENT"
        self.sessions_dir = self.project_root / "docs" / "development" / "sessions"
        self.current_month = datetime.now().strftime("%Y-%m")
        
    def analyze_completion_status(self, file_path: Path) -> Dict:
        """파일의 완료 상태를 지능형 분석"""
        content = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return {"status": "unknown", "confidence": 0, "reason": "파일 읽기 실패"}
            
        filename = file_path.name
        
        # 완료 신호들
        completion_signals = [
            ("완성도.*100%", 0.95),
            ("전체 완성도.*100%", 0.95),
            ("✅.*완료", 0.9),
            ("완료.*항목.*\\d+/\\d+", 0.85),
            ("테스트.*완료", 0.8),
            ("구현.*완료", 0.8),
            ("배포.*완료", 0.8),
            ("성공률.*100%", 0.85)
        ]
        
        # 파일명 기반 완료 신호
        filename_completion = [
            ("completion-report", 0.9),
            ("test-report-v\\d", 0.85),
            ("implementation-report", 0.85)
        ]
        
        # 진행중 신호들
        progress_signals = [
            ("⏳.*진행", 0.9),
            ("Active TODOs", 0.95),
            ("Current Sprint", 0.9),
            ("in_progress", 0.8)
        ]
        
        # 보존 신호들 (영구 보관 대상)
        preserve_signals = [
            ("active-todos", 0.95),
            ("status\\.md", 0.95),
            ("project_rules", 0.95),
            ("planning\\.md", 0.8)
        ]
        
        # 분석 수행
        max_completion_score = 0
        completion_reason = ""
        
        for pattern, score in completion_signals:
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                if score > max_completion_score:
                    max_completion_score = score
                    completion_reason = f"내용에서 '{pattern}' 패턴 감지"
        
        for pattern, score in filename_completion:
            if re.search(pattern, filename, re.IGNORECASE):
                if score > max_completion_score:
                    max_completion_score = score  
                    completion_reason = f"파일명에서 '{pattern}' 패턴 감지"
        
        # 진행중 신호 확인
        progress_score = 0
        for pattern, score in progress_signals:
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                progress_score = max(progress_score, score)
        
        # 보존 신호 확인  
        preserve_score = 0
        for pattern, score in preserve_signals:
            if re.search(pattern, filename, re.IGNORECASE):
                preserve_score = max(preserve_score, score)
        
        # 최종 상태 결정
        if preserve_score >= 0.8:
            return {
                "status": "preserve", 
                "confidence": preserve_score,
                "reason": f"영구 보존 대상 - {filename}"
            }
        elif progress_score >= 0.8:
            return {
                "status": "in_progress", 
                "confidence": progress_score,
                "reason": "진행중 신호 감지"
            }
        elif max_completion_score >= 0.8:
            return {
                "status": "completed", 
                "confidence": max_completion_score,
                "reason": completion_reason
            }
        else:
            return {
                "status": "uncertain", 
                "confidence": 0.5,
                "reason": "명확한 신호 없음 - 수동 확인 필요"
            }
    
    def scan_current_directory(self) -> Dict[str, List[Tuple[Path, Dict]]]:
        """CURRENT 디렉토리 전체 스캔 및 분류"""
        if not self.current_dir.exists():
            return {"completed": [], "in_progress": [], "preserve": [], "uncertain": []}
        
        results = {"completed": [], "in_progress": [], "preserve": [], "uncertain": []}
        
        for file_path in self.current_dir.glob("*.md"):
            analysis = self.analyze_completion_status(file_path)
            status = analysis["status"]
            results[status].append((file_path, analysis))
        
        return results
    
    def create_session_archive_dir(self) -> Path:
        """세션 아카이브 디렉토리 생성"""
        month_dir = self.sessions_dir / self.current_month
        month_dir.mkdir(parents=True, exist_ok=True)
        
        # 세션 번호 결정
        existing_sessions = list(month_dir.glob("session-*.md"))
        session_num = len(existing_sessions) + 1
        
        return month_dir / f"session-{session_num:03d}.md"
    
    def archive_completed_documents(self, completed_files: List[Tuple[Path, Dict]]) -> str:
        """완료 문서들을 세션 아카이브로 이동"""
        if not completed_files:
            return "아카이브할 완료 문서가 없습니다."
        
        archive_file = self.create_session_archive_dir()
        
        # 세션 아카이브 파일 생성
        archive_content = f"""# Session Archive - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 아카이브된 완료 문서들

"""
        
        for file_path, analysis in completed_files:
            # 파일 내용을 아카이브에 포함
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                archive_content += f"""
### {file_path.name}
**완료 이유**: {analysis['reason']} (신뢰도: {analysis['confidence']:.0%})

{content}

---

"""
                # 원본 파일 삭제
                file_path.unlink()
                
            except Exception as e:
                archive_content += f"""
### {file_path.name} (아카이브 실패)
**오류**: {str(e)}

---

"""
        
        # 아카이브 파일 저장
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(archive_content)
        
        return f"✅ {len(completed_files)}개 문서가 {archive_file}에 아카이브되었습니다."
    
    def generate_closure_report(self, scan_results: Dict) -> str:
        """세션 마감 리포트 생성"""
        total_files = sum(len(files) for files in scan_results.values())
        
        report = f"""
📊 **세션 마감 분석 결과**

**전체 파일 수**: {total_files}개

✅ **완료 문서** ({len(scan_results['completed'])}개):
"""
        
        for file_path, analysis in scan_results['completed']:
            report += f"  - {file_path.name} ({analysis['confidence']:.0%} 확신)\n"
        
        report += f"""
🔄 **진행중 문서** ({len(scan_results['in_progress'])}개):
"""
        for file_path, analysis in scan_results['in_progress']:
            report += f"  - {file_path.name} (유지)\n"
        
        report += f"""
📚 **보존 문서** ({len(scan_results['preserve'])}개):
"""
        for file_path, analysis in scan_results['preserve']:
            report += f"  - {file_path.name} (영구 보존)\n"
        
        if scan_results['uncertain']:
            report += f"""
❓ **불확실 문서** ({len(scan_results['uncertain'])}개):
"""
            for file_path, analysis in scan_results['uncertain']:
                report += f"  - {file_path.name} (수동 확인 필요)\n"
        
        return report

def main():
    """세션 마감 실행"""
    closure = SessionClosure()
    
    print("🔍 docs/CURRENT/ 디렉토리 분석 중...")
    scan_results = closure.scan_current_directory()
    
    # 분석 결과 출력
    print(closure.generate_closure_report(scan_results))
    
    # 완료 문서가 있으면 아카이브 여부 확인
    if scan_results['completed']:
        print(f"\n📦 {len(scan_results['completed'])}개의 완료 문서를 아카이브하시겠습니까?")
        print("⚠️  아카이브된 문서는 docs/development/sessions/에 이동되며 CURRENT에서 제거됩니다.")
        
        try:
            response = input("\n계속하시겠습니까? [Y/n]: ").strip().lower()
        except EOFError:
            # 비대화형 환경에서는 기본값 사용
            response = 'y'
            print("Y (자동 승인)")
        
        if response in ['y', 'yes', '']:
            result = closure.archive_completed_documents(scan_results['completed'])
            print(result)
            print("\n🎉 세션 마감이 완료되었습니다!")
        else:
            print("❌ 세션 마감이 취소되었습니다.")
    else:
        print("\n✅ 아카이브할 완료 문서가 없습니다. CURRENT 상태가 깨끗합니다!")

if __name__ == "__main__":
    main()