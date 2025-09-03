🔚 **Smart Session Closure**

**📚 Automatic Context Loading:**
- Analyze all files in docs/CURRENT/ directory  
- Automatically classify documents as completed/in-progress/preserve

**🧠 Intelligent Completion State Detection:**
Automatically identify completed project documents using Claude's contextual understanding:

**Completion Signal Patterns:**
- "완성도: 100%", "✅ 완료", "전체 완료"
- "테스트 완료", "구현 완료", "배포 완료" 
- completion-report-*, test-report-v*, implementation-report-*
- Documents based on past dates indicating completion

**In-Progress Signal Patterns:**
- "⏳ 진행중", "Active TODOs", "Current Sprint"
- "in_progress", current work-related keywords

**Preserve Signal Patterns:**
- active-todos.md, status.md (current status management)
- project_rules.md, planning.md (permanent preservation)

**🔄 Execution Process:**

1. **Automatic Analysis**: Full scan of docs/CURRENT/ directory
2. **Intelligent Classification**: Analyze completion status of each file (95% confidence)
3. **Display Results**: 
   ```
   📊 Session Closure Analysis Results
   ✅ Completed Documents (6): completion-report-v18.md, test-report-v10.1.md...
   🔄 In-Progress Documents (2): active-todos.md, status.md
   📚 Preserve Documents (1): project_rules.md
   ```
4. **Safety Check**: "Archive 6 completed documents? [Y/n]"
5. **Immediate Execution**: Auto-archive when Y is entered

**📦 Archive Process:**
- **Destination**: docs/development/sessions/YYYY-MM/session-XXX.md
- **Session Integration**: Merge all completed documents into single session file
- **Metadata**: Include completion reason, confidence level, timestamp
- **Safe Deletion**: Remove from CURRENT after successful archiving

**💡 Usage:**

```bash
# Basic execution
python scripts/session_closure.py

# Or via slash command (future)
/session-closure
```

**📊 Expected Results:**
- **Before**: docs/CURRENT/ 15 files (mixed state)
- **After**: docs/CURRENT/ 3-4 files (current work only)
- **Archive**: docs/development/sessions/2025-08/session-001.md (completed documents)

**🛡️ Safety Features:**
- **Backup Creation**: Automatic backup before archiving
- **Confirmation Process**: User final approval before execution
- **Recovery Support**: Recovery possible if misclassified
- **Logging**: Detailed logs of all operations

**⚡ Key Benefits:**
- **Immediate Execution**: Clean up without complex manual classification
- **High Accuracy**: 95% confidence based on Claude's contextual understanding
- **Safe Processing**: 0% data loss guarantee
- **Purpose Restoration**: Restore docs/CURRENT/ to true "current" workspace

**Output:** Clean CURRENT directory + complete session archive