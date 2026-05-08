#!/usr/bin/env python3
"""
테스트 실행 스크립트

프로젝트 루트에서 test 폴더의 모든 테스트를 실행합니다.
"""

import subprocess
import sys
import os


def main():
    """메인 실행 함수"""
    print("🚀 codyssey-team 프로젝트 테스트 시작")
    
    # test 폴더로 이동해서 실행
    test_dir = os.path.join(os.path.dirname(__file__), 'test')
    
    if not os.path.exists(test_dir):
        print("❌ test 폴더를 찾을 수 없습니다.")
        sys.exit(1)
    
    try:
        # test 폴더의 run_all_tests.py 실행
        result = subprocess.run(
            [sys.executable, os.path.join(test_dir, 'run_all_tests.py')],
            cwd=os.path.dirname(__file__)  # 프로젝트 루트에서 실행
        )
        
        sys.exit(result.returncode)
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
