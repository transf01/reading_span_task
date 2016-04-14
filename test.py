from unittest import TestCase

from stimuli import Stimuli, Stimulus


class Test(TestCase):

    def test_create(self):
        stimuli = Stimuli()
        self.assertEqual(4, stimuli.get_category_count())

    def test_get_stimuli(self):
        stimuli = Stimuli()
        first = stimuli.get_trial_stimuli()
        self.assertEqual(12, len(first))

        second = stimuli.get_trial_stimuli()
        self.assertEqual(16, len(second))
        self.assertEqual(set(), set(first) & set(second))

        third = stimuli.get_trial_stimuli()
        self.assertEqual(20, len(third))
        self.assertEqual(set(), set(first) & set(third))
        self.assertEqual(set(), set(second) & set(third))

        fourth = stimuli.get_trial_stimuli()
        self.assertEqual(24, len(fourth))
        self.assertEqual(set(), set(first) & set(fourth))
        self.assertEqual(set(), set(second) & set(fourth))
        self.assertEqual(set(), set(third) & set(fourth))

        self.assertEqual(12, len(stimuli.get_trial_stimuli()))
        self.assertEqual(16, len(stimuli.get_trial_stimuli()))
        self.assertEqual(20, len(stimuli.get_trial_stimuli()))
        self.assertEqual(24, len(stimuli.get_trial_stimuli()))

        self.assertIsNone(stimuli.get_trial_stimuli())

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



