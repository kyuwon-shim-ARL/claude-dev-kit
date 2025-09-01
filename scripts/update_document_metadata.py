#!/usr/bin/env python3
"""
Update document metadata - used by Git hooks
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from document_metadata import DocumentMetadata
from document_graph import DocumentGraph
from pathlib import Path

def update_file_metadata(file_path: str):
    """Update metadata for a single file"""
    
    if not file_path.endswith('.md'):
        return
    
    if not Path(file_path).exists():
        return
    
    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Initialize systems
    dm = DocumentMetadata()
    graph = DocumentGraph()
    
    # Get current context (simplified for hook usage)
    context = {
        'session_id': f'git_commit_{os.getenv("GIT_AUTHOR_DATE", "unknown")}',
        'current_file': file_path
    }
    
    # Update metadata
    updated_content = dm.insert_metadata_into_document(file_path, content, context)
    
    # Write back if changed
    if updated_content != content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        
        # Extract metadata and update graph
        metadata = dm.extract_metadata_from_document(file_path)
        if metadata:
            graph.add_document(metadata['id'], metadata)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_file_metadata(sys.argv[1])
