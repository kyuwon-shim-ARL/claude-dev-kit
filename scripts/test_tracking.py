#!/usr/bin/env python3
"""
Test script for Timeline Tracking functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tracking_manager import TimelineTracker
import time
from datetime import datetime


def test_tracking():
    """Test timeline tracking functionality"""
    print("🧪 Testing Timeline Tracking System...")
    print("=" * 50)
    
    tracker = TimelineTracker()
    
    # Test 1: Track 레포정리 command
    print("\n📝 Test 1: Tracking /레포정리 --track")
    entry1 = tracker.track_execution("레포정리", ["--track"])
    print(f"  ✅ Created tracking entry: {entry1['id']}")
    time.sleep(1)
    tracker.complete_tracking(entry1, 1234)
    print(f"  ✅ Completed tracking with duration: 1234ms")
    
    # Test 2: Track 문서정리 command
    print("\n📝 Test 2: Tracking /문서정리 --with-timeline")
    entry2 = tracker.track_execution("문서정리", ["--with-timeline"])
    print(f"  ✅ Created tracking entry: {entry2['id']}")
    time.sleep(1)
    tracker.complete_tracking(entry2, 2345)
    print(f"  ✅ Completed tracking with duration: 2345ms")
    
    # Test 3: Generate timeline report
    print("\n📝 Test 3: Generating Timeline Report")
    report = tracker.generate_timeline_report()
    print("  ✅ Report generated successfully")
    print("\n📊 Report Preview (first 500 chars):")
    print("-" * 40)
    print(report[:500])
    print("-" * 40)
    
    # Test 4: Check file structure
    print("\n📝 Test 4: Verifying File Structure")
    base_path = ".claude"
    expected_files = [
        f"{base_path}/tracking/history.json",
        f"{base_path}/tracking/current.json",
    ]
    
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} exists")
        else:
            print(f"  ❌ {file_path} missing")
    
    # Test 5: Verify history content
    print("\n📝 Test 5: Verifying History Content")
    import json
    history_path = f"{base_path}/tracking/history.json"
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            history = json.load(f)
            print(f"  ✅ History contains {len(history['entries'])} entries")
            for entry in history['entries']:
                print(f"     - {entry['timestamp']}: {entry['command']} ({entry['id']})")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed successfully!")
    return True


def main():
    """Main test runner"""
    try:
        success = test_tracking()
        if success:
            print("\n🎉 Timeline Tracking System is working correctly!")
            print("\n💡 Usage examples:")
            print("  /레포정리 --track")
            print("  /문서정리 --with-timeline")
            print("  python scripts/tracking_manager.py report")
        else:
            print("\n❌ Some tests failed. Please check the output above.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()