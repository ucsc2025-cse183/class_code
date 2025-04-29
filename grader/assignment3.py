import os
import time

from grade import (
    AssignmentBase,
    By,
    Keys,
    Soup,
    StopGrading,
    children,
    make_chrome_driver,
)


class Assignment(AssignmentBase):
    def __init__(self, folder):
        AssignmentBase.__init__(self, folder, max_grade=12)
        self.browser = make_chrome_driver()

    def goto(self, url):
        self.browser.get(url)

        self.browser.implicitly_wait(10)

    def refresh(self):
        self.browser.refresh()

        time.sleep(0.5)
        self.browser.implicitly_wait(4)

    def step01(self):
        "it chould be made of valid HTML and CSS."
        print("Start grading index/html")
        self.goto("file://" + os.path.join(self.folder, "index.html"))
        print("loading index.html")
        assert self.browser.find_element(By.TAG_NAME, "html")
        print("loading index.html ... success")
        self.add_comment("HTML is valid", 1)

    def step02(self):
        "it should use vue.js"
        scripts = self.browser.find_elements(By.TAG_NAME, "script")
        assert len(scripts) == 2, "The code should load two scripts"

        vue_found = any(
            "vue" in s.get_attribute("src").lower()
            for s in scripts
            if s.get_attribute("src")
        )
        assert vue_found, "Did not find vue script being loaded"
        self.add_comment("Code uses vue.js correcly", 1)

    def step03(self):
        "the UI of the game should consists of 9 cells organized in 3 rows of 3 columns each."
        self.cells = []

        time.sleep(0.2)
        table = self.browser.find_element(By.TAG_NAME, "table")
        assert table, "table not found"
        rows = table.find_elements(By.TAG_NAME, "tr")
        assert len(rows) == 3, f"found {len(rows)} rows, expected 3"
        for k, row in enumerate(rows):
            cols = row.find_elements(By.TAG_NAME, "td")
            self.cells.append(cols)
            assert len(cols) == 3, f"row {k+1} contains {len(cols)} cols, expected 3"
        self.add_comment("Table found with 3x3 cells", 1)

    def step04(self):
        "each cell chould contain a button of class `cell-i-j` where i,j is the cell index"
        self.button_elements = {}
        for i in range(3):
            for j in range(3):
                cell = self.cells[i][j]
                name = f"cell-{i}-{j}"
                try:

                    button = cell.find_element(By.TAG_NAME, "button")
                    self.button_elements[i, j] = button
                except Exception:
                    assert False, f"button not found in tr {i} td {j}"
                classes = button.get_attribute("class").split()
                assert (
                    name in classes
                ), f"button in tr {i} td {j} does not have class {name}. Classes found: {classes}"
        self.add_comment("All buttons found and named correcly", 1)

    def get_buttons(self):

        buttons = {}
        for i in range(3):
            for j in range(3):

                selector = f"button.cell-{i}-{j}"
                try:
                    buttons[i, j] = self.browser.find_element(By.CSS_SELECTOR, selector)
                except Exception as e:
                    print(f"Error finding button {selector}: {e}")

                    try:
                        table = self.browser.find_element(By.TAG_NAME, "table")
                        buttons[i, j] = table.find_element(By.CSS_SELECTOR, selector)
                    except Exception as e2:
                        assert (
                            False
                        ), f"Failed to find button {selector} even within table: {e2}"

        return buttons

    def step05(self):
        "each button should display the state of the correspoding cell '', 'X' or 'O'"
        for i in range(3):
            for j in range(3):
                self.refresh()
                buttons = self.get_buttons()
                button_to_click = buttons[i, j]

                assert (
                    button_to_click.is_enabled()
                ), f"Button {i},{j} is not enabled initially"
                button_to_click.click()
                time.sleep(0.3)

                clicked_button_text = self.browser.find_element(
                    By.CSS_SELECTOR, f".cell-{i}-{j}"
                ).text.strip()
                assert (
                    clicked_button_text == "X"
                ), f"Clicked on {i},{j}, expected 'X', but found '{clicked_button_text}'"

                buttons_after_move = self.get_buttons()
                for (r, c), btn in buttons_after_move.items():
                    text = btn.text.strip()
                    assert text in [
                        "",
                        "X",
                        "O",
                    ], f"Found invalid text '{text}' in button {r},{c}"
        self.add_comment("All buttons display correct symbols after clicks", 1)

    def show(self, buttons):

        board = ""
        for i in range(3):

            row_text = []
            for j in range(3):

                try:
                    btn_text = self.browser.find_element(
                        By.CSS_SELECTOR, f".cell-{i}-{j}"
                    ).text.strip()
                    row_text.append(btn_text or " ")
                except:
                    row_text.append("?")

            board += "[" + "".join(row_text) + "]\n"
        print(board, end="")

    def step06(self):
        "users can only play empty cells and computers will play immediately after the user."
        for i in range(3):
            for j in range(3):
                print("playing:", i, j)
                self.refresh()
                buttons = self.get_buttons()
                buttons[i, j].click()
                time.sleep(0.3)
                self.show(buttons)

                buttons_after_move = self.get_buttons()
                o_found = False
                for (r, c), button in buttons_after_move.items():
                    if button.text.strip() == "O":
                        o_found = True

                        is_disabled = button.get_attribute("disabled") is not None
                        if not is_disabled:

                            print(f"Trying to click O at {r},{c}")
                            try:
                                button.click()

                                time.sleep(0.1)
                                button_after_click = self.browser.find_element(
                                    By.CSS_SELECTOR, f".cell-{r}-{c}"
                                )
                                assert (
                                    button_after_click.text.strip() == "O"
                                ), f"Allowed overriding 'O' at {r},{c}. Text became '{button_after_click.text.strip()}'"
                            except Exception as e:

                                print(
                                    f"Correctly could not click 'O' button {r},{c} (or button state changed): {e}"
                                )
                                pass
                        else:
                            print(f"Button O at {r},{c} is correctly disabled.")
                        break

                if not o_found:
                    print("No 'O' found to test overriding.")

                buttons_after_move = self.get_buttons()
                x_button = buttons_after_move[i, j]
                is_disabled = x_button.get_attribute("disabled") is not None
                if not is_disabled:
                    print(f"Trying to click X at {i},{j}")
                    try:
                        x_button.click()
                        time.sleep(0.1)
                        button_after_click = self.browser.find_element(
                            By.CSS_SELECTOR, f".cell-{i}-{j}"
                        )
                        assert (
                            button_after_click.text.strip() == "X"
                        ), f"Allowed overriding 'X' at {i},{j}. Text became '{button_after_click.text.strip()}'"
                    except Exception as e:
                        print(
                            f"Correctly could not click 'X' button {i},{j} (or button state changed): {e}"
                        )
                        pass
                else:
                    print(f"Button X at {i},{j} is correctly disabled.")

        self.add_comment("Buttons disable correctly, cannot override moves", 3)

    def winner(self, buttons_dict):

        board_state = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                try:

                    button_element = self.browser.find_element(
                        By.CSS_SELECTOR, f".cell-{i}-{j}"
                    )
                    board_state[i][j] = button_element.text.strip()
                except Exception as e:
                    print(
                        f"Warning: Could not read button {i}-{j} in winner check: {e}"
                    )

                    board_state[i][j] = ""

        for player in "XO":

            for i in range(3):
                if all(board_state[i][j] == player for j in range(3)):
                    return player

            for j in range(3):
                if all(board_state[i][j] == player for i in range(3)):
                    return player

            if all(board_state[i][i] == player for i in range(3)):
                return player
            if all(board_state[i][2 - i] == player for i in range(3)):
                return player
        return None

    def step07(self):
        "the computer should never lose"

        MAX_WAIT_SECONDS = 2

        for game in range(3):
            print(f"\n--- Starting Game {game+1} ---")
            self.refresh()
            buttons = self.get_buttons()

            print("Grader plays X at (1, 1)")
            buttons[1, 1].click()

            start_time = time.time()
            while time.time() - start_time < MAX_WAIT_SECONDS:
                current_buttons = self.get_buttons()
                x_count = sum(
                    btn.text.strip() == "X" for btn in current_buttons.values()
                )
                o_count = sum(
                    btn.text.strip() == "O" for btn in current_buttons.values()
                )
                if x_count >= 1 and o_count >= 1:
                    print("X and O detected after initial move.")
                    break
                time.sleep(0.1)
            else:
                self.show(self.get_buttons())
                assert (
                    False
                ), f"Timeout: Did not find X and O after initial move in game {game+1}"

            self.show(self.get_buttons())

            for k in range(4):
                print(f"\nTurn {k+1} (X's move)")
                current_buttons = self.get_buttons()

                xos = sum(btn.text.strip() == "X" for btn in current_buttons.values())
                oos = sum(btn.text.strip() == "O" for btn in current_buttons.values())
                print(
                    f"State before X moves: X={xos}, O={oos}. Expecting X={k+1}, O={k+1}"
                )

                assert (
                    xos == k + 1
                ), f"Incorrect number of X's before player move {k+1}. Found {xos}, expected {k+1}"

                assert (
                    oos == k + 1
                ), f"Incorrect number of O's before player move {k+1}. Found {oos}, expected {k+1}"

                played_move = False
                for i in range(3):
                    for j in range(3):
                        button = current_buttons.get((i, j))
                        if button and not button.text.strip() and button.is_enabled():
                            print(f"Grader plays X at ({i}, {j})")
                            button.click()
                            played_move = True
                            break
                    if played_move:
                        break

                if not played_move:
                    print("No empty cells left for X - Draw or game ended.")
                    break

                expected_x = k + 2
                expected_o = k + 2

                start_time = time.time()
                final_state_reached = False
                while time.time() - start_time < MAX_WAIT_SECONDS:
                    current_buttons_after = self.get_buttons()
                    x_count_after = sum(
                        btn.text.strip() == "X"
                        for btn in current_buttons_after.values()
                    )
                    o_count_after = sum(
                        btn.text.strip() == "O"
                        for btn in current_buttons_after.values()
                    )
                    current_winner = self.winner(current_buttons_after)

                    if current_winner:
                        print(f"Winner detected: {current_winner}")
                        final_state_reached = True
                        break

                    is_full = all(
                        btn.text.strip() != "" for btn in current_buttons_after.values()
                    )
                    if is_full:
                        print("Board full detected.")
                        final_state_reached = True
                        break

                    if x_count_after == expected_x and o_count_after == expected_o:
                        print(
                            f"X={x_count_after}, O={o_count_after} detected after computer's move."
                        )
                        final_state_reached = True
                        break

                    time.sleep(0.1)

                self.show(self.get_buttons())

                if not final_state_reached:

                    print(
                        f"Warning: Final state (X={expected_x}, O={expected_o} or Win/Draw) not reached within {MAX_WAIT_SECONDS}s."
                    )

                final_winner = self.winner(self.get_buttons())
                assert (
                    not final_winner or final_winner == "O"
                ), f"Ouch! Computer lost. Winner: {final_winner}"
                if final_winner:
                    print(f"Game {game+1} ended. Winner: {final_winner}")
                    break

                if (
                    final_state_reached
                    and not final_winner
                    and all(
                        btn.text.strip() != "" for btn in self.get_buttons().values()
                    )
                ):
                    print(f"Game {game+1} ended. Result: Draw")
                    break

            final_winner_end_game = self.winner(self.get_buttons())
            assert (
                not final_winner_end_game or final_winner_end_game == "O"
            ), f"Ouch! Computer lost at end of Game {game+1}. Winner: {final_winner_end_game}"
            print(f"--- Game {game+1} Finished ---")

        self.add_comment("Computer never lost in tested games", 2)

    def step08(self):
        "there should be a button of class reset that when clicked, resets the game"
        self.refresh()
        buttons = self.get_buttons()
        buttons[0, 0].click()
        time.sleep(0.3)

        #try:
        reset = self.browser.find_element(By.CSS_SELECTOR, ".reset")
        #except:
        #    assert False, "Reset button with class 'reset' not found"

        assert (
            reset.is_displayed() and reset.is_enabled()
        ), "Reset button is not visible or not enabled"
        reset.click()
        time.sleep(0.3)

        buttons_after_reset = self.get_buttons()
        is_empty = all(b.text.strip() == "" for b in buttons_after_reset.values())
        assert is_empty, "Board cells were not empty after reset"

        all_enabled = all(b.is_enabled() for b in buttons_after_reset.values())
        assert all_enabled, "Buttons were not all enabled after reset"

        self.add_comment("Successful reset button", 2)
