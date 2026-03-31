from quiz_game import QuizGame


def main():
    game = QuizGame()
    while True:
        game.show_menu()
        choice = game.read_int_in_range("선택: ", 1, 5)

        if choice == 1:
            game.play_quiz()
        elif choice == 2:
            game.add_quiz()
        elif choice == 3:
            game.list_quizzes()
        elif choice == 4:
            game.show_best_score()
        elif choice == 5:
            game.save_state()
            print("게임을 종료합니다.")
            break


if __name__ == "__main__":
    main()
