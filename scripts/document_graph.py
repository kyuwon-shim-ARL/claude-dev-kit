#!/usr/bin/env python3
"""
Document Reference Graph System
Builds and manages relationships between documents
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
import re
from collections import defaultdict

class DocumentGraph:
    """Manages document relationships and reference graph"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.graph_dir = self.project_root / "docs" / ".graph"
        self.graph_dir.mkdir(parents=True, exist_ok=True)
        
        # Graph structure: adjacency list representation
        self.nodes = {}  # doc_id -> metadata
        self.edges = defaultdict(list)  # doc_id -> [(target_id, relation_type)]
        self.reverse_edges = defaultdict(list)  # For finding parents
        
        self._load_graph()
    
    def _load_graph(self):
        """Load existing graph from disk"""
        graph_file = self.graph_dir / "graph.json"
        if graph_file.exists():
            with open(graph_file, 'r') as f:
                data = json.load(f)
                self.nodes = data.get('nodes', {})
                self.edges = defaultdict(list, data.get('edges', {}))
                self.reverse_edges = defaultdict(list, data.get('reverse_edges', {}))
    
    def _save_graph(self):
        """Save graph to disk"""
        graph_file = self.graph_dir / "graph.json"
        data = {
            'nodes': self.nodes,
            'edges': dict(self.edges),
            'reverse_edges': dict(self.reverse_edges),
            'last_updated': datetime.now().isoformat()
        }
        with open(graph_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def add_document(self, doc_id: str, metadata: Dict):
        """Add a document node to the graph"""
        self.nodes[doc_id] = {
            **metadata,
            'added_to_graph': datetime.now().isoformat()
        }
        
        # Add edges based on metadata
        if metadata.get('parent'):
            self.add_edge(metadata['parent'], doc_id, 'generates')
        
        for trigger in metadata.get('triggers', []):
            # Triggers are code files that led to document creation
            self.add_edge(trigger, doc_id, 'documents')
        
        self._save_graph()
    
    def add_edge(self, source: str, target: str, relation_type: str):
        """Add an edge between two documents"""
        # Forward edge
        if (target, relation_type) not in self.edges[source]:
            self.edges[source].append((target, relation_type))
        
        # Reverse edge for efficient parent lookup
        if (source, relation_type) not in self.reverse_edges[target]:
            self.reverse_edges[target].append((source, relation_type))
        
        self._save_graph()
    
    def remove_edge(self, source: str, target: str):
        """Remove an edge between two documents"""
        # Remove all edges between source and target
        self.edges[source] = [(t, r) for t, r in self.edges[source] if t != target]
        self.reverse_edges[target] = [(s, r) for s, r in self.reverse_edges[target] if s != source]
        self._save_graph()
    
    def get_neighbors(self, doc_id: str, relation_type: Optional[str] = None) -> List[str]:
        """Get all neighbors of a document"""
        if relation_type:
            return [target for target, rel in self.edges.get(doc_id, []) if rel == relation_type]
        return [target for target, rel in self.edges.get(doc_id, [])]
    
    def get_parents(self, doc_id: str) -> List[str]:
        """Get all parent documents"""
        return [source for source, rel in self.reverse_edges.get(doc_id, []) if rel == 'generates']
    
    def get_children(self, doc_id: str) -> List[str]:
        """Get all child documents"""
        return self.get_neighbors(doc_id, 'generates')
    
    def find_related_documents(self, doc_id: str, max_depth: int = 2) -> Dict[int, Set[str]]:
        """Find all related documents up to max_depth"""
        visited = set()
        levels = defaultdict(set)
        queue = [(doc_id, 0)]
        
        while queue:
            current, depth = queue.pop(0)
            
            if current in visited or depth > max_depth:
                continue
            
            visited.add(current)
            levels[depth].add(current)
            
            # Add neighbors to queue
            for neighbor, _ in self.edges.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
            
            # Also check reverse edges
            for parent, _ in self.reverse_edges.get(current, []):
                if parent not in visited:
                    queue.append((parent, depth + 1))
        
        return dict(levels)
    
    def get_document_lineage(self, doc_id: str) -> Dict:
        """Get complete lineage of a document"""
        ancestors = self._get_all_ancestors(doc_id)
        descendants = self._get_all_descendants(doc_id)
        siblings = self._get_siblings(doc_id)
        
        return {
            'ancestors': list(ancestors),
            'descendants': list(descendants),
            'siblings': list(siblings),
            'immediate_parent': self.get_parents(doc_id)[0] if self.get_parents(doc_id) else None,
            'immediate_children': self.get_children(doc_id)
        }
    
    def _get_all_ancestors(self, doc_id: str) -> Set[str]:
        """Recursively get all ancestors"""
        ancestors = set()
        queue = [doc_id]
        
        while queue:
            current = queue.pop(0)
            parents = self.get_parents(current)
            for parent in parents:
                if parent not in ancestors:
                    ancestors.add(parent)
                    queue.append(parent)
        
        return ancestors
    
    def _get_all_descendants(self, doc_id: str) -> Set[str]:
        """Recursively get all descendants"""
        descendants = set()
        queue = [doc_id]
        
        while queue:
            current = queue.pop(0)
            children = self.get_children(current)
            for child in children:
                if child not in descendants:
                    descendants.add(child)
                    queue.append(child)
        
        return descendants
    
    def _get_siblings(self, doc_id: str) -> Set[str]:
        """Get sibling documents (same parent)"""
        siblings = set()
        parents = self.get_parents(doc_id)
        
        for parent in parents:
            children = self.get_children(parent)
            siblings.update(child for child in children if child != doc_id)
        
        return siblings
    
    def find_orphaned_documents(self) -> List[str]:
        """Find documents with no parents or children"""
        orphans = []
        
        for doc_id in self.nodes:
            if not self.get_parents(doc_id) and not self.get_children(doc_id):
                if doc_id not in self.edges and doc_id not in self.reverse_edges:
                    orphans.append(doc_id)
        
        return orphans
    
    def detect_cycles(self) -> List[List[str]]:
        """Detect cycles in the document graph"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor, _ in self.edges.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor, path.copy()):
                        return True
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            
            rec_stack.remove(node)
            return False
        
        for node in self.nodes:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def get_statistics(self) -> Dict:
        """Get graph statistics"""
        stats = {
            'total_documents': len(self.nodes),
            'total_edges': sum(len(edges) for edges in self.edges.values()),
            'orphaned_documents': len(self.find_orphaned_documents()),
            'cycles_detected': len(self.detect_cycles()),
            'document_types': defaultdict(int),
            'document_statuses': defaultdict(int),
            'average_connections': 0
        }
        
        # Count by type and status
        for node in self.nodes.values():
            stats['document_types'][node.get('type', 'unknown')] += 1
            stats['document_statuses'][node.get('status', 'unknown')] += 1
        
        # Calculate average connections
        if self.nodes:
            total_connections = sum(
                len(self.edges.get(doc_id, [])) + len(self.reverse_edges.get(doc_id, []))
                for doc_id in self.nodes
            )
            stats['average_connections'] = total_connections / len(self.nodes)
        
        return stats
    
    def visualize_graph_text(self, doc_id: Optional[str] = None) -> str:
        """Generate a text-based visualization of the graph"""
        output = []
        
        if doc_id:
            # Show specific document and its connections
            lineage = self.get_document_lineage(doc_id)
            node = self.nodes.get(doc_id, {})
            
            output.append(f"📄 {doc_id}")
            output.append(f"   Type: {node.get('type', 'unknown')}")
            output.append(f"   Status: {node.get('status', 'unknown')}")
            
            if lineage['immediate_parent']:
                output.append(f"\n⬆️  Parent: {lineage['immediate_parent']}")
            
            if lineage['immediate_children']:
                output.append("\n⬇️  Children:")
                for child in lineage['immediate_children']:
                    child_node = self.nodes.get(child, {})
                    output.append(f"   - {child} ({child_node.get('type', 'unknown')})")
            
            if lineage['siblings']:
                output.append("\n↔️  Siblings:")
                for sibling in lineage['siblings']:
                    sibling_node = self.nodes.get(sibling, {})
                    output.append(f"   - {sibling} ({sibling_node.get('type', 'unknown')})")
        else:
            # Show overall graph structure
            output.append("📊 Document Graph Overview")
            output.append("=" * 40)
            
            stats = self.get_statistics()
            output.append(f"Total Documents: {stats['total_documents']}")
            output.append(f"Total Connections: {stats['total_edges']}")
            output.append(f"Orphaned Documents: {stats['orphaned_documents']}")
            
            output.append("\n📁 Document Types:")
            for doc_type, count in stats['document_types'].items():
                output.append(f"   {doc_type}: {count}")
            
            output.append("\n📋 Document Statuses:")
            for status, count in stats['document_statuses'].items():
                output.append(f"   {status}: {count}")
        
        return "\n".join(output)


def main():
    """Test the graph system"""
    graph = DocumentGraph()
    
    # Add test documents
    graph.add_document("doc_001", {
        "type": "planning",
        "status": "published",
        "file_path": "PRD_v1.md"
    })
    
    graph.add_document("doc_002", {
        "type": "tutorial",
        "status": "draft",
        "parent": "doc_001",
        "file_path": "auth_guide.md"
    })
    
    graph.add_document("doc_003", {
        "type": "test",
        "status": "draft", 
        "parent": "doc_001",
        "triggers": ["auth.py"],
        "file_path": "auth_test.md"
    })
    
    # Test graph operations
    print("Graph Statistics:")
    print(json.dumps(graph.get_statistics(), indent=2))
    
    print("\n" + "="*50 + "\n")
    
    print("Document Lineage for doc_002:")
    print(json.dumps(graph.get_document_lineage("doc_002"), indent=2))
    
    print("\n" + "="*50 + "\n")
    
    print("Graph Visualization:")
    print(graph.visualize_graph_text())
    
    print("\n" + "="*50 + "\n")
    
    print("Specific Document View (doc_002):")
    print(graph.visualize_graph_text("doc_002"))


if __name__ == "__main__":
    main()