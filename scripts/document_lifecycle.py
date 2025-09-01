#!/usr/bin/env python3
"""
Document Lifecycle Management System
Manages document status transitions and lifecycle automation
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum
import re

class DocumentStatus(Enum):
    """Document status enumeration"""
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class DocumentLifecycle:
    """Manages document lifecycle and status transitions"""
    
    # Valid status transitions
    TRANSITIONS = {
        DocumentStatus.DRAFT: [DocumentStatus.REVIEW, DocumentStatus.ARCHIVED],
        DocumentStatus.REVIEW: [DocumentStatus.PUBLISHED, DocumentStatus.DRAFT],
        DocumentStatus.PUBLISHED: [DocumentStatus.DEPRECATED, DocumentStatus.REVIEW],
        DocumentStatus.DEPRECATED: [DocumentStatus.ARCHIVED, DocumentStatus.PUBLISHED],
        DocumentStatus.ARCHIVED: []  # Terminal state
    }
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.lifecycle_dir = self.project_root / "docs" / ".lifecycle"
        self.lifecycle_dir.mkdir(parents=True, exist_ok=True)
        
        # Load document metadata and graph
        self.metadata_cache = self._load_metadata_cache()
        self.graph = self._load_graph()
        self.transition_log = self._load_transition_log()
    
    def _load_metadata_cache(self) -> Dict:
        """Load document metadata cache"""
        cache_file = self.project_root / "docs" / ".metadata" / "cache.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_metadata_cache(self):
        """Save metadata cache"""
        cache_file = self.project_root / "docs" / ".metadata" / "cache.json"
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_file, 'w') as f:
            json.dump(self.metadata_cache, f, indent=2, default=str)
    
    def _load_graph(self) -> Dict:
        """Load document graph"""
        graph_file = self.project_root / "docs" / ".graph" / "graph.json"
        if graph_file.exists():
            with open(graph_file, 'r') as f:
                return json.load(f)
        return {'nodes': {}, 'edges': {}, 'reverse_edges': {}}
    
    def _load_transition_log(self) -> List:
        """Load transition history log"""
        log_file = self.lifecycle_dir / "transitions.json"
        if log_file.exists():
            with open(log_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_transition_log(self):
        """Save transition log"""
        log_file = self.lifecycle_dir / "transitions.json"
        with open(log_file, 'w') as f:
            json.dump(self.transition_log, f, indent=2, default=str)
    
    def can_transition(self, doc_id: str, target_status: DocumentStatus) -> bool:
        """Check if a status transition is valid"""
        if doc_id not in self.metadata_cache:
            return False
        
        current_status_str = self.metadata_cache[doc_id].get('status', 'draft')
        try:
            current_status = DocumentStatus(current_status_str)
        except ValueError:
            return False
        
        return target_status in self.TRANSITIONS.get(current_status, [])
    
    def transition_to(self, doc_id: str, target_status: DocumentStatus, reason: str = "") -> bool:
        """Transition a document to a new status"""
        if not self.can_transition(doc_id, target_status):
            return False
        
        old_status = self.metadata_cache[doc_id].get('status')
        self.metadata_cache[doc_id]['status'] = target_status.value
        self.metadata_cache[doc_id]['updated'] = datetime.now().isoformat()
        
        # Log the transition
        self.transition_log.append({
            'doc_id': doc_id,
            'from_status': old_status,
            'to_status': target_status.value,
            'timestamp': datetime.now().isoformat(),
            'reason': reason
        })
        
        self._save_metadata_cache()
        self._save_transition_log()
        
        # Trigger cascading effects
        self._handle_transition_effects(doc_id, target_status)
        
        return True
    
    def _handle_transition_effects(self, doc_id: str, new_status: DocumentStatus):
        """Handle cascading effects of status transitions"""
        
        # If a PRD is updated, mark children for review
        if new_status == DocumentStatus.REVIEW:
            doc_meta = self.metadata_cache.get(doc_id, {})
            if doc_meta.get('type') == 'planning':
                self._cascade_to_children(doc_id, DocumentStatus.REVIEW)
        
        # If a document is archived, check if children should be archived too
        elif new_status == DocumentStatus.ARCHIVED:
            self._check_orphaned_children(doc_id)
    
    def _cascade_to_children(self, parent_id: str, target_status: DocumentStatus):
        """Cascade status change to child documents"""
        edges = self.graph.get('edges', {}).get(parent_id, [])
        
        for child_id, relation in edges:
            if relation == 'generates' and child_id in self.metadata_cache:
                child_status = self.metadata_cache[child_id].get('status')
                if child_status != 'archived':
                    self.transition_to(child_id, target_status, 
                                     f"Parent {parent_id} changed to {target_status.value}")
    
    def _check_orphaned_children(self, parent_id: str):
        """Check if children should be archived when parent is archived"""
        edges = self.graph.get('edges', {}).get(parent_id, [])
        
        for child_id, relation in edges:
            if relation == 'generates' and child_id in self.metadata_cache:
                # Check if child has other active parents
                reverse_edges = self.graph.get('reverse_edges', {}).get(child_id, [])
                active_parents = [
                    p for p, r in reverse_edges 
                    if r == 'generates' and p != parent_id 
                    and self.metadata_cache.get(p, {}).get('status') != 'archived'
                ]
                
                if not active_parents:
                    # No other active parents, consider archiving
                    self.transition_to(child_id, DocumentStatus.ARCHIVED,
                                     f"Parent {parent_id} archived and no other active parents")
    
    def auto_transition_stale_documents(self, days_threshold: int = 30):
        """Automatically transition stale documents"""
        now = datetime.now()
        threshold = now - timedelta(days=days_threshold)
        
        transitions_made = []
        
        for doc_id, metadata in self.metadata_cache.items():
            updated_str = metadata.get('updated', metadata.get('created'))
            if not updated_str:
                continue
            
            # Parse ISO format datetime
            updated = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
            
            current_status = DocumentStatus(metadata.get('status', 'draft'))
            
            # Check if document is stale
            if updated < threshold:
                if current_status == DocumentStatus.PUBLISHED:
                    if self.transition_to(doc_id, DocumentStatus.DEPRECATED, 
                                        f"No updates for {days_threshold} days"):
                        transitions_made.append((doc_id, 'published', 'deprecated'))
                
                elif current_status == DocumentStatus.DRAFT:
                    if self.transition_to(doc_id, DocumentStatus.ARCHIVED,
                                        f"Draft unchanged for {days_threshold} days"):
                        transitions_made.append((doc_id, 'draft', 'archived'))
        
        return transitions_made
    
    def check_trigger_validity(self, doc_id: str) -> bool:
        """Check if document triggers (related code files) still exist"""
        if doc_id not in self.metadata_cache:
            return False
        
        triggers = self.metadata_cache[doc_id].get('triggers', [])
        
        for trigger in triggers:
            trigger_path = self.project_root / trigger
            if not trigger_path.exists():
                return False
        
        return True if triggers else True  # Return True if no triggers
    
    def auto_archive_invalid_documents(self) -> List[str]:
        """Archive documents whose triggers no longer exist"""
        archived = []
        
        for doc_id, metadata in self.metadata_cache.items():
            if metadata.get('status') == 'archived':
                continue
            
            if not self.check_trigger_validity(doc_id):
                if self.transition_to(doc_id, DocumentStatus.ARCHIVED,
                                    "Related code files no longer exist"):
                    archived.append(doc_id)
        
        return archived
    
    def get_transition_history(self, doc_id: Optional[str] = None) -> List[Dict]:
        """Get transition history for a document or all documents"""
        if doc_id:
            return [t for t in self.transition_log if t['doc_id'] == doc_id]
        return self.transition_log
    
    def get_documents_by_age(self, status: Optional[DocumentStatus] = None) -> List[Tuple[str, int]]:
        """Get documents sorted by age (days since last update)"""
        now = datetime.now()
        documents_with_age = []
        
        for doc_id, metadata in self.metadata_cache.items():
            if status and metadata.get('status') != status.value:
                continue
            
            updated_str = metadata.get('updated', metadata.get('created'))
            if updated_str:
                updated = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
                age_days = (now - updated).days
                documents_with_age.append((doc_id, age_days))
        
        return sorted(documents_with_age, key=lambda x: x[1], reverse=True)
    
    def suggest_transitions(self) -> Dict[str, List[Dict]]:
        """Suggest recommended status transitions"""
        suggestions = {
            'stale_published': [],
            'ready_for_review': [],
            'orphaned': [],
            'invalid_triggers': []
        }
        
        for doc_id, metadata in self.metadata_cache.items():
            status = metadata.get('status')
            
            # Check for stale published documents
            if status == 'published':
                age = self._get_document_age_days(doc_id)
                if age > 30:
                    suggestions['stale_published'].append({
                        'doc_id': doc_id,
                        'age_days': age,
                        'suggested_action': 'deprecate'
                    })
            
            # Check for drafts that might be ready for review
            elif status == 'draft':
                age = self._get_document_age_days(doc_id)
                if 3 <= age <= 30:  # Not too new, not too old
                    suggestions['ready_for_review'].append({
                        'doc_id': doc_id,
                        'age_days': age,
                        'suggested_action': 'review'
                    })
            
            # Check for orphaned documents
            reverse_edges = self.graph.get('reverse_edges', {}).get(doc_id, [])
            if not reverse_edges and status not in ['published', 'archived']:
                suggestions['orphaned'].append({
                    'doc_id': doc_id,
                    'status': status,
                    'suggested_action': 'link or archive'
                })
            
            # Check for invalid triggers
            if not self.check_trigger_validity(doc_id) and status != 'archived':
                suggestions['invalid_triggers'].append({
                    'doc_id': doc_id,
                    'status': status,
                    'suggested_action': 'archive'
                })
        
        return suggestions
    
    def _get_document_age_days(self, doc_id: str) -> int:
        """Get document age in days"""
        metadata = self.metadata_cache.get(doc_id, {})
        updated_str = metadata.get('updated', metadata.get('created'))
        
        if not updated_str:
            return 0
        
        updated = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
        return (datetime.now() - updated).days
    
    def generate_lifecycle_report(self) -> str:
        """Generate a comprehensive lifecycle report"""
        report = []
        report.append("📊 Document Lifecycle Report")
        report.append("=" * 50)
        
        # Status distribution
        status_counts = {}
        for metadata in self.metadata_cache.values():
            status = metadata.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        report.append("\n📋 Status Distribution:")
        for status, count in sorted(status_counts.items()):
            report.append(f"  {status}: {count}")
        
        # Recent transitions
        recent_transitions = self.transition_log[-5:] if self.transition_log else []
        if recent_transitions:
            report.append("\n🔄 Recent Transitions:")
            for trans in reversed(recent_transitions):
                report.append(f"  {trans['doc_id']}: {trans['from_status']} → {trans['to_status']}")
        
        # Suggestions
        suggestions = self.suggest_transitions()
        
        if suggestions['stale_published']:
            report.append(f"\n⚠️  Stale Published Documents ({len(suggestions['stale_published'])}):")
            for item in suggestions['stale_published'][:3]:
                report.append(f"  - {item['doc_id']} ({item['age_days']} days old)")
        
        if suggestions['ready_for_review']:
            report.append(f"\n✅ Ready for Review ({len(suggestions['ready_for_review'])}):")
            for item in suggestions['ready_for_review'][:3]:
                report.append(f"  - {item['doc_id']} ({item['age_days']} days old)")
        
        if suggestions['orphaned']:
            report.append(f"\n🔗 Orphaned Documents ({len(suggestions['orphaned'])}):")
            for item in suggestions['orphaned'][:3]:
                report.append(f"  - {item['doc_id']} (status: {item['status']})")
        
        return "\n".join(report)


def main():
    """Test the lifecycle system"""
    lifecycle = DocumentLifecycle()
    
    # Test data - simulate some documents
    test_docs = {
        "doc_001": {
            "type": "planning",
            "status": "published",
            "created": (datetime.now() - timedelta(days=45)).isoformat(),
            "updated": (datetime.now() - timedelta(days=35)).isoformat()
        },
        "doc_002": {
            "type": "tutorial",
            "status": "draft",
            "created": (datetime.now() - timedelta(days=5)).isoformat(),
            "updated": (datetime.now() - timedelta(days=2)).isoformat()
        },
        "doc_003": {
            "type": "test",
            "status": "review",
            "created": (datetime.now() - timedelta(days=10)).isoformat(),
            "updated": (datetime.now() - timedelta(days=1)).isoformat(),
            "triggers": ["nonexistent.py"]
        }
    }
    
    # Simulate metadata cache
    lifecycle.metadata_cache = test_docs
    lifecycle._save_metadata_cache()
    
    # Test lifecycle operations
    print("Initial Report:")
    print(lifecycle.generate_lifecycle_report())
    
    print("\n" + "="*50 + "\n")
    
    # Test transitions
    print("Testing Transitions:")
    if lifecycle.can_transition("doc_002", DocumentStatus.REVIEW):
        lifecycle.transition_to("doc_002", DocumentStatus.REVIEW, "Ready for review")
        print("✅ Transitioned doc_002 to review")
    
    # Auto transitions
    print("\nAuto-transitioning stale documents...")
    transitions = lifecycle.auto_transition_stale_documents(30)
    for doc_id, from_status, to_status in transitions:
        print(f"  {doc_id}: {from_status} → {to_status}")
    
    print("\n" + "="*50 + "\n")
    
    print("Final Report:")
    print(lifecycle.generate_lifecycle_report())


if __name__ == "__main__":
    main()