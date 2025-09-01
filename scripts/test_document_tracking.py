#!/usr/bin/env python3
"""
Test the document tracking system
"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from document_metadata import DocumentMetadata
from document_graph import DocumentGraph
from document_lifecycle import DocumentLifecycle, DocumentStatus

def test_system():
    """Test all components of the tracking system"""
    
    print("🧪 Testing Document Tracking System")
    print("=" * 40)
    
    # Test 1: Metadata insertion
    print("\n1. Testing metadata insertion...")
    dm = DocumentMetadata()
    test_content = "# Test Document\n\nThis is a test."
    result = dm.insert_metadata_into_document(
        "test.md", 
        test_content,
        {'session_id': 'test_session'}
    )
    
    if "---\nmeta:" in result:
        print("   ✅ Metadata insertion works")
    else:
        print("   ❌ Metadata insertion failed")
        return False
    
    # Test 2: Graph building
    print("\n2. Testing graph system...")
    graph = DocumentGraph()
    graph.add_document("test_001", {
        "type": "planning",
        "status": "draft",
        "file_path": "test.md"
    })
    
    stats = graph.get_statistics()
    if stats['total_documents'] > 0:
        print(f"   ✅ Graph system works ({stats['total_documents']} documents)")
    else:
        print("   ❌ Graph system failed")
        return False
    
    # Test 3: Lifecycle management
    print("\n3. Testing lifecycle management...")
    lifecycle = DocumentLifecycle()
    
    # Add test document to cache
    lifecycle.metadata_cache["test_001"] = {
        "type": "planning",
        "status": "draft",
        "created": "2024-01-01T00:00:00"
    }
    
    if lifecycle.can_transition("test_001", DocumentStatus.REVIEW):
        print("   ✅ Lifecycle transitions work")
    else:
        print("   ❌ Lifecycle transitions failed")
        return False
    
    print("\n" + "=" * 40)
    print("✅ All tests passed! System is ready.")
    return True

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)
