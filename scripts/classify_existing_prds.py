#!/usr/bin/env python3
"""
기존 PRD 파일들을 새로운 위계 체계로 자동 분류
"""

import os
import re
from pathlib import Path

# 분류 키워드 맵
CLASSIFICATION_MAP = {
    'VISION': ['비전', 'vision', '장기', '전체', 'overall'],
    'STRATEGY': ['전략', 'strategy', '사업', '비즈니스', 'business'],
    'ROADMAP': ['로드맵', 'roadmap', '일정', '계획', 'plan'],
    'PHASE': ['페이즈', 'phase', '스프린트', 'sprint', 'v1', 'v2'],
    'FEATURE': ['기능', 'feature', '구현', '개발', 'dev'],
    'SPIKE': ['조사', 'spike', '연구', 'research', '분석', 'analysis']
}

def classify_document(filepath):
    """파일 내용 분석하여 문서 타입 결정"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    
    filename = Path(filepath).name.lower()
    
    # 파일명과 내용을 종합하여 점수 계산
    scores = {}
    for doc_type, keywords in CLASSIFICATION_MAP.items():
        score = 0
        for keyword in keywords:
            score += content.count(keyword) * 2
            score += filename.count(keyword) * 5
        scores[doc_type] = score
    
    # 최고 점수 문서 타입 반환
    best_type = max(scores.items(), key=lambda x: x[1])
    return best_type[0] if best_type[1] > 0 else 'UNKNOWN'

def migrate_prd_files():
    """PRD 파일들을 새 구조로 이동"""
    prd_files = list(Path('.').glob('**/*PRD*.md')) + \
                list(Path('.').glob('**/*prd*.md'))
    
    for filepath in prd_files:
        doc_type = classify_document(filepath)
        
        # 새 파일명 생성
        if doc_type == 'VISION':
            new_path = Path('docs/VISION.md')
        elif doc_type == 'STRATEGY':
            new_path = Path('docs/STRATEGY.md')
        elif doc_type == 'ROADMAP':
            new_path = Path('docs/ROADMAP.md')
        elif doc_type.startswith('PHASE'):
            # 버전 번호 추출 시도
            version_match = re.search(r'v?(\d+)', filepath.name)
            phase_num = version_match.group(1) if version_match else '01'
            new_path = Path(f'docs/phases/PHASE-{phase_num:0>2}-{filepath.stem}.md')
        elif doc_type == 'FEATURE':
            new_path = Path(f'docs/features/FEAT-{filepath.stem}.md')
        else:
            new_path = Path(f'docs/archive/legacy/{filepath.name}')
        
        # 디렉토리 생성 및 파일 이동
        new_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not new_path.exists():
            filepath.rename(new_path)
            print(f"✅ {filepath} → {new_path}")
        else:
            print(f"⚠️ {new_path} already exists, skipping {filepath}")

if __name__ == '__main__':
    migrate_prd_files()