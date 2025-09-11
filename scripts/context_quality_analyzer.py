#!/usr/bin/env python3
"""
컨텍스트 품질 분석기
프로젝트의 컨텍스트 일관성, 완성도, 최신성을 자동 분석
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

class ContextQualityAnalyzer:
    """컨텍스트 품질 분석기"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.analysis_results = {}
        
    def analyze_context_hierarchy(self) -> Dict:
        """3단계 컨텍스트 계층 분석"""
        hierarchy = {
            "strategic": self._analyze_strategic_context(),
            "tactical": self._analyze_tactical_context(), 
            "operational": self._analyze_operational_context()
        }
        
        return hierarchy
    
    def _analyze_strategic_context(self) -> Dict:
        """전략적 컨텍스트 (project_rules.md) 분석"""
        project_rules_paths = [
            self.project_root / "project_rules.md",
            self.project_root / "docs/specs/project_rules.md"
        ]
        
        found_rules = None
        for path in project_rules_paths:
            if path.exists():
                found_rules = path
                break
        
        if not found_rules:
            return {
                "status": "missing",
                "score": 0,
                "issues": ["project_rules.md not found in standard locations"],
                "recommendations": ["Create project_rules.md with core principles"]
            }
        
        # 내용 분석
        with open(found_rules, 'r', encoding='utf-8') as f:
            content = f.read()
        
        score = 0
        issues = []
        recommendations = []
        
        # 필수 섹션 체크
        essential_sections = ["목표", "원칙", "규칙", "가이드라인"]
        present_sections = sum(1 for section in essential_sections if section in content)
        score += (present_sections / len(essential_sections)) * 60
        
        if present_sections < len(essential_sections):
            issues.append(f"필수 섹션 부족: {len(essential_sections) - present_sections}개 누락")
            recommendations.append("누락된 필수 섹션 추가")
        
        # 문서 크기 체크 (너무 짧거나 길면 안됨)
        if len(content) < 500:
            score -= 10
            issues.append("문서가 너무 간략함")
            recommendations.append("상세한 가이드라인 추가")
        elif len(content) > 10000:
            score -= 5
            issues.append("문서가 너무 장황함") 
            recommendations.append("핵심 내용으로 압축")
        else:
            score += 20
        
        # 최신성 체크
        mod_time = datetime.fromtimestamp(found_rules.stat().st_mtime)
        days_old = (datetime.now() - mod_time).days
        
        if days_old < 30:
            score += 20
        elif days_old < 90:
            score += 10
            issues.append("문서가 90일 이상 업데이트되지 않음")
            recommendations.append("최신 상황에 맞게 업데이트")
        else:
            issues.append(f"문서가 {days_old}일 동안 업데이트되지 않음")
            recommendations.append("긴급 업데이트 필요")
        
        return {
            "status": "found",
            "path": str(found_rules),
            "score": min(100, max(0, score)),
            "size": len(content),
            "last_modified": mod_time.isoformat(),
            "days_since_update": days_old,
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _analyze_tactical_context(self) -> Dict:
        """전술적 컨텍스트 (CLAUDE.md) 분석"""
        claude_md_path = self.project_root / "CLAUDE.md"
        
        if not claude_md_path.exists():
            return {
                "status": "missing",
                "score": 0,
                "issues": ["CLAUDE.md not found"],
                "recommendations": ["Run 'claude init' to generate CLAUDE.md"]
            }
        
        with open(claude_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        score = 0
        issues = []
        recommendations = []
        
        # 필수 섹션 체크
        essential_sections = ["Project Overview", "Structure", "Commands", "Usage"]
        present_sections = sum(1 for section in essential_sections 
                             if section.lower() in content.lower())
        score += (present_sections / len(essential_sections)) * 50
        
        # 메타데이터 존재 체크
        if "@meta" in content:
            score += 10
        else:
            issues.append("메타데이터 누락")
            recommendations.append("문서 메타데이터 추가")
        
        # Git 상태와 동기화 체크
        mod_time = datetime.fromtimestamp(claude_md_path.stat().st_mtime)
        git_last_commit = self._get_last_git_commit_time()
        
        if git_last_commit and mod_time >= git_last_commit - timedelta(minutes=5):
            score += 20
            sync_status = "synchronized"
        else:
            score += 5
            sync_status = "outdated"
            issues.append("Git 커밋과 동기화되지 않음")
            recommendations.append("claude init 실행으로 동기화")
        
        # 크기 적정성 체크
        if 1000 <= len(content) <= 50000:
            score += 20
        else:
            issues.append("문서 크기 부적절")
            recommendations.append("적정 크기로 조정")
        
        return {
            "status": "found",
            "path": str(claude_md_path),
            "score": min(100, score),
            "size": len(content),
            "last_modified": mod_time.isoformat(),
            "sync_status": sync_status,
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _analyze_operational_context(self) -> Dict:
        """운영적 컨텍스트 (docs/CURRENT/) 분석"""
        current_dir = self.project_root / "docs/CURRENT"
        
        if not current_dir.exists():
            return {
                "status": "missing",
                "score": 0,
                "issues": ["docs/CURRENT/ directory not found"],
                "recommendations": ["Create docs/CURRENT/ directory for active work"]
            }
        
        files = list(current_dir.glob("*.md"))
        
        score = 0
        issues = []
        recommendations = []
        
        # 파일 개수 체크
        if len(files) >= 5:
            score += 30
        elif len(files) >= 2:
            score += 20
        else:
            issues.append(f"활성 문서 부족: {len(files)}개")
            recommendations.append("현재 작업 문서 추가")
        
        # 최신성 체크
        recent_files = 0
        for file_path in files:
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            if (datetime.now() - mod_time).days < 7:
                recent_files += 1
        
        if recent_files >= len(files) * 0.5:
            score += 30
        else:
            issues.append("최신 문서 부족")
            recommendations.append("활발히 관리되는 문서 증가")
        
        # 필수 파일 체크  
        essential_files = ["status.md", "active-todos.md"]
        present_essential = sum(1 for ef in essential_files 
                              if any(ef in f.name for f in files))
        score += (present_essential / len(essential_files)) * 40
        
        if present_essential < len(essential_files):
            missing = [ef for ef in essential_files 
                      if not any(ef in f.name for f in files)]
            issues.append(f"필수 파일 누락: {', '.join(missing)}")
            recommendations.append("필수 파일 생성")
        
        return {
            "status": "found",
            "path": str(current_dir),
            "score": min(100, score),
            "file_count": len(files),
            "recent_file_count": recent_files,
            "files": [f.name for f in files],
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _get_last_git_commit_time(self) -> Optional[datetime]:
        """마지막 Git 커밋 시간"""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ct"],
                capture_output=True, text=True, cwd=self.project_root
            )
            if result.returncode == 0:
                timestamp = int(result.stdout.strip())
                return datetime.fromtimestamp(timestamp)
        except:
            pass
        return None
    
    def calculate_overall_score(self, hierarchy: Dict) -> Dict:
        """전체 품질 점수 계산"""
        weights = {"strategic": 0.4, "tactical": 0.35, "operational": 0.25}
        
        total_score = 0
        for level, weight in weights.items():
            level_score = hierarchy[level]["score"]
            total_score += level_score * weight
        
        # 등급 계산
        if total_score >= 90:
            grade = "A"
            status = "excellent"
        elif total_score >= 80:
            grade = "B"
            status = "good"
        elif total_score >= 70:
            grade = "C"
            status = "acceptable"
        elif total_score >= 60:
            grade = "D"
            status = "needs_improvement"
        else:
            grade = "F"
            status = "critical"
        
        return {
            "total_score": round(total_score, 1),
            "grade": grade,
            "status": status,
            "breakdown": {
                level: {"score": hierarchy[level]["score"], "weight": weight}
                for level, weight in weights.items()
            }
        }
    
    def generate_report(self) -> Dict:
        """종합 분석 리포트 생성"""
        print("🔍 Analyzing project context quality...")
        
        hierarchy = self.analyze_context_hierarchy()
        overall = self.calculate_overall_score(hierarchy)
        
        # 전체 이슈 및 추천사항 수집
        all_issues = []
        all_recommendations = []
        
        for level_name, level_data in hierarchy.items():
            for issue in level_data.get("issues", []):
                all_issues.append(f"{level_name.title()}: {issue}")
            for rec in level_data.get("recommendations", []):
                all_recommendations.append(f"{level_name.title()}: {rec}")
        
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "overall_quality": overall,
            "context_hierarchy": hierarchy,
            "issues": all_issues,
            "recommendations": all_recommendations,
            "next_actions": self._generate_next_actions(overall, all_issues)
        }
        
        return report
    
    def _generate_next_actions(self, overall: Dict, issues: List[str]) -> List[str]:
        """다음 액션 제안"""
        actions = []
        
        if overall["total_score"] < 60:
            actions.append("🚨 긴급: 기본 컨텍스트 구조 구축")
        
        if any("missing" in issue.lower() for issue in issues):
            actions.append("📝 누락된 핵심 문서 생성")
            
        if any("outdated" in issue.lower() or "업데이트" in issue for issue in issues):
            actions.append("🔄 기존 문서 업데이트")
            
        if any("동기화" in issue for issue in issues):
            actions.append("⚙️ 자동 동기화 시스템 설정")
            
        return actions
    
    def print_dashboard(self, report: Dict):
        """컨텍스트 품질 대시보드 출력"""
        print("\n" + "="*60)
        print("📊 CONTEXT QUALITY DASHBOARD")
        print("="*60)
        
        overall = report["overall_quality"]
        print(f"🎯 Overall Score: {overall['grade']} ({overall['total_score']}/100)")
        print(f"📈 Status: {overall['status'].replace('_', ' ').title()}")
        print()
        
        # 계층별 점수
        for level_name, level_data in report["context_hierarchy"].items():
            emoji = {"strategic": "🎯", "tactical": "⚡", "operational": "🔧"}
            print(f"{emoji.get(level_name, '📋')} {level_name.title()}: "
                  f"{level_data['score']}/100 ({level_data['status']})")
        
        print()
        
        # 주요 이슈
        if report["issues"]:
            print("⚠️  Issues Found:")
            for issue in report["issues"][:5]:
                print(f"   • {issue}")
            if len(report["issues"]) > 5:
                print(f"   ... and {len(report['issues']) - 5} more issues")
            print()
        
        # 다음 액션
        if report["next_actions"]:
            print("🚀 Next Actions:")
            for action in report["next_actions"]:
                print(f"   {action}")
        
        print("="*60)

def main():
    """메인 실행"""
    analyzer = ContextQualityAnalyzer()
    report = analyzer.generate_report()
    
    # 대시보드 출력
    analyzer.print_dashboard(report)
    
    # 리포트 저장
    report_path = Path("docs/CURRENT/context-quality-report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed report saved to: {report_path}")
    
    # 점수에 따른 exit code
    if report["overall_quality"]["total_score"] < 60:
        return 1
    return 0

if __name__ == "__main__":
    exit(main())