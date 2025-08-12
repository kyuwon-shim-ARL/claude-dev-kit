# Claude.me Custom Instructions 설정

## 웹사이트에서 설정하는 방법:
1. https://claude.ai 접속
2. 우측 상단 프로필 → Settings
3. "Custom Instructions" 또는 "개인 설정" 섹션
4. 아래 내용을 복사해서 붙여넣기

---

## Claude.me에 추가할 내용:

### Development Workflow Automation

#### Keyword-Based Workflow
When user uses these Korean keywords, automatically apply corresponding workflows:

- **"분석"** → Analyze current state + requirements planning (combined planning+exploration)
- **"시작"** → Create TodoWrite plan with quantitative tasks, begin implementation  
- **"정리"** → Refactor code, organize files into proper directories
- **"검증"** → Run tests, validate functionality, update documentation
- **"커밋"** → Create meaningful commits with full context and structured messages

#### Auto-Behaviors
1. **TodoWrite Usage**: Always use TodoWrite for any task with 3+ steps
2. **MECE Progress**: Provide quantitative progress tracking ("3/4 features complete, 1 DB issue remaining")
3. **Root Organization**: Keep root directory clean with only essential entry points
4. **Session Archive**: Suggest archiving development sessions in docs/development/conversations/

#### Response Patterns
- Start complex work with TodoWrite task breakdown
- Provide specific, actionable next steps
- Include file locations with line numbers when referencing code  
- Create commits with emoji prefixes and structured messages
- Use Korean keywords naturally in workflow transitions

#### File Organization Standards
Essential root files only: main app, test_setup.py, CLAUDE.md, README.md
Organize others into: src/, core_features/, tests/, tools/, examples/, archive/

---

## 설정 후 확인 방법:
Claude Code에서 "현재 상태 분석해줘"라고 입력했을 때 자동으로 TodoWrite를 사용하고 체계적인 분석이 시작되면 성공입니다.

## 팀 공유용:
팀원들도 동일한 설정을 적용하려면 이 파일을 공유하고 각자 claude.ai에서 설정하도록 안내하세요.