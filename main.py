import flet as ft
import time
import threading

def main(page: ft.Page):
    page.title = "Click the Button Game"
    page.window_width = 400
    page.window_height = 300

    score = ft.Text(value="Score: 0", size=30)
    timer = ft.Text(value="Time left: 10", size=20)
    click_button = ft.ElevatedButton(text="CLICK ME!", on_click=lambda e: increase_score())
    click_button.disabled = True

    countdown = 10
    current_score = 0

    def increase_score():
        nonlocal current_score
        current_score += 1
        score.value = f"Score: {current_score}"
        page.update()

    def start_game(e):
        nonlocal countdown, current_score
        countdown = 10
        current_score = 0
        score.value = "Score: 0"
        click_button.disabled = False
        page.update()

        def run_timer():
            nonlocal countdown
            while countdown > 0:
                timer.value = f"Time left: {countdown}"
                page.update()
                time.sleep(1)
                countdown -= 1
            timer.value = "Time's up!"
            click_button.disabled = True
            page.update()

        threading.Thread(target=run_timer).start()

    start_button = ft.ElevatedButton(text="Start Game", on_click=start_game)

    page.add(
        ft.Column(
            controls=[score, timer, click_button, start_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
