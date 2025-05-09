import importlib
import os
import sys
import time
import traceback

import requests
from grade import (
    AssignmentBase,
    By,
    Keys,
    Soup,
    StopGrading,
    children,
    make_chrome_driver,
    Py4web,
)

import re
from pydal import DAL, Field


def fetch(method, url, body=None):
    print(f"Trying {method} {body or ''} to {url} ...")
    if method == "GET":
        response = requests.get(url, allow_redirects=True)
    if method == "PUT":
        response = requests.put(url, json=body)
    if method == "POST":
        response = requests.post(url, json=body)
    if method == "DELETE":
        response = requests.delete(url)
    assert (
        response.status_code == 200
    ), f"Expected 200 OK but received {response.status_code}"
    try:
        json = response.json()
    except Exception:
        assert False, f"received:\n{repr(response.content)}\nand this is invalid JSON"
    print(f"JSON response {json}")
    return json


class Assignment(AssignmentBase, Py4web):
    def __init__(self, folder):
        AssignmentBase.__init__(self, folder, max_grade=12)
        self.start_server(folder + "/apps", "bird_spotter")
        self.browser = make_chrome_driver()

    def goto(self, url):
        print(f"Loading {url}")
        self.browser.get(url)
        self.browser.implicitly_wait(10)
        time.sleep(4)

    def find(self, css):
        print(f'Looking for "{css}" selector in page')
        element = self.browser.find_element(By.CSS_SELECTOR, css)
        assert element, "element not found"
        print("element found")
        return element

    def refresh(self):
        self.browser.refresh()
        self.browser.implicitly_wait(4)
        time.sleep(4)

    def step01(self):
        "it chould be made of valid HTML and CSS."
        print("Start grading index/html")
        self.goto(self.url)
        self.find(".logo")
        input = self.find("input")
        self.find("button")
        self.add_comment("Page loads correctly", 1.0)

    def step02(self):
        """Check model definition without full common.py execution"""
        models_path = os.path.join(self.apps_folder, "bird_spotter", "models.py")
        if not os.path.exists(models_path):
            raise AssertionError("models.py not found")
        sys.path.append(os.path.join(self.apps_folder))        
        env = {}
        try:
            exec("import bird_spotter.models as testmodule", env)
        except Exception:
            print(traceback.format_exc())
            raise AssertionError("unable to load bird_spotter/models.py")
        testmodule = env.get("testmodule")
        assert testmodule and hasattr(testmodule, "db"), "no db defined models.py"
        assert "bird" in testmodule.db.tables, "table bird not found in models.py"
        bird = testmodule.db["bird"]
        assert "name" in bird.fields, "Bird has no name field"
        assert "sightings" in bird.fields, "Bird has no sightings field"
        assert "habitat" in bird.fields, "Bird has no habitat field"
        assert "weight" in bird.fields, "Bird has no weight field"
        assert bird.name.type == "string", "db.bird.name is not a string"
        assert bird.sightings.type == "integer", "db.bird.sightings is not an integer"
        assert bird.habitat.type == "string", "db.bird.habitat is not a string"
        assert bird.weight.type == "float", "db.bird.weight is not a float"
        self.add_comment("Model defined correctly", 1.0)

    def step03(self):
        "Checking api"
        # self.url = "http://127.0.0.1:8000/bird_spotter/"
        self.url_birds = self.url + "api/birds"
        res = fetch("GET", self.url_birds)
        print("I got", res)
        assert res == {"birds": []}
        print("GET api seems to work but no data yet")
        print("adding a bird...")
        assert fetch("POST", self.url_birds, {"name": "pigeon"}) == {
            "id": 1,
            "errors": {},
        }
        res = fetch("GET", self.url_birds)
        expected = {
            "birds": [
                {"id": 1, "name": "pigeon", "habitat": "", "weight": 0, "sightings": 0}
            ]
        }
        assert res == expected, f"Expected this exact answer {expected}"
        self.add_comment("GET and POST API work", 2.0)

    def step04(self):
        "Checking api"
        assert fetch("POST", self.url_birds, {"name": "penguin"}) == {
            "id": 2,
            "errors": {},
        }
        for k in range(5):
            fetch("POST", self.url + "api/birds/1/increase_sightings")
        for k in range(2):
            fetch("POST", self.url + "api/birds/2/increase_sightings")
        assert fetch("GET", self.url_birds) == {
            "birds": [
                {
                    "id": 1,
                    "name": "pigeon",
                    "habitat": "",
                    "weight": 0.0,
                    "sightings": 5,
                },
                {
                    "id": 2,
                    "name": "penguin",
                    "habitat": "",
                    "weight": 0.0,
                    "sightings": 2,
                },
            ]
        }
        self.add_comment("increase_sightings API works", 1.0)

    def step05(self):
        "Checking api"
        res = fetch(
            "PUT", self.url + "api/birds/2", {"habitat": "south pole", "weight": 20.0}
        )
        assert res["updated"] and not res["errors"], "Invalid response"
        assert fetch("GET", self.url_birds) == {
            "birds": [
                {
                    "id": 1,
                    "name": "pigeon",
                    "habitat": "",
                    "weight": 0.0,
                    "sightings": 5,
                },
                {
                    "id": 2,
                    "name": "penguin",
                    "habitat": "south pole",
                    "weight": 20.0,
                    "sightings": 2,
                },
            ]
        }
        self.add_comment("PUT API works", 1.0)

    def step06(self):
        "Checking api"
        fetch("DELETE", self.url + "api/birds/2")
        fetch("GET", self.url_birds) == {
            "birds": [
                {
                    "id": 1,
                    "name": "pigeon",
                    "habitat": "",
                    "weight": 0.0,
                    "sightings": 5,
                }
            ]
        }
        self.add_comment("DELETE API works", 1.0)

    def step07(self):
        print(fetch("POST", self.url_birds, {"name": "seagull"}))
        self.refresh()
        print("HTML I see:")
        print(self.find("html").get_attribute("innerHTML"))
        titles = self.browser.find_elements(By.CLASS_NAME, "card-header-title")
        print("birds found in page", len(titles))
        assert any(
            "seagull" in t.text for t in titles
        ), "Store a seagull but page does not show it upon reloading"
        self.add_comment("page loads birds correctly", 0.5)

    def step08(self):
        inputs = self.browser.find_elements(By.TAG_NAME, "input")
        inputs[0].send_keys("albatross")
        time.sleep(1)
        buttons = self.browser.find_elements(By.TAG_NAME, "button")
        buttons[0].click()
        time.sleep(1)
        titles = self.browser.find_elements(By.CLASS_NAME, "card-header-title")
        assert any(
            "albatross" in t.text for t in titles
        ), "Store a seagull but page does not show it upon reloading"
        self.add_comment("page creates new bird correctly", 0.5)

    def step09(self):
        inputs = self.browser.find_elements(By.TAG_NAME, "input")
        inputs[0].send_keys("pigeon")
        birds = fetch("GET", self.url_birds).get("birds")
        print(birds)
        count1 = [bird["sightings"] for bird in birds if bird["name"] == "pigeon"][0]
        buttons = self.browser.find_elements(By.TAG_NAME, "button")
        buttons[0].click()
        time.sleep(5)
        birds = fetch("GET", self.url_birds).get("birds")
        print(birds)
        count2 = [bird["sightings"] for bird in birds if bird["name"] == "pigeon"][0]
        assert (
            count2 == count1 + 1
        ), "I clicked on the increasing sighting but count did not inrease"
        self.add_comment("page creates new bird correctly", 0.5)

    def step10(self):
        # select the bird
        inputs = self.browser.find_elements(By.TAG_NAME, "input")
        # click the edit button, 0 is the add sightings button
        buttons = self.browser.find_elements(By.TAG_NAME, "button")
        buttons[1].click()
        time.sleep(1)
        # fill the input fields
        inputs = self.browser.find_elements(By.TAG_NAME, "input")
        inputs[1].send_keys("city")
        inputs[2].send_keys("4")
        # click the save button, 0 is the add sightings button
        buttons = self.browser.find_elements(By.TAG_NAME, "button")
        buttons[1].click()
        time.sleep(5)
        # check the database using APIs
        birds = fetch("GET", self.url_birds).get("birds")
        print(birds)
        bird = [bird for bird in birds if bird["name"] == "pigeon"][0]
        assert bird["habitat"] == "city", "Unable to update bird info"
        self.add_comment("bird info updated successfully", 0.5)

    def step11(self):
        "it chould be made of valid HTML and CSS."
        print("step11")
        print("checking for input validations")
        res = fetch("POST", self.url_birds, {"name": "pigeon"})
        assert res["errors"], "Expected an error"
        res = fetch("PUT", self.url + "api/birds/1", {"weight": -1.0})
        assert res["errors"], "Expected an error"
        self.add_comment("Inputs validated correctly", 1)

    def step12(self):
        """Check for error display on invalid input using robust selectors (concise)"""
        print("step12: Checking UI error display")
        self.refresh()
        target_bird_name = "pigeon"
        time.sleep(2)

        try:
            pigeon_card_xpath = f"//div[contains(@class, 'card') and .//div[contains(@class, 'card-header-title') and normalize-space()='{target_bird_name}']]"
            pigeon_card = self.browser.find_element(By.XPATH, pigeon_card_xpath)
            print(f"Found card for '{target_bird_name}'")

            edit_button = pigeon_card.find_element(
                By.XPATH, ".//button[normalize-space()='Edit']"
            )
            edit_button.click()
            print("Clicked 'Edit'.")
            time.sleep(1)

            weight_input = pigeon_card.find_element(
                By.XPATH,
                ".//th[contains(text(), 'Weight')]/following-sibling::td/input",
            )
            weight_input.clear()
            weight_input.send_keys("-1")
            print("Entered '-1' in weight.")
            time.sleep(0.5)

            save_button = pigeon_card.find_element(
                By.XPATH, ".//button[normalize-space()='Save']"
            )
            save_button.click()
            print("Clicked 'Save'.")

            print("Waiting for potential error display...")
            time.sleep(5)

            error_element = pigeon_card.find_element(By.CSS_SELECTOR, ".errors")
            error_text = error_element.text
            print(f"Found error element with text: '{error_text}'")

            assert (
                "weight" in error_text.lower()
            ), f"Error div found, but does not contain 'weight'. Text: '{error_text}'"

            print("Correct error message containing 'weight' found.")
            self.add_comment("Correct error reporting", 2.0)

        except Exception as e:
            card_html = "Could not get card HTML."
            try:
                pigeon_card_element = self.browser.find_element(
                    By.XPATH, pigeon_card_xpath
                )
                card_html = pigeon_card_element.get_attribute("outerHTML")
            except:
                pass
            print("\n--- Pigeon Card HTML at time of error check ---")
            print(card_html)
            print("--- End Card HTML ---\n")
            assert (
                False
            ), f"Failed to find an expected element within the pigeon card ({e.msg})"
        except Exception as e:
            assert False, f"An unexpected error occurred during step 12: {e}"
