#!/usr/bin/env python3
"""
Research Project Manager - 다국어 사용 예제
한글과 영어를 자유롭게 사용하는 예제
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_manager_hybrid import HybridResearchManager
from research_manager_korean import 연구관리자


def demonstrate_flexibility():
    """명령어 유연성 시연"""
    
    print("\n🌐 Research Manager - 유연한 명령어 시연")
    print("=" * 60)
    
    # 하이브리드 매니저 생성
    manager = HybridResearchManager()
    
    print("\n1️⃣ 다양한 방식으로 프로젝트 생성:")
    print("-" * 40)
    
    # 한글 명령어
    result1 = manager.execute("생성", "한글프로젝트", "한글로 생성")
    if "error" not in result1:
        print(f"   ✅ '생성' → {result1['project_id']}")
    
    # 영어 명령어
    result2 = manager.execute("init", "english_project", "Created in English")
    if "error" not in result2:
        print(f"   ✅ 'init' → {result2['project_id']}")
    
    # 별칭 사용
    result3 = manager.execute("new", "alias_project", "Using alias")
    if "error" not in result3:
        print(f"   ✅ 'new' → {result3['project_id']}")
    
    print("\n2️⃣ 진행사항 기록 - 언어 혼용:")
    print("-" * 40)
    
    # 한글 명령어 + 영어 내용
    manager.execute("진행", "Completed data preprocessing")
    print("   ✅ 한글 명령 + 영어 내용: '진행' + 'Completed...'")
    
    # 영어 명령어 + 한글 내용
    manager.track_progress("데이터 전처리 완료")
    print("   ✅ 영어 명령 + 한글 내용: 'track_progress' + '데이터...'")
    
    print("\n3️⃣ 축약어와 별칭:")
    print("-" * 40)
    
    commands = [
        ("save", "체크포인트 저장"),      # save = checkpoint
        ("log", "작업 기록"),             # log = track_progress
        ("test", "실험1", "테스트 실험"),  # test = experiment
    ]
    
    for cmd in commands:
        result = manager.execute(*cmd)
        if "error" not in result:
            print(f"   ✅ '{cmd[0]}' 명령어 실행 성공")
    
    print("\n4️⃣ 직접 메서드 호출 (한/영):")
    print("-" * 40)
    
    # 한글 메서드
    manager.마일스톤_설정("첫 단계", "다국어 지원 완료")
    print("   ✅ 한글: 마일스톤_설정()")
    
    # 영어 메서드
    manager.set_hypothesis("Multilingual support improves usability")
    print("   ✅ 영어: set_hypothesis()")
    
    print("\n" + "=" * 60)
    print("✨ 결론: 한글, 영어, 축약어 모두 자유롭게 사용 가능!")
    print("=" * 60)


def korean_only_example():
    """완전 한글 인터페이스 예제"""
    
    print("\n🇰🇷 완전 한글 인터페이스 예제")
    print("=" * 60)
    
    관리자 = 연구관리자()
    
    # 모든 작업을 한글로
    관리자.프로젝트_생성("유전체분석", "한국인 유전체 분석 프로젝트")
    관리자.진행사항_기록("샘플 100개 수집 완료")
    관리자.가설_설정("특정 SNP가 질병과 연관됨")
    관리자.실험_시작("시퀀싱", "NGS 시퀀싱 진행")
    관리자.마일스톤_설정("데이터수집완료", "모든 샘플 시퀀싱 완료")
    
    print("✅ 모든 명령어를 한글로 실행 완료!")
    
    # 프로젝트 목록 확인
    프로젝트들 = 관리자.프로젝트_목록()
    print(f"\n📋 생성된 프로젝트: {len(프로젝트들)}개")
    for 프로젝트 in 프로젝트들[:3]:  # 처음 3개만 표시
        print(f"   - {프로젝트['name']}")


def practical_workflow():
    """실제 워크플로우 - 편한대로 사용"""
    
    print("\n💼 실제 사용 시나리오 - 자유롭게 섞어서")
    print("=" * 60)
    
    m = HybridResearchManager()
    
    # 아침: 한글로 시작
    m.execute("생성", "ai_신약", "AI 기반 신약 개발")
    print("🌅 아침: 프로젝트 생성 (한글)")
    
    # 오전: 국제 협업 - 영어로
    m.track_progress("Collaborated with Harvard team")
    m.track_progress("Received compound library data")
    print("☀️ 오전: 국제 협업 기록 (영어)")
    
    # 점심 후: 다시 한글로
    m.execute("실험", "분자도킹", "AutoDock Vina 사용")
    m.execute("진행", "도킹 시뮬레이션 500개 완료")
    print("🌤️ 오후: 실험 진행 (한글)")
    
    # 저녁: 체크포인트 (축약어)
    m.execute("save", "오늘 작업 완료, 내일 분석 예정")
    print("🌙 저녁: 체크포인트 저장 (축약어)")
    
    print("\n✅ 하루 종일 편한 언어로 작업 완료!")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("   Research Project Manager - 다국어 지원 데모")
    print("=" * 70)
    
    # 1. 유연성 시연
    demonstrate_flexibility()
    
    # 2. 한글 전용 예제
    korean_only_example()
    
    # 3. 실제 워크플로우
    practical_workflow()
    
    print("\n" + "=" * 70)
    print("   🎉 모든 예제 완료! 편한 언어로 사용하세요!")
    print("=" * 70)
    print("\n💡 Tip: HybridResearchManager를 사용하면")
    print("   한글, 영어, 축약어를 자유롭게 섞어 쓸 수 있습니다!")