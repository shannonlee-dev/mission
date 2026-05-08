import json
from pathlib import Path

from quiz import Quiz


DEFAULT_QUIZ_DATA = [
    {
        "question": "Python의 창시자는 누구인가?",
        "choices": ["귀도 반 로섬", "리누스 토르발스", "제임스 고슬링", "비야네 스트롭스트룹"],
        "answer": 1,
    },
    {
        "question": "Python에서 리스트를 만들 때 사용하는 기호는 무엇인가?",
        "choices": ["{}", "[]", "()", "<>"],
        "answer": 2,
    },
    {
        "question": "조건이 참일 때만 실행 흐름을 나누는 문법은 무엇인가?",
        "choices": ["for", "while", "if", "def"],
        "answer": 3,
    },
    {
        "question": "문자열을 숫자로 변환할 때 주로 사용하는 함수는 무엇인가?",
        "choices": ["str()", "list()", "int()", "dict()"],
        "answer": 3,
    },
    {
        "question": "반복 가능한 객체를 순회할 때 자주 사용하는 반복문은 무엇인가?",
        "choices": ["if", "for", "class", "try"],
        "answer": 2,
    },
]


class QuizGame:
    # 기능 구분 기준: 저장, 입력 처리, 게임 진행처럼 비슷한 책임끼리 묶는다.

    # 상태 초기화 영역
    # 게임 상태를 초기화한다.
    def __init__(self):
        self.state_path = Path("state.json")
        self.quizzes = []
        self.best_score = None
        self.best_total_questions = None
        self.load_state()

    # 기본 데이터 준비 영역
    # 기본 퀴즈 목록을 만든다.
    def build_default_quizzes(self):
        return [Quiz.from_dict(item) for item in DEFAULT_QUIZ_DATA]

    # 파일 입출력 영역
    # 저장 파일에서 상태를 불러온다.
    def load_state(self):
        if not self.state_path.exists():
            self.quizzes = self.build_default_quizzes()
            self.best_score = None
            self.best_total_questions = None
            self.save_state()
            print("state.json 파일이 없어 기본 퀴즈 데이터로 시작합니다.")
            return

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("state.json 최상위 구조가 dict가 아닙니다.")

            quizzes_data = data.get("quizzes")
            best_score = data.get("best_score")
            best_total_questions = data.get("best_total_questions")

            if not isinstance(quizzes_data, list):
                raise ValueError("quizzes 값이 리스트가 아닙니다.")

            loaded_quizzes = [Quiz.from_dict(item) for item in quizzes_data]

            if best_score is not None and not isinstance(best_score, int):
                raise ValueError("best_score 값이 정수가 아닙니다.")

            if best_total_questions is not None and not isinstance(best_total_questions, int):
                raise ValueError("best_total_questions 값이 정수가 아닙니다.")

            self.quizzes = loaded_quizzes
            self.best_score = best_score
            self.best_total_questions = best_total_questions

            best_score_text = (
                "없음"
                if self.best_score is None
                else f"{self.best_score} / {self.best_total_questions}"
            )

            print(
                f"저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개, 최고 점수: {best_score_text})"
            )

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print("state.json 파일이 없거나 손상되어 기본 데이터로 복구합니다.")
            print(f"상세 원인: {error}")
            self.quizzes = self.build_default_quizzes()
            self.best_score = None
            self.best_total_questions = None
            self.save_state()

    # 현재 상태를 파일에 저장한다.
    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_total_questions": self.best_total_questions,
        }

        try:
            with self.state_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"state.json 저장 중 오류가 발생했습니다: {error}")

    # 입력 처리 영역
    # 저장 후 안전하게 종료한다.
    def safe_exit(self):
        print("\n입력이 중단되어 현재 상태를 저장한 뒤 안전하게 종료합니다.")
        self.save_state()
        raise SystemExit(0)

    # 빈 문자열이 아닌 입력만 받는다.
    def read_non_empty_text(self, prompt):
        while True:
            try:
                value = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                self.safe_exit()

            if value == "":
                print("빈 입력은 허용되지 않습니다. 다시 입력하세요.")
                continue

            return value

    # 범위 안의 정수만 받는다.
    def read_int_in_range(self, prompt, min_value, max_value):
        while True:
            try:
                raw = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                self.safe_exit()

            if raw == "":
                print("빈 입력은 허용되지 않습니다. 다시 입력하세요.")
                continue

            try:
                value = int(raw)
            except ValueError:
                print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if not (min_value <= value <= max_value):
                print(f"범위를 벗어났습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return value

    # 게임 진행 영역
    # 메인 메뉴를 출력한다.
    def show_menu(self):
        print()
        print("========================================")
        print("        나만의 퀴즈 게임")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

    # 퀴즈를 진행하고 점수를 계산한다.
    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        total = len(self.quizzes)

        print()
        print(f"퀴즈를 시작합니다. (총 {total}문제)")
        print()

        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.display(index)
            user_answer = self.read_int_in_range("정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_answer):
                print("정답입니다.")
                score += 1
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                print(f"오답입니다. 정답은 {quiz.answer}번: {correct_choice}")
            print()

        percentage = int((score / total) * 100)

        print("========================================")
        print(f"결과: {total}문제 중 {score}문제 정답! ({percentage}점)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_total_questions = total
            print("새로운 최고 점수입니다.")
        else:
            print("최고 점수는 유지되었습니다.")
        self.save_state()
        print("========================================")

    # 새 퀴즈를 추가한다.
    def add_quiz(self):
        print()
        print("새로운 퀴즈를 추가합니다.")

        question = self.read_non_empty_text("문제를 입력하세요: ")

        choices = []
        for index in range(1, 5):
            choice = self.read_non_empty_text(f"선택지 {index}: ")
            choices.append(choice)

        answer = self.read_int_in_range("정답 번호 (1-4): ", 1, 4)

        new_quiz = Quiz(question=question, choices=choices, answer=answer)
        self.quizzes.append(new_quiz)
        self.save_state()

        print("퀴즈가 추가되었습니다.")

    # 등록된 퀴즈 목록을 보여준다.
    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print()
        print(f"등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("----------------------------------------")

    # 현재 최고 점수를 보여준다.
    def show_best_score(self):
        if self.best_score is None or self.best_total_questions is None:
            print("아직 퀴즈를 풀지 않았습니다.")
            return

        percentage = int((self.best_score / self.best_total_questions) * 100)
        print(
            f"최고 점수: {percentage}점 "
            f"({self.best_total_questions}문제 중 {self.best_score}문제 정답)"
        )
