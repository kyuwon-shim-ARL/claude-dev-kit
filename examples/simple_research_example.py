#!/usr/bin/env python3
"""
Research Project Manager - 간단한 사용 예제
5분 안에 시작할 수 있는 실용적인 예제
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_project_manager import ResearchProjectManager


def simple_example():
    """가장 간단한 사용 예제"""
    
    print("\n🔬 Research Project Manager - Simple Example")
    print("=" * 50)
    
    # 1. Manager 초기화
    manager = ResearchProjectManager()
    print("✅ Manager 초기화 완료")
    
    # 2. 새 프로젝트 생성
    result = manager.init_project(
        name="simple_test",
        description="간단한 테스트 프로젝트"
    )
    
    if "error" not in result:
        project_id = result.get("project_id")
        print(f"✅ 프로젝트 생성: {project_id}")
        print(f"📁 위치: {result.get('path')}")
        
        # 3. 진행사항 기록
        manager.track_progress("첫 번째 작업 완료")
        print("✅ 진행사항 기록됨")
        
        # 4. 마일스톤 설정
        manager.set_milestone("초기 설정", "프로젝트 환경 구성 완료")
        print("✅ 마일스톤 설정됨")
        
        # 5. 프로젝트 정보 확인
        print("\n📊 프로젝트 정보:")
        current = manager.metadata.get("active_project")
        if current and current in manager.metadata["projects"]:
            info = manager.metadata["projects"][current]
            print(f"  - 이름: {info.get('name')}")
            print(f"  - 상태: {info.get('status', 'active')}")
            print(f"  - 마일스톤: {len(info.get('milestones', []))}개")
    else:
        print(f"⚠️  프로젝트가 이미 존재합니다")
    
    print("\n✅ 예제 완료!")
    print("💡 Tip: research_projects/ 폴더를 확인해보세요")


def list_projects_example():
    """프로젝트 목록 확인 예제"""
    
    print("\n📋 프로젝트 목록 확인")
    print("=" * 50)
    
    manager = ResearchProjectManager()
    
    # 모든 프로젝트 나열
    projects = manager.list_projects()
    
    if projects:
        print(f"총 {len(projects)}개 프로젝트:")
        for proj in projects:
            status_icon = "🟢" if proj.get("status") == "active" else "📦"
            created = proj.get("created", "").split("T")[0] if proj.get("created") else "N/A"
            print(f"  {status_icon} {proj['name']} (생성: {created})")
    else:
        print("프로젝트가 없습니다. init_project()로 생성하세요.")


def directory_detection_example():
    """디렉토리 자동 감지 예제"""
    
    print("\n🔍 디렉토리 자동 감지 테스트")
    print("=" * 50)
    
    # 현재 위치 표시
    current_dir = Path.cwd()
    print(f"현재 위치: {current_dir}")
    
    # Manager 생성 (자동 감지)
    manager = ResearchProjectManager()
    
    # 감지된 프로젝트 확인
    active = manager.metadata.get("active_project")
    if active:
        print(f"✅ 활성 프로젝트 감지: {active}")
    else:
        print("📍 연구 프로젝트 디렉토리가 아닙니다")
        print("   research_projects/ 하위에서 실행하면 자동 감지됩니다")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  Research Project Manager - 간단한 예제")
    print("=" * 60)
    
    # 1. 기본 사용법
    simple_example()
    
    # 2. 프로젝트 목록
    list_projects_example()
    
    # 3. 디렉토리 감지
    directory_detection_example()
    
    print("\n" + "=" * 60)
    print("  모든 예제 완료! 🎉")
    print("=" * 60)