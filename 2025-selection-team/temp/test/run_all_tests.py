#!/usr/bin/env python3
"""
전체 프로젝트 테스트 실행 스크립트

이 스크립트는 모든 Stage의 테스트를 순차적으로 실행하고 결과를 종합합니다.
"""

import subprocess
import sys
import os
import time
from pathlib import Path


def print_banner(title):
    """테스트 섹션 배너 출력"""
    print("\n" + "="*80)
    print(f"🧪 {title}")
    print("="*80)


def run_test_file(test_file):
    """개별 테스트 파일 실행"""
    # test 폴더 안의 파일이므로 상대 경로 조정
    test_file_path = test_file if os.path.exists(test_file) else os.path.join('test', test_file)
    
    if not os.path.exists(test_file_path):
        print(f"❌ 테스트 파일을 찾을 수 없습니다: {test_file_path}")
        return False
    
    print(f"🔄 {test_file} 실행 중...")
    
    try:
        # pytest를 사용하여 테스트 실행
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', test_file_path, '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=300  # 5분 타임아웃
        )
        
        if result.returncode == 0:
            print(f"✅ {test_file} 모든 테스트 통과")
            return True
        else:
            print(f"❌ {test_file} 테스트 실패")
            print("stderr:", result.stderr)
            if result.stdout:
                print("stdout:", result.stdout)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_file} 테스트 타임아웃 (5분 초과)")
        return False
    except Exception as e:
        print(f"❌ {test_file} 실행 중 오류: {e}")
        return False


def run_direct_module_test(module_name, description):
    """모듈을 직접 실행하여 테스트"""
    print(f"🔄 {description} 직접 실행 테스트...")
    
    if not os.path.exists(f"{module_name}.py"):
        print(f"❌ {module_name}.py 파일을 찾을 수 없습니다.")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, f"{module_name}.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"✅ {description} 실행 성공")
            return True
        else:
            print(f"❌ {description} 실행 실패")
            if result.stderr:
                print("오류:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} 실행 타임아웃")
        return False
    except Exception as e:
        print(f"❌ {description} 실행 중 오류: {e}")
        return False


def check_prerequisites():
    """테스트 실행을 위한 전제 조건 확인"""
    print_banner("전제 조건 확인")
    
    # Python 버전 확인
    python_version = sys.version_info
    print(f"🐍 Python 버전: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        return False
    
    # 필수 라이브러리 확인
    required_packages = ['pandas', 'matplotlib', 'pytest']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 설치됨")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 미설치")
    
    if missing_packages:
        print(f"❌ 필수 패키지를 설치해주세요: {', '.join(missing_packages)}")
        return False
    
    # 데이터 파일 확인
    data_files = ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']
    missing_data = []
    
    for file in data_files:
        # 상위 디렉토리에서 파일 확인
        file_path = os.path.join('..', file) if os.getcwd().endswith('test') else file
        if os.path.exists(file_path):
            print(f"✅ {file} 존재")
        else:
            missing_data.append(file)
            print(f"❌ {file} 없음")
    
    if missing_data:
        print("⚠️ 일부 데이터 파일이 없습니다. 관련 테스트는 건너뛸 수 있습니다.")
    
    # Python 파일 확인
    py_files = ['caffee_map.py', 'map_draw.py', 'map_direct_save.py']
    missing_py = []
    
    for file in py_files:
        # 상위 디렉토리에서 파일 확인
        file_path = os.path.join('..', file) if os.getcwd().endswith('test') else file
        if os.path.exists(file_path):
            print(f"✅ {file} 존재")
        else:
            missing_py.append(file)
            print(f"❌ {file} 없음")
    
    if missing_py:
        print(f"❌ 필수 Python 파일이 없습니다: {', '.join(missing_py)}")
        return False
    
    return True


def main():
    """메인 테스트 실행 함수"""
    start_time = time.time()
    
    print("🚀 프로젝트 통합 테스트 시작")
    print(f"📁 작업 디렉토리: {os.getcwd()}")
    
    # 전제 조건 확인
    if not check_prerequisites():
        print("❌ 전제 조건 확인 실패. 테스트를 중단합니다.")
        sys.exit(1)
    
    # 테스트 결과 추적
    test_results = {}
    
    # Stage 1 테스트
    print_banner("Stage 1: 데이터 수집 및 분석 테스트")
    test_results['stage1_unit'] = run_test_file('test_caffee_map.py')
    test_results['stage1_direct'] = run_direct_module_test('caffee_map', 'Stage 1 직접 실행')
    
    # Stage 2 테스트
    print_banner("Stage 2: 지도 시각화 테스트")
    test_results['stage2_unit'] = run_test_file('test_map_draw.py')
    test_results['stage2_direct'] = run_direct_module_test('map_draw', 'Stage 2 직접 실행')
    
    # Stage 3 테스트
    print_banner("Stage 3: 최단 경로 찾기 테스트")
    test_results['stage3_unit'] = run_test_file('test_map_direct_save.py')
    test_results['stage3_direct'] = run_direct_module_test('map_direct_save', 'Stage 3 직접 실행')
    
    # 통합 테스트
    print_banner("통합 테스트")
    test_results['integration'] = run_test_file('test_integration.py')
    
    # 결과 종합
    print_banner("테스트 결과 종합")
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"📊 전체 테스트 결과:")
    print(f"   - 총 테스트: {total_tests}개")
    print(f"   - 통과: {passed_tests}개")
    print(f"   - 실패: {failed_tests}개")
    print(f"   - 성공률: {(passed_tests/total_tests)*100:.1f}%")
    
    # 개별 테스트 결과 상세
    print(f"\n📋 개별 테스트 상세:")
    for test_name, result in test_results.items():
        status = "✅ 통과" if result else "❌ 실패"
        print(f"   - {test_name}: {status}")
    
    # 생성된 파일들 확인
    print(f"\n📁 생성된 출력 파일들:")
    output_files = ['map.png', 'home_to_cafe.csv', 'map_final.png']
    for file in output_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   - {file}: {size:,} bytes")
        else:
            print(f"   - {file}: 없음")
    
    # 실행 시간
    elapsed_time = time.time() - start_time
    print(f"\n⏱️ 총 실행 시간: {elapsed_time:.2f}초")
    
    # 최종 결과
    if failed_tests == 0:
        print("\n🎉 모든 테스트가 성공적으로 완료되었습니다!")
        sys.exit(0)
    else:
        print(f"\n⚠️ {failed_tests}개의 테스트가 실패했습니다. 로그를 확인해주세요.")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 테스트가 중단되었습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1)
