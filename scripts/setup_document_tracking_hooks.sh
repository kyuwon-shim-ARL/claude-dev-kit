#!/bin/bash
# Setup script for document tracking Git hooks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}📋 Setting up Document Tracking System Git Hooks${NC}"
echo "================================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    echo "Please run this script from the root of your git repository"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Document Tracking System - Pre-commit Hook

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python3 not found. Skipping document tracking."
    exit 0
fi

# Check if tracking scripts exist
SCRIPT_DIR="scripts"
if [ ! -f "$SCRIPT_DIR/document_metadata.py" ]; then
    # Silently skip if scripts not found (not all repos need tracking)
    exit 0
fi

echo "📊 Updating document metadata and graph..."

# Update metadata for modified markdown files
for file in $(git diff --cached --name-only --diff-filter=AM | grep '\.md$'); do
    if [ -f "$file" ]; then
        echo "  Processing: $file"
        python3 "$SCRIPT_DIR/update_document_metadata.py" "$file" 2>/dev/null || true
    fi
done

# Rebuild document graph
if [ -f "$SCRIPT_DIR/document_graph.py" ]; then
    python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from document_graph import DocumentGraph
graph = DocumentGraph()
stats = graph.get_statistics()
print(f'  📈 Graph updated: {stats[\"total_documents\"]} documents, {stats[\"total_edges\"]} connections')
" 2>/dev/null || true
fi

# Check document lifecycle
if [ -f "$SCRIPT_DIR/document_lifecycle.py" ]; then
    python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from document_lifecycle import DocumentLifecycle
lifecycle = DocumentLifecycle()
suggestions = lifecycle.suggest_transitions()

# Show warnings for important transitions
if suggestions['stale_published']:
    print('  ⚠️  Warning: {} stale published documents'.format(len(suggestions['stale_published'])))
if suggestions['invalid_triggers']:
    print('  ⚠️  Warning: {} documents with invalid triggers'.format(len(suggestions['invalid_triggers'])))
" 2>/dev/null || true
fi

# Add updated metadata files to commit
if [ -d "docs/.metadata" ]; then
    git add docs/.metadata/* 2>/dev/null || true
fi
if [ -d "docs/.graph" ]; then
    git add docs/.graph/* 2>/dev/null || true
fi
if [ -d "docs/.lifecycle" ]; then
    git add docs/.lifecycle/* 2>/dev/null || true
fi

exit 0
EOF

# Create post-commit hook
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Document Tracking System - Post-commit Hook

# Only run if tracking is enabled
if [ ! -f "scripts/document_lifecycle.py" ]; then
    exit 0
fi

echo "📋 Document tracking post-commit analysis..."

python3 -c "
import sys
sys.path.insert(0, 'scripts')
from document_lifecycle import DocumentLifecycle

lifecycle = DocumentLifecycle()
report = lifecycle.generate_lifecycle_report()
print(report)

# Auto-transition stale documents
transitions = lifecycle.auto_transition_stale_documents(30)
if transitions:
    print('\n🔄 Auto-transitions performed:')
    for doc_id, from_status, to_status in transitions:
        print(f'  {doc_id}: {from_status} → {to_status}')
" 2>/dev/null || true

exit 0
EOF

# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit

# Create the update script for manual metadata updates
cat > scripts/update_document_metadata.py << 'EOF'
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
EOF

chmod +x scripts/update_document_metadata.py

# Create a test to verify the system works
cat > scripts/test_document_tracking.py << 'EOF'
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
EOF

chmod +x scripts/test_document_tracking.py

echo ""
echo -e "${GREEN}✅ Git hooks installed successfully!${NC}"
echo ""
echo "The following hooks have been created:"
echo "  • pre-commit: Automatically updates document metadata"
echo "  • post-commit: Performs lifecycle analysis"
echo ""
echo "The system will track:"
echo "  📋 Document metadata (type, status, references)"
echo "  📊 Document relationships (parent-child, triggers)"
echo "  🔄 Lifecycle transitions (draft → review → published)"
echo ""
echo -e "${YELLOW}To test the system, run:${NC}"
echo "  python3 scripts/test_document_tracking.py"
echo ""
echo -e "${YELLOW}To manually update a document's metadata:${NC}"
echo "  python3 scripts/update_document_metadata.py <file.md>"