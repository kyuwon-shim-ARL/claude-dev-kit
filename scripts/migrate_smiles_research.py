#!/usr/bin/env python3
"""
SMILES 연구 프로젝트 마이그레이션 스크립트
진행 중인 연구를 연구 명령어 체계에 맞춰 정리
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict
import json
from datetime import datetime


class SMILESResearchMigrator:
    def __init__(self, smiles_path: str = "/home/kyuwon/projects/SMILES_property_webapp"):
        self.smiles_path = Path(smiles_path)
        self.research_dir = self.smiles_path / "research" / "smiles_chemical_analysis"
        
    def setup_research_structure(self) -> bool:
        """연구 프로젝트 폴더 구조 생성"""
        dirs_to_create = [
            "data/raw",
            "data/processed", 
            "analysis/scripts",
            "analysis/notebooks",
            "results/experiments",
            "results/models",
            "reports/papers",
            "reports/presentations",
            "logs",
            "config"
        ]
        
        for dir_path in dirs_to_create:
            full_path = self.research_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {full_path}")
            
        return True
    
    def migrate_analysis_files(self) -> List[str]:
        """분석 관련 파일들을 research 폴더로 이전"""
        analysis_patterns = [
            "*analysis*.py",
            "*rgcca*.py", 
            "compare_*.py",
            "*interpretability*.py",
            "run_*.py",
            "test_*.py",
            "verify_*.py"
        ]
        
        migrated_files = []
        
        for pattern in analysis_patterns:
            for file_path in self.smiles_path.glob(pattern):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    dest_path = self.research_dir / "analysis" / "scripts" / file_path.name
                    try:
                        shutil.move(str(file_path), str(dest_path))
                        migrated_files.append(file_path.name)
                        print(f"📁 Moved: {file_path.name} → analysis/scripts/")
                    except Exception as e:
                        print(f"⚠️ Failed to move {file_path.name}: {e}")
        
        return migrated_files
    
    def migrate_results_and_logs(self) -> Dict[str, int]:
        """결과 파일들과 로그들을 이전"""
        migration_stats = {"results": 0, "logs": 0, "reports": 0}
        
        # Results 폴더 이전
        if (self.smiles_path / "results").exists():
            dest_results = self.research_dir / "results"
            if dest_results.exists():
                shutil.rmtree(dest_results)
            shutil.move(str(self.smiles_path / "results"), str(dest_results))
            migration_stats["results"] = len(list(dest_results.rglob("*")))
            print(f"📊 Moved results/ directory with {migration_stats['results']} files")
        
        # Reports 폴더 이전 
        if (self.smiles_path / "reports").exists():
            dest_reports = self.research_dir / "reports"
            if dest_reports.exists():
                shutil.rmtree(dest_reports)
            shutil.move(str(self.smiles_path / "reports"), str(dest_reports))
            migration_stats["reports"] = len(list(dest_reports.rglob("*")))
            print(f"📄 Moved reports/ directory with {migration_stats['reports']} files")
        
        # 로그 파일들 이전
        for log_file in self.smiles_path.glob("*.log"):
            dest_path = self.research_dir / "logs" / log_file.name
            shutil.move(str(log_file), str(dest_path))
            migration_stats["logs"] += 1
            print(f"📝 Moved log: {log_file.name}")
            
        return migration_stats
    
    def create_research_metadata(self) -> bool:
        """연구 메타데이터 파일 생성"""
        metadata = {
            "project_name": "smiles_chemical_analysis",
            "description": "SMILES 화학 화합물 분석 및 항생제 효능 예측 연구",
            "created_date": datetime.now().isoformat(),
            "version": "5.1.0",
            "status": "production_ready",
            "key_achievements": [
                "4단계 분석 파이프라인 구현",
                "8,000개 화학 화합물 처리 성능 달성",
                "RGCCA 기반 해석가능한 AI 시스템 완성",
                "Streamlit 웹앱 프로덕션 배포"
            ],
            "current_experiments": [
                "RGCCA vs 기존 방법론 성능 비교",
                "SHAP 희석 효과 분석",
                "화학 공간 분석 결과 검증"
            ],
            "next_milestones": [
                "해석가능성 메트릭 개선",
                "대규모 데이터셋 검증",
                "논문 작성 및 게재"
            ]
        }
        
        metadata_path = self.research_dir / ".research_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Created research metadata: {metadata_path}")
        return True
    
    def initialize_research_commands(self) -> bool:
        """연구 명령어로 프로젝트 초기화"""
        try:
            os.chdir(self.smiles_path)
            
            # 연구 프로젝트 초기화
            cmd = ["/bin/bash", "-c", 
                  "source ~/.bashrc && /연구 init smiles_chemical_analysis 'SMILES 화학 화합물 분석 및 항생제 효능 예측 연구'"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Research project initialized successfully")
                return True
            else:
                print(f"⚠️ Research initialization warning: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to initialize research commands: {e}")
            return False
    
    def run_full_migration(self) -> Dict[str, any]:
        """전체 마이그레이션 프로세스 실행"""
        print("🚀 Starting SMILES Research Migration...")
        print("=" * 50)
        
        results = {
            "structure_created": False,
            "files_migrated": [],
            "migration_stats": {},
            "metadata_created": False,
            "research_initialized": False,
            "success": False
        }
        
        try:
            # 1. 폴더 구조 생성
            results["structure_created"] = self.setup_research_structure()
            
            # 2. 분석 파일들 이전
            results["files_migrated"] = self.migrate_analysis_files()
            
            # 3. 결과 및 로그 이전
            results["migration_stats"] = self.migrate_results_and_logs()
            
            # 4. 메타데이터 생성
            results["metadata_created"] = self.create_research_metadata()
            
            # 5. 연구 명령어 초기화
            results["research_initialized"] = self.initialize_research_commands()
            
            # 전체 성공 여부 판단
            results["success"] = (results["structure_created"] and 
                                results["metadata_created"])
            
            print("=" * 50)
            if results["success"]:
                print("🎉 SMILES Research Migration Completed Successfully!")
                print(f"📁 Research directory: {self.research_dir}")
                print(f"📊 Files migrated: {len(results['files_migrated'])}")
                print(f"📈 Results files: {results['migration_stats'].get('results', 0)}")
                print(f"📝 Log files: {results['migration_stats'].get('logs', 0)}")
            else:
                print("⚠️ Migration completed with some warnings")
                
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            results["success"] = False
            
        return results


def main():
    """메인 실행 함수"""
    migrator = SMILESResearchMigrator()
    results = migrator.run_full_migration()
    
    # 결과 요약 출력
    if results["success"]:
        print("\n🎯 Next Steps:")
        print("1. cd /home/kyuwon/projects/SMILES_property_webapp")
        print("2. /연구 track 'v5.1.0 프로덕션 배포 완료'")
        print("3. /연구 hypothesis 'RGCCA 기반 분석의 해석가능성 향상'")
        print("4. /연구 status  # 현재 연구 상태 확인")
        return 0
    else:
        print("\n❌ Migration failed. Please check error messages above.")
        return 1


if __name__ == "__main__":
    exit(main())