from random import shuffle


class Stimulus():
    def __init__(self, kind, data):
        self.type = kind;
        self.index = data[0]
        self.sentence = data[1]
        self.start_word = data[2]
        self.middle_word = data[3]
        self.end_word = data[4]
        self.not_in_word = data[5]

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(repr(self))

    def __str__(self):
        return 'type:'+self.type+' index:'+self.index

    def __repr__(self):
        return self.__str__()


class Stimuli():
    def __init__(self):
        self.stimuli = {}
        self.kinds = ['oo', 'os', 'ss', 'so']
        self.trial_index = 0
        self.sentence_count = 3
        for type in self.kinds:
            self.stimuli[type] = self.create_stimuli_from_file(type)

    def create_stimuli_from_file(self, kind):
        result = list()
        with open(kind+ '.csv') as file:
            file.readline()
            data = file.readlines()
            for line in data:
                result.append(Stimulus(kind, line.strip().split(",")))
        shuffle(result)
        return result

    def get_category_count(self):
        return len(self.kinds)

    def set_next_trial(self):
        self.trial_index += 1;
        self.sentence_count += 1;

        if self.sentence_count == 7:
            self.sentence_count = 3

    def get_trial_stimuli(self):
        stimuli = list()
        for kind in self.kinds:
            if not self.stimuli[kind]:
                return None
            for x in range(self.sentence_count):
                stimuli.append(self.stimuli[kind].pop())
        self.set_next_trial()
        return stimuli
