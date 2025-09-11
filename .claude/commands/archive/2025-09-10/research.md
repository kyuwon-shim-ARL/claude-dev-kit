# /research - Research Project Management Slash Command

## Usage
```
/research [subcommand] [arguments]
```

## Subcommands

### Project Management
- `init <name> <description>` - Create new project
- `list` - List all projects  
- `switch <project_id>` - Switch to project
- `status` - Show current status

### Research Tracking
- `track <message>` - Track progress
- `experiment <name> <desc>` - Start experiment
- `hypothesis <content>` - Set hypothesis
- `milestone <name> <desc>` - Set milestone
- `validate <desc>` - Validate results
- `checkpoint <memo>` - Create checkpoint

## Implementation

Execute ResearchProjectManager commands through Python:

```python
import sys
sys.path.append('/home/kyuwon/projects/claude-dev-kit/src')
from research_manager_hybrid import HybridResearchManager

manager = HybridResearchManager()
# Execute based on subcommand
```