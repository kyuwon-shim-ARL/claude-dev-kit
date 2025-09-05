#!/usr/bin/env python3
"""
Context Filtering and Optimization System
컨텍스트 필터링 및 최적화 시스템
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json
import subprocess
from datetime import datetime

class ContextOptimizer:
    """컨텍스트 최적화 시스템"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.claudeignore_path = self.project_root / ".claudeignore"
        
        # 기본 필터링 규칙
        self.default_ignore_patterns = [
            # Build outputs
            "*.pyc", "__pycache__/", "*.pyo", "*.pyd", ".Python",
            "build/", "develop-eggs/", "dist/", "downloads/", "eggs/",
            ".eggs/", "lib/", "lib64/", "parts/", "sdist/", "var/",
            "wheels/", "*.egg-info/", ".installed.cfg", "*.egg",
            
            # Node.js
            "node_modules/", "npm-debug.log*", "yarn-debug.log*",
            "yarn-error.log*", ".npm", ".yarn-integrity",
            
            # IDE and editors
            ".vscode/", ".idea/", "*.swp", "*.swo", "*~", ".DS_Store",
            
            # Version control
            ".git/", ".svn/", ".hg/", ".bzr/",
            
            # Logs and temporary files
            "*.log", "logs/", "*.tmp", "*.temp", ".cache/", ".pytest_cache/",
            
            # Environment and secrets
            ".env", ".env.local", ".env.*.local", "*.key", "*.pem",
            
            # OS generated
            "Thumbs.db", "ehthumbs.db", "Desktop.ini",
            
            # Large data files
            "*.csv", "*.xlsx", "*.json", "*.xml", "*.sql",
            
            # Images and media (저장소 크기 고려)
            "*.jpg", "*.jpeg", "*.png", "*.gif", "*.svg", "*.ico",
            "*.mp3", "*.mp4", "*.avi", "*.mov", "*.pdf",
        ]
        
        # 중요도 기반 파일 분류
        self.file_priority = {
            "critical": [".md", ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css"],
            "important": [".json", ".yaml", ".yml", ".toml", ".cfg", ".ini"],
            "optional": [".txt", ".log", ".md~", ".bak"]
        }
    
    def analyze_project_structure(self) -> Dict:
        """프로젝트 구조 분석"""
        analysis = {
            "total_files": 0,
            "total_size_mb": 0,
            "file_types": {},
            "large_files": [],  # >1MB
            "deep_directories": [],  # depth > 5
            "potential_bloat": []
        }
        
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            depth = len(root_path.parts) - len(self.project_root.parts)
            
            if depth > 5:
                analysis["deep_directories"].append(str(root_path))
            
            for file in files:
                file_path = root_path / file
                if not file_path.exists():
                    continue
                    
                try:
                    file_size = file_path.stat().st_size
                    analysis["total_files"] += 1
                    analysis["total_size_mb"] += file_size / (1024 * 1024)
                    
                    # 파일 유형별 분류
                    suffix = file_path.suffix.lower()
                    analysis["file_types"][suffix] = analysis["file_types"].get(suffix, 0) + 1
                    
                    # 큰 파일 감지 (1MB 이상)
                    if file_size > 1024 * 1024:
                        analysis["large_files"].append({
                            "path": str(file_path),
                            "size_mb": round(file_size / (1024 * 1024), 2)
                        })
                    
                    # 잠재적 bloat 감지
                    if self._is_potential_bloat(file_path):
                        analysis["potential_bloat"].append(str(file_path))
                        
                except (OSError, PermissionError):
                    continue
        
        return analysis
    
    def _is_potential_bloat(self, file_path: Path) -> bool:
        """잠재적 bloat 파일 감지"""
        bloat_patterns = [
            r"\.tmp$", r"\.temp$", r"\.bak$", r"\.old$",
            r"\.cache", r"__pycache__", r"node_modules",
            r"\.pyc$", r"\.pyo$", r"\.pyd$",
            r"~$", r"\.swp$", r"\.swo$"
        ]
        
        file_str = str(file_path)
        return any(re.search(pattern, file_str, re.IGNORECASE) for pattern in bloat_patterns)
    
    def generate_optimal_claudeignore(self) -> List[str]:
        """최적화된 .claudeignore 생성"""
        analysis = self.analyze_project_structure()
        
        ignore_patterns = self.default_ignore_patterns.copy()
        
        # 프로젝트별 맞춤 규칙
        if analysis["file_types"].get(".py", 0) > 10:  # Python 프로젝트
            ignore_patterns.extend([
                "venv/", "env/", ".venv/", "ENV/",
                "pip-log.txt", "pip-delete-this-directory.txt",
                ".coverage", "htmlcov/", ".pytest_cache/",
                "*.so", "*.dylib", "*.dll"
            ])
        
        if analysis["file_types"].get(".js", 0) > 10 or analysis["file_types"].get(".ts", 0) > 10:
            ignore_patterns.extend([
                "coverage/", ".nyc_output/", "*.tgz", "*.tar.gz",
                ".eslintcache", ".parcel-cache/"
            ])
        
        # 큰 파일들 자동 제외
        for large_file in analysis["large_files"]:
            if large_file["size_mb"] > 5:  # 5MB 이상
                ignore_patterns.append(large_file["path"])
        
        # 중복 제거 및 정렬
        unique_patterns = sorted(list(set(ignore_patterns)))
        
        return unique_patterns
    
    def estimate_context_savings(self) -> Dict:
        """컨텍스트 절약 효과 추정"""
        analysis = self.analyze_project_structure()
        ignore_patterns = self.generate_optimal_claudeignore()
        
        # 제외될 파일 크기 계산
        excluded_size = 0
        excluded_files = 0
        
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                file_path = Path(root) / file
                if self._should_ignore(file_path, ignore_patterns):
                    try:
                        excluded_size += file_path.stat().st_size
                        excluded_files += 1
                    except (OSError, PermissionError):
                        continue
        
        total_size = analysis["total_size_mb"] * 1024 * 1024
        savings_percentage = (excluded_size / total_size * 100) if total_size > 0 else 0
        
        return {
            "total_files": analysis["total_files"],
            "excluded_files": excluded_files,
            "remaining_files": analysis["total_files"] - excluded_files,
            "total_size_mb": analysis["total_size_mb"],
            "excluded_size_mb": excluded_size / (1024 * 1024),
            "remaining_size_mb": (total_size - excluded_size) / (1024 * 1024),
            "savings_percentage": round(savings_percentage, 1),
            "context_efficiency": "excellent" if savings_percentage > 70 else "good" if savings_percentage > 50 else "needs_improvement"
        }
    
    def _should_ignore(self, file_path: Path, ignore_patterns: List[str]) -> bool:
        """파일이 무시되어야 하는지 확인"""
        file_str = str(file_path)
        
        for pattern in ignore_patterns:
            if pattern.endswith("/"):
                # 디렉토리 패턴
                if f"/{pattern}" in f"/{file_str}/" or file_str.endswith(pattern[:-1]):
                    return True
            elif "*" in pattern:
                # 글로브 패턴
                import fnmatch
                if fnmatch.fnmatch(file_str, pattern) or fnmatch.fnmatch(file_path.name, pattern):
                    return True
            else:
                # 정확한 매치
                if pattern in file_str or file_path.name == pattern:
                    return True
        
        return False
    
    def create_context_priority_map(self) -> Dict:
        """컨텍스트 우선순위 맵 생성"""
        priority_map = {
            "critical": [],
            "important": [], 
            "optional": [],
            "exclude": []
        }
        
        ignore_patterns = self.generate_optimal_claudeignore()
        
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                file_path = Path(root) / file
                
                if self._should_ignore(file_path, ignore_patterns):
                    priority_map["exclude"].append(str(file_path))
                    continue
                
                suffix = file_path.suffix.lower()
                
                if suffix in self.file_priority["critical"]:
                    priority_map["critical"].append(str(file_path))
                elif suffix in self.file_priority["important"]:
                    priority_map["important"].append(str(file_path))
                else:
                    priority_map["optional"].append(str(file_path))
        
        return priority_map
    
    def update_claudeignore(self) -> Dict:
        """claudeignore 파일 업데이트"""
        optimal_patterns = self.generate_optimal_claudeignore()
        
        # 기존 사용자 정의 패턴 보존
        existing_custom_patterns = []
        if self.claudeignore_path.exists():
            with open(self.claudeignore_path, 'r') as f:
                content = f.read()
                # 사용자 정의 섹션 찾기
                if "# Custom patterns" in content:
                    custom_section = content.split("# Custom patterns")[1]
                    existing_custom_patterns = [
                        line.strip() for line in custom_section.strip().split('\n')
                        if line.strip() and not line.startswith('#')
                    ]
        
        # 새로운 .claudeignore 생성
        new_content = []
        new_content.append("# Auto-generated by Context Optimization System")
        new_content.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        new_content.append("")
        
        new_content.append("# Build outputs and dependencies")
        for pattern in optimal_patterns:
            if any(keyword in pattern.lower() for keyword in ["build", "dist", "node_modules", "__pycache__"]):
                new_content.append(pattern)
        
        new_content.append("")
        new_content.append("# Temporary and cache files")
        for pattern in optimal_patterns:
            if any(keyword in pattern.lower() for keyword in ["tmp", "cache", "log", "bak"]):
                new_content.append(pattern)
        
        new_content.append("")
        new_content.append("# IDE and OS files")
        for pattern in optimal_patterns:
            if any(keyword in pattern.lower() for keyword in ["vscode", "idea", "ds_store", "thumbs"]):
                new_content.append(pattern)
        
        if existing_custom_patterns:
            new_content.append("")
            new_content.append("# Custom patterns")
            new_content.extend(existing_custom_patterns)
        
        with open(self.claudeignore_path, 'w') as f:
            f.write('\n'.join(new_content))
        
        return {
            "success": True,
            "path": str(self.claudeignore_path),
            "patterns_count": len(optimal_patterns),
            "custom_patterns_preserved": len(existing_custom_patterns)
        }
    
    def run_optimization(self) -> Dict:
        """전체 컨텍스트 최적화 실행"""
        print("🔧 Running context optimization...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "project_analysis": self.analyze_project_structure(),
            "context_savings": self.estimate_context_savings(),
            "priority_map": self.create_context_priority_map(),
            "claudeignore_update": self.update_claudeignore()
        }
        
        return results

def main():
    """메인 실행 함수"""
    optimizer = ContextOptimizer()
    results = optimizer.run_optimization()
    
    # 결과 출력
    print("\n" + "="*60)
    print("🔧 CONTEXT OPTIMIZATION REPORT")
    print("="*60)
    
    analysis = results["project_analysis"]
    savings = results["context_savings"]
    
    print(f"📊 Project Analysis:")
    print(f"   Total files: {analysis['total_files']}")
    print(f"   Total size: {analysis['total_size_mb']:.1f} MB")
    print(f"   File types: {len(analysis['file_types'])} different types")
    
    if analysis["large_files"]:
        print(f"   Large files: {len(analysis['large_files'])} files > 1MB")
    
    print(f"\n💾 Context Optimization:")
    print(f"   Files to exclude: {savings['excluded_files']} ({savings['savings_percentage']}%)")
    print(f"   Context size reduction: {savings['excluded_size_mb']:.1f} MB")
    print(f"   Efficiency: {savings['context_efficiency'].replace('_', ' ').title()}")
    
    priority_map = results["priority_map"]
    print(f"\n🎯 Priority Distribution:")
    print(f"   Critical files: {len(priority_map['critical'])}")
    print(f"   Important files: {len(priority_map['important'])}")
    print(f"   Optional files: {len(priority_map['optional'])}")
    print(f"   Excluded files: {len(priority_map['exclude'])}")
    
    claudeignore_update = results["claudeignore_update"]
    status = "✅" if claudeignore_update["success"] else "❌"
    print(f"\n{status} .claudeignore: Updated with {claudeignore_update['patterns_count']} patterns")
    
    if claudeignore_update["custom_patterns_preserved"] > 0:
        print(f"   Custom patterns preserved: {claudeignore_update['custom_patterns_preserved']}")
    
    # 권장사항
    if savings['savings_percentage'] < 50:
        print(f"\n💡 Recommendations:")
        print(f"   - Consider excluding more file types")
        print(f"   - Review large files for necessity")
        
    if analysis["deep_directories"]:
        print(f"   - Simplify deep directory structures ({len(analysis['deep_directories'])} found)")
    
    # 상세 결과 저장
    report_path = Path("docs/CURRENT/context-optimization-report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed report saved to: {report_path}")
    print("="*60)
    
    return 0 if savings['context_efficiency'] in ['excellent', 'good'] else 1

if __name__ == "__main__":
    exit(main())