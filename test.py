import uuid
from datetime import datetime
from enum import Enum
from unittest import TestCase

from database import Database
from main import TrialHandler, SentenceHandler, WordHandler, BlockEndHandler, ExperimentEndHandler
from stimuli import Stimuli, Stimulus
from trial import Trial, Word, WordPosition


class ExperimentStatus(Enum):
    enter = 0
    sentence_intro = 1
    sentence = 2
    word_intro = 3
    word = 4
    block_end = 5
    experiment_end = 6

class Test(TestCase):

    def test_create(self):
        stimuli = Stimuli()
        self.assertEqual(4, stimuli.get_category_count())

    def check_trial_stimuli(self, kinds, stimuli, count):
        for kind in kinds:
            self.assertEqual(count, len(stimuli[kind]))

    def test_get_stimuli(self):
        stimuli = Stimuli()
        kinds = stimuli.get_shuffled_groups();

        for x in range(0, 2):
            for count in range(3, 7):
                self.check_trial_stimuli(kinds, stimuli.get_chunk(count), count)

    def test_get_sentence(self):
        stimuli = Stimuli()
        for sentence_number in range(3, 7):
            trial = Trial(stimuli.get_chunk(sentence_number), stimuli.get_shuffled_groups())
            for group in stimuli.get_shuffled_groups():
                sentences, words = trial.get_one_group_data_from_chunk()
                self.assertEqual(sentence_number, len(sentences))
                self.assertEqual(sentence_number*4, len(words))
            self.assertEqual((None, None), trial.get_one_group_data_from_chunk())

    def check_trial_update(self, text):
        if self.exp_state == ExperimentStatus.enter:
            self.assertEqual(text, SentenceHandler.intro)
        elif self.exp_state == ExperimentStatus.sentence_intro:
            self.assertEqual(self.chunk_count*4, self.word_count)
            self.assertEqual(text, SentenceHandler.intro)
        elif self.exp_state == ExperimentStatus.sentence:
            self.sentence_count += 1
        elif self.exp_state == ExperimentStatus.word_intro:
            self.assertEqual(text, WordHandler.intro)
            self.assertEqual(self.chunk_count, self.sentence_count)
        elif self.exp_state == ExperimentStatus.word:
            self.word_count +=1
        elif self.exp_state == ExperimentStatus.block_end:
            self.assertEqual(BlockEndHandler.intro, text)
        elif self.exp_state == ExperimentStatus.experiment_end:
            self.assertEqual(ExperimentEndHandler.intro, text)

    def trial_end_callback(self):
        self.traial_all_end = True

    def test_experiment(self):
        self.traial_all_end = False
        self.exp_state = ExperimentStatus.enter
        db = Database('test.db')
        db.clear()
        trial_handler = TrialHandler(db, self.check_trial_update, self.trial_end_callback)
        for block_count in range(0, 2):
            for self.chunk_count in range(3, 7):
                for group in range(0, 4):
                    self.sentence_count = 0
                    self.word_count = 0
                    self.exp_state = ExperimentStatus.sentence
                    for x in range(0, self.chunk_count):
                        trial_handler.handle_keyboard((32, 'spacebar'))
                    self.exp_state = ExperimentStatus.word_intro
                    trial_handler.handle_keyboard((32, 'spacebar'))
                    self.exp_state = ExperimentStatus.word
                    for x in range(0, self.chunk_count*4):
                        trial_handler.handle_keyboard((122, 'z'))
                    if self.chunk_count == 6 and group == 3:
                        if block_count == 1:
                            self.exp_state = ExperimentStatus.experiment_end
                        else:
                            self.exp_state = ExperimentStatus.block_end
                        trial_handler.handle_keyboard((32, 'spacebar'))
                    self.exp_state = ExperimentStatus.sentence_intro
                    trial_handler.handle_keyboard((32, 'spacebar'))
        self.assertTrue(self.traial_all_end)

    def test_stimulus_equality(self):
        a = Stimulus('oo', ['1', 'sentence', 'start', 'middle', 'end', 'non'])
        b = Stimulus('oo', ['2', 'sentence', 'start', 'middle', 'end', 'non'])

        c = Stimulus('oo', ['1', 'sentence', 'start', 'middle', 'end', 'non'])
        d = Stimulus('oo', ['3', 'sentence', 'start', 'middle', 'end', 'non'])

        self.assertEqual(a, c)
        self.assertNotEqual(a, b)

        list_a = [a, c]
        list_b = [c, d]

        print(set(list_a) & set(list_b))

    def test_inner_word_correct(self):
        word = Word('oo', '1', WordPosition.middle, 'test');
        word.set_response((47, '?'), 100)
        self.assertFalse(word.is_correct_response)
        word.set_response((122, 'z'), 100)
        self.assertTrue(word.is_correct_response)

    def test_non_word_correct(self):
        word = Word('oo', '1', WordPosition.none, 'test');
        word.set_response((47, '?'), 100)
        self.assertTrue(word.is_correct_response)
        word.set_response((122, 'z'), 100)
        self.assertFalse(word.is_correct_response)

    def test_if(self):
        a = None
        b = {}
        self.assertIsNone(a)
        self.assertIsNotNone(b)
        self.assertTrue(not b)

    def test_db(self):
        db = Database('test.db')
        db.add_user(uuid.uuid4(), '1234', '010-555-5555')
        word = Word('oo', '1', WordPosition.none, 'test')
        word.set_response((122, 'z'), 300)
        db.add_response(word)

