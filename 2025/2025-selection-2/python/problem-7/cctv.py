import zipfile
from pathlib import Path
import cv2


def show_images(image_files):
    current_index = 0
    window_name = 'CCTV Image Viewer'
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  #OpenCV 윈도우 생성, WIONDOW_NORMAL은 창 크기 조절할 수 있는 인자
    
    while True:
        current_image_path = image_files[current_index]
        print(f"[{current_index + 1}/{len(image_files)}] {current_image_path.name}")
        
        image = cv2.imread(current_image_path)
        
        if image is None:
            print(f"이미지를 읽을 수 없습니다: {current_image_path.name}")
            current_index = (current_index + 1) % len(image_files)
            continue

        cv2.imshow(window_name, image)
        key = cv2.waitKey(0)
        
        if key == 27:  # ESC
            print("종료")
            break

        elif key == 83:  # 오른쪽 화살표
            current_index = (current_index + 1) % len(image_files)
        elif key == 81:  # 왼쪽 화살표
            current_index = (current_index - 1) % len(image_files)
    
    cv2.destroyAllWindows()
    print("프로그램 종료")


def detect_people_in_images(image_files):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    window_name = 'CCTV Person Detection'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    found_count = 0
    
    for index, image_path in enumerate(image_files):
        print(f"[{index + 1}/{len(image_files)}] 검색 중: {image_path.name}")
        
        # 이미지 읽기
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"이미지를 읽을 수 없습니다.")
            continue

        # 사람 탐지
        boxes, weights = hog.detectMultiScale(
            image,
            winStride=(1, 1), #이거 조절하면 신뢰도 조정 가능. 이동 간 간격(단위:픽셀)
            padding=(8, 8),
            scale=1.05,
            useMeanshiftGrouping=False
        )
        
        # 사람이 발견된 경우
        if len(boxes) > 0:
            found_count += 1
            print(f"  사람 발견! ({len(boxes)}명)\n  신뢰도 : {weights}")
            
            cv2.imshow(window_name, image)
            print("  Enter 키를 눌러 계속 검색...")
            
            key = cv2.waitKey(0)
            if key == 27:  # ESC로 종료
                print("\n검색 중단")
                cv2.destroyAllWindows()
                return
            
    cv2.destroyAllWindows()
    print("="*50)
    print(f"총 {len(image_files)}개 이미지 중 {found_count}개에서 사람 발견")
    print("="*50)


def main():
    zip_path = 'cctv.zip'

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            Path('CCTV').mkdir(parents=True, exist_ok=True)
            zf.extractall(Path('CCTV'))

    except Exception as e:
        print(f"압축 파일에서의 오류: {e}")
        return

    print(f"압축 해제 완료")
    
    cctv_folder = Path('CCTV')
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    
    image_files = []

    for file_path in cctv_folder.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    if not image_files:
        print("이미지 파일을 찾을 수 없습니다.")
        return
    
    
    print("="*50)
    print("1. 모든 이미지 보기")
    print("2. 사람 탐지 모드")
    print("="*50)
    
    while True:

        mode = input("입력: ").strip()
        if mode in ['1', '2']:
            break
        else:
            print("1 또는 2를 입력하세요.")        
    if mode == '1':
        show_images(image_files)
    elif mode == '2':
        detect_people_in_images(image_files)


if __name__ == '__main__':
    main()