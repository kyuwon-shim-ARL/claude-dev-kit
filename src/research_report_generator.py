#!/usr/bin/env python3
"""
연구 보고서 자동 생성 시스템
/연구 명령어로 수집된 모든 데이터를 통합하여 완전한 보고서 생성
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import re
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ResearchEntry:
    """연구 기록 항목"""
    timestamp: datetime
    command: str
    content: str
    project_name: str
    metadata: Dict[str, Any]


class ResearchReportGenerator:
    """연구 보고서 자동 생성기"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.research_dir = self.project_path / "research"
        self.output_dir = self.project_path / "reports" / "research"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def collect_research_data(self, project_name: str) -> Dict[str, List[ResearchEntry]]:
        """연구 프로젝트의 모든 데이터 수집"""
        research_data = defaultdict(list)
        
        # 1. .research_projects/ 디렉토리에서 데이터 수집
        projects_dir = self.project_path / ".research_projects"
        if projects_dir.exists():
            project_file = projects_dir / f"{project_name}.json"
            if project_file.exists():
                with open(project_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for entry in data.get('history', []):
                    research_data[entry['type']].append(ResearchEntry(
                        timestamp=datetime.fromisoformat(entry['timestamp']),
                        command=entry['type'],
                        content=entry['content'],
                        project_name=project_name,
                        metadata=entry.get('metadata', {})
                    ))
        
        # 2. 연구 디렉토리에서 메타데이터 수집
        project_research_dir = self.research_dir / project_name
        if project_research_dir.exists():
            metadata_file = project_research_dir / ".research_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    research_data['metadata'] = [metadata]
        
        return dict(research_data)
    
    def generate_academic_report(self, project_name: str, research_data: Dict[str, List[ResearchEntry]]) -> str:
        """학술 논문 스타일의 연구 보고서 생성"""
        
        # 메타데이터 추출
        metadata = research_data.get('metadata', [{}])[0]
        
        report = f"""# {project_name}

## 📋 연구 개요

**프로젝트명**: {project_name}  
**연구 기간**: {metadata.get('created_date', 'N/A')} ~ {datetime.now().strftime('%Y-%m-%d')}  
**현재 버전**: {metadata.get('version', 'N/A')}  
**연구 상태**: {metadata.get('status', 'N/A')}  
**보고서 생성일**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 연구 목적 및 배경

{metadata.get('description', '연구 목적이 기록되지 않았습니다.')}

## 🔬 연구 방법론

### 연구 설계
"""
        
        # 가설들 정리
        hypotheses = research_data.get('hypothesis', [])
        if hypotheses:
            report += "\n### 연구 가설\n\n"
            for i, hyp in enumerate(hypotheses, 1):
                report += f"{i}. **{hyp.content}**\n"
                report += f"   - 제시일: {hyp.timestamp.strftime('%Y-%m-%d')}\n\n"
        
        # 실험들 정리
        experiments = research_data.get('experiment', [])
        if experiments:
            report += "\n### 실험 설계\n\n"
            for exp in experiments:
                report += f"#### {exp.content}\n"
                report += f"- **시작일**: {exp.timestamp.strftime('%Y-%m-%d')}\n"
                if exp.metadata:
                    report += f"- **설명**: {exp.metadata.get('description', '설명 없음')}\n"
                report += "\n"
        
        # 진행 과정 정리
        tracks = research_data.get('track', [])
        if tracks:
            report += "\n## 📈 연구 진행 과정\n\n"
            report += "### 주요 마일스톤\n\n"
            
            # 시간순으로 정렬
            sorted_tracks = sorted(tracks, key=lambda x: x.timestamp)
            
            current_month = None
            for track in sorted_tracks:
                track_month = track.timestamp.strftime('%Y-%m')
                if current_month != track_month:
                    current_month = track_month
                    report += f"\n#### {track.timestamp.strftime('%Y년 %m월')}\n\n"
                
                report += f"- **{track.timestamp.strftime('%m-%d')}**: {track.content}\n"
        
        # 마일스톤들 정리
        milestones = research_data.get('milestone', [])
        if milestones:
            report += "\n### 달성된 마일스톤\n\n"
            for milestone in sorted(milestones, key=lambda x: x.timestamp):
                report += f"- ✅ **{milestone.content}** ({milestone.timestamp.strftime('%Y-%m-%d')})\n"
        
        # 주요 성과 정리 (메타데이터에서)
        achievements = metadata.get('key_achievements', [])
        if achievements:
            report += "\n## 🏆 주요 연구 성과\n\n"
            for i, achievement in enumerate(achievements, 1):
                report += f"{i}. {achievement}\n"
        
        # 현재 진행 중인 실험들
        current_experiments = metadata.get('current_experiments', [])
        if current_experiments:
            report += "\n## 🔬 현재 진행 중인 연구\n\n"
            for exp in current_experiments:
                report += f"- {exp}\n"
        
        # 체크포인트들 정리
        checkpoints = research_data.get('checkpoint', [])
        if checkpoints:
            report += "\n## ✅ 검증 및 체크포인트\n\n"
            for cp in sorted(checkpoints, key=lambda x: x.timestamp):
                report += f"### {cp.timestamp.strftime('%Y-%m-%d')}: {cp.content}\n\n"
                if cp.metadata.get('validation_results'):
                    report += f"**검증 결과**: {cp.metadata['validation_results']}\n\n"
        
        # 향후 계획
        next_milestones = metadata.get('next_milestones', [])
        if next_milestones:
            report += "\n## 🗺️ 향후 연구 계획\n\n"
            for i, milestone in enumerate(next_milestones, 1):
                report += f"{i}. {milestone}\n"
        
        # 연구 통계
        report += f"\n## 📊 연구 통계\n\n"
        # metadata를 제외한 실제 연구 기록만 카운트
        total_records = sum(len(entries) for key, entries in research_data.items() 
                           if isinstance(entries, list) and key != 'metadata')
        report += f"- **총 연구 기록**: {total_records}\n"
        report += f"- **가설 수**: {len(hypotheses)}\n"
        report += f"- **실험 수**: {len(experiments)}\n"
        report += f"- **마일스톤**: {len(milestones)}\n"
        report += f"- **체크포인트**: {len(checkpoints)}\n"
        
        # 연구 파일 및 자료
        if self.research_dir.exists():
            project_dir = self.research_dir / project_name
            if project_dir.exists():
                report += "\n## 📁 연구 자료\n\n"
                
                # 분석 스크립트
                analysis_dir = project_dir / "analysis" / "scripts"
                if analysis_dir.exists():
                    scripts = list(analysis_dir.glob("*.py"))
                    if scripts:
                        report += "### 분석 스크립트\n"
                        for script in scripts[:10]:  # 최대 10개만 표시
                            report += f"- `{script.name}`\n"
                
                # 결과 파일들
                results_dir = project_dir / "results"
                if results_dir.exists():
                    report += "\n### 연구 결과 파일\n"
                    result_files = list(results_dir.rglob("*"))[:10]
                    for result_file in result_files:
                        if result_file.is_file():
                            report += f"- `{result_file.relative_to(project_dir)}`\n"
        
        # 결론
        report += f"\n## 🎯 결론 및 제언\n\n"
        report += f"본 연구는 {project_name} 프로젝트를 통해 다음과 같은 성과를 달성했습니다:\n\n"
        
        for achievement in achievements:
            report += f"- {achievement}\n"
        
        if next_milestones:
            report += f"\n향후 연구에서는 다음 사항들을 중점적으로 진행할 예정입니다:\n\n"
            for milestone in next_milestones:
                report += f"- {milestone}\n"
        
        # 부록
        report += f"\n---\n\n"
        report += f"*본 보고서는 /연구 명령어 시스템을 통해 자동 생성되었습니다.*  \n"
        report += f"*생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return report
    
    def generate_comprehensive_report(self, project_name: str) -> str:
        """완전한 연구 보고서 생성 및 저장"""
        
        print(f"📊 {project_name} 연구 보고서 생성 중...")
        
        # 1. 연구 데이터 수집
        research_data = self.collect_research_data(project_name)
        
        if not research_data:
            return f"❌ {project_name} 프로젝트의 연구 데이터를 찾을 수 없습니다."
        
        # 2. 학술 보고서 생성
        report_content = self.generate_academic_report(project_name, research_data)
        
        # 3. 파일 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"{project_name}_research_report_{timestamp}.md"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # 4. 최신 보고서 링크 생성
        latest_link = self.output_dir / f"{project_name}_latest_report.md"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(filename)
        
        return str(filepath)


def main():
    """메인 실행 함수"""
    import sys
    
    if len(sys.argv) < 2:
        print("사용법: python research_report_generator.py <project_name> [project_path]")
        return 1
    
    project_name = sys.argv[1]
    project_path = sys.argv[2] if len(sys.argv) > 2 else "."
    
    generator = ResearchReportGenerator(project_path)
    report_path = generator.generate_comprehensive_report(project_name)
    
    if report_path.startswith("❌"):
        print(report_path)
        return 1
    
    print(f"✅ 연구 보고서 생성 완료!")
    print(f"📁 저장 위치: {report_path}")
    print(f"🔗 최신 보고서: {Path(report_path).parent / f'{project_name}_latest_report.md'}")
    
    return 0


if __name__ == "__main__":
    exit(main())