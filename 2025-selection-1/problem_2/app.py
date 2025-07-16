print(f"✅ sub_module.py 파일이 로딩되었습니다. 이 파일의 __name__은 [ {__name__} ] 입니다.")

def sub_function():
    print(">>> 부품 파일(sub_module)의 함수가 호출되었습니다.")

# 이 파일을 '직접' 실행했을 때만 아래 코드가 작동합니다.
if __name__ == "__main__":
    print("... sub_module.py를 직접 실행했군요! ...")
    sub_function()