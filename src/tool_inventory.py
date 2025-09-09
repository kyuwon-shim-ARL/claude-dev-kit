#!/usr/bin/env python3
"""
Tool Inventory System
연구에서 사용 가능한 도구 자동 관리
"""
import os
import ast
import json
from pathlib import Path
from typing import Dict, List, Any


class ToolInventory:
    """개발된 도구 자동 카탈로그"""
    
    def __init__(self, src_dir: str = "src"):
        self.src_dir = Path(src_dir)
        self.inventory_file = Path(".tool_inventory.json")
        self.tools = {}
        
    def scan_tools(self) -> Dict[str, Any]:
        """src/ 디렉토리에서 사용 가능한 도구 스캔"""
        tools = {}
        
        for py_file in self.src_dir.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            with open(py_file, 'r') as f:
                try:
                    tree = ast.parse(f.read())
                    
                    for node in ast.walk(tree):
                        # 함수 찾기
                        if isinstance(node, ast.FunctionDef):
                            if not node.name.startswith('_'):  # public 함수만
                                func_info = {
                                    'type': 'function',
                                    'file': str(py_file),
                                    'line': node.lineno,
                                    'docstring': ast.get_docstring(node),
                                    'params': [arg.arg for arg in node.args.args],
                                    'usage_example': self._generate_usage(node.name, py_file)
                                }
                                tools[node.name] = func_info
                        
                        # 클래스 찾기
                        elif isinstance(node, ast.ClassDef):
                            if not node.name.startswith('_'):
                                class_info = {
                                    'type': 'class',
                                    'file': str(py_file),
                                    'line': node.lineno,
                                    'docstring': ast.get_docstring(node),
                                    'methods': self._get_methods(node),
                                    'usage_example': self._generate_class_usage(node.name, py_file)
                                }
                                tools[node.name] = class_info
                                
                except Exception as e:
                    print(f"Error parsing {py_file}: {e}")
        
        self.tools = tools
        self._save_inventory()
        return tools
    
    def _get_methods(self, class_node) -> List[str]:
        """클래스의 public 메소드 추출"""
        methods = []
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_') or node.name == '__init__':
                    methods.append(node.name)
        return methods
    
    def _generate_usage(self, func_name: str, file_path: Path) -> str:
        """함수 사용 예시 생성"""
        module = file_path.stem
        parent = file_path.parent.name
        
        if parent != 'src':
            import_path = f"from src.{parent}.{module} import {func_name}"
        else:
            import_path = f"from src.{module} import {func_name}"
            
        return f"{import_path}\nresult = {func_name}(...)"
    
    def _generate_class_usage(self, class_name: str, file_path: Path) -> str:
        """클래스 사용 예시 생성"""
        module = file_path.stem
        parent = file_path.parent.name
        
        if parent != 'src':
            import_path = f"from src.{parent}.{module} import {class_name}"
        else:
            import_path = f"from src.{module} import {class_name}"
            
        return f"{import_path}\ninstance = {class_name}()\nresult = instance.method(...)"
    
    def _save_inventory(self):
        """인벤토리 저장"""
        with open(self.inventory_file, 'w') as f:
            json.dump(self.tools, f, indent=2)
    
    def search_tool(self, query: str) -> List[Dict[str, Any]]:
        """도구 검색"""
        results = []
        query_lower = query.lower()
        
        for name, info in self.tools.items():
            # 이름 매칭
            if query_lower in name.lower():
                results.append({'name': name, 'score': 1.0, **info})
                continue
            
            # docstring 매칭
            if info.get('docstring'):
                if query_lower in info['docstring'].lower():
                    results.append({'name': name, 'score': 0.7, **info})
        
        return sorted(results, key=lambda x: x['score'], reverse=True)
    
    def generate_research_context(self) -> str:
        """연구용 컨텍스트 생성"""
        context = """# 📦 Available Tools for Research

## IMPORTANT: Use existing tools instead of creating new ones!

### Quick Reference:
"""
        
        # 카테고리별 정리
        categories = {}
        for name, info in self.tools.items():
            file_path = info['file']
            category = Path(file_path).parent.name
            
            if category not in categories:
                categories[category] = []
            categories[category].append((name, info))
        
        for category, tools in categories.items():
            context += f"\n### {category}/\n"
            for name, info in tools:
                if info['type'] == 'function':
                    docstring = info.get('docstring', '')
                    desc = docstring.split('\n')[0] if docstring else 'No description'
                    context += f"- `{name}()`: {desc}\n"
                else:
                    docstring = info.get('docstring', '')
                    desc = docstring.split('\n')[0] if docstring else 'No description'
                    context += f"- `{name}` (class): {desc}\n"
        
        context += "\n### Usage Examples:\n"
        
        # 주요 도구 사용 예시
        for name, info in list(self.tools.items())[:5]:  # 상위 5개만
            context += f"\n#### {name}\n```python\n{info['usage_example']}\n```\n"
        
        return context


class ResearchToolEnforcer:
    """연구에서 기존 도구 사용 강제"""
    
    def __init__(self):
        self.inventory = ToolInventory()
        self.inventory.scan_tools()
    
    def before_research_start(self) -> str:
        """연구 시작 전 도구 컨텍스트 주입"""
        return self.inventory.generate_research_context()
    
    def validate_code(self, code: str) -> Dict[str, Any]:
        """코드에서 불필요한 재구현 검사"""
        issues = []
        
        # AST 파싱
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 비슷한 기능이 이미 있는지 확인
                    similar = self.inventory.search_tool(node.name)
                    if similar:
                        issues.append({
                            'type': 'potential_duplicate',
                            'function': node.name,
                            'existing': similar[0]['name'],
                            'suggestion': f"Use existing: {similar[0]['usage_example']}"
                        })
        except:
            pass
        
        return {
            'has_issues': len(issues) > 0,
            'issues': issues
        }


if __name__ == "__main__":
    # 도구 인벤토리 생성
    inventory = ToolInventory()
    tools = inventory.scan_tools()
    
    print(f"📦 Found {len(tools)} tools")
    
    # 연구 컨텍스트 생성
    enforcer = ResearchToolEnforcer()
    context = enforcer.before_research_start()
    
    print("\n" + context)