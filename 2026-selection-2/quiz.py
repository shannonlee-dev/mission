class Quiz:
    # 기능 구분 기준: 퀴즈 1개의 데이터와 동작만 맡는다.

    # 상태 보관 영역
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    # 출력 영역
    def display(self, index):
        print("----------------------------------------")
        print(f"[문제 {index}]")
        print(self.question)
        print()

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

        print()

    # 정답 판별 영역
    def is_correct(self, user_answer):
        return user_answer == self.answer

    # 저장 변환 영역
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    # 복원 변환 영역
    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )
