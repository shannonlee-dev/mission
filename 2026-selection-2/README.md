# Python 콘솔 퀴즈 게임

## 1. 프로젝트 개요
이 프로젝트는 Python 기초 상식을 주제로 한 콘솔 퀴즈 게임을 만드는 과제이다.

### 터미널 작업 시작 위치
프로젝트 작업은 아래 경로에서 시작했다.

```zsh
cd ~/dev
```

실행 결과:

```text
/Users/shh921shh4393/dev
```

```zsh
mkdir -p python-quiz-game-mission
```

실행 결과:

```text
(출력 없음)
```

```zsh
cd python-quiz-game-mission
```

실행 결과:

```text
(출력 없음)
```

```zsh
pwd
```

실행 결과:

```text
/Users/shh921shh4393/dev/python-quiz-game-mission
```

### 초기 프로젝트 생성 로그
기본 폴더와 파일을 만든 뒤 현재 구조를 확인했다.

```zsh
mkdir -p docs/screenshots
```

실행 결과:

```text
(출력 없음)
```

```zsh
touch main.py
```

실행 결과:

```text
(출력 없음)
```

```zsh
touch quiz.py
```

실행 결과:

```text
(출력 없음)
```

```zsh
touch quiz_game.py
```

실행 결과:

```text
(출력 없음)
```

```zsh
touch README.md
```

실행 결과:

```text
(출력 없음)
```

```zsh
touch .gitignore
```

실행 결과:

```text
(출력 없음)
```

```zsh
ls -la
```

실행 결과:

```text
total 48
drwxr-xr-x  10 shh921shh4393  shh921shh4393  320 Mar 31 18:14 .
drwxr-xr-x   7 shh921shh4393  shh921shh4393  224 Mar 31 18:13 ..
drwxr-xr-x  13 shh921shh4393  shh921shh4393  416 Mar 31 18:16 .git
-rw-r--r--   1 shh921shh4393  shh921shh4393   30 Mar 31 18:13 .gitignore
drwxr-xr-x   3 shh921shh4393  shh921shh4393   96 Mar 31 18:13 docs
-rw-r--r--   1 shh921shh4393  shh921shh4393   53 Mar 31 18:13 main.py
-rw-r--r--   1 shh921shh4393  shh921shh4393   62 Mar 31 18:13 quiz_game.py
-rw-r--r--   1 shh921shh4393  shh921shh4393   52 Mar 31 18:13 quiz.py
-rw-r--r--   1 shh921shh4393  shh921shh4393  968 Mar 31 18:18 README.md
-rw-r--r--   1 shh921shh4393  shh921shh4393   40 Mar 31 18:13 state.json
```

## 2. 퀴즈 주제 선정 이유

## 3. 실행 환경
- Python: Python 3.9.6
- Python 경로: /usr/bin/python3
- Git: git version 2.53.0
- Shell: /bin/zsh
- OS: Darwin 24.6.0 x86_64
- 에디터: VSCode

## 4. 실행 방법

## 5. 기능 목록

## 6. 프로젝트 구조

## 7. 클래스 설계

## 8. 데이터 파일 설명
`state.json`은 프로젝트 루트에 위치하며, 퀴즈 목록과 최고 점수를 UTF-8 JSON 형식으로 저장한다.
프로그램 종료 후 다시 실행해도 추가한 퀴즈와 최고 점수가 유지되도록 하기 위해 사용한다.

```zsh
ls -la
```

실행 결과:

```text
total 64
drwxr-xr-x   5 shh921shh4393  shh921shh4393   160 Mar 31 19:14 __pycache__
drwxr-xr-x  11 shh921shh4393  shh921shh4393   352 Mar 31 19:12 .
drwxr-xr-x   7 shh921shh4393  shh921shh4393   224 Mar 31 18:13 ..
drwxr-xr-x  14 shh921shh4393  shh921shh4393   448 Mar 31 19:20 .git
-rw-r--r--   1 shh921shh4393  shh921shh4393    30 Mar 31 18:13 .gitignore
drwxr-xr-x   3 shh921shh4393  shh921shh4393    96 Mar 31 18:13 docs
-rw-r--r--   1 shh921shh4393  shh921shh4393   556 Mar 31 19:14 main.py
-rw-r--r--   1 shh921shh4393  shh921shh4393  8661 Mar 31 19:14 quiz_game.py
-rw-r--r--   1 shh921shh4393  shh921shh4393   881 Mar 31 18:28 quiz.py
-rw-r--r--   1 shh921shh4393  shh921shh4393  4023 Mar 31 19:00 README.md
-rw-r--r--   1 shh921shh4393  shh921shh4393  1530 Mar 31 19:20 state.json
```

## 9. 상태 저장 및 복구 방식
프로그램은 시작 시 `state.json`을 읽어 퀴즈 목록과 최고 점수를 복구한다.
파일이 없거나 JSON 구조가 손상된 경우에는 기본 퀴즈 데이터로 다시 초기화하고 즉시 `state.json`을 재생성한다.

```zsh
cat state.json
```

실행 결과:

```json
{
    "quizzes": [
        {
            "question": "Python의 창시자는 누구인가?",
            "choices": [
                "귀도 반 로섬",
                "리누스 토르발스",
                "제임스 고슬링",
                "비야네 스트롭스트룹"
            ],
            "answer": 1
        },
        {
            "question": "Python에서 리스트를 만들 때 사용하는 기호는 무엇인가?",
            "choices": [
                "{}",
                "[]",
                "()",
                "<>"
            ],
            "answer": 2
        },
        {
            "question": "조건이 참일 때만 실행 흐름을 나누는 문법은 무엇인가?",
            "choices": [
                "for",
                "while",
                "if",
                "def"
            ],
            "answer": 3
        },
        {
            "question": "문자열을 숫자로 변환할 때 주로 사용하는 함수는 무엇인가?",
            "choices": [
                "str()",
                "list()",
                "int()",
                "dict()"
            ],
            "answer": 3
        },
        {
            "question": "반복 가능한 객체를 순회할 때 자주 사용하는 반복문은 무엇인가?",
            "choices": [
                "if",
                "for",
                "class",
                "try"
            ],
            "answer": 2
        }
    ],
    "best_score": 5,
    "best_total_questions": 5
}
```

파일이 없을 때도 기본 데이터로 자동 복구되는지 확인했다.

```zsh
rm -f state.json
```

실행 결과:

```text
(출력 없음)
```

```zsh
python3 main.py
```

실행 결과:

```text
state.json 파일이 없어 기본 퀴즈 데이터로 시작합니다.

========================================
        나만의 퀴즈 게임
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
========================================
선택:
```

아래 스크린샷은 `state.json` 파일이 없을 때 기본 퀴즈 데이터로 복구되는 화면이다.

![state-file-missing-recover](docs/screenshots/state-file-missing-recover.png)

손상된 JSON 파일이 있을 때도 기본 데이터로 자동 복구되는지 확인했다.

```zsh
echo "{broken json" > state.json
```

실행 결과:

```text
(출력 없음)
```

```zsh
python3 main.py
```

실행 결과:

```text
state.json 파일이 없거나 손상되어 기본 데이터로 복구합니다.
상세 원인: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

========================================
        나만의 퀴즈 게임
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
========================================
선택: 게임을 종료합니다.
```

```zsh
cat state.json
```

실행 결과:

```json
{
    "quizzes": [
        {
            "question": "Python의 창시자는 누구인가?",
            "choices": [
                "귀도 반 로섬",
                "리누스 토르발스",
                "제임스 고슬링",
                "비야네 스트롭스트룹"
            ],
            "answer": 1
        },
        {
            "question": "Python에서 리스트를 만들 때 사용하는 기호는 무엇인가?",
            "choices": [
                "{}",
                "[]",
                "()",
                "<>"
            ],
            "answer": 2
        },
        {
            "question": "조건이 참일 때만 실행 흐름을 나누는 문법은 무엇인가?",
            "choices": [
                "for",
                "while",
                "if",
                "def"
            ],
            "answer": 3
        },
        {
            "question": "문자열을 숫자로 변환할 때 주로 사용하는 함수는 무엇인가?",
            "choices": [
                "str()",
                "list()",
                "int()",
                "dict()"
            ],
            "answer": 3
        },
        {
            "question": "반복 가능한 객체를 순회할 때 자주 사용하는 반복문은 무엇인가?",
            "choices": [
                "if",
                "for",
                "class",
                "try"
            ],
            "answer": 2
        }
    ],
    "best_score": null,
    "best_total_questions": null
}
```

아래 스크린샷은 손상된 `state.json` 파일이 복구되는 화면이다.

![state-file-corrupted-recover](docs/screenshots/state-file-corrupted-recover.png)

## 10. 입력 검증 및 예외 처리 방식

## 11. Git 작업 기록
프로젝트 시작 직후 Git 저장소를 초기화하고 첫 커밋을 만들었다.

```zsh
git init
```

실행 결과:

```text
Initialized empty Git repository in /Users/shh921shh4393/dev/python-quiz-game-mission/.git/
```

```zsh
git add .
```

실행 결과:

```text
(출력 없음)
```

```zsh
git commit -m "Chore: 프로젝트 기본 구조와 README 뼈대 초기화"
```

실행 결과:

```text
[main (root-commit) 8a1ec54] Chore: 프로젝트 기본 구조와 README 뼈대 초기화
 6 files changed, 52 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 main.py
 create mode 100644 quiz.py
 create mode 100644 quiz_game.py
 create mode 100644 state.json
```

```zsh
git branch
```

실행 결과:

```text
* main
```

이후 GitHub 원격 저장소를 연결하고 첫 push를 완료했다.

```zsh
git remote add origin https://github.com/shannonlee-dev/python-quiz-game-mission.git
```

실행 결과:

```text
(출력 없음)
```

```zsh
git push -u origin main
```

실행 결과:

```text
To https://github.com/shannonlee-dev/python-quiz-game-mission.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

퀴즈 출제 기능은 별도 브랜치에서 작업하기 위해 기능 브랜치를 생성했다.

```zsh
git checkout -b feature/play-quiz
```

실행 결과:

```text
Switched to a new branch 'feature/play-quiz'
```

```zsh
git branch
```

실행 결과:

```text
* feature/play-quiz
  main
```

## 12. 검증 방법

## 13. 실행 결과 스크린샷

## 14. 트러블슈팅

## 15. 저장소 링크
https://github.com/shannonlee-dev/python-quiz-game-mission
