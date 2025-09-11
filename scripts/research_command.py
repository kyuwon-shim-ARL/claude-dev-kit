#!/usr/bin/env python3
"""
/연구 슬래시 커맨드 실행 스크립트
Research Project Manager CLI
"""
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_project_manager import ResearchProjectManager, ResearchTimeline
import argparse


def main():
    parser = argparse.ArgumentParser(description="Research Project Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Basic commands
    init_parser = subparsers.add_parser("init", help="Initialize new research project")
    init_parser.add_argument("name", help="Project name")
    init_parser.add_argument("description", nargs="?", default="", help="Project description")
    
    track_parser = subparsers.add_parser("track", help="Track research progress")
    track_parser.add_argument("note", help="Progress note")
    track_parser.add_argument("--files", nargs="*", help="Related files")
    
    milestone_parser = subparsers.add_parser("milestone", help="Set a milestone")
    milestone_parser.add_argument("name", help="Milestone name")
    milestone_parser.add_argument("description", nargs="?", default="", help="Milestone description")
    
    reproduce_parser = subparsers.add_parser("reproduce", help="Reproduce a checkpoint")
    reproduce_parser.add_argument("checkpoint", help="Checkpoint ID or timestamp")
    
    subparsers.add_parser("archive", help="Archive current project")
    subparsers.add_parser("list", help="List all research projects")
    
    switch_parser = subparsers.add_parser("switch", help="Switch active project")
    switch_parser.add_argument("project_id", help="Project ID to switch to")
    
    subparsers.add_parser("status", help="Show current project status")
    
    # Extended commands
    explore_parser = subparsers.add_parser("explore", help="Explore data and perform EDA")
    explore_parser.add_argument("description", nargs="?", default="", help="Exploration description")
    
    hypothesis_parser = subparsers.add_parser("hypothesis", help="Set research hypothesis")
    hypothesis_parser.add_argument("hypothesis", help="Hypothesis text")
    
    experiment_parser = subparsers.add_parser("experiment", help="Start new experiment")
    experiment_parser.add_argument("name", help="Experiment name")
    experiment_parser.add_argument("description", nargs="?", default="", help="Experiment description")
    
    validate_parser = subparsers.add_parser("validate", help="Validate results")
    validate_parser.add_argument("description", nargs="?", default="", help="Validation description")
    
    analyze_parser = subparsers.add_parser("analyze", help="Analyze results")
    analyze_parser.add_argument("description", nargs="?", default="", help="Analysis description")
    
    compare_parser = subparsers.add_parser("compare", help="Compare experiments")
    compare_parser.add_argument("exp1", help="First experiment")
    compare_parser.add_argument("exp2", help="Second experiment")
    
    # Tool management
    subparsers.add_parser("tools", help="List available tools")
    
    checkpoint_parser = subparsers.add_parser("checkpoint", help="Create checkpoint for tool development")
    checkpoint_parser.add_argument("description", help="Checkpoint description")
    
    resume_parser = subparsers.add_parser("resume", help="Resume from checkpoint")
    resume_parser.add_argument("checkpoint_id", nargs="?", help="Checkpoint ID (latest if not specified)")
    
    # Collaboration
    subparsers.add_parser("share", help="Prepare results for sharing")
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = ResearchProjectManager()
    
    # Execute commands
    if args.command == "init":
        result = manager.init_project(args.name, args.description)
        if result.get("success"):
            print(f"✅ {result['message']}")
            print(f"📁 Project location: {result['path']}")
            print(f"🆔 Project ID: {result['project_id']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "track":
        result = manager.track_progress(args.note, args.files)
        if result.get("success"):
            print(f"✅ {result['message']}")
            print(f"⏰ Timestamp: {result['timestamp']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "milestone":
        result = manager.set_milestone(args.name, args.description)
        if result.get("success"):
            print(f"🎯 {result['message']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "reproduce":
        result = manager.reproduce_checkpoint(args.checkpoint)
        if result.get("success"):
            print(f"✅ {result['message']}")
            if "environment" in result:
                print("\n📦 Environment:")
                print(f"  Python: {result['environment'].get('python_version', 'N/A')}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "archive":
        result = manager.archive_project()
        if result.get("success"):
            print(f"📦 {result['message']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "list":
        projects = manager.list_projects()
        if not projects:
            print("No research projects found.")
        else:
            print("\n📚 Research Projects:")
            for proj in projects:
                status_icon = "🟢" if proj["status"] == "active" else "📦"
                print(f"\n{status_icon} {proj['name']} ({proj['id']})")
                print(f"   Created: {proj['created'][:10]}")
                print(f"   Milestones: {proj['milestones']} | Checkpoints: {proj['checkpoints']}")
    
    elif args.command == "switch":
        result = manager.switch_project(args.project_id)
        if result.get("success"):
            print(f"✅ {result['message']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "status":
        if manager.metadata.get("active_project"):
            project_id = manager.metadata["active_project"]
            project_info = manager.metadata["projects"][project_id]
            print(f"\n🔬 Active Research Project: {project_info['name']}")
            print(f"📁 ID: {project_id}")
            print(f"📝 Description: {project_info['description']}")
            print(f"📅 Created: {project_info['created'][:10]}")
            print(f"🎯 Milestones: {len(project_info['milestones'])}")
            print(f"💾 Checkpoints: {len(project_info['checkpoints'])}")
        else:
            print("No active research project. Use '/연구 init' to start.")
    
    # Extended commands
    elif args.command == "explore":
        result = manager.explore_data(args.description)
        if result.get("success"):
            print(f"🔍 {result['message']}")
            print(f"📓 Notebook: {result['notebook_path']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "hypothesis":
        result = manager.set_hypothesis(args.hypothesis)
        if result.get("success"):
            print(f"💡 {result['message']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "experiment":
        result = manager.start_experiment(args.name, args.description)
        if result.get("success"):
            print(f"🧪 {result['message']}")
            print(f"📓 Notebook: {result['notebook_path']}")
            print(f"🆔 Experiment ID: {result['experiment_id']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "validate":
        result = manager.validate_results(args.description)
        if result.get("success"):
            print(f"🔍 {result['message']}")
            print(f"📜 Script: {result['script_path']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "analyze":
        result = manager.analyze_results(args.description)
        if result.get("success"):
            print(f"📊 {result['message']}")
            print(f"📄 Report: {result['report_path']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "compare":
        result = manager.compare_experiments(args.exp1, args.exp2)
        if result.get("success"):
            print(f"🔄 {result['message']}")
            print(f"📓 Notebook: {result['notebook_path']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "tools":
        result = manager.list_tools()
        if result.get("success"):
            print(f"\n🛠️ Available Tools ({result['count']} total):")
            for category, tools in result['categories'].items():
                print(f"\n📂 {category}/")
                for tool in tools:
                    print(f"  • {tool}")
        else:
            print(f"❌ Error: {result.get('error')}")
            print(f"💡 Hint: {result.get('message')}")
    
    elif args.command == "checkpoint":
        result = manager.checkpoint(args.description)
        if result.get("success"):
            print(f"⏸️ {result['message']}")
            print(f"🆔 Checkpoint ID: {result['checkpoint_id']}")
            print(f"➡️ {result['next_steps']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "resume":
        result = manager.resume_from_checkpoint(args.checkpoint_id)
        if result.get("success"):
            print(f"▶️ {result['message']}")
            print(f"🆔 Checkpoint ID: {result['checkpoint_id']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    elif args.command == "share":
        result = manager.share_results()
        if result.get("success"):
            print(f"📤 {result['message']}")
            print(f"📁 Share package: {result['share_path']}")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()