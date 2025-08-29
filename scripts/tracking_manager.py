#!/usr/bin/env python3
"""
Timeline Tracking Manager for Claude Dev Kit
Version: 1.0.0
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import hashlib


class TimelineTracker:
    """Manages timeline tracking for repository and documentation commands"""
    
    def __init__(self, base_path: str = ".claude"):
        self.base_path = Path(base_path)
        self.tracking_dir = self.base_path / "tracking"
        self.reports_dir = self.base_path / "reports" / "timeline"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        self.tracking_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Create initial files if not exist
        history_file = self.tracking_dir / "history.json"
        if not history_file.exists():
            history_file.write_text(json.dumps({"version": "1.0", "entries": []}, indent=2))
    
    def track_execution(self, command: str, args: List[str] = None) -> Dict:
        """Track command execution with metadata"""
        start_time = datetime.now()
        
        # Collect Git information
        git_info = self._get_git_info()
        
        # Collect file changes
        changes = self._get_file_changes()
        
        # Create tracking entry
        entry = {
            "id": self._generate_id(),
            "timestamp": start_time.isoformat(),
            "command": command,
            "parameters": args or [],
            "git": git_info,
            "changes": changes,
            "generated": {
                "reports": [],
                "metadata": []
            }
        }
        
        # Save to current session
        current_file = self.tracking_dir / "current.json"
        current_file.write_text(json.dumps(entry, indent=2))
        
        return entry
    
    def _get_git_info(self) -> Dict:
        """Get current Git information"""
        try:
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True, text=True, check=False
            ).stdout.strip()
            
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, check=False
            ).stdout.strip()
            
            author = subprocess.run(
                ["git", "config", "user.email"],
                capture_output=True, text=True, check=False
            ).stdout.strip()
            
            return {
                "commit": commit[:8] if commit else None,
                "branch": branch or "main",
                "author": author or "unknown"
            }
        except Exception:
            return {"commit": None, "branch": None, "author": None}
    
    def _get_file_changes(self) -> Dict:
        """Get file change statistics"""
        try:
            # Get modified files count
            modified = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True, text=True, check=False
            ).stdout.strip().split('\n')
            
            # Get diff statistics
            stats = subprocess.run(
                ["git", "diff", "--shortstat"],
                capture_output=True, text=True, check=False
            ).stdout.strip()
            
            # Parse stats
            lines_added = 0
            lines_removed = 0
            if "insertion" in stats:
                import re
                added_match = re.search(r'(\d+) insertion', stats)
                if added_match:
                    lines_added = int(added_match.group(1))
            if "deletion" in stats:
                import re
                removed_match = re.search(r'(\d+) deletion', stats)
                if removed_match:
                    lines_removed = int(removed_match.group(1))
            
            return {
                "files_modified": len([f for f in modified if f]),
                "lines_added": lines_added,
                "lines_removed": lines_removed
            }
        except Exception:
            return {"files_modified": 0, "lines_added": 0, "lines_removed": 0}
    
    def _generate_id(self) -> str:
        """Generate unique tracking ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = hashlib.md5(os.urandom(16)).hexdigest()[:6]
        return f"tr-{timestamp}-{random_suffix}"
    
    def complete_tracking(self, entry: Dict, duration_ms: int):
        """Complete tracking entry and save to history"""
        entry["duration_ms"] = duration_ms
        
        # Load history
        history_file = self.tracking_dir / "history.json"
        history = json.loads(history_file.read_text())
        
        # Add entry to history
        history["entries"].append(entry)
        
        # Save updated history
        history_file.write_text(json.dumps(history, indent=2))
        
        # Archive by month
        self._archive_by_month(entry)
    
    def _archive_by_month(self, entry: Dict):
        """Archive tracking data by month"""
        timestamp = datetime.fromisoformat(entry["timestamp"])
        month_dir = self.tracking_dir / timestamp.strftime("%Y-%m")
        month_dir.mkdir(exist_ok=True)
        
        week_file = month_dir / f"week-{timestamp.strftime('%V')}.json"
        
        # Load or create week file
        if week_file.exists():
            week_data = json.loads(week_file.read_text())
        else:
            week_data = {"entries": []}
        
        week_data["entries"].append(entry)
        week_file.write_text(json.dumps(week_data, indent=2))
    
    def generate_timeline_report(self, since: Optional[str] = None) -> str:
        """Generate timeline report"""
        history_file = self.tracking_dir / "history.json"
        if not history_file.exists():
            return "No tracking history found."
        
        history = json.loads(history_file.read_text())
        entries = history["entries"]
        
        # Filter by date if specified
        if since:
            since_date = datetime.fromisoformat(since)
            entries = [
                e for e in entries 
                if datetime.fromisoformat(e["timestamp"]) >= since_date
            ]
        
        # Generate report
        report_lines = [
            "# 📊 Timeline Tracking Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"## Summary",
            f"- Total executions: {len(entries)}",
            f"- Commands tracked: {', '.join(set(e['command'] for e in entries))}",
            "",
            "## Timeline",
            ""
        ]
        
        for entry in sorted(entries, key=lambda x: x["timestamp"], reverse=True):
            timestamp = datetime.fromisoformat(entry["timestamp"])
            report_lines.extend([
                f"### {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {entry['command']}",
                f"- **ID**: {entry['id']}",
                f"- **Parameters**: {', '.join(entry['parameters']) if entry['parameters'] else 'None'}",
                f"- **Git**: {entry['git']['branch']} @ {entry['git']['commit']}",
                f"- **Changes**: {entry['changes']['files_modified']} files, "
                f"+{entry['changes']['lines_added']}/-{entry['changes']['lines_removed']} lines",
                f"- **Duration**: {entry.get('duration_ms', 0)}ms",
                ""
            ])
        
        report_content = "\n".join(report_lines)
        
        # Save report
        report_file = self.reports_dir / f"timeline-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        report_file.write_text(report_content)
        
        return report_content


def main():
    """CLI interface for timeline tracking"""
    import sys
    
    tracker = TimelineTracker()
    
    if len(sys.argv) < 2:
        print("Usage: tracking_manager.py <command> [options]")
        print("Commands:")
        print("  track <command> [args...] - Track command execution")
        print("  report [--since=YYYY-MM-DD] - Generate timeline report")
        return
    
    command = sys.argv[1]
    
    if command == "track":
        if len(sys.argv) < 3:
            print("Error: Please specify command to track")
            return
        
        cmd = sys.argv[2]
        args = sys.argv[3:] if len(sys.argv) > 3 else []
        
        entry = tracker.track_execution(cmd, args)
        print(f"Tracking started: {entry['id']}")
        
        # Simulate execution
        import time
        time.sleep(1)
        
        tracker.complete_tracking(entry, 1000)
        print(f"Tracking completed: {entry['id']}")
    
    elif command == "report":
        since = None
        for arg in sys.argv[2:]:
            if arg.startswith("--since="):
                since = arg.split("=")[1]
        
        report = tracker.generate_timeline_report(since)
        print(report)
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()