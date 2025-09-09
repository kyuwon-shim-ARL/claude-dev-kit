#!/usr/bin/env python3
"""
입력 검증 및 보안 시스템
사용자 입력의 안전성을 보장하고 파일시스템 위험을 방지합니다.
"""
import re
import unicodedata
from pathlib import Path
from typing import Optional


class ValidationError(Exception):
    """입력 검증 오류"""
    pass


class InputValidator:
    """안전한 입력 검증 및 정규화"""
    
    # 파일시스템 위험 문자들
    DANGEROUS_CHARS = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
    
    # 허용된 문자 패턴 (한글, 영문, 숫자, 하이픈, 언더스코어, 공백)
    ALLOWED_PATTERN = re.compile(r'[^\w\-가-힣\s]', re.UNICODE)
    
    # 최대 길이 제한
    MAX_PROJECT_NAME_LENGTH = 40  # 날짜 prefix 고려하여 줄임
    MIN_PROJECT_NAME_LENGTH = 1
    
    @staticmethod
    def sanitize_project_name(name: str) -> str:
        """
        프로젝트명을 파일시스템 안전하게 정규화
        
        Args:
            name: 원본 프로젝트명
            
        Returns:
            정규화된 안전한 프로젝트명
            
        Raises:
            ValidationError: 검증 실패 시
        """
        if not name or not name.strip():
            raise ValidationError("프로젝트명은 비어있을 수 없습니다")
        
        # 1. 앞뒤 공백 제거
        sanitized = name.strip()
        
        # 2. 유니코드 정규화 (NFD -> NFC)
        sanitized = unicodedata.normalize('NFC', sanitized)
        
        # 3. 위험한 문자 제거
        for dangerous_char in InputValidator.DANGEROUS_CHARS:
            sanitized = sanitized.replace(dangerous_char, '')
        
        # 4. 허용되지 않은 특수문자 제거 (한글, 영문, 숫자, 하이픈, 언더스코어만 유지)
        sanitized = InputValidator.ALLOWED_PATTERN.sub('', sanitized)
        
        # 5. 연속 공백을 단일 공백으로 변환 후 언더스코어로 치환
        sanitized = re.sub(r'\s+', '_', sanitized)
        
        # 6. 길이 검증
        if len(sanitized) == 0:
            raise ValidationError("유효한 문자가 포함된 프로젝트명이 필요합니다")
        
        if len(sanitized) > InputValidator.MAX_PROJECT_NAME_LENGTH:
            # 안전하게 잘라내기 (한글 깨짐 방지)
            sanitized = InputValidator._safe_truncate(
                sanitized, 
                InputValidator.MAX_PROJECT_NAME_LENGTH
            )
        
        # 7. 최종 검증
        if len(sanitized) < InputValidator.MIN_PROJECT_NAME_LENGTH:
            raise ValidationError(f"프로젝트명이 너무 짧습니다 (최소 {InputValidator.MIN_PROJECT_NAME_LENGTH}자)")
            
        return sanitized
    
    @staticmethod
    def _safe_truncate(text: str, max_length: int) -> str:
        """
        유니코드 안전하게 문자열 자르기
        
        Args:
            text: 자를 문자열
            max_length: 최대 길이
            
        Returns:
            안전하게 자른 문자열
        """
        if len(text) <= max_length:
            return text
        
        # max_length에서 자른 후, 마지막 문자가 완전한지 확인
        truncated = text[:max_length]
        
        # 한글이나 특수 유니코드가 깨졌는지 확인
        try:
            # 인코딩/디코딩으로 깨진 문자 확인
            truncated.encode('utf-8').decode('utf-8')
            return truncated
        except UnicodeError:
            # 마지막 문자가 깨졌으면 1자씩 줄여가며 안전한 지점 찾기
            for i in range(max_length - 1, 0, -1):
                try:
                    safe_text = text[:i]
                    safe_text.encode('utf-8').decode('utf-8')
                    return safe_text
                except UnicodeError:
                    continue
            
            # 모두 실패하면 ASCII만 남기기
            return re.sub(r'[^\x00-\x7F]', '', text)[:max_length]
    
    @staticmethod
    def validate_description(description: str) -> str:
        """
        프로젝트 설명 검증 및 정리
        
        Args:
            description: 원본 설명
            
        Returns:
            정리된 설명
        """
        if not description:
            return ""
        
        # 기본 정리
        cleaned = description.strip()
        
        # 길이 제한 (500자)
        if len(cleaned) > 500:
            cleaned = cleaned[:500]
            
        return cleaned
    
    @staticmethod
    def is_safe_path(path_str: str) -> bool:
        """
        경로가 안전한지 검증
        
        Args:
            path_str: 검증할 경로 문자열
            
        Returns:
            안전하면 True, 위험하면 False
        """
        # 기본 위험 패턴들
        dangerous_patterns = [
            '..',           # 상위 디렉토리 접근
            '/etc/',        # 시스템 디렉토리
            '/root/',       # 루트 홈
            '/home/',       # 다른 사용자 홈 (상대적)
            '~',            # 홈 디렉토리 단축어
            '$',            # 환경변수
            '`',            # 명령 실행
            ';',            # 명령 체이닝
            '|',            # 파이프
            '&',            # 백그라운드 실행
        ]
        
        path_lower = path_str.lower()
        return not any(pattern in path_lower for pattern in dangerous_patterns)


class ProjectNameSanitizer:
    """프로젝트명 전용 정규화 클래스"""
    
    @staticmethod
    def create_safe_project_id(name: str, date_prefix: str = None) -> str:
        """
        안전한 프로젝트 ID 생성
        
        Args:
            name: 프로젝트명
            date_prefix: 날짜 접두어 (예: "2025-09-09")
            
        Returns:
            안전한 프로젝트 ID (예: "2025-09-09_safe_project_name")
        """
        # 1. 프로젝트명 정규화
        safe_name = InputValidator.sanitize_project_name(name)
        
        # 2. 날짜 접두어 처리
        if date_prefix:
            # 날짜 형식 검증 (YYYY-MM-DD)
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_prefix):
                from datetime import datetime
                date_prefix = datetime.now().strftime('%Y-%m-%d')
                
            project_id = f"{date_prefix}_{safe_name}"
        else:
            project_id = safe_name
        
        return project_id
    
    @staticmethod
    def extract_name_from_id(project_id: str) -> str:
        """
        프로젝트 ID에서 실제 프로젝트명 추출
        
        Args:
            project_id: 프로젝트 ID (예: "2025-09-09_project_name")
            
        Returns:
            프로젝트명 (예: "project_name")
        """
        # 날짜 접두어 패턴 제거
        if re.match(r'^\d{4}-\d{2}-\d{2}_', project_id):
            return project_id[11:]  # "YYYY-MM-DD_" 제거
        
        return project_id


# 전역 검증자 인스턴스
validator = InputValidator()
sanitizer = ProjectNameSanitizer()


# 편의 함수들
def safe_project_name(name: str) -> str:
    """프로젝트명을 안전하게 정규화 (편의 함수)"""
    return validator.sanitize_project_name(name)


def safe_project_id(name: str, date_prefix: str = None) -> str:
    """안전한 프로젝트 ID 생성 (편의 함수)"""
    return sanitizer.create_safe_project_id(name, date_prefix)


if __name__ == "__main__":
    # 테스트 실행
    test_cases = [
        "정상 프로젝트",
        "project/with\\dangerous..chars",
        "",
        "a" * 100,
        "한글프로젝트_with_English123",
        "  앞뒤 공백   ",
        "special!@#$%^&*()chars"
    ]
    
    print("🧪 입력 검증 테스트:")
    for test_case in test_cases:
        try:
            result = safe_project_name(test_case)
            print(f"✅ '{test_case}' → '{result}'")
        except ValidationError as e:
            print(f"❌ '{test_case}' → Error: {e}")