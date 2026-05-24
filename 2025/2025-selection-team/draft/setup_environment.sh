#!/bin/bash

# Codyssey Team 프로젝트 환경 설정 스크립트

echo "🚀 Codyssey Team 프로젝트 환경을 설정합니다..."

# Python 버전 확인
echo "📋 Python 버전 확인 중..."
python_version=$(python3 --version 2>/dev/null || python --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ $python_version 이 설치되어 있습니다."
else
    echo "❌ Python이 설치되어 있지 않습니다. Python 3.8 이상을 설치해주세요."
    exit 1
fi

# 가상환경 생성
echo "🐍 가상환경을 생성합니다..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv 2>/dev/null || python -m venv .venv
    if [ $? -eq 0 ]; then
        echo "✅ 가상환경이 성공적으로 생성되었습니다."
    else
        echo "❌ 가상환경 생성에 실패했습니다."
        exit 1
    fi
else
    echo "✅ 가상환경이 이미 존재합니다."
fi

# 가상환경 활성화 확인
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "🔄 Windows 환경에서 가상환경을 활성화합니다..."
    source .venv/Scripts/activate
else
    # macOS/Linux
    echo "🔄 가상환경을 활성화합니다..."
    source .venv/bin/activate
fi

# pip 업데이트
echo "📦 pip을 업데이트합니다..."
pip install --upgrade pip

# 의존성 설치
echo "📚 필요한 패키지들을 설치합니다..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ 모든 패키지가 성공적으로 설치되었습니다."
    else
        echo "❌ 패키지 설치 중 오류가 발생했습니다."
        exit 1
    fi
else
    echo "❌ requirements.txt 파일을 찾을 수 없습니다."
    exit 1
fi

# 설치 확인
echo "🔍 설치된 패키지를 확인합니다..."
pip list | grep -E "(pandas|matplotlib|pytest)"

echo ""
echo "🎉 환경 설정이 완료되었습니다!"
echo ""
echo "사용 방법:"
echo "  1. 가상환경 활성화:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    echo "     source .venv/Scripts/activate"
else
    echo "     source .venv/bin/activate"
fi
echo "  2. 프로그램 실행:"
echo "     python mas_map.py"
echo "     python map_draw.py"
echo "     python map_direct_save.py"
echo "  3. 테스트 실행:"
echo "     python -m pytest test/"
