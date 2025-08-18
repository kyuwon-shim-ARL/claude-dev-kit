#!/usr/bin/env python3
"""
Prompt synchronization utility for claude-dev-kit
Generates all prompt formats from the central API source
"""

import json
import os
from pathlib import Path

def load_prompts():
    """Load prompts from api.json"""
    with open("prompts/api.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_claude_commands(prompts_data):
    """Generate Claude Code slash commands"""
    commands_dir = Path("prompts/claude-commands")
    commands_dir.mkdir(exist_ok=True)
    
    for keyword, data in prompts_data["prompts"].items():
        command_file = commands_dir / f"{keyword}.md"
        with open(command_file, "w", encoding="utf-8") as f:
            f.write(data["text"])
        print(f"✅ Generated: {command_file}")

def generate_raw_prompts(prompts_data):
    """Generate raw text prompts for external consumption"""
    raw_dir = Path("prompts/raw")
    raw_dir.mkdir(exist_ok=True)
    
    for keyword, data in prompts_data["prompts"].items():
        raw_file = raw_dir / f"{keyword}.txt"
        with open(raw_file, "w", encoding="utf-8") as f:
            f.write(data["text"])
        print(f"✅ Generated: {raw_file}")

def generate_telegram_format(prompts_data):
    """Generate telegram-specific format"""
    telegram_dir = Path("prompts/telegram-format")
    telegram_dir.mkdir(exist_ok=True)
    
    # Generate individual buttons
    for keyword, data in prompts_data["prompts"].items():
        telegram_file = telegram_dir / f"{keyword}.json"
        telegram_data = {
            "button_text": f"@{keyword}",
            "description": data["description"],
            "message": data["text"]
        }
        with open(telegram_file, "w", encoding="utf-8") as f:
            json.dump(telegram_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Generated: {telegram_file}")
    
    # Generate combined workflows
    workflows = {
        "전체사이클": ["기획", "구현", "안정화", "배포"],
        "개발완료": ["기획", "구현", "안정화"],
        "품질보증": ["안정화", "배포"],
        "실행완료": ["구현", "안정화", "배포"]
    }
    
    for workflow_name, steps in workflows.items():
        combined_text = f"{workflow_name}을 진행해줘.\n\n"
        for i, step in enumerate(steps, 1):
            step_data = prompts_data["prompts"][step]
            combined_text += f"{i}. **{step} 단계**: {step_data['description']}\n"
            combined_text += f"   {step_data['text'].split('.', 1)[1].strip()}\n\n"
        
        workflow_file = telegram_dir / f"{workflow_name}.json"
        workflow_data = {
            "button_text": workflow_name,
            "description": f"{' → '.join(steps)} 연속 실행",
            "message": combined_text.strip()
        }
        with open(workflow_file, "w", encoding="utf-8") as f:
            json.dump(workflow_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Generated: {workflow_file}")

def main():
    """Sync all prompt formats"""
    print("🔄 Synchronizing prompts from api.json...")
    print("=" * 50)
    
    try:
        prompts_data = load_prompts()
        
        print("\n📁 Generating Claude Code commands...")
        generate_claude_commands(prompts_data)
        
        print("\n📄 Generating raw text prompts...")
        generate_raw_prompts(prompts_data)
        
        print("\n🤖 Generating Telegram format...")
        generate_telegram_format(prompts_data)
        
        print("\n" + "=" * 50)
        print("🎉 Prompt synchronization complete!")
        print(f"📊 Generated formats for {len(prompts_data['prompts'])} prompts")
        print(f"🏷️  Version: {prompts_data['version']}")
        
        print("\n💡 Usage:")
        print("  - Claude Code: Copy prompts/claude-commands/ to .claude/commands/")
        print("  - Telegram: Use prompts/telegram-format/ JSON files")
        print("  - External: HTTP GET prompts/raw/[keyword].txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)