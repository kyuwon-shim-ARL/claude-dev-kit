#!/usr/bin/env python3
"""
Context Synchronization System
컨텍스트 자동 동기화 및 검증 시스템
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import json

class ContextSyncManager:
    """컨텍스트 동기화 관리자"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.claude_md_path = self.project_root / "CLAUDE.md"
        self.project_rules_path = self.project_root / "project_rules.md"
        
    def check_claude_init_availability(self) -> bool:
        """claude init 명령어 가용성 확인"""
        try:
            result = subprocess.run(
                ["claude", "--help"], 
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def run_claude_init(self, silent: bool = True) -> Tuple[bool, str]:
        """claude init 실행"""
        try:
            cmd = ["claude", "init"]
            
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return True, "CLAUDE.md updated successfully"
            else:
                return False, f"claude init failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "claude init timed out"
        except FileNotFoundError:
            return False, "claude command not found"
    
    def get_last_git_commit_time(self) -> datetime:
        """마지막 Git 커밋 시간 조회"""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ct"],
                capture_output=True, text=True, cwd=self.project_root
            )
            if result.returncode == 0:
                timestamp = int(result.stdout.strip())
                return datetime.fromtimestamp(timestamp)
        except (subprocess.SubprocessError, ValueError):
            pass
        return datetime.min
    
    def get_file_modification_time(self, filepath: Path) -> datetime:
        """파일 수정 시간 조회"""
        if filepath.exists():
            return datetime.fromtimestamp(filepath.stat().st_mtime)
        return datetime.min
    
    def is_claude_md_outdated(self) -> bool:
        """CLAUDE.md가 Git 커밋보다 오래된지 확인"""
        if not self.claude_md_path.exists():
            return True
            
        git_time = self.get_last_git_commit_time()
        claude_time = self.get_file_modification_time(self.claude_md_path)
        
        # Git 커밋이 5분 이상 최신이면 outdated
        return (git_time - claude_time).total_seconds() > 300
    
    def sync_claude_md(self) -> Dict:
        """CLAUDE.md 동기화"""
        sync_result = {
            "attempted": True,
            "success": False,
            "method": None,
            "message": "",
            "timestamp": datetime.now().isoformat()
        }
        
        # Claude CLI 가용성 확인
        if self.check_claude_init_availability():
            success, message = self.run_claude_init()
            sync_result.update({
                "success": success,
                "method": "claude_init",
                "message": message
            })
        else:
            # 폴백: 수동 업데이트 알림
            sync_result.update({
                "success": False,
                "method": "manual_required",
                "message": "Claude CLI not available. Manual update required."
            })
        
        return sync_result
    
    def validate_project_rules_completeness(self) -> Dict:
        """project_rules.md 완성도 검증"""
        if not self.project_rules_path.exists():
            return {
                "complete": False,
                "missing_sections": ["전체 파일 누락"],
                "recommendations": ["project_rules.md 파일 생성"]
            }
        
        with open(self.project_rules_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        essential_sections = ["목표", "원칙", "규칙", "가이드라인"]
        missing_sections = [
            section for section in essential_sections 
            if section not in content
        ]
        
        recommendations = []
        if missing_sections:
            recommendations.append(f"누락된 섹션 추가: {', '.join(missing_sections)}")
        
        if len(content) < 500:
            recommendations.append("상세한 내용 추가 (최소 500자)")
        
        return {
            "complete": len(missing_sections) == 0,
            "missing_sections": missing_sections,
            "recommendations": recommendations,
            "content_length": len(content)
        }
    
    def setup_git_hooks(self) -> Dict:
        """Git 훅 설정 및 업데이트"""
        hook_path = self.project_root / ".git/hooks/post-commit"
        
        hook_content = '''#!/bin/bash
# Context Auto-Sync: Post-commit hook

echo "🔄 Context synchronization check..."

# CLAUDE.md 동기화 확인
if command -v claude >/dev/null 2>&1; then
    echo "   📝 Updating CLAUDE.md..."
    claude init --silent
    if [[ $? -eq 0 ]]; then
        echo "   ✅ CLAUDE.md synchronized"
    else
        echo "   ⚠️ CLAUDE.md sync failed"
    fi
else
    echo "   ⚠️ Claude CLI not available - manual sync required"
fi

# 문서 메타데이터 업데이트
changed_docs=$(git diff --name-only HEAD~1 HEAD | grep '\\.md$')

if [[ -n "$changed_docs" ]]; then
    echo "   📝 Updating document metadata..."
    
    for doc in $changed_docs; do
        if [[ -f "$doc" ]]; then
            # 업데이트 시간 갱신
            if grep -q "updated:" "$doc"; then
                sed -i "s/updated: .*/updated: $(date +%Y-%m-%d)/" "$doc" 2>/dev/null
            fi
            echo "      ✅ Updated $doc"
        fi
    done
    
    # 메타데이터 변경사항을 다음 커밋에 포함
    git add $changed_docs 2>/dev/null
fi

echo "✅ Context synchronization completed"
'''
        
        try:
            hook_path.parent.mkdir(exist_ok=True)
            with open(hook_path, 'w') as f:
                f.write(hook_content)
            hook_path.chmod(0o755)
            
            return {
                "success": True,
                "message": "Git post-commit hook updated successfully",
                "path": str(hook_path)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update Git hook: {str(e)}",
                "path": str(hook_path)
            }
    
    def run_comprehensive_sync_check(self) -> Dict:
        """포괄적 동기화 상태 검사"""
        print("🔄 Running comprehensive context sync check...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "claude_md_sync": {},
            "project_rules_validation": {},
            "git_hooks_setup": {},
            "overall_status": "unknown"
        }
        
        # CLAUDE.md 동기화 검사
        if self.is_claude_md_outdated():
            print("   📝 CLAUDE.md is outdated, attempting sync...")
            results["claude_md_sync"] = self.sync_claude_md()
        else:
            results["claude_md_sync"] = {
                "attempted": False,
                "success": True,
                "message": "CLAUDE.md is up to date"
            }
        
        # project_rules.md 검증
        print("   📋 Validating project_rules.md...")
        results["project_rules_validation"] = self.validate_project_rules_completeness()
        
        # Git 훅 설정
        print("   ⚙️ Setting up Git hooks...")
        results["git_hooks_setup"] = self.setup_git_hooks()
        
        # 전체 상태 판정
        claude_ok = results["claude_md_sync"]["success"]
        rules_ok = results["project_rules_validation"]["complete"]
        hooks_ok = results["git_hooks_setup"]["success"]
        
        if claude_ok and rules_ok and hooks_ok:
            results["overall_status"] = "excellent"
        elif claude_ok and hooks_ok:
            results["overall_status"] = "good"
        else:
            results["overall_status"] = "needs_improvement"
        
        return results

def main():
    """메인 실행 함수"""
    sync_manager = ContextSyncManager()
    results = sync_manager.run_comprehensive_sync_check()
    
    # 결과 출력
    print("\n" + "="*50)
    print("🔄 CONTEXT SYNCHRONIZATION REPORT")
    print("="*50)
    
    # CLAUDE.md 상태
    claude_sync = results["claude_md_sync"]
    if claude_sync["attempted"]:
        status = "✅" if claude_sync["success"] else "❌"
        print(f"{status} CLAUDE.md Sync: {claude_sync['message']}")
    else:
        print("✅ CLAUDE.md Sync: Up to date")
    
    # project_rules.md 상태
    rules_check = results["project_rules_validation"]
    status = "✅" if rules_check["complete"] else "⚠️"
    print(f"{status} Project Rules: {'Complete' if rules_check['complete'] else 'Needs improvement'}")
    
    if rules_check["recommendations"]:
        for rec in rules_check["recommendations"][:2]:
            print(f"   • {rec}")
    
    # Git 훅 상태
    hooks_setup = results["git_hooks_setup"]
    status = "✅" if hooks_setup["success"] else "❌"
    print(f"{status} Git Hooks: {hooks_setup['message']}")
    
    # 전체 상태
    overall_emoji = {"excellent": "🎉", "good": "✅", "needs_improvement": "⚠️"}
    print(f"\n{overall_emoji.get(results['overall_status'], '❓')} Overall Status: {results['overall_status'].replace('_', ' ').title()}")
    
    # 상세 결과 저장
    report_path = Path("docs/CURRENT/context-sync-report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed report saved to: {report_path}")
    
    return 0 if results["overall_status"] in ["excellent", "good"] else 1

if __name__ == "__main__":
    exit(main())