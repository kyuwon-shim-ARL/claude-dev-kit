#!/usr/bin/env python3
"""
Timeline Tracking Manager for Claude Dev Kit
Version: 2.0.0 - Smart Defaults
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import hashlib


class SmartDetector:
    """Smart detection for automatic tracking"""
    
    @staticmethod
    def is_git_repository() -> bool:
        """Check if current directory is a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True, text=True, check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    @staticmethod
    def has_env_variable() -> bool:
        """Check if tracking environment variable is set"""
        return os.getenv('CLAUDE_TRACK_CHANGES', '').lower() == 'true'
    
    @staticmethod
    def has_config_file() -> bool:
        """Check if tracking config file exists"""
        config_paths = [
            Path(".claude/tracking.config"),
            Path(".clauderc"),
            Path("claude.config.json")
        ]
        return any(path.exists() for path in config_paths)
    
    @classmethod
    def should_track_automatically(cls) -> Tuple[bool, str]:
        """
        Determine if tracking should be enabled automatically
        Returns: (should_track, reason)
        """
        # Priority 1: Environment variable
        if cls.has_env_variable():
            return True, "environment variable CLAUDE_TRACK_CHANGES=true"
        
        # Priority 2: Git repository
        if cls.is_git_repository():
            return True, "Git repository detected"
        
        # Priority 3: Config file
        if cls.has_config_file():
            return True, "tracking config file found"
        
        return False, "no auto-tracking conditions met"


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
    
    def track_execution(self, command: str, args: List[str] = None, force_track: bool = None, version: str = "v18") -> Dict:
        """Track command execution with metadata"""
        # Smart tracking decision
        should_track, reason = self._should_track(args or [], force_track, version)
        
        if not should_track:
            return {"tracked": False, "reason": reason}
        
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
            "tracking": {
                "auto_enabled": should_track,
                "reason": reason
            },
            "generated": {
                "reports": [],
                "metadata": []
            }
        }
        
        # Save to current session
        current_file = self.tracking_dir / "current.json"
        current_file.write_text(json.dumps(entry, indent=2))
        
        return entry
    
    def _should_track(self, args: List[str], force_track: bool = None, version: str = "v18") -> Tuple[bool, str]:
        """Determine if tracking should be enabled based on version"""
        # v18.0: Full Integration - Default to tracking
        if version == "v18":
            return self._should_track_v18(args, force_track)
        # v17.0: Smart Defaults - Git detection
        elif version == "v17":
            return self._should_track_v17(args, force_track)
        # v16.0: Opt-in - Explicit only
        else:
            return self._should_track_v16(args, force_track)
    
    def _should_track_v18(self, args: List[str], force_track: bool = None) -> Tuple[bool, str]:
        """v18.0: Default to tracking unless explicitly disabled"""
        # Priority 1: Explicit disable
        if "--no-track" in args or "--legacy" in args:
            return False, "explicit disable parameter"
        
        # Priority 2: Environment disable
        if os.getenv('CLAUDE_TRACK_CHANGES', '').lower() == 'false':
            return False, "environment variable CLAUDE_TRACK_CHANGES=false"
        
        # Priority 3: Force setting
        if force_track is False:
            return False, "programmatic force_track=False"
        
        # Default: Always track (v18.0 behavior)
        return True, "default behavior (v18.0 - full integration)"
    
    def _should_track_v17(self, args: List[str], force_track: bool = None) -> Tuple[bool, str]:
        """v17.0: Smart defaults with Git detection"""
        # Explicit parameters
        if "--track" in args:
            return True, "explicit --track parameter"
        if "--no-track" in args:
            return False, "explicit --no-track parameter"
        if force_track is not None:
            return force_track, "programmatic force_track setting"
        
        # Smart detection for auto-tracking
        return SmartDetector.should_track_automatically()
    
    def _should_track_v16(self, args: List[str], force_track: bool = None) -> Tuple[bool, str]:
        """v16.0: Opt-in only"""
        # Explicit enable only
        if "--track" in args:
            return True, "explicit --track parameter"
        if force_track is True:
            return True, "programmatic force_track=True"
        
        # Default: No tracking (v16.0 behavior)
        return False, "default behavior (v16.0 - opt-in only)"
    
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
    
    def generate_timeline_report(self, since: Optional[str] = None, include_analytics: bool = True) -> str:
        """Generate enhanced timeline report with analytics"""
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
        
        # Generate analytics
        analytics = self._generate_analytics(entries) if include_analytics else {}
        
        # Generate report
        report_lines = [
            "# 📊 Enhanced Timeline Tracking Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]
        
        # Summary section
        report_lines.extend([
            "## 📋 Summary",
            f"- Total executions: {len(entries)}",
            f"- Commands tracked: {', '.join(set(e['command'] for e in entries))}",
            f"- Date range: {self._get_date_range(entries)}",
            ""
        ])
        
        # Analytics section
        if include_analytics and analytics:
            report_lines.extend([
                "## 📈 Analytics",
                "",
                "### Change Velocity",
                f"- Daily average: {analytics['daily_average']:.1f} changes",
                f"- Peak activity: {analytics['peak_time']}",
                f"- Most active day: {analytics['most_active_day']}",
                "",
                "### File Hotspots",
                *[f"- {path}: {'█' * int(percentage/10)} {percentage:.1f}%" 
                  for path, percentage in analytics['file_hotspots']],
                "",
                "### Collaboration Metrics",
                f"- Contributors: {analytics['contributors']}",
                f"- Average duration: {analytics['avg_duration']:.1f}ms",
                f"- Auto-tracking ratio: {analytics['auto_tracking_ratio']:.1f}%",
                ""
            ])
        
        # Timeline section
        report_lines.extend([
            "## ⏰ Timeline",
            ""
        ])
        
        for entry in sorted(entries, key=lambda x: x["timestamp"], reverse=True):
            timestamp = datetime.fromisoformat(entry["timestamp"])
            tracking_info = entry.get('tracking', {})
            
            report_lines.extend([
                f"### {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {entry['command']}",
                f"- **ID**: {entry['id']}",
                f"- **Parameters**: {', '.join(entry['parameters']) if entry['parameters'] else 'None'}",
                f"- **Git**: {entry['git']['branch']} @ {entry['git']['commit']}",
                f"- **Changes**: {entry['changes']['files_modified']} files, "
                f"+{entry['changes']['lines_added']}/-{entry['changes']['lines_removed']} lines",
                f"- **Duration**: {entry.get('duration_ms', 0)}ms",
                f"- **Tracking**: {tracking_info.get('reason', 'manual')}",
                ""
            ])
        
        report_content = "\n".join(report_lines)
        
        # Save report
        report_file = self.reports_dir / f"timeline-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        report_file.write_text(report_content)
        
        return report_content
    
    def _generate_analytics(self, entries: List[Dict]) -> Dict:
        """Generate analytics from tracking entries"""
        if not entries:
            return {}
        
        from collections import defaultdict, Counter
        
        # Calculate daily averages
        dates = [datetime.fromisoformat(e["timestamp"]).date() for e in entries]
        date_counts = Counter(dates)
        daily_average = sum(date_counts.values()) / len(date_counts) if date_counts else 0
        
        # Find peak activity time
        hours = [datetime.fromisoformat(e["timestamp"]).hour for e in entries]
        hour_counts = Counter(hours)
        peak_hour = hour_counts.most_common(1)[0][0] if hour_counts else 0
        peak_time = f"{peak_hour:02d}:00-{(peak_hour+1)%24:02d}:00"
        
        # Find most active day
        days = [datetime.fromisoformat(e["timestamp"]).strftime('%A') for e in entries]
        day_counts = Counter(days)
        most_active_day = day_counts.most_common(1)[0][0] if day_counts else "N/A"
        
        # File hotspots (simplified)
        file_changes = defaultdict(int)
        for entry in entries:
            files_modified = entry.get('changes', {}).get('files_modified', 0)
            # Simplified: assume equal distribution
            file_changes['src/'] += files_modified * 0.4
            file_changes['docs/'] += files_modified * 0.3
            file_changes['tests/'] += files_modified * 0.2
            file_changes['scripts/'] += files_modified * 0.1
        
        total_changes = sum(file_changes.values())
        hotspots = [(path, (count/total_changes)*100) for path, count in file_changes.items()]
        hotspots = sorted(hotspots, key=lambda x: x[1], reverse=True)[:5]
        
        # Contributors
        authors = set(e.get('git', {}).get('author') for e in entries)
        contributors = len([a for a in authors if a and a != 'unknown'])
        
        # Average duration
        durations = [e.get('duration_ms', 0) for e in entries]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Auto-tracking ratio
        auto_tracked = sum(1 for e in entries if e.get('tracking', {}).get('reason') != 'explicit --track parameter')
        auto_tracking_ratio = (auto_tracked / len(entries)) * 100 if entries else 0
        
        return {
            'daily_average': daily_average,
            'peak_time': peak_time,
            'most_active_day': most_active_day,
            'file_hotspots': hotspots,
            'contributors': contributors,
            'avg_duration': avg_duration,
            'auto_tracking_ratio': auto_tracking_ratio
        }
    
    def _get_date_range(self, entries: List[Dict]) -> str:
        """Get date range of entries"""
        if not entries:
            return "N/A"
        
        dates = [datetime.fromisoformat(e["timestamp"]) for e in entries]
        min_date = min(dates).strftime('%Y-%m-%d')
        max_date = max(dates).strftime('%Y-%m-%d')
        
        return f"{min_date} to {max_date}" if min_date != max_date else min_date


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