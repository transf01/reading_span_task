from enum import Enum


class WordPosition(Enum):
    middle = 1
    end = 2
    none = 3


class Word:
    def __init__(self, group, index, position, word):
        self.group = group
        self.index = index
        self.position = position
        self.text = word
        self.rt = 0
        self.is_correct_response = None

    #122:z    47:/
    def set_response(self, keycode, rt):
        is_correct = False
        if self.position == WordPosition.none:
            if keycode[0] == 47:
                is_correct = True
        else :
            if keycode[0] == 122:
                is_correct = True
        self.is_correct_response = is_correct
        self.rt = rt

class Trial:
    def __init__(self, chunk, groups):
        self.chunk = chunk
        self.groups = list(groups)

    def is_end(self):
        if not self.groups:
            return True
        return False

    def get_one_group_data_from_chunk(self):
        if self.is_end():
            return None,None

        group = self.groups.pop()
        sentences = list()
        words = list()
        for stimulus in self.chunk[group]:
            sentences.append(stimulus.sentence)
            words.append(Word(group, stimulus.index, WordPosition.middle, stimulus.middle_word_1))
            words.append(Word(group, stimulus.index, WordPosition.middle, stimulus.middle_word_2))
            words.append(Word(group, stimulus.index, WordPosition.end, stimulus.end_word))
            words.append(Word(group, stimulus.index, WordPosition.none, stimulus.not_in_word))
        return sentences, words