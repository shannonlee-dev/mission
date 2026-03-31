# Python 콘솔 퀴즈 게임

## 1. 프로젝트 개요

이 프로젝트는 **Python 기초 상식**을 주제로 한 콘솔 퀴즈 게임이다.  
Python 기본 문법, 클래스(객체 지향), 파일 입출력, Git/GitHub 사용을 한 번에 연습하기 위해 만들었다.

이 프로젝트를 통해 아래를 구현했다.

- 메뉴 기반 콘솔 프로그램
- `Quiz`, `QuizGame` 클래스를 통한 역할 분리
- `state.json`을 이용한 퀴즈/점수 영속성 구현
- 잘못된 입력 및 예외 상황 처리
- Git 브랜치, 병합, `clone`, `pull` 실습 기록
- README 기반 검증 문서화

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
touch main.py
touch quiz.py
touch quiz_game.py
touch README.md
touch .gitignore
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

---

## 2. 퀴즈 주제 선정 이유

퀴즈 주제는 **Python 기초 상식**으로 정했다.

선정 이유는 다음과 같다.

- 이번 과제의 핵심 학습 목표가 Python 기본 문법, 클래스, 파일 저장 구조를 이해하는 것이기 때문이다.
- 프로그램 주제와 학습 주제가 동일하면 문제를 만들고 검증하는 과정이 자연스럽다.
- 사용자가 퀴즈를 풀면서 Python 개념을 같이 복습할 수 있어 과제 목적과 잘 맞는다.

즉, 이 프로젝트는 단순한 게임 구현이 아니라 **Python 학습 내용을 퀴즈 형태로 다시 확인하는 구조**를 의도했다.

---

## 3. 실행 환경

- Python: Python 3.9.6
- Python 경로: `/usr/bin/python3`
- Git: `git version 2.53.0`
- Shell: `/bin/zsh`
- OS: `Darwin 24.6.0 x86_64`
- 에디터: VSCode

> 주의: 과제 요구사항은 **Python 3.10 이상**이다. 현재 로컬 실행 환경 로그는 Python 3.9.6 기준으로 정리되어 있으므로, 제출 전에 Python 3.10 이상 환경으로 다시 검증하는 것이 가장 안전하다.

---

## 4. 실행 방법

### 4-1. 저장소 clone

```zsh
git clone https://github.com/shannonlee-dev/python-quiz-game-mission.git
cd python-quiz-game-mission
```

### 4-2. 프로그램 실행

```zsh
python3 main.py
```

### 4-3. 실행 후 사용 흐름

프로그램을 실행하면 메뉴가 출력된다.

- `1`: 퀴즈 풀기
- `2`: 퀴즈 추가
- `3`: 퀴즈 목록
- `4`: 점수 확인
- `5`: 종료

프로그램은 종료 전 `state.json`에 현재 상태를 저장하며, 다음 실행 시 저장된 퀴즈 목록과 최고 점수를 다시 불러온다.

---

## 5. 기능 목록

- 퀴즈 풀기
  - 저장된 퀴즈를 순서대로 출제
  - 정답 입력 처리
  - 정답/오답 판별
  - 최종 점수 계산 및 출력
- 퀴즈 추가
  - 문제, 선택지 4개, 정답 번호 입력
  - 추가 즉시 파일 저장
- 퀴즈 목록 보기
  - 등록된 전체 퀴즈 질문 목록 출력
  - 퀴즈가 없을 경우 안내 메시지 출력
- 최고 점수 확인
  - 최고 정답 수와 문제 수 기준 점수 출력
  - 아직 플레이 기록이 없으면 안내 메시지 출력
- 상태 저장/불러오기
  - `state.json`에 퀴즈 목록과 최고 점수 저장
  - 재실행 시 자동 복구
- 예외 처리
  - 빈 입력 차단
  - 숫자 변환 실패 차단
  - 허용 범위 밖 입력 차단
  - `KeyboardInterrupt`, `EOFError` 발생 시 저장 후 안전 종료
- 복구 처리
  - `state.json`이 없으면 기본 퀴즈 데이터로 초기화
  - `state.json`이 손상되면 안내 후 기본 데이터로 복구

---

## 6. 프로젝트 구조

```text
python-quiz-game-mission/
├── main.py
├── quiz.py
├── quiz_game.py
├── README.md
├── .gitignore
├── state.json
└── docs/
    └── screenshots/
```

### 구조를 이렇게 나눈 이유

- `main.py`
  - 프로그램 실행 시작점만 담당한다.
  - 메뉴 루프와 기능 호출 흐름을 연결한다.
- `quiz.py`
  - 개별 퀴즈 1개를 표현하는 `Quiz` 클래스를 담는다.
  - 문제, 선택지, 정답, 출력, 정답 판별, 객체-딕셔너리 변환 책임을 가진다.
- `quiz_game.py`
  - 전체 게임 흐름을 관리하는 `QuizGame` 클래스를 담는다.
  - 메뉴, 퀴즈 진행, 추가, 목록, 점수, 저장/불러오기, 입력 검증을 담당한다.
- `state.json`
  - 퀴즈 목록과 최고 점수를 저장하는 상태 파일이다.
- `docs/screenshots`
  - 실행 결과와 검증 증거 스크린샷을 보관한다.
- `.gitignore`
  - 캐시 파일과 macOS 시스템 파일 등 Git 추적이 필요 없는 파일을 제외한다.

현재 프로젝트 루트 구조는 아래와 같다.

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

---

## 7. 클래스 설계

## `Quiz`

개별 퀴즈 1개를 표현하는 클래스다.

### 속성
- `question`
- `choices`
- `answer`

### 메서드
- `display(index)`
  - 문제 번호, 질문, 선택지를 출력한다.
- `is_correct(user_answer)`
  - 사용자가 입력한 정답 번호가 맞는지 판별한다.
- `to_dict()`
  - 현재 퀴즈 객체를 JSON 저장용 딕셔너리로 변환한다.
- `from_dict(data)`
  - 딕셔너리 데이터를 다시 `Quiz` 객체로 복원한다.

## `QuizGame`

게임 전체를 관리하는 클래스다.

### 속성
- `quizzes`
- `best_score`
- `best_total_questions`
- `state_path`

### 메서드
- `show_menu()`
- `play_quiz()`
- `add_quiz()`
- `list_quizzes()`
- `show_best_score()`
- `load_state()`
- `save_state()`
- `read_non_empty_text()`
- `read_int_in_range()`
- `safe_exit()`

### 역할 분리 이유

`Quiz`는 **퀴즈 1개**의 정보와 동작을 담당하고,  
`QuizGame`은 **게임 전체 흐름**과 저장 상태를 관리한다.

이렇게 분리하면 개별 문제 로직과 전체 프로그램 로직이 섞이지 않아 코드가 더 읽기 쉽고 수정하기 쉽다.

---

## 8. 데이터 파일 설명

`state.json`은 프로젝트 루트에 위치하며, 퀴즈 목록과 최고 점수를 UTF-8 JSON 형식으로 저장한다.  
프로그램 종료 후 다시 실행해도 추가한 퀴즈와 최고 점수가 유지되도록 하기 위해 사용한다.

### 저장 스키마

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
        }
    ],
    "best_score": 3,
    "best_total_questions": 5
}
```

### 현재 확인된 실제 상태 파일 예시

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

---

## 9. 상태 저장 및 복구 방식

프로그램은 시작 시 `state.json`을 읽어 퀴즈 목록과 최고 점수를 복구한다.  
파일이 없거나 JSON 구조가 손상된 경우에는 기본 퀴즈 데이터로 다시 초기화하고 즉시 `state.json`을 재생성한다.

### 9-1. 파일이 없을 때 복구

```zsh
rm -f state.json
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

### 9-2. 손상된 JSON 파일 복구

```zsh
echo "{broken json" > state.json
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

복구 후 `state.json`을 다시 확인했다.

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

### 9-3. 재실행 후 데이터 유지 확인

프로그램을 다시 실행했을 때 추가한 퀴즈와 최고 점수가 유지되는지도 확인했다.

아래 스크린샷은 재실행 직후 저장된 퀴즈 개수와 최고 점수가 다시 불러와지는 화면이다.

![persistence-check](docs/screenshots/persistence-check.png)

---

## 10. 입력 검증 및 예외 처리 방식

숫자 입력이 필요한 메뉴와 정답 입력에서 다음을 공통 처리했다.

- 입력 앞뒤 공백 제거
- 빈 입력 차단
- 숫자 변환 실패 차단
- 허용 범위 밖 숫자 차단
- `KeyboardInterrupt`, `EOFError` 발생 시 저장 후 안전 종료

아래 스크린샷은 빈 입력, 문자 입력, 범위 밖 숫자 입력을 차례로 검증한 화면이다.

![invalid-input-check](docs/screenshots/invalid-input-check.png)

메뉴 입력 또는 퀴즈 입력 도중 `KeyboardInterrupt`, `EOFError`가 발생하면 현재 상태를 `state.json`에 저장한 뒤 안전하게 종료하도록 처리했다.

아래 스크린샷은 `Ctrl + C` 입력 시 traceback 없이 안전 종료되는 화면이다.

![safe-exit](docs/screenshots/safe-exit.png)

---

## 11. Git 작업 기록

프로젝트 시작 직후 Git 저장소를 초기화하고 첫 커밋을 만들었다.

```zsh
git init
git add .
git commit -m "Chore: 프로젝트 기본 구조와 README 뼈대 초기화"
git branch
```

실행 결과:

```text
Initialized empty Git repository in /Users/shh921shh4393/dev/python-quiz-game-mission/.git/
[main (root-commit) 8a1ec54] Chore: 프로젝트 기본 구조와 README 뼈대 초기화
 6 files changed, 52 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 main.py
 create mode 100644 quiz.py
 create mode 100644 quiz_game.py
 create mode 100644 state.json

* main
```

이후 GitHub 원격 저장소를 연결하고 첫 push를 완료했다.

```zsh
git remote add origin https://github.com/shannonlee-dev/python-quiz-game-mission.git
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
git branch
```

실행 결과:

```text
Switched to a new branch 'feature/play-quiz'
* feature/play-quiz
  main
```

### `clone` 실습

```zsh
git clone https://github.com/shannonlee-dev/python-quiz-game-mission.git python-quizgame-mission-clone
pwd
ls -la
```

실행 결과:

```text
Cloning into 'python-quizgame-mission-clone'...
remote: Enumerating objects: 62, done.
remote: Counting objects: 100% (62/62), done.
remote: Compressing objects: 100% (39/39), done.
remote: Total 62 (delta 26), reused 54 (delta 18), pack-reused 0 (from 0)
Receiving objects: 100% (62/62), 374.64 KiB | 31.22 MiB/s, done.
Resolving deltas: 100% (26/26), done.

/Users/shh921shh4393/dev/python-quizgame-mission-clone

total 80
drwxr-xr-x  10 shh921shh4393  shh921shh4393    320 Mar 31 19:49 .
drwxr-xr-x   8 shh921shh4393  shh921shh4393    256 Mar 31 19:49 ..
drwxr-xr-x  12 shh921shh4393  shh921shh4393    384 Mar 31 19:49 .git
-rw-r--r--   1 shh921shh4393  shh921shh4393     30 Mar 31 19:49 .gitignore
drwxr-xr-x   3 shh921shh4393  shh921shh4393     96 Mar 31 19:49 docs
-rw-r--r--   1 shh921shh4393  shh921shh4393    556 Mar 31 19:49 main.py
-rw-r--r--   1 shh921shh4393  shh921shh4393   8661 Mar 31 19:49 quiz_game.py
-rw-r--r--   1 shh921shh4393  shh921shh4393    881 Mar 31 19:49 quiz.py
-rw-r--r--   1 shh921shh4393  shh921shh4393  11178 Mar 31 19:49 README.md
-rw-r--r--   1 shh921shh4393  shh921shh4393   1761 Mar 31 19:49 state.json
```

### `pull` 실습

```zsh
git pull origin main
tail -n 5 README.md
```

실행 결과:

```text
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (1/1), done.
remote: Total 3 (delta 2), reused 3 (delta 2), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 379 bytes | 126.00 KiB/s, done.
From https://github.com/shannonlee-dev/python-quiz-game-mission
 * branch            main       -> FETCH_HEAD
   c8fae8d..2470336  main       -> origin/main
Updating c8fae8d..2470336
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)

## 15. 저장소 링크
https://github.com/shannonlee-dev/python-quiz-game-mission

- clone 실습으로 추가한 문장입니다.
```

### Git 그래프 기록

아래 스크린샷은 `git log --oneline --graph --all` 결과를 캡처한 것이다.

![git-log-graph](docs/screenshots/git-log-graph.png)

---

## 12. 검증 방법

| 항목 | 검증 방법 | 결과 | 근거 |
|---|---|---|---|
| 메뉴 출력 | `python3 main.py` 실행 | 정상 출력 | `menu.png` |
| 퀴즈 추가 | 메뉴 2번 선택 후 문제/선택지/정답 입력 | 저장 후 목록 반영 확인 | `add-quiz.png`, `quiz-list.png` |
| 퀴즈 목록 | 메뉴 3번 선택 | 등록된 질문 목록 출력 확인 | `quiz-list.png` |
| 퀴즈 플레이 | 메뉴 1번 선택 후 정답 입력 | 정답/오답/최종 결과 출력 확인 | `play-quiz.png` |
| 최고 점수 확인 | 메뉴 4번 선택 | 최고 점수 출력 확인 | `best-score.png` |
| 데이터 유지 | 종료 후 재실행 | 추가 퀴즈와 최고 점수 유지 확인 | `persistence-check.png` |
| 파일 누락 복구 | `rm -f state.json` 후 실행 | 기본 데이터로 복구 확인 | `state-file-missing-recover.png` |
| 파일 손상 복구 | `echo "{broken json" > state.json` 후 실행 | 복구 메시지 및 정상 실행 확인 | `state-file-corrupted-recover.png` |
| 입력 검증 | 빈 입력, 문자 입력, 범위 밖 숫자 입력 | 재입력 처리 확인 | `invalid-input-check.png` |
| 안전 종료 | 메뉴 입력 중 `Ctrl + C` | 저장 후 안전 종료 확인 | `safe-exit.png` |
| 문법 검사 | `python3 -m py_compile main.py quiz.py quiz_game.py` | 오류 없이 통과해야 함 | 로컬 실행 검증 |
| Git 브랜치 | `git checkout -b feature/play-quiz`, 병합 로그 확인 | 브랜치 생성/병합 기록 확인 | `git-log-graph.png` |
| Git clone/pull | `git clone`, `git pull origin main` | 복제/최신 반영 확인 | README 기록 및 터미널 로그 |

---

## 13. 실행 결과 스크린샷

### 메뉴 화면
![menu](docs/screenshots/menu.png)

### 퀴즈 추가
![add-quiz](docs/screenshots/add-quiz.png)

### 퀴즈 목록
![quiz-list](docs/screenshots/quiz-list.png)

### 퀴즈 플레이 결과
![play-quiz](docs/screenshots/play-quiz.png)

### 최고 점수 확인
![best-score](docs/screenshots/best-score.png)

### 데이터 유지 확인
![persistence-check](docs/screenshots/persistence-check.png)

### 파일 누락 복구
![state-file-missing-recover](docs/screenshots/state-file-missing-recover.png)

### 파일 손상 복구
![state-file-corrupted-recover](docs/screenshots/state-file-corrupted-recover.png)

### 잘못된 입력 처리
![invalid-input-check](docs/screenshots/invalid-input-check.png)

### 안전 종료
![safe-exit](docs/screenshots/safe-exit.png)

### Git 로그 그래프
![git-log-graph](docs/screenshots/git-log-graph.png)

---

## 14. 트러블슈팅

### 문제 1. `state.json`이 없을 때 프로그램이 시작되지 않을 수 있었다

- 문제: 첫 실행 시 저장 파일이 없으면 상태 복구 단계에서 실패할 수 있다.
- 원인 가설: 파일 존재 여부를 먼저 검사하지 않고 바로 읽기를 시도하면 예외가 날 수 있다.
- 확인: `rm -f state.json` 후 `python3 main.py`를 실행해 파일 누락 상황을 직접 재현했다.
- 해결: 파일이 없으면 기본 퀴즈 데이터를 사용하고 즉시 `state.json`을 새로 저장하도록 처리했다.

### 문제 2. 손상된 JSON 때문에 상태 복구가 실패할 수 있었다

- 문제: `state.json`이 깨진 경우 `json.JSONDecodeError`로 로딩이 중단될 수 있다.
- 원인 가설: 사용자가 파일을 잘못 수정했거나 비정상 종료로 인해 JSON 구조가 깨질 수 있다.
- 확인: `echo "{broken json" > state.json` 후 실행하여 오류를 직접 재현했다.
- 해결: 예외를 잡아 안내 메시지를 출력하고 기본 퀴즈 데이터로 복구한 뒤 새 상태 파일을 다시 저장하도록 처리했다.

### 문제 3. 잘못된 입력이나 강제 중단으로 프로그램 흐름이 깨질 수 있었다

- 문제: 메뉴 입력에서 빈 값, 문자, 범위 밖 숫자가 들어오거나 `Ctrl + C`가 발생하면 흐름이 끊길 수 있다.
- 원인 가설: 입력값 검증과 중단 처리가 공통 메서드로 묶여 있지 않으면 프로그램이 쉽게 비정상 종료될 수 있다.
- 확인: 빈 입력, `abc`, `9`, `Ctrl + C`를 직접 입력해 재현했다.
- 해결: `read_int_in_range()`, `read_non_empty_text()`, `safe_exit()` 메서드로 공통 처리 로직을 분리해 안정적으로 재입력 또는 저장 후 종료되도록 구성했다.

---

## 15. 저장소 링크

GitHub Repository:  
`https://github.com/shannonlee-dev/python-quiz-game-mission`

- clone 실습으로 추가한 문장입니다.

---

## 16. 제출 전 최종 체크리스트

- [ ] Python 3.10 이상 환경에서 다시 검증했는가
- [ ] `python3 main.py` 실행 시 메뉴가 정상 출력되는가
- [ ] 퀴즈 풀기 / 추가 / 목록 / 점수 확인 / 종료 기능이 전부 동작하는가
- [ ] 종료 후 재실행해도 퀴즈와 최고 점수가 유지되는가
- [ ] `state.json` 누락 시 기본 데이터로 복구되는가
- [ ] 손상된 `state.json`에서도 프로그램이 정상 복구되는가
- [ ] 빈 입력 / 문자 입력 / 범위 밖 숫자 입력이 재입력 처리되는가
- [ ] `KeyboardInterrupt`, `EOFError` 발생 시 저장 후 안전 종료되는가
- [ ] `Quiz`, `QuizGame` 최소 2개 클래스가 존재하는가
- [ ] Git 커밋 수가 10개 이상인가
- [ ] 브랜치 생성 및 병합 기록이 남아 있는가
- [ ] `clone`, `pull` 실습 결과가 README에 기록되어 있는가
- [ ] GitHub 저장소 링크 하나로 README, 코드, 스크린샷, Git 기록을 확인할 수 있는가
- [ ] 민감정보가 과도하게 노출되지 않았는가