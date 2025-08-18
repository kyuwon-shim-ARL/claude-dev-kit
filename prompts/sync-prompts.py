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
    
    # Generate individual commands
    for keyword, data in prompts_data["prompts"].items():
        command_file = commands_dir / f"{keyword}.md"
        with open(command_file, "w", encoding="utf-8") as f:
            f.write(data["text"])
        print(f"✅ Generated: {command_file}")
    
    # Generate workflow combinations
    workflows = {
        "전체사이클": ["기획", "구현", "안정화", "배포"],
        "개발완료": ["구현", "안정화"],
        "품질보증": ["안정화", "배포"],
        "기획구현": ["기획", "구현"]
    }
    
    for workflow_name, steps in workflows.items():
        workflow_file = commands_dir / f"{workflow_name}.md"
        combined_content = []
        
        # Add workflow header
        if workflow_name == "전체사이클":
            combined_content.append("🔄 **전체 개발 워크플로우 실행**\n")
            combined_content.append("다음 4단계를 순차적으로 진행하되, 현재 프로젝트 상태를 고려하여 필요한 단계에 집중해주세요:\n")
        elif workflow_name == "개발완료":
            combined_content.append("⚡ **개발 완료 워크플로우**\n")
            combined_content.append("구현이 완료된 상태에서 안정화까지 진행합니다:\n")
        elif workflow_name == "품질보증":
            combined_content.append("🎯 **품질보증 및 배포 워크플로우**\n")
            combined_content.append("개발이 완료된 시스템의 최종 검증과 배포를 진행합니다:\n")
        elif workflow_name == "기획구현":
            combined_content.append("📋 **기획부터 구현까지 워크플로우**\n")
            combined_content.append("아이디어부터 동작하는 코드까지 완성합니다:\n")
        
        combined_content.append("\n" + "="*50 + "\n")
        
        for i, step in enumerate(steps):
            if step in prompts_data["prompts"]:
                # Add transition context between steps
                if i > 0:
                    transitions = {
                        ("기획", "구현"): "\n📍 **기획 완료 → 구현 시작**\n위에서 수립한 계획을 바탕으로 실제 구현을 진행합니다:\n",
                        ("구현", "안정화"): "\n📍 **구현 완료 → 안정화 시작**\n구현된 코드의 구조적 지속가능성을 확보합니다:\n",
                        ("안정화", "배포"): "\n📍 **안정화 완료 → 배포 시작**\n검증된 시스템을 프로덕션에 배포합니다:\n"
                    }
                    
                    prev_step = steps[i-1]
                    transition_key = (prev_step, step)
                    if transition_key in transitions:
                        combined_content.append(transitions[transition_key])
                
                combined_content.append(prompts_data["prompts"][step]["text"])
                
                if i < len(steps) - 1:  # Not the last step
                    combined_content.append("\n" + "="*50 + "\n")
        
        with open(workflow_file, "w", encoding="utf-8") as f:
            f.write("\n".join(combined_content))
        print(f"✅ Generated: {workflow_file} (조합: {' → '.join(steps)})")

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