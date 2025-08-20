#!/usr/bin/env python3
"""
컨텍스트 관리 성능 모니터링 도구
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class PerformanceMetrics:
    """성능 메트릭 데이터 클래스"""
    timestamp: str
    session_id: str
    task_type: str  # 'strategic', 'tactical', 'operational'
    
    # 효율성 메트릭
    token_count_before: Optional[int] = None
    token_count_after: Optional[int] = None
    response_time_ms: Optional[float] = None
    first_attempt_success: bool = False
    
    # 품질 메트릭
    context_miss_detected: bool = False
    duplicate_work_detected: bool = False
    consistency_violation: bool = False
    error_repeated: bool = False
    
    # 추가 메타데이터
    compact_triggered: bool = False
    rollback_triggered: bool = False
    notes: str = ""

class ContextPerformanceMonitor:
    """컨텍스트 성능 모니터링 클래스"""
    
    def __init__(self, metrics_file: str = "docs/CURRENT/context_metrics.json"):
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.current_session = self._generate_session_id()
        
    def _generate_session_id(self) -> str:
        """세션 ID 생성"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def start_measurement(self, task_type: str, task_description: str) -> str:
        """측정 시작"""
        metric_id = f"{self.current_session}_{int(time.time())}"
        
        metric = PerformanceMetrics(
            timestamp=datetime.now().isoformat(),
            session_id=self.current_session,
            task_type=task_type,
            notes=task_description
        )
        
        self._save_metric(metric_id, metric)
        return metric_id
    
    def update_metric(self, metric_id: str, **kwargs) -> None:
        """메트릭 업데이트"""
        metrics = self._load_metrics()
        if metric_id in metrics:
            metric_dict = metrics[metric_id]
            metric_dict.update(kwargs)
            metrics[metric_id] = metric_dict
            self._save_all_metrics(metrics)
    
    def calculate_performance_score(self) -> Dict:
        """성능 점수 계산"""
        metrics = self._load_metrics()
        if not metrics:
            return {"score": 0, "metrics": {}}
        
        recent_metrics = list(metrics.values())[-10:]  # 최근 10개
        
        # 효율성 점수 계산
        token_improvements = []
        response_times = []
        success_rates = []
        
        for m in recent_metrics:
            if m.get('token_count_before') and m.get('token_count_after'):
                improvement = (m['token_count_before'] - m['token_count_after']) / m['token_count_before'] * 100
                token_improvements.append(improvement)
            
            if m.get('response_time_ms'):
                response_times.append(m['response_time_ms'])
                
            success_rates.append(1.0 if m.get('first_attempt_success') else 0.0)
        
        # 품질 점수 계산
        quality_issues = sum([
            1 for m in recent_metrics if (
                m.get('context_miss_detected') or
                m.get('duplicate_work_detected') or  
                m.get('consistency_violation') or
                m.get('error_repeated')
            )
        ])
        
        quality_score = max(0, 100 - (quality_issues / len(recent_metrics) * 100))
        
        return {
            "overall_score": (
                (sum(token_improvements) / len(token_improvements) if token_improvements else 0) * 0.3 +
                (sum(success_rates) / len(success_rates) * 100) * 0.4 +
                quality_score * 0.3
            ),
            "metrics": {
                "avg_token_improvement": sum(token_improvements) / len(token_improvements) if token_improvements else 0,
                "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
                "success_rate": sum(success_rates) / len(success_rates) * 100,
                "quality_score": quality_score,
                "sample_size": len(recent_metrics)
            }
        }
    
    def check_rollback_conditions(self) -> Dict:
        """롤백 조건 확인"""
        performance = self.calculate_performance_score()
        metrics = performance["metrics"]
        
        rollback_triggers = []
        
        if metrics["success_rate"] < 70:
            rollback_triggers.append(f"첫시도 성공률 {metrics['success_rate']:.1f}% < 70%")
            
        if metrics["quality_score"] < 75:
            rollback_triggers.append(f"품질 점수 {metrics['quality_score']:.1f} < 75")
            
        if metrics.get("avg_token_improvement", 0) < 0:
            rollback_triggers.append("토큰 효율성 감소")
        
        return {
            "should_rollback": len(rollback_triggers) > 0,
            "triggers": rollback_triggers,
            "performance_score": performance["overall_score"]
        }
    
    def _load_metrics(self) -> Dict:
        """메트릭 로드"""
        if not self.metrics_file.exists():
            return {}
        try:
            with open(self.metrics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_metric(self, metric_id: str, metric: PerformanceMetrics) -> None:
        """메트릭 저장"""
        metrics = self._load_metrics()
        metrics[metric_id] = asdict(metric)
        self._save_all_metrics(metrics)
    
    def _save_all_metrics(self, metrics: Dict) -> None:
        """전체 메트릭 저장"""
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)

def main():
    """CLI 인터페이스"""
    import sys
    
    monitor = ContextPerformanceMonitor()
    
    if len(sys.argv) < 2:
        print("Usage: python context_performance_monitor.py [start|update|score|check] [args...]")
        return
    
    command = sys.argv[1]
    
    if command == "start":
        if len(sys.argv) < 4:
            print("Usage: start <task_type> <description>")
            return
        metric_id = monitor.start_measurement(sys.argv[2], sys.argv[3])
        print(f"Started measurement: {metric_id}")
        
    elif command == "score":
        score = monitor.calculate_performance_score()
        print(f"Performance Score: {score['overall_score']:.1f}")
        print(f"Metrics: {score['metrics']}")
        
    elif command == "check":
        rollback_check = monitor.check_rollback_conditions()
        print(f"Should rollback: {rollback_check['should_rollback']}")
        if rollback_check['triggers']:
            print(f"Triggers: {rollback_check['triggers']}")

if __name__ == "__main__":
    main()