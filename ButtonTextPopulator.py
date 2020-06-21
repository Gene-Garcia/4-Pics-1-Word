from random import shuffle
class ButtonPopulator:

    @staticmethod
    def populateButton(word):
        """
        :param: word is the current guess word
        :return: 1-D array, with a length of 12
        """
        maxButtons = 12
        buttonKeys = []

        for w in word.strip():
            buttonKeys.append(w.upper())

        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

        length = maxButtons - len(buttonKeys)

        for i in range(length):
            buttonKeys.append(alphabet[i])
        shuffle(buttonKeys)

        return buttonKeys
