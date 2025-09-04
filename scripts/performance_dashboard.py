#!/usr/bin/env python3
"""
컨텍스트 관리 성능 대시보드
"""
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np

class PerformanceDashboard:
    """성능 대시보드 클래스"""
    
    def __init__(self, 
                 metrics_file: str = "docs/CURRENT/context_metrics.json",
                 ab_test_file: str = "docs/CURRENT/ab_test_results.json"):
        self.metrics_file = Path(metrics_file)
        self.ab_test_file = Path(ab_test_file)
        
    def generate_report(self, output_file: str = "docs/CURRENT/performance_report.md") -> Dict:
        """종합 성능 리포트 생성"""
        
        # 데이터 로드
        performance_data = self._load_performance_data()
        ab_test_data = self._load_ab_test_data()
        
        # 분석 수행
        performance_analysis = self._analyze_performance(performance_data)
        ab_test_analysis = self._analyze_ab_test(ab_test_data)
        recommendations = self._generate_recommendations(performance_analysis, ab_test_analysis)
        
        # 리포트 생성
        report = self._generate_markdown_report(performance_analysis, ab_test_analysis, recommendations)
        
        # 파일 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return {
            "performance_score": performance_analysis.get("overall_score", 0),
            "ab_test_winner": ab_test_analysis.get("winner", "inconclusive"),
            "recommendation": recommendations.get("primary_action", "continue_monitoring"),
            "report_file": output_file
        }
    
    def _load_performance_data(self) -> Dict:
        """성능 데이터 로드"""
        if not self.metrics_file.exists():
            return {}
        try:
            with open(self.metrics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _load_ab_test_data(self) -> Dict:
        """A/B 테스트 데이터 로드"""
        if not self.ab_test_file.exists():
            return {}
        try:
            with open(self.ab_test_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _analyze_performance(self, data: Dict) -> Dict:
        """성능 데이터 분석"""
        if not data:
            return {"error": "No performance data available"}
        
        # 최근 메트릭 계산
        recent_metrics = list(data.values())[-20:]  # 최근 20개
        
        # 효율성 메트릭
        token_improvements = []
        response_times = []
        success_rates = []
        
        for metric in recent_metrics:
            if metric.get('token_count_before') and metric.get('token_count_after'):
                improvement = (metric['token_count_before'] - metric['token_count_after']) / metric['token_count_before'] * 100
                token_improvements.append(improvement)
            
            if metric.get('response_time_ms'):
                response_times.append(metric['response_time_ms'])
            
            success_rates.append(1.0 if metric.get('first_attempt_success') else 0.0)
        
        # 품질 메트릭
        quality_issues = [
            metric for metric in recent_metrics 
            if (metric.get('context_miss_detected') or 
                metric.get('duplicate_work_detected') or
                metric.get('consistency_violation'))
        ]
        
        return {
            "sample_size": len(recent_metrics),
            "avg_token_improvement": np.mean(token_improvements) if token_improvements else 0,
            "avg_response_time": np.mean(response_times) if response_times else 0,
            "success_rate": np.mean(success_rates) * 100,
            "quality_issue_rate": len(quality_issues) / len(recent_metrics) * 100,
            "overall_score": self._calculate_overall_score(token_improvements, success_rates, quality_issues, recent_metrics),
            "trend": self._analyze_trend(recent_metrics)
        }
    
    def _analyze_ab_test(self, data: Dict) -> Dict:
        """A/B 테스트 분석"""
        if not data:
            return {"error": "No A/B test data available"}
        
        control_sessions = [s for s in data.values() if s["group"] == "control"]
        treatment_sessions = [s for s in data.values() if s["group"] == "treatment"]
        
        if len(control_sessions) < 5 or len(treatment_sessions) < 5:
            return {"error": "Insufficient data for A/B analysis"}
        
        control_stats = self._calculate_group_stats(control_sessions)
        treatment_stats = self._calculate_group_stats(treatment_sessions)
        
        # 승자 결정
        winner = "inconclusive"
        if treatment_stats["success_rate"] > control_stats["success_rate"] * 1.05:  # 5% 이상 개선
            if treatment_stats["avg_completion_time"] <= control_stats["avg_completion_time"] * 1.1:  # 시간은 10% 이내 증가 허용
                winner = "treatment"
        elif control_stats["success_rate"] > treatment_stats["success_rate"] * 1.05:
            winner = "control"
        
        return {
            "control_stats": control_stats,
            "treatment_stats": treatment_stats,
            "winner": winner,
            "confidence": self._calculate_confidence(control_sessions, treatment_sessions)
        }
    
    def _generate_recommendations(self, performance: Dict, ab_test: Dict) -> Dict:
        """추천사항 생성"""
        recommendations = []
        
        # 성능 기반 추천
        if performance.get("overall_score", 0) > 75:
            if performance.get("success_rate", 0) > 70:
                recommendations.append("성능 기준 통과: 다음 단계 진행 가능")
            else:
                recommendations.append("성능은 좋으나 성공률 개선 필요")
        else:
            recommendations.append("성능 기준 미달: 시스템 조정 필요")
        
        # A/B 테스트 기반 추천
        ab_winner = ab_test.get("winner", "inconclusive")
        if ab_winner == "treatment":
            recommendations.append("Treatment group 우세: 컨텍스트 관리 확대 권장")
        elif ab_winner == "control":
            recommendations.append("Control group 우세: 기존 방식 유지 권장")
        else:
            recommendations.append("A/B 테스트 결과 불분명: 추가 데이터 수집 필요")
        
        # 주요 액션 결정
        primary_action = "continue_monitoring"
        if performance.get("overall_score", 0) > 80 and ab_winner == "treatment":
            primary_action = "expand_rollout"
        elif performance.get("overall_score", 0) < 60:
            primary_action = "rollback_changes"
        
        return {
            "recommendations": recommendations,
            "primary_action": primary_action
        }
    
    def _calculate_overall_score(self, token_improvements, success_rates, quality_issues, all_metrics) -> float:
        """전체 점수 계산"""
        if not all_metrics:
            return 0
        
        # 가중치 기반 점수 계산
        efficiency_score = np.mean(token_improvements) if token_improvements else 0
        quality_score = np.mean(success_rates) * 100
        reliability_score = max(0, 100 - (len(quality_issues) / len(all_metrics) * 100))
        
        return (efficiency_score * 0.3 + quality_score * 0.5 + reliability_score * 0.2)
    
    def _analyze_trend(self, metrics: List[Dict]) -> str:
        """트렌드 분석"""
        if len(metrics) < 10:
            return "insufficient_data"
        
        recent_scores = []
        for metric in metrics[-10:]:
            # 간단한 점수 계산
            score = 0
            if metric.get('first_attempt_success'):
                score += 50
            if not metric.get('context_miss_detected'):
                score += 25
            if not metric.get('duplicate_work_detected'):
                score += 25
            recent_scores.append(score)
        
        # 선형 회귀로 트렌드 계산
        x = np.arange(len(recent_scores))
        slope = np.polyfit(x, recent_scores, 1)[0]
        
        if slope > 2:
            return "improving"
        elif slope < -2:
            return "declining"
        else:
            return "stable"
    
    def _calculate_group_stats(self, sessions: List[Dict]) -> Dict:
        """그룹 통계 계산"""
        completed = [s for s in sessions if s.get("completion_time_minutes") is not None]
        
        if not completed:
            return {"error": "No completed sessions"}
        
        return {
            "total_sessions": len(sessions),
            "completed_sessions": len(completed),
            "success_rate": sum(1 for s in completed if s.get("success_achieved")) / len(completed) * 100,
            "avg_completion_time": sum(s["completion_time_minutes"] for s in completed) / len(completed),
            "consistency_rate": sum(1 for s in completed if s.get("consistency_maintained")) / len(completed) * 100
        }
    
    def _calculate_confidence(self, control: List[Dict], treatment: List[Dict]) -> float:
        """신뢰도 계산 (간단한 버전)"""
        control_size = len([s for s in control if s.get("completion_time_minutes")])
        treatment_size = len([s for s in treatment if s.get("completion_time_minutes")])
        
        if control_size >= 30 and treatment_size >= 30:
            return 0.95
        elif control_size >= 15 and treatment_size >= 15:
            return 0.80
        elif control_size >= 10 and treatment_size >= 10:
            return 0.65
        else:
            return 0.50
    
    def _generate_markdown_report(self, performance: Dict, ab_test: Dict, recommendations: Dict) -> str:
        """마크다운 리포트 생성"""
        report = f"""# 컨텍스트 관리 시스템 성능 리포트

## 📅 리포트 생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 전체 성능 요약

### 종합 점수: {performance.get('overall_score', 0):.1f}/100

### 주요 메트릭
- **성공률**: {performance.get('success_rate', 0):.1f}%
- **토큰 효율성**: {performance.get('avg_token_improvement', 0):.1f}% 개선
- **품질 이슈율**: {performance.get('quality_issue_rate', 0):.1f}%
- **트렌드**: {performance.get('trend', 'unknown')}

## 🧪 A/B 테스트 결과

### 승자: {ab_test.get('winner', 'inconclusive')}

#### Control Group (기존 방식)
{self._format_group_stats(ab_test.get('control_stats', {}))}

#### Treatment Group (새 방식)  
{self._format_group_stats(ab_test.get('treatment_stats', {}))}

### 신뢰도: {ab_test.get('confidence', 0):.0%}

## 💡 추천사항

"""
        
        for i, rec in enumerate(recommendations.get('recommendations', []), 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
## 🎯 주요 액션

**{recommendations.get('primary_action', 'continue_monitoring')}**

## 📈 다음 단계

"""
        
        primary_action = recommendations.get('primary_action', 'continue_monitoring')
        if primary_action == "expand_rollout":
            report += "- 컨텍스트 관리 시스템을 더 많은 사용자에게 확대\n- 모니터링 지속\n- 성능 임계값 재조정"
        elif primary_action == "rollback_changes":
            report += "- 즉시 기존 시스템으로 롤백\n- 문제점 분석 및 개선\n- 재테스트 계획 수립"  
        else:
            report += "- 현재 상태 유지하며 데이터 수집 지속\n- 주간 성과 검토\n- 임계값 도달 시 재평가"
        
        return report
    
    def _format_group_stats(self, stats: Dict) -> str:
        """그룹 통계 포맷팅"""
        if not stats or "error" in stats:
            return "- 데이터 부족"
        
        return f"""- 완료 세션: {stats.get('completed_sessions', 0)}개
- 성공률: {stats.get('success_rate', 0):.1f}%  
- 평균 완료 시간: {stats.get('avg_completion_time', 0):.1f}분
- 일관성 유지율: {stats.get('consistency_rate', 0):.1f}%"""

def main():
    """메인 실행"""
    dashboard = PerformanceDashboard()
    result = dashboard.generate_report()
    
    print(f"성능 리포트 생성 완료: {result['report_file']}")
    print(f"전체 점수: {result['performance_score']:.1f}")
    print(f"A/B 테스트 승자: {result['ab_test_winner']}")
    print(f"권장 액션: {result['recommendation']}")

if __name__ == "__main__":
    main()