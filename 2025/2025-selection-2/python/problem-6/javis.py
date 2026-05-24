import os
import csv
import wave
import glob
from datetime import datetime

import pyaudio
import speech_recognition as sr


class VoiceProcessor:
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))  #절대경로에서 dirname 만
        self.records_dir = os.path.join(self.base_dir, 'records')
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100  # 1초에 44100 프레임 읽으면 1024/44100초   1프레임    1청크에 1024 버퍼   1프레임 읽는데 걸리는 시간이 20ms      
        self.recognizer = sr.Recognizer()

        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)
    
    def record_audio(self, duration=10):

        now = datetime.now()
        filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        filepath = os.path.join(self.records_dir, filename)

        audio = pyaudio.PyAudio()
        
        try:
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,  #마이크
                frames_per_buffer=self.chunk
            )
            
            print(f'녹음을 시작합니다... ({duration}초)')
            frames = []
            
            # 녹음
            for i in range(0, int(self.rate / self.chunk * duration)):  # 1청크에 프레임1024개, 초당 44100 프레임  
                data = stream.read(self.chunk)
                frames.append(data)
            
            print('녹음이 완료되었습니다.')
            
            # 스트림 닫기
            stream.stop_stream()
            stream.close()
            
            # WAV 파일로 저장
            wf = wave.open(filepath, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))  
            wf.close()
            
            print(f'파일이 저장되었습니다: {filepath}')
            return filepath
        except:
            print("알 수 없는 오류가 발생했습니다.")
            return
        finally:
            audio.terminate()
    
    def get_audio_files(self):

        audio_files = glob.glob(os.path.join(self.records_dir, '*.wav'))
        return sorted(audio_files)
    
    def speech_to_text(self, audio_file):
        results = []
        timestamp_str = '00:00:00'
        
        try:
            with sr.AudioFile(audio_file) as source:
                # 노이즈 제거를 위한 환경 조정
                self.recognizer.adjust_for_ambient_noise(source)
                
                # 전체 오디오 로드
                audio_data = self.recognizer.record(source)
                
                try:
                    # Google Web Speech API를 사용하여 텍스트 변환
                    text = self.recognizer.recognize_google(audio_data, language='ko-KR')

                    results.append((timestamp_str, text))
                    
                    print(f'STT 결과: {text}')
                    
                except sr.UnknownValueError:
                    print('음성을 인식할 수 없습니다.')
                    results.append((timestamp_str, '[인식 불가]'))
                    
                except sr.RequestError as e:
                    print(f'STT 서비스 요청 오류: {e}')
                    results.append((timestamp_str, '[서비스 오류]'))
        
        except Exception as e:
            print(f'오디오 파일 처리 중 오류 발생: {e}')
            results.append((timestamp_str, '[파일 오류]'))
        
        return results
    
    def save_to_csv(self, audio_file, stt_results):

        # 오디오 파일명에서 확장자를 제거하고 .csv 확장자 추가
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        csv_filename = base_name + '.csv'
        csv_filepath = os.path.join(self.records_dir, csv_filename)
        
        try:
            with open(csv_filepath, 'w', newline='', encoding='utf-8') as c:
                writer = csv.writer(c)

                writer.writerow(['시간', '인식된 텍스트'])
                for time_stamp, text in stt_results:
                    writer.writerow([time_stamp, text])
            
            print(f'CSV 파일이 저장되었습니다: {csv_filepath}')
            
        except Exception as e:
            print(f'CSV 파일 저장 중 오류 발생: {e}')
    
    def process_audio_file(self, audio_file):

        print(f'처리 중인 파일: {audio_file}')
        
        # STT 수행
        stt_results = self.speech_to_text(audio_file)
        
        # CSV로 저장
        self.save_to_csv(audio_file, stt_results)
    
    def process_all_audio_files(self):

        audio_files = self.get_audio_files()

        if not audio_files:
            print('처리할 오디오 파일이 없습니다.')
            return
        
        print(f'총 {len(audio_files)}개의 오디오 파일을 처리합니다.')
        
        for audio_file in audio_files:
            self.process_audio_file(audio_file)
            print('=' * 60)


def main():
    processor = VoiceProcessor()
    
    while True:
        print('=' * 21 + ' 음성 처리 시스템 ' + '=' * 21)
        print('1. 음성 녹음')
        print('2. 오디오 파일 목록 보기')
        print('3. STT 처리 (모든 파일)')
        print('4. 종료')
        print('=' * 60)

        choice = input('\n선택하세요 (1-4): ')
        
        if choice == '1':
            try:
                duration = int(input('녹음 시간을 입력하세요 (초): ').strip())
                processor.record_audio(duration)
            except ValueError:
                print('올바른 숫자를 입력하세요.')
        
        elif choice == '2':
            audio_files = processor.get_audio_files()
            if audio_files:
                print('\n=== 오디오 파일 목록 ===')
                for i, file in enumerate(audio_files, 1):
                    relative_path = os.path.relpath(file, processor.base_dir)
                    print(f'{i}. {relative_path}')
            else:
                print('오디오 파일이 없습니다.')
            input('메뉴로 돌아가려면 아무 키나 눌러주세요')    
        
        elif choice == '3':
            processor.process_all_audio_files()
        
        elif choice == '4':
            print('프로그램을 종료합니다.')
            break
        
        else:
            print('올바른 선택지를 입력하세요.')


if __name__ == '__main__':
    main()