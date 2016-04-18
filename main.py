# coding: utf-8
import uuid
from datetime import datetime
from enum import Enum

from django.forms import TextInput
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

from database import Database
from stimuli import Stimuli
from trial import Trial, WordPosition
import os


class TestExperimentEndHandler():
    intro = '연습이 모두 종료되었습니다.\n\n\n' \
            '스페이스바를 누르면 본 실험이 시작됩니다'

    def __init__(self, update, end_callback):
        update(TestExperimentEndHandler.intro)
        self.end_callback = end_callback

    def handle_keyboard(self, keycode):
        if keycode[1] is not 'spacebar':
            return
        self.end_callback()

class ExperimentEndHandler():
    intro = "모든 실험이 종료되었습니다"

    def __init__(self, update, end_callback):
        self.end_callback = end_callback
        update(ExperimentEndHandler.intro)

    def handle_keyboard(self, keycode):
        print("---end---")
        self.end_callback()


class BlockEndHandler():
    intro = "2분 휴식후 다시 시작해 주세요"
    def __init__(self, update, end_callback):
        update(BlockEndHandler.intro)
        self.end_callback = end_callback

    def handle_keyboard(self, keycode):
        self.end_callback()


class SentenceHandler():
    intro = "화면에 나오는 문장을 모두 소리내어 읽으세요. \n\n\n" \
            "다 읽고 스페이스바를 누르면 새로운 문장이 나옵니다"

    def __init__(self, sentences, update, end_callback):
        self.sentences = sentences
        self.update = update
        self.update(SentenceHandler.intro)
        self.end_callback = end_callback

    def handle_keyboard(self, keycode):
        if not self.sentences:
            self.end_callback()
            return

        if keycode[1] is not 'spacebar':
            return

        self.update(self.sentences.pop())


class WordHandler():
    intro = "단어가 하나씩 화면에 나옵니다.\n\n\n" \
            "방금 읽은 문장들 속에 있었던 단어라면 'Z'를, 없었다면 '/'를 빠르게 눌러 주세요.\n\n\n" \
            "준비되었으면 'Z'나 '/'중의 하나를 눌러 주세요"

    def __init__(self, words, update, end_callback, db):
        self.words = words
        self.update = update
        self.update(WordHandler.intro)
        self.end_callback = end_callback
        self.current_word = None
        self.update_time = None
        self.db = db

    def handle_keyboard(self, keycode):

        #122:z    47:/
        if keycode[0] is not 122 and keycode[0] is not 47:
            return

        if self.current_word is not None:
            dt = round((datetime.now() - self.update_time).total_seconds() * 1000.0)
            self.current_word.set_response(keycode, dt)
            if self.db is not None:
                self.db.add_response(self.current_word)

        if not self.words:
            self.end_callback()
            return

        self.current_word = self.words.pop()
        self.update(self.current_word.text)
        self.update_time = datetime.now()


class TrialHandler():
    def __init__(self, db, update, end_callback, groups=None):
        self.db = db
        self.stimuli = Stimuli(groups)
        self.update = update
        self.sentence_count = 3
        self.trial = Trial(self.stimuli.get_chunk(self.sentence_count), self.stimuli.get_shuffled_groups())
        self.start_sentence_task()
        self.end_callback = end_callback

    def handle_keyboard(self, keycode):
        self.current_handler.handle_keyboard(keycode)

    def start_sentence_task(self):
        self.sentences, self.words = self.trial.get_one_group_data_from_chunk()
        self.current_handler = SentenceHandler(self.sentences, self.update, self.start_word_task)

    def start_word_task(self):
        self.current_handler = WordHandler(self.words, self.update, self.next_task, self.db)

    def next_task(self):
        if self.trial.is_end():
            if self.sentence_count == 6:
                self.sentence_count = 3
                chunk = self.stimuli.get_chunk(self.sentence_count)
                if chunk is None:
                    self.current_handler = ExperimentEndHandler(self.update, self.end_callback)
                    return
                else:
                    self.current_handler = BlockEndHandler(self.update, self.start_sentence_task)
                self.trial = Trial(chunk, self.stimuli.get_shuffled_groups())
                return
            else:
                self.sentence_count += 1
                self.trial = Trial(self.stimuli.get_chunk(self.sentence_count), self.stimuli.get_shuffled_groups())
        self.start_sentence_task()


class TestTrialHandler(TrialHandler):
    def __init__(self, update, end_callback):
        self.groups= ['test']
        self.end_callback = end_callback
        super(TestTrialHandler, self).__init__(None, update, end_callback, self.groups)

    def next_task(self):
        chunk = self.stimuli.get_chunk(self.sentence_count)
        if chunk is None:
            self.current_handler = TestExperimentEndHandler(self.update, self.end_callback)
            return
        self.trial = Trial(chunk, self.groups)
        self.start_sentence_task()


class KeyLabel(Label):
    def __init__(self, db, **kwargs):
        super(KeyLabel, self).__init__(**kwargs)
        self.db = db
        self.trial_handler = TestTrialHandler(self.update, self.end_test_trial)

    def bind_keyboard(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.trial_handler.handle_keyboard(keycode)

    def update(self, text):
        self.text = text

    def end_test_trial(self):
        self.trial_handler = TrialHandler(self.db, self.update, self.end_all_trial)

    def end_all_trial(self):
        pass


class SignInPopup(Popup):
    pass


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.db = Database()

    def build(self):
        self.label = KeyLabel(self.db)
        return self.label

    def on_start(self):
        super(TestApp, self).on_start()
        popup = SignInPopup(title='이름과 연락처를 입력해주세요')
        popup.bind(on_dismiss=self.popup_dismiss)
        popup.open()

    def popup_dismiss(self, instance):
        self.label.bind_keyboard()
        print (instance.user_number.text, instance.user_phone.text)
        self.db.add_user(uuid.uuid4(), instance.user_number.text, instance.user_phone.text)

if __name__ == "__main__":
    TestApp().run()
