#!/usr/bin/env python3
"""
문서 메타데이터 자동 추가 스크립트
"""
import os
import re
import sys
from datetime import datetime
from pathlib import Path

METADATA_TEMPLATE = """<!--
@meta
id: {doc_type}_{timestamp}_{title}
type: {doc_type}
scope: {scope}
status: {status}
created: {created}
updated: {updated}
tags: {tags}
related: {related}
-->

"""

def add_metadata(filepath, doc_type=None, scope=None, tags=None):
    """문서에 메타데이터 추가"""
    if not Path(filepath).exists():
        print(f"❌ File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 이미 메타데이터가 있으면 스킵
    if '@meta' in content:
        print(f"⚠️ Metadata already exists in {filepath}")
        return
    
    # 자동으로 타입 감지
    if not doc_type:
        doc_type = detect_document_type(filepath)
    
    # 자동으로 스코프 감지
    if not scope:
        scope = detect_scope(filepath)
    
    # 자동으로 태그 생성
    if not tags:
        tags = generate_tags(filepath)
    
    metadata = METADATA_TEMPLATE.format(
        doc_type=doc_type,
        timestamp=datetime.now().strftime('%Y%m%d_%H%M'),
        title=Path(filepath).stem,
        scope=scope,
        status='active' if 'current' in str(filepath).lower() else 'archived',
        created=datetime.now().strftime('%Y-%m-%d'),
        updated=datetime.now().strftime('%Y-%m-%d'),
        tags=', '.join(tags) if isinstance(tags, list) else tags,
        related=''
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(metadata + content)
    
    print(f"✅ Added metadata to {filepath}")

def detect_document_type(filepath):
    """파일 경로와 이름으로 문서 타입 감지"""
    path_str = str(filepath).lower()
    filename = Path(filepath).name.lower()
    
    if 'vision' in filename:
        return 'vision'
    elif 'strategy' in filename:
        return 'strategy'
    elif 'roadmap' in filename:
        return 'roadmap'
    elif '/phases/' in path_str or 'phase' in filename:
        return 'phase'
    elif '/features/' in path_str or 'feat' in filename:
        return 'feature'
    elif '/spikes/' in path_str or 'spike' in filename:
        return 'spike'
    else:
        return 'document'

def detect_scope(filepath):
    """문서의 범위 감지"""
    doc_type = detect_document_type(filepath)
    
    scope_map = {
        'vision': 'strategic',
        'strategy': 'strategic', 
        'roadmap': 'tactical',
        'phase': 'tactical',
        'feature': 'operational',
        'spike': 'operational'
    }
    
    return scope_map.get(doc_type, 'operational')

def generate_tags(filepath):
    """파일 경로와 내용으로 태그 자동 생성"""
    tags = []
    
    # 디렉토리 기반 태그
    parts = Path(filepath).parts
    for part in parts:
        if part not in ['.', '..', 'docs', 'archive']:
            tags.append(part)
    
    # 파일명 기반 태그
    filename = Path(filepath).stem
    filename_parts = re.split(r'[-_\s]+', filename)
    tags.extend([part for part in filename_parts if len(part) > 2])
    
    return list(set(tags))[:5]  # 최대 5개 태그

def process_all_documents():
    """모든 markdown 문서에 메타데이터 추가"""
    md_files = list(Path('.').glob('**/*.md'))
    
    for md_file in md_files:
        # .git 디렉토리는 스킵
        if '.git' in str(md_file):
            continue
            
        add_metadata(md_file)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # 특정 파일 처리
        filepath = sys.argv[1]
        doc_type = sys.argv[2] if len(sys.argv) > 2 else None
        scope = sys.argv[3] if len(sys.argv) > 3 else None
        tags = sys.argv[4].split(',') if len(sys.argv) > 4 else None
        
        add_metadata(filepath, doc_type, scope, tags)
    else:
        # 모든 문서 처리
        process_all_documents()