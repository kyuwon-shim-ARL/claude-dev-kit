#!/usr/bin/env python3
"""
Research Project Manager
바이오인포매틱스 연구 프로젝트 관리 시스템
"""
import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import subprocess

# 입력 검증 시스템 import
try:
    from .input_validator import InputValidator, ValidationError, safe_project_id
except ImportError:
    # 상대 import 실패 시 절대 import 시도
    import sys
    sys.path.append(os.path.dirname(__file__))
    from input_validator import InputValidator, ValidationError, safe_project_id


class ResearchProjectManager:
    """연구 프로젝트 생성 및 관리"""
    
    def __init__(self, base_dir: str = "research_projects"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.base_dir / ".research_metadata.json"
        self.checkpoint_context = {}  # 체크포인트 컨텍스트 저장
        self.load_metadata()
    
    def load_metadata(self):
        """프로젝트 메타데이터 로드"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "projects": {},
                "active_project": None,
                "created": datetime.now().isoformat()
            }
            self.save_metadata()
    
    def save_metadata(self):
        """메타데이터 저장"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def init_project(self, name: str, description: str = "") -> Dict[str, Any]:
        """새 연구 프로젝트 초기화"""
        try:
            # 입력 검증 및 정규화
            timestamp = datetime.now().strftime("%Y-%m-%d")
            project_id = safe_project_id(name, timestamp)
            description = InputValidator.validate_description(description)
            
        except ValidationError as e:
            raise ValueError(str(e))  # 테스트와의 호환성을 위해 ValueError로 변환
        
        # 프로젝트 디렉토리 생성
        project_dir = self.base_dir / project_id
        
        if project_dir.exists():
            return {"error": f"Project {project_id} already exists"}
        
        project_dir.mkdir(parents=True)
        
        # 기본 구조 생성
        structure = {
            "notebooks": "Jupyter notebooks for analysis",
            "data": "Raw and processed data",
            "results": "Analysis results and outputs",
            "figures": "Visualizations and plots",
            "docs": "Documentation and notes",
            "scripts": "Analysis scripts and utilities"
        }
        
        for folder, desc in structure.items():
            folder_path = project_dir / folder
            folder_path.mkdir()
            (folder_path / ".gitkeep").touch()
            (folder_path / "README.md").write_text(f"# {folder.title()}\n\n{desc}\n")
        
        # README 생성
        readme_content = f"""# {name}

**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Description**: {description}

## Project Structure
```
{project_id}/
├── notebooks/     # Jupyter notebooks
├── data/          # Data files
├── results/       # Analysis outputs
├── figures/       # Visualizations
├── docs/          # Documentation
└── scripts/       # Analysis scripts
```

## Timeline
See `timeline.md` for detailed progress tracking.

## Quick Start
1. Place data files in `data/`
2. Create analysis notebooks in `notebooks/`
3. Save results in `results/`
4. Document findings in `docs/`

## Reproducibility
All analysis steps are tracked in `timeline.md` with Git checkpoints.
"""
        (project_dir / "README.md").write_text(readme_content)
        
        # 타임라인 초기화
        timeline_content = f"""# Research Timeline - {name}

## Project Start
- **Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Objective**: {description}
- **Status**: Initialized

---

"""
        (project_dir / "timeline.md").write_text(timeline_content)
        
        # 환경 정보 저장
        system_info = {}
        if hasattr(os, 'uname'):
            uname = os.uname()
            system_info = {
                "sysname": uname.sysname,
                "nodename": uname.nodename,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine
            }
        
        env_info = {
            "python_version": subprocess.getoutput("python --version"),
            "packages": self._get_installed_packages(),
            "system": system_info
        }
        (project_dir / "environment.json").write_text(json.dumps(env_info, indent=2))
        
        # 개발 도구 심링크 (있으면) - 현재 작업 디렉토리가 유효한 경우에만
        try:
            src_dir = Path.cwd() / "src"
            if src_dir.exists():
                tools_link = project_dir / "tools"
                tools_link.symlink_to(src_dir.resolve())
        except (FileNotFoundError, OSError):
            # 현재 작업 디렉토리가 없거나 접근할 수 없는 경우 무시
            pass
        
        # 메타데이터 업데이트 (정규화된 데이터 사용)
        original_name = name
        self.metadata["projects"][project_id] = {
            "name": InputValidator.sanitize_project_name(name),  # 정규화된 이름
            "original_name": original_name,  # 원본 이름 보존
            "description": description,  # 이미 검증됨
            "created": datetime.now().isoformat(),
            "status": "active",
            "checkpoints": [],
            "milestones": [],
            "hypotheses": [],  # 가설 목록 추가
            "experiments": []   # 실험 목록 추가
        }
        self.metadata["active_project"] = project_id
        self.save_metadata()
        
        return {
            "success": True,
            "project_id": project_id,
            "path": str(project_dir),
            "message": f"Research project '{name}' initialized successfully"
        }
    
    def track_progress(self, note: str, files: List[str] = None) -> Dict[str, Any]:
        """연구 진행사항 추적"""
        if not self.metadata["active_project"]:
            return {"error": "No active project. Use 'init' first."}
        
        project_id = self.metadata["active_project"]
        project_dir = self.base_dir / project_id
        timeline_file = project_dir / "timeline.md"
        
        # 타임라인 업데이트
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"""
## {timestamp}
**Note**: {note}
"""
        
        if files:
            entry += "\n**Files**:\n"
            for file in files:
                entry += f"- `{file}`\n"
        
        # Git 체크포인트 생성 (있으면)
        if (project_dir / ".git").exists():
            commit_hash = subprocess.getoutput(
                f"cd {project_dir} && git rev-parse HEAD"
            )[:7]
            entry += f"\n**Git Checkpoint**: `{commit_hash}`\n"
            
            # 체크포인트 메타데이터 저장
            self.metadata["projects"][project_id]["checkpoints"].append({
                "timestamp": timestamp,
                "note": note,
                "commit": commit_hash,
                "files": files or []
            })
            self.save_metadata()
        
        entry += "\n---\n"
        
        with open(timeline_file, 'a') as f:
            f.write(entry)
        
        return {
            "success": True,
            "message": f"Progress tracked: {note}",
            "timestamp": timestamp
        }
    
    def set_milestone(self, name: str, description: str = "") -> Dict[str, Any]:
        """주요 마일스톤 설정"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        project_dir = self.base_dir / project_id
        
        milestone = {
            "name": name,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "status": "reached"
        }
        
        self.metadata["projects"][project_id]["milestones"].append(milestone)
        self.save_metadata()
        
        # 타임라인에도 기록
        self.track_progress(f"🎯 MILESTONE: {name} - {description}")
        
        return {
            "success": True,
            "message": f"Milestone '{name}' set successfully"
        }
    
    def reproduce_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        """특정 체크포인트 재현"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        project_dir = self.base_dir / project_id
        checkpoints = self.metadata["projects"][project_id]["checkpoints"]
        
        # 체크포인트 찾기
        checkpoint = None
        for cp in checkpoints:
            if cp["commit"] == checkpoint_id or cp["timestamp"] == checkpoint_id:
                checkpoint = cp
                break
        
        if not checkpoint:
            return {"error": f"Checkpoint {checkpoint_id} not found"}
        
        # Git으로 체크아웃 (있으면)
        if (project_dir / ".git").exists():
            result = subprocess.run(
                ["git", "checkout", checkpoint["commit"]],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return {"error": f"Failed to checkout: {result.stderr}"}
        
        # 환경 정보 표시
        env_file = project_dir / "environment.json"
        if env_file.exists():
            with open(env_file, 'r') as f:
                env_info = json.load(f)
            
            return {
                "success": True,
                "message": f"Reproduced checkpoint {checkpoint_id}",
                "checkpoint": checkpoint,
                "environment": env_info
            }
        
        return {
            "success": True,
            "message": f"Reproduced checkpoint {checkpoint_id}",
            "checkpoint": checkpoint
        }
    
    def explore_data(self, description: str = "") -> Dict[str, Any]:
        """데이터 탐색 및 EDA"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        project_dir = self.base_dir / project_id
        
        # EDA 노트북 생성
        eda_notebook = project_dir / "notebooks" / f"EDA_{datetime.now().strftime('%Y%m%d_%H%M')}.ipynb"
        eda_template = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": f"# Exploratory Data Analysis\n\n**Date**: {datetime.now().isoformat()}\n**Description**: {description}"
                },
                {
                    "cell_type": "code", 
                    "source": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n# Load data\n# df = pd.read_csv('data/your_data.csv')"
                }
            ]
        }
        
        with open(eda_notebook, 'w') as f:
            json.dump(eda_template, f, indent=2)
        
        # 타임라인 기록
        self.track_progress(f"🔍 EXPLORE: {description}", [str(eda_notebook)])
        
        return {
            "success": True,
            "message": f"EDA notebook created: {eda_notebook}",
            "notebook_path": str(eda_notebook)
        }
    
    def set_hypothesis(self, hypothesis: str) -> Dict[str, Any]:
        """연구 가설 설정"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        
        # 가설 저장
        if "hypotheses" not in self.metadata["projects"][project_id]:
            self.metadata["projects"][project_id]["hypotheses"] = []
        
        hypothesis_entry = {
            "hypothesis": hypothesis,
            "timestamp": datetime.now().isoformat(),
            "status": "active",
            "tests": [],
            "results": []
        }
        
        self.metadata["projects"][project_id]["hypotheses"].append(hypothesis_entry)
        self.save_metadata()
        
        # 타임라인 기록
        self.track_progress(f"💡 HYPOTHESIS: {hypothesis}")
        
        return {
            "success": True,
            "message": f"Hypothesis set: {hypothesis}"
        }
    
    def start_experiment(self, experiment_name: str, description: str = "") -> Dict[str, Any]:
        """새로운 실험 시작"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        project_dir = self.base_dir / project_id
        
        # 실험 디렉토리 생성
        exp_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        exp_id = f"{exp_timestamp}_{experiment_name}"
        exp_dir = project_dir / "experiments" / exp_id
        exp_dir.mkdir(parents=True)
        
        # 실험 메타데이터
        exp_metadata = {
            "name": experiment_name,
            "description": description,
            "started": datetime.now().isoformat(),
            "status": "running",
            "parameters": {},
            "results": {},
            "notebook": f"experiments/{exp_id}/experiment.ipynb"
        }
        
        if "experiments" not in self.metadata["projects"][project_id]:
            self.metadata["projects"][project_id]["experiments"] = []
        
        self.metadata["projects"][project_id]["experiments"].append(exp_metadata)
        self.save_metadata()
        
        # 실험 노트북 생성
        exp_notebook = exp_dir / "experiment.ipynb"
        notebook_template = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": f"# Experiment: {experiment_name}\n\n**Started**: {datetime.now().isoformat()}\n**Description**: {description}"
                },
                {
                    "cell_type": "code",
                    "source": "# Experiment setup\nimport sys\nsys.path.append('../../tools')\n\n# Import project tools\n# from your_module import your_function"
                }
            ]
        }
        
        with open(exp_notebook, 'w') as f:
            json.dump(notebook_template, f, indent=2)
        
        # 타임라인 기록
        self.track_progress(f"🧪 EXPERIMENT STARTED: {experiment_name}", [str(exp_notebook)])
        
        return {
            "success": True,
            "message": f"Experiment '{experiment_name}' started",
            "experiment_id": exp_id,
            "notebook_path": str(exp_notebook)
        }
    
    def validate_results(self, description: str = "") -> Dict[str, Any]:
        """결과 검증 및 테스트"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        project_dir = self.base_dir / project_id
        
        # 검증 스크립트 생성
        validation_script = project_dir / "scripts" / f"validate_{datetime.now().strftime('%Y%m%d_%H%M')}.py"
        
        validation_template = f'''#!/usr/bin/env python3
"""
Validation Script - {description}
Generated: {datetime.now().isoformat()}
"""
import sys
import os
sys.path.append('../tools')

def validate_model_performance():
    """모델 성능 검증"""
    # TODO: Implement validation logic
    pass

def validate_statistical_significance():
    """통계적 유의성 검증"""
    # TODO: Implement statistical tests
    pass

def validate_reproducibility():
    """재현성 검증"""
    # TODO: Implement reproducibility checks  
    pass

if __name__ == "__main__":
    print("🔍 Running validation tests...")
    
    print("1. Model performance validation...")
    validate_model_performance()
    
    print("2. Statistical significance validation...")
    validate_statistical_significance()
    
    print("3. Reproducibility validation...")
    validate_reproducibility()
    
    print("✅ Validation complete!")
'''
        
        with open(validation_script, 'w') as f:
            f.write(validation_template)
        
        # 실행 권한 부여
        os.chmod(validation_script, 0o755)
        
        # 타임라인 기록
        self.track_progress(f"🔍 VALIDATION: {description}", [str(validation_script)])
        
        return {
            "success": True,
            "message": f"Validation script created: {validation_script}",
            "script_path": str(validation_script)
        }
    
    def analyze_results(self, description: str = "") -> Dict[str, Any]:
        """결과 분석 및 리포트 생성"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        project_dir = self.base_dir / project_id
        
        # 분석 보고서 생성
        analysis_report = project_dir / "reports" / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        analysis_report.parent.mkdir(exist_ok=True)
        
        report_template = f"""# Analysis Report

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Description**: {description}
**Project**: {self.metadata['projects'][project_id]['name']}

## Summary
<!-- Key findings and insights -->

## Results
<!-- Detailed results -->

## Visualizations
<!-- References to figures/ directory -->

## Conclusions
<!-- Main conclusions -->

## Next Steps
<!-- Recommended actions -->

## Methodology
<!-- Methods used -->

## Data Sources
<!-- Data files used -->
"""
        
        with open(analysis_report, 'w') as f:
            f.write(report_template)
        
        # 타임라인 기록
        self.track_progress(f"📊 ANALYSIS: {description}", [str(analysis_report)])
        
        return {
            "success": True,
            "message": f"Analysis report created: {analysis_report}",
            "report_path": str(analysis_report)
        }
    
    def compare_experiments(self, exp1: str, exp2: str) -> Dict[str, Any]:
        """실험 결과 비교"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        project_dir = self.base_dir / project_id
        
        # 비교 분석 노트북 생성
        comparison_notebook = project_dir / "notebooks" / f"compare_{exp1}_vs_{exp2}_{datetime.now().strftime('%Y%m%d_%H%M')}.ipynb"
        
        notebook_template = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": f"# Experiment Comparison: {exp1} vs {exp2}\n\n**Date**: {datetime.now().isoformat()}"
                },
                {
                    "cell_type": "code",
                    "source": f"# Load results from {exp1}\n# Load results from {exp2}\n# Compare metrics\n# Generate visualizations"
                }
            ]
        }
        
        with open(comparison_notebook, 'w') as f:
            json.dump(notebook_template, f, indent=2)
        
        # 타임라인 기록
        self.track_progress(f"🔄 COMPARE: {exp1} vs {exp2}", [str(comparison_notebook)])
        
        return {
            "success": True,
            "message": f"Comparison notebook created for {exp1} vs {exp2}",
            "notebook_path": str(comparison_notebook)
        }
    
    def checkpoint(self, description: str) -> Dict[str, Any]:
        """개발 필요 시 체크포인트 생성"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        
        # 체크포인트 생성
        checkpoint_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_data = {
            "id": checkpoint_id,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "project_state": "research_paused",
            "context": {
                "last_action": "checkpoint_created",
                "next_action": "tool_development_needed"
            }
        }
        
        # 체크포인트 저장
        self.checkpoint_context[checkpoint_id] = checkpoint_data
        
        if "checkpoints" not in self.metadata["projects"][project_id]:
            self.metadata["projects"][project_id]["checkpoints"] = []
        
        self.metadata["projects"][project_id]["checkpoints"].append(checkpoint_data)
        self.save_metadata()
        
        # 타임라인 기록
        self.track_progress(f"⏸️ CHECKPOINT: {description} (ID: {checkpoint_id})")
        
        return {
            "success": True,
            "message": f"Checkpoint created: {description}",
            "checkpoint_id": checkpoint_id,
            "next_steps": "Use development commands (/구현, /테스트) then /연구 resume"
        }
    
    def resume_from_checkpoint(self, checkpoint_id: str = None) -> Dict[str, Any]:
        """체크포인트에서 연구 재개"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        
        # 최신 체크포인트 선택 (ID 없으면)
        if not checkpoint_id:
            checkpoints = self.metadata["projects"][project_id].get("checkpoints", [])
            if not checkpoints:
                return {"error": "No checkpoints found"}
            checkpoint_id = checkpoints[-1]["id"]
        
        # 메타데이터에서 체크포인트 찾기
        checkpoints = self.metadata["projects"][project_id].get("checkpoints", [])
        checkpoint_data = None
        
        for cp in checkpoints:
            if cp["id"] == checkpoint_id:
                checkpoint_data = cp
                break
        
        if not checkpoint_data:
            return {"error": f"Checkpoint {checkpoint_id} not found"}
        
        # 타임라인 기록
        self.track_progress(f"▶️ RESUME: From checkpoint {checkpoint_id}")
        
        return {
            "success": True,
            "message": f"Resumed from checkpoint: {checkpoint_data['description']}",
            "checkpoint_id": checkpoint_id,
            "context": checkpoint_data
        }
    
    def list_tools(self) -> Dict[str, Any]:
        """사용 가능한 도구 목록"""
        # Tool Inventory와 연동
        try:
            from tool_inventory import ToolInventory
            inventory = ToolInventory()
            inventory.scan_tools()
            tools = inventory.tools
            
            return {
                "success": True,
                "tools": tools,
                "count": len(tools),
                "categories": self._categorize_tools(tools)
            }
        except ImportError:
            return {
                "error": "Tool inventory not available",
                "message": "Run tool inventory scan first"
            }
    
    def _categorize_tools(self, tools: Dict) -> Dict[str, List[str]]:
        """도구 카테고리 분류"""
        categories = {}
        for name, info in tools.items():
            file_path = info['file']
            category = Path(file_path).parent.name
            
            if category not in categories:
                categories[category] = []
            categories[category].append(name)
        
        return categories
    
    def share_results(self) -> Dict[str, Any]:
        """연구 결과 공유 준비"""
        if not self.metadata["active_project"]:
            return {"error": "No active project"}
        
        project_id = self.metadata["active_project"]
        project_dir = self.base_dir / project_id
        
        # 공유 패키지 디렉토리 생성
        share_dir = project_dir / "share_package"
        share_dir.mkdir(exist_ok=True)
        
        # README 생성
        readme_content = f"""# {self.metadata['projects'][project_id]['name']}

## Project Overview
{self.metadata['projects'][project_id]['description']}

## Key Results
<!-- Add your key findings here -->

## Data Files
- Check `data/` directory

## Analysis Notebooks
- Check `notebooks/` directory

## Reproduction
1. Install requirements: `pip install -r requirements.txt`
2. Run notebooks in order
3. Check `results/` for outputs

## Contact
<!-- Add contact information -->
"""
        
        with open(share_dir / "README.md", 'w') as f:
            f.write(readme_content)
        
        # requirements.txt 생성
        with open(share_dir / "requirements.txt", 'w') as f:
            f.write("# Add your dependencies here\n")
        
        # 타임라인 기록
        self.track_progress(f"📤 SHARE: Package prepared in {share_dir}")
        
        return {
            "success": True,
            "message": f"Share package created in {share_dir}",
            "share_path": str(share_dir)
        }
    
    def archive_project(self) -> Dict[str, Any]:
        """연구 프로젝트 아카이빙"""
        if not self.metadata["active_project"]:
            return {"error": "No active project to archive"}
        
        project_id = self.metadata["active_project"]
        
        # 상태 업데이트
        self.metadata["projects"][project_id]["status"] = "archived"
        self.metadata["projects"][project_id]["archived_at"] = datetime.now().isoformat()
        self.metadata["active_project"] = None
        self.save_metadata()
        
        # 최종 보고서 생성
        self._generate_final_report(project_id)
        
        return {
            "success": True,
            "message": f"Project {project_id} archived successfully"
        }
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """모든 연구 프로젝트 목록"""
        projects = []
        for project_id, info in self.metadata["projects"].items():
            projects.append({
                "id": project_id,
                "name": info["name"],
                "status": info["status"],
                "created": info["created"],
                "milestones": len(info["milestones"]),
                "checkpoints": len(info["checkpoints"])
            })
        return sorted(projects, key=lambda x: x["created"], reverse=True)
    
    def detect_current_project(self) -> Optional[str]:
        """현재 디렉토리 기반 프로젝트 자동 감지 - 완전 재설계"""
        import os
        from pathlib import Path
        
        try:
            # 1단계: 재귀적 상위 디렉토리 탐색으로 메타데이터 찾기
            current = Path(os.getcwd())
            project_context = self._find_project_root_recursive(current)
            
            if project_context:
                # 현재 경로에서 프로젝트 ID 추론 (동적 로딩 전에)
                detected_project = self._extract_project_id_from_path(current, project_context)
                if detected_project:
                    # 성공적으로 감지된 경우만 메타데이터 업데이트
                    self._load_metadata_from_context(project_context)
                    return detected_project
            
            # 2단계: 기존 메타데이터에서 최근 활동한 프로젝트
            recent_activity = self._get_recent_activity_project(minutes=5)
            if recent_activity:
                return recent_activity
            
            # 3단계: 메타데이터의 기본 활성 프로젝트
            return self.metadata.get("active_project")
            
        except Exception as e:
            # 오류 발생 시 기존 방식으로 fallback (안정성 보장)
            print(f"⚠️ Directory detection error: {e}")
            return self.metadata.get("active_project")
    
    def _find_project_root_recursive(self, start_path: Path) -> Optional[Dict[str, Any]]:
        """재귀적으로 상위 디렉토리를 탐색하여 연구 프로젝트 루트 찾기"""
        current = start_path
        max_depth = 10  # 무한루프 방지
        depth = 0
        
        # 먼저 현재 경로가 research_projects 내부인지 확인
        path_parts = current.parts
        research_index = None
        
        # 경로에서 'research_projects' 찾기
        for i, part in enumerate(path_parts):
            if part == "research_projects":
                research_index = i
                break
        
        if research_index is not None:
            # research_projects 디렉토리 재구성
            research_dir = Path(*path_parts[:research_index + 1])  # research_projects까지의 경로
            metadata_file = research_dir / ".research_metadata.json"
            
            if metadata_file.exists() and metadata_file.is_file():
                try:
                    import json
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    return {
                        "metadata_path": metadata_file,
                        "research_dir": research_dir,
                        "project_root": research_dir.parent,
                        "metadata": metadata
                    }
                except (json.JSONDecodeError, IOError, PermissionError) as e:
                    print(f"⚠️ Metadata file error at {metadata_file}: {e}")
        
        # Fallback: 상위 디렉토리에서 research_projects 찾기
        while depth < max_depth:
            research_subdir = current / "research_projects"
            if research_subdir.exists() and research_subdir.is_dir():
                metadata_file = research_subdir / ".research_metadata.json"
                if metadata_file.exists() and metadata_file.is_file():
                    try:
                        import json
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        return {
                            "metadata_path": metadata_file,
                            "research_dir": research_subdir,
                            "project_root": current,
                            "metadata": metadata
                        }
                    except (json.JSONDecodeError, IOError, PermissionError) as e:
                        print(f"⚠️ Metadata file error at {metadata_file}: {e}")
            
            # 상위 디렉토리로 이동
            parent = current.parent
            if parent == current:  # 루트 디렉토리 도달
                break
            current = parent
            depth += 1
        
        return None
    
    def _load_metadata_from_context(self, project_context: Dict[str, Any]) -> None:
        """프로젝트 컨텍스트에서 메타데이터 동적 로딩"""
        # 기존 설정 업데이트
        self.base_dir = project_context["research_dir"]
        self.metadata_file = project_context["metadata_path"]
        self.metadata = project_context["metadata"]
    
    def _extract_project_id_from_path(self, current_path: Path, project_context: Dict[str, Any]) -> Optional[str]:
        """현재 경로에서 프로젝트 ID 추론"""
        try:
            research_dir = project_context["research_dir"]
            
            # 현재 경로가 research_projects 디렉토리 내부인지 확인
            try:
                relative_path = current_path.relative_to(research_dir)
            except ValueError:
                # current_path가 research_dir 내부가 아님
                return None
            
            # 상대 경로의 첫 번째 부분이 프로젝트 ID
            path_parts = relative_path.parts
            if len(path_parts) > 0:
                potential_project_id = path_parts[0]
                
                # 메타데이터에서 해당 프로젝트 ID 존재 확인
                if potential_project_id in project_context["metadata"].get("projects", {}):
                    return potential_project_id
            
            return None
            
        except Exception as e:
            print(f"⚠️ Project ID extraction error: {e}")
            return None
    
    def _get_recent_activity_project(self, minutes: int = 5) -> Optional[str]:
        """최근 활동한 프로젝트 감지"""
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_project = None
        latest_time = None
        
        for project_id, project_info in self.metadata["projects"].items():
            # 체크포인트에서 최근 활동 시간 확인
            checkpoints = project_info.get("checkpoints", [])
            if checkpoints:
                latest_checkpoint = checkpoints[-1]
                checkpoint_time = datetime.fromisoformat(latest_checkpoint["timestamp"])
                
                if checkpoint_time > cutoff_time:
                    if latest_time is None or checkpoint_time > latest_time:
                        latest_time = checkpoint_time
                        recent_project = project_id
        
        return recent_project
    
    def auto_switch_project(self) -> Dict[str, Any]:
        """현재 컨텍스트 기반 자동 프로젝트 전환"""
        detected_project = self.detect_current_project()
        
        if not detected_project:
            projects = list(self.metadata["projects"].keys())
            if len(projects) == 1:
                detected_project = projects[0]
            elif len(projects) > 1:
                return {
                    "error": "Multiple projects available",
                    "projects": projects,
                    "suggestion": "Use 'switch' command to select project"
                }
            else:
                return {"error": "No projects found"}
        
        # 이미 활성 프로젝트인 경우
        if self.metadata.get("active_project") == detected_project:
            return {
                "success": True,
                "message": f"Already active: {detected_project}",
                "no_change": True
            }
        
        # 프로젝트 전환
        return self.switch_project(detected_project)
    
    def switch_project(self, project_id: str) -> Dict[str, Any]:
        """활성 프로젝트 전환"""
        if project_id not in self.metadata["projects"]:
            return {"error": f"Project {project_id} not found"}
        
        self.metadata["active_project"] = project_id
        self.save_metadata()
        
        return {
            "success": True,
            "message": f"Switched to project {project_id}"
        }
    
    def _get_installed_packages(self) -> List[str]:
        """설치된 패키지 목록 가져오기"""
        try:
            result = subprocess.run(
                ["pip", "freeze"],
                capture_output=True,
                text=True
            )
            return result.stdout.strip().split('\n')
        except:
            return []
    
    def _generate_final_report(self, project_id: str):
        """최종 연구 보고서 생성"""
        project_dir = self.base_dir / project_id
        project_info = self.metadata["projects"][project_id]
        
        report_content = f"""# Final Research Report - {project_info['name']}

## Project Overview
- **ID**: {project_id}
- **Created**: {project_info['created']}
- **Archived**: {project_info.get('archived_at', 'N/A')}
- **Description**: {project_info['description']}

## Milestones Achieved
"""
        
        for milestone in project_info['milestones']:
            report_content += f"- **{milestone['name']}** ({milestone['timestamp']}): {milestone['description']}\n"
        
        report_content += f"""

## Research Checkpoints
Total checkpoints: {len(project_info['checkpoints'])}

## Project Structure
```
{project_id}/
├── notebooks/     # Analysis notebooks
├── data/          # Research data
├── results/       # Final outputs
├── figures/       # Visualizations
├── docs/          # Documentation
└── scripts/       # Analysis scripts
```

## Reproducibility
All checkpoints are preserved with Git commits and environment snapshots.
See `timeline.md` for complete research history.
"""
        
        (project_dir / "FINAL_REPORT.md").write_text(report_content)


class ResearchTimeline:
    """연구 타임라인 추적 시스템"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.timeline_file = project_dir / "timeline.md"
        self.checkpoints_dir = project_dir / ".checkpoints"
        self.checkpoints_dir.mkdir(exist_ok=True)
    
    def add_entry(self, category: str, content: str, metadata: Dict = None):
        """타임라인 엔트리 추가"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = f"\n## [{category}] {timestamp}\n"
        entry += content + "\n"
        
        if metadata:
            entry += "\n**Metadata**:\n"
            for key, value in metadata.items():
                entry += f"- {key}: {value}\n"
        
        entry += "\n---\n"
        
        with open(self.timeline_file, 'a') as f:
            f.write(entry)
    
    def create_checkpoint(self, name: str):
        """체크포인트 생성"""
        checkpoint_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_dir = self.checkpoints_dir / checkpoint_id
        checkpoint_dir.mkdir()
        
        # 현재 상태 스냅샷
        snapshot = {
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "files": self._list_project_files(),
            "environment": self._capture_environment()
        }
        
        with open(checkpoint_dir / "snapshot.json", 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        self.add_entry("CHECKPOINT", f"Created checkpoint: {name}", {
            "checkpoint_id": checkpoint_id
        })
        
        return checkpoint_id
    
    def _list_project_files(self) -> List[str]:
        """프로젝트 파일 목록"""
        files = []
        for root, _, filenames in os.walk(self.project_dir):
            if '.git' in root or '__pycache__' in root:
                continue
            for filename in filenames:
                rel_path = os.path.relpath(
                    os.path.join(root, filename),
                    self.project_dir
                )
                files.append(rel_path)
        return files
    
    def _capture_environment(self) -> Dict:
        """환경 정보 캡처"""
        return {
            "python_version": subprocess.getoutput("python --version"),
            "working_directory": str(self.project_dir),
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # 테스트 실행
    manager = ResearchProjectManager()
    
    # 새 프로젝트 생성
    result = manager.init_project(
        "drug_discovery_ml",
        "Machine learning for drug discovery using molecular fingerprints"
    )
    print(f"Project created: {result}")
    
    # 진행사항 추적
    manager.track_progress("Loaded SMILES dataset with 10,000 compounds")
    manager.track_progress("Calculated molecular descriptors", ["notebooks/01_descriptors.ipynb"])
    
    # 마일스톤 설정
    manager.set_milestone("Data Preparation", "All molecular features calculated")
    
    # 프로젝트 목록
    projects = manager.list_projects()
    print(f"Active projects: {projects}")