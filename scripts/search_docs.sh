#!/bin/bash
# 문서 검색 도구

function search_by_type() {
    echo "🔍 Document Type: $1"
    find docs/ -name "*.md" -exec grep -l "@meta" {} \; 2>/dev/null | \
    xargs grep -l "type: $1" 2>/dev/null | sort
}

function search_by_date() {
    echo "🔍 Documents from: $1"
    find docs/ -name "*.md" -exec grep -l "created: $1" {} \; 2>/dev/null | sort
}

function search_by_tag() {
    echo "🔍 Tag: $1"
    find docs/ -name "*.md" -exec grep -l "tags:.*$1" {} \; 2>/dev/null | sort
}

function search_by_content() {
    echo "🔍 Content: $1"
    grep -r -l "$1" docs/ --include="*.md" 2>/dev/null | sort
}

function search_by_status() {
    echo "🔍 Status: $1"
    find docs/ -name "*.md" -exec grep -l "status: $1" {} \; 2>/dev/null | sort
}

function show_document_info() {
    echo "📄 Document Info: $1"
    if [[ -f "$1" ]]; then
        echo "   File: $1"
        grep -A 10 "@meta" "$1" 2>/dev/null || echo "   No metadata found"
        echo ""
    else
        echo "   File not found: $1"
    fi
}

function list_all_types() {
    echo "📂 Available Document Types:"
    find docs/ -name "*.md" -exec grep -h "type: " {} \; 2>/dev/null | \
    sed 's/type: //' | sort | uniq | sed 's/^/   - /'
}

function list_all_tags() {
    echo "🏷️ Available Tags:"
    find docs/ -name "*.md" -exec grep -h "tags: " {} \; 2>/dev/null | \
    sed 's/tags: //' | tr ',' '\n' | sed 's/^ *//' | sort | uniq | head -20 | sed 's/^/   - /'
}

# 사용법 출력
if [[ $# -eq 0 ]]; then
    echo "📚 Claude Dev Kit Document Search Tool"
    echo "======================================"
    echo ""
    echo "Usage: $0 [command] [search_term]"
    echo ""
    echo "Commands:"
    echo "  type [type]       # Find documents by type"
    echo "  date [YYYY-MM]    # Find documents by creation date"
    echo "  tag [tag]         # Find documents with specific tag"
    echo "  content [term]    # Find documents containing text"
    echo "  status [status]   # Find documents by status (active/archived)"
    echo "  info [file]       # Show document metadata"
    echo "  types             # List all available types"
    echo "  tags              # List all available tags"
    echo ""
    echo "Examples:"
    echo "  $0 type vision     # 비전 문서 찾기"
    echo "  $0 date 2025-01    # 1월 문서 찾기"  
    echo "  $0 tag TADD        # TADD 태그 문서"
    echo "  $0 content SMILES  # SMILES 언급 문서"
    echo "  $0 status active   # 활성 문서만"
    echo "  $0 info docs/VISION.md  # 문서 정보 보기"
    echo ""
    exit 1
fi

case $1 in
    "type") search_by_type "$2" ;;
    "date") search_by_date "$2" ;;
    "tag") search_by_tag "$2" ;;
    "content") search_by_content "$2" ;;
    "status") search_by_status "$2" ;;
    "info") show_document_info "$2" ;;
    "types") list_all_types ;;
    "tags") list_all_tags ;;
    *) echo "Unknown command: $1. Use '$0' for help." ;;
esac