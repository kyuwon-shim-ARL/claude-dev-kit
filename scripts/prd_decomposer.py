#!/usr/bin/env python3
"""
PRD Decomposer - Automatically extract specs from PRD documents
Addresses the docs/specs vs docs/CURRENT separation issue
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json


class PRDDecomposer:
    """Automatically decompose PRD into architecture and requirements specs"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.specs_dir = self.base_path / "docs" / "specs"
        self.current_dir = self.base_path / "docs" / "CURRENT"
        self.prd_files = []
        
    def find_prd_files(self) -> List[Path]:
        """Find all PRD files in docs/specs/"""
        prd_pattern = re.compile(r'PRD-v\d+.*\.md$')
        prd_files = []
        
        for file_path in self.specs_dir.glob("*.md"):
            if prd_pattern.match(file_path.name):
                prd_files.append(file_path)
                
        return sorted(prd_files)
    
    def extract_requirements(self, prd_content: str, version: str) -> str:
        """Extract requirements from PRD content"""
        requirements = [
            f"# Requirements Specification (Extracted from {version})",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Functional Requirements",
            ""
        ]
        
        # Extract requirements sections
        functional_reqs = self._extract_section(prd_content, "Requirements", "Implementation")
        if functional_reqs:
            requirements.extend(functional_reqs.split('\n'))
        
        requirements.extend([
            "",
            "## Non-Functional Requirements",
            ""
        ])
        
        # Extract performance/quality requirements
        nfr_section = self._extract_section(prd_content, "Success Metrics", "Timeline")
        if not nfr_section:
            nfr_section = self._extract_section(prd_content, "Performance", "Implementation")
            
        if nfr_section:
            requirements.extend(nfr_section.split('\n'))
        else:
            requirements.extend([
                "- Performance targets defined in PRD",
                "- Quality metrics specified in test cases",
                "- Compatibility requirements as per version strategy"
            ])
            
        requirements.extend([
            "",
            "## Constraints",
            "- Backward compatibility maintained",
            "- Performance impact minimized",
            "- User experience consistency preserved",
            "",
            "---",
            f"*Extracted from {version} PRD. See full PRD for complete context.*"
        ])
        
        return "\n".join(requirements)
    
    def extract_architecture(self, prd_content: str, version: str) -> str:
        """Extract architecture from PRD content"""
        architecture = [
            f"# Architecture Specification (Extracted from {version})",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## System Overview",
            ""
        ]
        
        # Extract technical design sections
        tech_design = self._extract_section(prd_content, "Technical Design", "Implementation")
        if not tech_design:
            tech_design = self._extract_section(prd_content, "Implementation", "Timeline")
            
        if tech_design:
            architecture.extend(tech_design.split('\n'))
        
        architecture.extend([
            "",
            "## Component Architecture",
            ""
        ])
        
        # Extract component information
        components = self._extract_components(prd_content)
        architecture.extend(components)
        
        architecture.extend([
            "",
            "## Data Flow",
            "- Input: User commands and parameters",
            "- Processing: Version-specific logic routing",
            "- Storage: JSON-based metadata persistence", 
            "- Output: Enhanced reports and analytics",
            "",
            "## Integration Points",
            "- Git repository integration",
            "- Environment variable configuration",
            "- File system metadata storage",
            "- Command parameter processing",
            "",
            "---",
            f"*Extracted from {version} PRD. See full PRD for implementation details.*"
        ])
        
        return "\n".join(architecture)
    
    def _extract_section(self, content: str, start_marker: str, end_marker: str) -> Optional[str]:
        """Extract content between two section markers"""
        start_pattern = rf"##.*{start_marker}"
        end_pattern = rf"##.*{end_marker}"
        
        start_match = re.search(start_pattern, content, re.IGNORECASE)
        if not start_match:
            return None
            
        start_pos = start_match.end()
        end_match = re.search(end_pattern, content[start_pos:], re.IGNORECASE)
        
        if end_match:
            end_pos = start_pos + end_match.start()
            return content[start_pos:end_pos].strip()
        else:
            return content[start_pos:].strip()
    
    def _extract_components(self, content: str) -> List[str]:
        """Extract component information from PRD"""
        components = []
        
        # Look for class definitions, modules, or architectural elements
        class_pattern = r'class\s+(\w+):'
        module_pattern = r'(\w+)\.py'
        
        classes = re.findall(class_pattern, content)
        modules = re.findall(module_pattern, content)
        
        if classes:
            components.append("### Core Classes")
            for cls in set(classes):
                components.append(f"- **{cls}**: Core component for system functionality")
            components.append("")
            
        if modules:
            components.append("### Modules")
            for module in set(modules):
                components.append(f"- **{module}.py**: Implementation module")
            components.append("")
                
        if not components:
            components = [
                "### Core Components",
                "- **Command Processor**: Handles user input and routing",
                "- **Tracking Manager**: Manages timeline and metadata",
                "- **Report Generator**: Creates analysis and reports",
                "- **Configuration Manager**: Handles settings and preferences",
                ""
            ]
        
        return components
    
    def move_project_rules(self) -> bool:
        """Move project_rules.md from root to docs/specs/ if exists"""
        root_rules = self.base_path / "project_rules.md"
        specs_rules = self.specs_dir / "project_rules.md"
        
        if root_rules.exists() and not specs_rules.exists():
            try:
                # Copy content to specs directory
                content = root_rules.read_text()
                specs_rules.write_text(content)
                
                # Remove from root
                root_rules.unlink()
                return True
            except Exception as e:
                print(f"Warning: Could not move project_rules.md: {e}")
                return False
        
        return specs_rules.exists()
    
    def decompose_all_prds(self) -> Dict[str, bool]:
        """Decompose all PRD files into specs"""
        results = {}
        prd_files = self.find_prd_files()
        
        if not prd_files:
            print("No PRD files found in docs/specs/")
            return results
        
        print(f"Found {len(prd_files)} PRD files to decompose...")
        
        # Ensure specs directory exists
        self.specs_dir.mkdir(parents=True, exist_ok=True)
        
        # Process each PRD
        for prd_file in prd_files:
            try:
                print(f"Processing {prd_file.name}...")
                
                # Read PRD content
                prd_content = prd_file.read_text()
                version = self._extract_version(prd_file.name)
                
                # Extract requirements
                requirements_content = self.extract_requirements(prd_content, version)
                requirements_file = self.specs_dir / "requirements.md"
                
                # Extract architecture  
                architecture_content = self.extract_architecture(prd_content, version)
                architecture_file = self.specs_dir / "architecture.md"
                
                # Write files (append to existing or create new)
                self._append_or_create(requirements_file, requirements_content, version)
                self._append_or_create(architecture_file, architecture_content, version)
                
                results[prd_file.name] = True
                print(f"  ✅ Decomposed {version}")
                
            except Exception as e:
                print(f"  ❌ Error processing {prd_file.name}: {e}")
                results[prd_file.name] = False
        
        # Move project_rules.md
        rules_moved = self.move_project_rules()
        results["project_rules.md"] = rules_moved
        
        return results
    
    def _extract_version(self, filename: str) -> str:
        """Extract version from PRD filename"""
        match = re.search(r'PRD-v(\d+(?:\.\d+)?)', filename)
        return f"v{match.group(1)}" if match else filename
    
    def _append_or_create(self, file_path: Path, content: str, version: str):
        """Append to existing file or create new one"""
        if file_path.exists():
            # Append new version
            existing = file_path.read_text()
            separator = f"\n\n---\n\n# {version} Addition\n\n"
            file_path.write_text(existing + separator + content)
        else:
            # Create new file
            file_path.write_text(content)
    
    def generate_report(self, results: Dict[str, bool]) -> str:
        """Generate decomposition report"""
        report = [
            "# PRD Decomposition Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Results",
            ""
        ]
        
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        report.append(f"**Success Rate**: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
        report.append("")
        
        for file_name, success in results.items():
            status = "✅" if success else "❌"
            report.append(f"- {status} {file_name}")
        
        report.extend([
            "",
            "## Generated Files",
            "- `docs/specs/requirements.md` - Consolidated requirements",
            "- `docs/specs/architecture.md` - System architecture", 
            "- `docs/specs/project_rules.md` - Project guidelines (moved from root)",
            "",
            "## Next Steps",
            "1. Review generated specs for accuracy",
            "2. Update /기획 prompt to use new structure",
            "3. Test with actual planning workflow",
            ""
        ])
        
        return "\n".join(report)


def main():
    """Main execution"""
    print("🔧 PRD Decomposer - Fixing docs/specs separation")
    print("=" * 50)
    
    decomposer = PRDDecomposer()
    results = decomposer.decompose_all_prds()
    
    # Generate and save report
    report = decomposer.generate_report(results)
    print("\n" + report)
    
    # Save report to CURRENT (this is temporary analysis)
    report_file = Path("docs/CURRENT/prd-decomposition-report.md")
    report_file.parent.mkdir(exist_ok=True)
    report_file.write_text(report)
    
    print(f"\n📝 Report saved: {report_file}")
    
    return all(results.values())


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)