# 📦 Archive Note: Prompts v1 Central Management System

**Archived Date**: 2025-08-31
**Reason**: Deprecated in favor of direct .claude/commands/ management

## Original Purpose
This was the initial centralized prompt management system that supported:
- Multiple format generation (Markdown, JSON, TXT)
- Telegram bot integration
- External API support

## Why Archived
1. **Redundancy**: .claude/commands/ became the single source of truth
2. **Complexity**: Unnecessary sync-prompts.py workflow
3. **Maintenance**: Double management burden
4. **Usage**: Only .claude/commands/ is actively used

## Contents
- `api.json`: Central prompt repository
- `sync-prompts.py`: Format synchronization script
- `claude-commands/`: Generated Markdown commands
- `telegram-format/`: Telegram bot JSON format
- `raw/`: Plain text format

## Migration Path
All active commands are now maintained in:
```
.claude/commands/
```

Updates are distributed via:
```bash
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/update.sh | bash
```

---
*This legacy system is preserved for historical reference only.*