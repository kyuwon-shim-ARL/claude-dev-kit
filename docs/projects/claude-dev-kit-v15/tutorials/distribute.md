<!--
@meta
id: document_20250905_1110_distribute
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-09
tags: distribute.md, projects, tutorials, distribute, claude-dev-kit-v15
related: 
-->

# Claude Code Template Distribution Plan

## 배포 방법들

### Option 1: GitHub Repository (추천)
```bash
# 1. 템플릿 레포 생성
github.com/username/claude-code-template

# 2. 사용자가 원클릭 사용
curl -sSL https://raw.githubusercontent.com/username/claude-code-template/main/install.sh | bash

# 또는
git clone https://github.com/username/claude-code-template.git
cd claude-code-template
./safe-init-claude-repo.sh my_project
```

### Option 2: NPM Package
```bash
npm install -g claude-code-template
claude-init my-project "My project description"
```

### Option 3: GitHub Template Repository
- 템플릿 레포 설정으로 "Use this template" 버튼 제공
- 사용자가 새 레포 생성 시 자동으로 구조 복사

### Option 4: One-liner installer
```bash
# 모든 걸 자동으로
bash <(curl -s https://raw.githubusercontent.com/user/claude-code-template/main/one-click-install.sh)
```

## 권장 배포 구조

### Repository 구조:
```
claude-code-template/
├── install.sh                    # 원클릭 설치
├── safe-init-claude-repo.sh       # 안전한 초기화
├── setup_claude_code_structure.py # 구조 생성
├── templates/
│   ├── CLAUDE.md                 # CLAUDE.md 템플릿
│   ├── gitignore                 # .gitignore 템플릿
│   └── workflow-guide.md         # 워크플로우 가이드
├── docs/
│   ├── README.md                 # 사용 가이드
│   └── examples/                 # 예제들
└── tests/                        # 템플릿 테스트
```

### install.sh 내용:
```bash
#!/bin/bash
PROJECT_NAME=${1:-$(basename $(pwd))}
PROJECT_DESC=${2:-"A Claude Code project"}

echo "📥 Downloading Claude Code template..."
curl -sSL https://github.com/user/claude-code-template/archive/main.tar.gz | tar -xz --strip-components=1

echo "🚀 Initializing project: $PROJECT_NAME"
./safe-init-claude-repo.sh "$PROJECT_NAME" "$PROJECT_DESC"

echo "🧹 Cleaning up..."
rm -rf templates/ docs/ tests/ install.sh safe-init-claude-repo.sh setup_claude_code_structure.py
```

## 즉시 사용 가능한 방법들

### A. PaperFlow 내에서 배포
```bash
# PaperFlow 레포에 추가
mkdir tools/claude-code-template
cp /tmp/claude-code-template/* tools/claude-code-template/
```

### B. Gist로 간단 배포
```bash
# GitHub Gist에 업로드 후
curl -sSL https://gist.github.com/user/xxx/raw/install.sh | bash
```

### C. 직접 다운로드 링크
```bash
# 파일들을 웹에서 직접 다운로드
wget https://example.com/claude-template.zip
unzip claude-template.zip
./safe-init-claude-repo.sh
```