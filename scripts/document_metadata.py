#!/usr/bin/env python3
"""
Document Metadata Management System
Automatically inserts and manages metadata for all documents
"""

import os
import yaml
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import re

class DocumentMetadata:
    """Manages document metadata insertion and tracking"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.metadata_dir = self.project_root / "docs" / ".metadata"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_cache = self._load_metadata_cache()
    
    def _load_metadata_cache(self) -> Dict:
        """Load existing metadata cache"""
        cache_file = self.metadata_dir / "cache.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_metadata_cache(self):
        """Save metadata cache to disk"""
        cache_file = self.metadata_dir / "cache.json"
        with open(cache_file, 'w') as f:
            json.dump(self.metadata_cache, f, indent=2, default=str)
    
    def generate_document_id(self, doc_path: str, doc_type: str) -> str:
        """Generate unique document ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_part = Path(doc_path).stem.replace('-', '_').replace(' ', '_')[:20]
        return f"doc_{timestamp}_{name_part}"
    
    def detect_document_type(self, content: str, file_path: str) -> str:
        """Automatically detect document type from content and path"""
        path_lower = file_path.lower()
        content_lower = content.lower()
        
        # Path-based detection
        if 'tutorial' in path_lower or 'guide' in path_lower:
            return 'tutorial'
        elif 'planning' in path_lower or 'prd' in path_lower:
            return 'planning'
        elif 'research' in path_lower or 'analysis' in path_lower:
            return 'research'
        elif 'test' in path_lower:
            return 'test'
        elif 'api' in path_lower:
            return 'api'
        
        # Content-based detection
        if any(word in content_lower for word in ['how to', 'step by step', 'tutorial']):
            return 'tutorial'
        elif any(word in content_lower for word in ['requirements', 'specifications', 'goals']):
            return 'planning'
        elif any(word in content_lower for word in ['analysis', 'research', 'benchmark']):
            return 'research'
        elif any(word in content_lower for word in ['test', 'assert', 'expect']):
            return 'test'
        
        return 'documentation'
    
    def find_parent_document(self, current_context: Dict) -> Optional[str]:
        """Find parent document from current context"""
        # Check if explicitly referenced in context
        if 'parent' in current_context:
            return current_context['parent']
        
        # Look for PRD or main planning documents
        prd_pattern = re.compile(r'PRD[_\-]?v?\d*\.?\d*', re.IGNORECASE)
        for doc_id, metadata in self.metadata_cache.items():
            if metadata.get('type') == 'planning':
                if prd_pattern.search(metadata.get('file_path', '')):
                    return doc_id
        
        return None
    
    def extract_triggers(self, current_context: Dict) -> List[str]:
        """Extract trigger files from current context"""
        triggers = []
        
        # Check for explicitly mentioned files
        if 'modified_files' in current_context:
            triggers.extend(current_context['modified_files'])
        
        # Check for files in current working context
        if 'current_file' in current_context:
            triggers.append(current_context['current_file'])
        
        return list(set(triggers))  # Remove duplicates
    
    def create_metadata(self, 
                       file_path: str, 
                       content: str,
                       current_context: Optional[Dict] = None) -> Dict:
        """Create metadata for a document"""
        if current_context is None:
            current_context = {}
        
        doc_type = self.detect_document_type(content, file_path)
        doc_id = self.generate_document_id(file_path, doc_type)
        
        metadata = {
            'id': doc_id,
            'type': doc_type,
            'status': 'draft',
            'parent': self.find_parent_document(current_context),
            'triggers': self.extract_triggers(current_context),
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'session': current_context.get('session_id', 'unknown'),
            'context_hash': hashlib.sha256(
                json.dumps(current_context, sort_keys=True).encode()
            ).hexdigest()[:12],
            'file_path': file_path,
            'references': [],  # Will be populated by reference graph
            'keywords': self._extract_keywords(content)
        }
        
        # Cache the metadata
        self.metadata_cache[doc_id] = metadata
        self._save_metadata_cache()
        
        return metadata
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from document content"""
        # Simple keyword extraction - can be enhanced with NLP
        important_words = []
        
        # Extract headers (markdown)
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        important_words.extend(headers)
        
        # Extract bold text
        bold = re.findall(r'\*\*([^*]+)\*\*', content)
        important_words.extend(bold)
        
        # Clean and deduplicate
        keywords = []
        for word in important_words:
            cleaned = word.strip().lower()
            if cleaned and cleaned not in keywords:
                keywords.append(cleaned)
        
        return keywords[:10]  # Limit to 10 keywords
    
    def insert_metadata_into_document(self, 
                                     file_path: str,
                                     content: str,
                                     current_context: Optional[Dict] = None) -> str:
        """Insert metadata into document as YAML front matter"""
        
        # Check if document already has metadata
        if content.startswith('---\nmeta:'):
            # Update existing metadata
            return self._update_existing_metadata(file_path, content, current_context)
        
        # Create new metadata
        metadata = self.create_metadata(file_path, content, current_context)
        
        # Format as YAML front matter
        yaml_metadata = yaml.dump({'meta': metadata}, default_flow_style=False)
        
        # Insert at beginning of document
        return f"---\n{yaml_metadata}---\n\n{content}"
    
    def _update_existing_metadata(self, 
                                 file_path: str,
                                 content: str,
                                 current_context: Optional[Dict] = None) -> str:
        """Update existing metadata in document"""
        # Extract existing metadata
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            return content
        
        try:
            existing_meta = yaml.safe_load(match.group(1))
            metadata = existing_meta.get('meta', {})
            
            # Update only changeable fields
            metadata['updated'] = datetime.now().isoformat()
            if current_context:
                metadata['session'] = current_context.get('session_id', metadata.get('session'))
                new_triggers = self.extract_triggers(current_context)
                existing_triggers = metadata.get('triggers', [])
                metadata['triggers'] = list(set(existing_triggers + new_triggers))
            
            # Update cache
            self.metadata_cache[metadata['id']] = metadata
            self._save_metadata_cache()
            
            # Rebuild document with updated metadata
            yaml_metadata = yaml.dump({'meta': metadata}, default_flow_style=False)
            document_content = content[match.end():]
            
            return f"---\n{yaml_metadata}---\n{document_content}"
            
        except yaml.YAMLError:
            return content
    
    def extract_metadata_from_document(self, file_path: str) -> Optional[Dict]:
        """Extract metadata from an existing document"""
        if not Path(file_path).exists():
            return None
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            return None
        
        try:
            meta_data = yaml.safe_load(match.group(1))
            return meta_data.get('meta')
        except yaml.YAMLError:
            return None
    
    def update_document_status(self, doc_id: str, new_status: str) -> bool:
        """Update document status"""
        valid_statuses = ['draft', 'review', 'published', 'deprecated', 'archived']
        
        if new_status not in valid_statuses:
            return False
        
        if doc_id in self.metadata_cache:
            self.metadata_cache[doc_id]['status'] = new_status
            self.metadata_cache[doc_id]['updated'] = datetime.now().isoformat()
            self._save_metadata_cache()
            return True
        
        return False
    
    def get_documents_by_status(self, status: str) -> List[Dict]:
        """Get all documents with a specific status"""
        return [
            meta for meta in self.metadata_cache.values()
            if meta.get('status') == status
        ]
    
    def get_documents_by_type(self, doc_type: str) -> List[Dict]:
        """Get all documents of a specific type"""
        return [
            meta for meta in self.metadata_cache.values()
            if meta.get('type') == doc_type
        ]


def main():
    """Test the metadata system"""
    dm = DocumentMetadata()
    
    # Test document
    test_content = """# Authentication Guide

This tutorial shows how to implement authentication in your application.

## Prerequisites
- Python 3.8+
- FastAPI

## Steps
1. Install dependencies
2. Configure authentication
3. Test the system
"""
    
    # Test context
    test_context = {
        'session_id': 'test_session_001',
        'modified_files': ['auth.py', 'auth_test.py'],
        'current_file': 'docs/tutorials/auth_guide.md'
    }
    
    # Insert metadata
    result = dm.insert_metadata_into_document(
        'docs/tutorials/auth_guide.md',
        test_content,
        test_context
    )
    
    print("Document with metadata:")
    print(result)
    print("\n" + "="*50 + "\n")
    
    # Show cached metadata
    print("Cached metadata:")
    print(json.dumps(dm.metadata_cache, indent=2, default=str))


if __name__ == "__main__":
    main()