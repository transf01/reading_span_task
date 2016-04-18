from random import shuffle


class Stimulus():
    def __init__(self, group, data):
        self.group = group;
        self.index = data[0]
        self.sentence = data[1]
        self.middle_word_1 = data[2]
        self.middle_word_2 = data[3]
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
        return 'type:'+self.group + ' index:' + self.index

    def __repr__(self):
        return self.__str__()


class Stimuli():
    def __init__(self, groups=None):
        self.raw_data = {}
        self.groups = groups
        if self.groups is None:
            self.groups = ['oo', 'os', 'ss', 'so']
        self.trial_index = 0
        self.sentence_count = 3
        for group in self.groups:
            self.raw_data[group] = self.create_raw_data_from_file(group)

    def get_shuffled_groups(self):
        shuffle(self.groups)
        return self.groups

    def create_raw_data_from_file(self, group):
        result = list()
        with open(group+ '.csv') as file:
            file.readline()
            data = file.readlines()
            for line in data:
                result.append(Stimulus(group, line.strip().split(",")))
        shuffle(result)
        return result

    def get_category_count(self):
        return len(self.groups)

    def get_chunk(self, count):
        trial_stimuli = {}

        for group in self.groups:
            if not self.raw_data[group]:
                return None

            stimuli = []
            for x in range(count):
                stimuli.append(self.raw_data[group].pop())
            trial_stimuli[group] = stimuli

        return trial_stimuli
