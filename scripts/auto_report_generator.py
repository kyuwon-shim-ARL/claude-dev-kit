#!/usr/bin/env python3
"""
Auto Report Generator v1.0
기획-구현-결과를 자동으로 추적하여 보고서 생성하는 시스템

핵심 원리:
1. Git 커밋 기반 자동 진행상황 추적
2. TODO 변화 기반 단계별 정리
3. 코드 변화 분석으로 핵심 성과 추출
4. 자동 템플릿 기반 보고서 생성
"""

import os
import json
import datetime
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

class AutoReportGenerator:
    """자동 보고서 생성 시스템"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.getcwd())
        self.setup_logging()
        
    def setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def extract_planning_context(self) -> Dict[str, Any]:
        """기획 컨텍스트 자동 추출"""
        context = {
            'objectives': [],
            'requirements': [],
            'approach': [],
            'scope': ''
        }
        
        # PRD 파일에서 목표 추출
        prd_files = list(self.project_root.glob('docs/CURRENT/*Specification*.md'))
        prd_files.extend(list(self.project_root.glob('docs/specs/PRD*.md')))
        
        for prd_file in prd_files:
            if prd_file.exists():
                content = prd_file.read_text(encoding='utf-8')
                
                # 목적/목표 추출
                objectives = self._extract_section(content, '목적|목표|Purpose|Objective')
                if objectives:
                    context['objectives'].extend(objectives)
                
                # 접근방법 추출
                approach = self._extract_section(content, '접근|방법론|Approach|Methodology')
                if approach:
                    context['approach'].extend(approach)
                
                # 범위 추출
                scope = self._extract_section(content, '범위|Scope')
                if scope:
                    context['scope'] = scope[0] if scope else ''
                
                break
        
        return context
    
    def extract_implementation_progress(self) -> Dict[str, Any]:
        """구현 진행상황 자동 추출"""
        
        # Git 커밋 분석
        commits = self._get_recent_commits()
        
        # 파일 변화 분석
        file_changes = self._analyze_file_changes()
        
        # TODO 진행상황
        todo_progress = self._get_todo_progress()
        
        return {
            'commits': commits,
            'file_changes': file_changes,
            'todo_progress': todo_progress,
            'key_achievements': self._identify_key_achievements(commits, file_changes)
        }
    
    def extract_results_and_outcomes(self) -> Dict[str, Any]:
        """결과 및 성과 자동 추출"""
        
        results = {
            'deliverables': [],
            'code_metrics': {},
            'test_results': {},
            'performance_metrics': {}
        }
        
        # 산출물 식별
        deliverables = self._identify_deliverables()
        results['deliverables'] = deliverables
        
        # 코드 메트릭스
        results['code_metrics'] = self._calculate_code_metrics()
        
        # 테스트 결과 (있다면)
        results['test_results'] = self._get_test_results()
        
        return results
    
    def generate_auto_report(self, title: str = None) -> str:
        """자동 보고서 생성 (메인 함수)"""
        
        # 1. 컨텍스트 수집
        planning_context = self.extract_planning_context()
        implementation_progress = self.extract_implementation_progress()
        results = self.extract_results_and_outcomes()
        
        # 2. 보고서 생성
        report_content = self._generate_report_content(
            title or "프로젝트 자동 진행 보고서",
            planning_context,
            implementation_progress,
            results
        )
        
        # 3. 저장
        report_path = self._save_report(report_content)
        
        self.logger.info(f"✅ 자동 보고서 생성 완료: {report_path}")
        return report_path
    
    def _extract_section(self, content: str, section_pattern: str) -> List[str]:
        """마크다운에서 특정 섹션 추출"""
        import re
        
        lines = content.split('\n')
        in_section = False
        section_lines = []
        
        section_regex = re.compile(rf'#{1,4}\s*.*({section_pattern})', re.IGNORECASE)
        
        for line in lines:
            if section_regex.search(line):
                in_section = True
                continue
            elif line.startswith('#') and in_section:
                break
            elif in_section and line.strip():
                # 불필요한 마크다운 문법 제거
                clean_line = re.sub(r'[*_`]', '', line.strip())
                if clean_line and not clean_line.startswith('-'):
                    section_lines.append(clean_line)
        
        return section_lines[:3]  # 최대 3개만 추출
    
    def _get_recent_commits(self, limit: int = 10) -> List[Dict[str, str]]:
        """최근 커밋 정보 조회"""
        try:
            cmd = ['git', 'log', f'--max-count={limit}', '--pretty=format:%h|%s|%ad', '--date=short']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            commits = []
            for line in result.stdout.split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        commits.append({
                            'hash': parts[0],
                            'message': parts[1],
                            'date': parts[2]
                        })
            return commits
        except:
            return []
    
    def _analyze_file_changes(self) -> Dict[str, int]:
        """파일 변화 분석"""
        try:
            # 최근 변경된 파일들
            cmd = ['git', 'diff', '--name-status', 'HEAD~5..HEAD']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            changes = {'added': 0, 'modified': 0, 'deleted': 0}
            for line in result.stdout.split('\n'):
                if line:
                    status = line[0]
                    if status == 'A':
                        changes['added'] += 1
                    elif status == 'M':
                        changes['modified'] += 1
                    elif status == 'D':
                        changes['deleted'] += 1
            
            return changes
        except:
            return {'added': 0, 'modified': 0, 'deleted': 0}
    
    def _get_todo_progress(self) -> Dict[str, Any]:
        """TODO 진행상황 분석"""
        
        # .claude/tracking/current.json에서 TODO 상태 읽기
        current_file = self.project_root / '.claude/tracking/current.json'
        if not current_file.exists():
            return {'total': 0, 'completed': 0, 'in_progress': 0, 'pending': 0}
        
        try:
            with open(current_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            todos = data.get('todos', [])
            progress = {'total': len(todos), 'completed': 0, 'in_progress': 0, 'pending': 0}
            
            for todo in todos:
                status = todo.get('status', 'pending')
                progress[status] = progress.get(status, 0) + 1
            
            return progress
        except:
            return {'total': 0, 'completed': 0, 'in_progress': 0, 'pending': 0}
    
    def _identify_key_achievements(self, commits: List[Dict], file_changes: Dict) -> List[str]:
        """핵심 성과 식별"""
        achievements = []
        
        # 커밋 메시지에서 주요 성과 추출
        for commit in commits[:5]:  # 최근 5개
            message = commit['message'].lower()
            if any(keyword in message for keyword in ['feat:', 'add:', 'implement', '구현', '완료', '추가']):
                # feat: 접두사 제거하고 정리
                clean_message = commit['message'].replace('feat:', '').replace('add:', '').strip()
                if clean_message and len(clean_message) > 10:
                    achievements.append(f"✅ {clean_message}")
        
        # 파일 변화량이 많으면 주요 개발로 간주
        total_changes = sum(file_changes.values())
        if total_changes > 10:
            achievements.append(f"📊 {total_changes}개 파일 변경으로 대규모 개발 완료")
        
        return achievements[:5]  # 최대 5개만
    
    def _identify_deliverables(self) -> List[str]:
        """산출물 자동 식별"""
        deliverables = []
        
        # 주요 산출물 패턴 확인
        patterns = {
            'Python Scripts': '**/*.py',
            'Documentation': ['**/*.md', '**/*.rst'],
            'Configuration': ['**/*.json', '**/*.yml', '**/*.yaml'],
            'Tests': ['**/test_*.py', '**/*_test.py'],
            'Data Files': ['**/*.xlsx', '**/*.csv', '**/*.json']
        }
        
        for category, pattern in patterns.items():
            if isinstance(pattern, list):
                count = sum(len(list(self.project_root.glob(p))) for p in pattern)
            else:
                count = len(list(self.project_root.glob(pattern)))
            
            if count > 0:
                deliverables.append(f"{category}: {count}개 파일")
        
        return deliverables
    
    def _calculate_code_metrics(self) -> Dict[str, int]:
        """코드 메트릭스 계산"""
        metrics = {'total_lines': 0, 'python_files': 0, 'functions': 0}
        
        for py_file in self.project_root.glob('**/*.py'):
            if '.git' in str(py_file) or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                lines = len(content.split('\n'))
                functions = content.count('def ')
                
                metrics['total_lines'] += lines
                metrics['python_files'] += 1
                metrics['functions'] += functions
            except:
                continue
        
        return metrics
    
    def _get_test_results(self) -> Dict[str, Any]:
        """테스트 결과 조회 (pytest 기반)"""
        try:
            # pytest 결과가 있다면 조회
            cmd = ['pytest', '--tb=no', '--quiet', '--no-header']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                return {'status': 'PASS', 'details': 'All tests passed'}
            else:
                return {'status': 'FAIL', 'details': result.stdout}
        except:
            return {'status': 'N/A', 'details': 'No test results available'}
    
    def _generate_report_content(
        self, 
        title: str, 
        planning: Dict, 
        implementation: Dict, 
        results: Dict
    ) -> str:
        """보고서 내용 생성"""
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""# {title}

**생성일시**: {timestamp}
**자동생성**: Auto Report Generator v1.0

## 📋 요약

{self._generate_executive_summary(planning, implementation, results)}

## 🎯 기획 단계 (Planning)

### 목표 및 요구사항
{self._format_list(planning.get('objectives', ['목표 정보 없음']))}

### 접근 방법
{self._format_list(planning.get('approach', ['접근방법 정보 없음']))}

### 프로젝트 범위
{planning.get('scope', '범위 정보 없음')}

## 🔧 구현 단계 (Implementation)

### 주요 성과
{self._format_list(implementation.get('key_achievements', ['주요 성과 없음']))}

### 개발 진행상황
- **커밋 수**: {len(implementation.get('commits', []))}개
- **파일 변경**: 추가 {implementation.get('file_changes', {}).get('added', 0)}개, 수정 {implementation.get('file_changes', {}).get('modified', 0)}개
- **TODO 진행률**: {self._calculate_todo_completion(implementation.get('todo_progress', {}))}

### 최근 커밋 이력
{self._format_commits(implementation.get('commits', [])[:5])}

## 📊 결과 단계 (Results)

### 산출물
{self._format_list(results.get('deliverables', ['산출물 정보 없음']))}

### 코드 메트릭스
{self._format_code_metrics(results.get('code_metrics', {}))}

### 테스트 결과
**상태**: {results.get('test_results', {}).get('status', 'N/A')}

## 🎉 결론 및 다음 단계

{self._generate_conclusion(implementation, results)}

---
*이 보고서는 Git 이력, TODO 진행상황, 코드 변화를 자동 분석하여 생성되었습니다.*
"""
        return report
    
    def _generate_executive_summary(self, planning: Dict, implementation: Dict, results: Dict) -> str:
        """요약 자동 생성"""
        
        todo_progress = implementation.get('todo_progress', {})
        completed = todo_progress.get('completed', 0)
        total = todo_progress.get('total', 0)
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        file_changes = implementation.get('file_changes', {})
        total_changes = sum(file_changes.values())
        
        summary = f"""
프로젝트 진행률 **{completion_rate:.1f}%** 달성
- {len(implementation.get('key_achievements', []))}개 주요 성과 완료
- {total_changes}개 파일 변경으로 활발한 개발 진행
- {len(results.get('deliverables', []))}개 카테고리 산출물 생성
        """.strip()
        
        return summary
    
    def _format_list(self, items: List[str]) -> str:
        """리스트 포맷팅"""
        if not items:
            return "- 정보 없음"
        return '\n'.join(f"- {item}" for item in items[:5])  # 최대 5개만
    
    def _format_commits(self, commits: List[Dict]) -> str:
        """커밋 포맷팅"""
        if not commits:
            return "- 최근 커밋 정보 없음"
        
        formatted = []
        for commit in commits:
            formatted.append(f"- `{commit['hash']}` {commit['message']} ({commit['date']})")
        
        return '\n'.join(formatted)
    
    def _calculate_todo_completion(self, todo_progress: Dict) -> str:
        """TODO 완료율 계산"""
        total = todo_progress.get('total', 0)
        completed = todo_progress.get('completed', 0)
        
        if total == 0:
            return "0% (TODO 없음)"
        
        rate = completed / total * 100
        return f"{rate:.1f}% ({completed}/{total})"
    
    def _format_code_metrics(self, metrics: Dict) -> str:
        """코드 메트릭스 포맷팅"""
        if not metrics or not any(metrics.values()):
            return "- 코드 메트릭스 정보 없음"
        
        return f"""- **Python 파일**: {metrics.get('python_files', 0)}개
- **총 라인 수**: {metrics.get('total_lines', 0):,}줄
- **함수 수**: {metrics.get('functions', 0)}개"""
    
    def _generate_conclusion(self, implementation: Dict, results: Dict) -> str:
        """결론 자동 생성"""
        
        achievements_count = len(implementation.get('key_achievements', []))
        deliverables_count = len(results.get('deliverables', []))
        
        if achievements_count >= 3 and deliverables_count >= 3:
            return "프로젝트가 성공적으로 진행되어 주요 목표들이 달성되었습니다. 다음 단계로 테스트 및 배포를 준비할 수 있습니다."
        elif achievements_count >= 1:
            return "프로젝트가 순조롭게 진행되고 있으며, 추가 개발을 통해 목표 완성도를 높일 수 있습니다."
        else:
            return "프로젝트 초기 단계로, 지속적인 개발과 모니터링이 필요합니다."
    
    def _save_report(self, content: str) -> str:
        """보고서 저장"""
        
        # reports 디렉토리 생성
        reports_dir = self.project_root / 'docs' / 'reports'
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # 파일명 생성 (타임스탬프 포함)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"auto_progress_report_{timestamp}.md"
        
        report_path = reports_dir / filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(report_path)


def main():
    """메인 실행 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='자동 보고서 생성')
    parser.add_argument('--title', default='프로젝트 자동 진행 보고서', help='보고서 제목')
    parser.add_argument('--project-root', help='프로젝트 루트 디렉토리')
    
    args = parser.parse_args()
    
    generator = AutoReportGenerator(args.project_root)
    report_path = generator.generate_auto_report(args.title)
    
    print(f"✅ 자동 보고서 생성 완료!")
    print(f"📄 파일 위치: {report_path}")
    print(f"🔍 확인: cat '{report_path}'")


if __name__ == "__main__":
    main()