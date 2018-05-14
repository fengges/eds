import jieba

class JiebaUtil:
    def __init__(self):
        self.stopwords = [line.strip() for line in open('data/StopWords.txt', encoding='utf-8').readlines()]
        self.fill = ['v', 'vd', 'vn', 'vf ', 'vx ', 'vi', 'vl', 'vg', 'n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf',
                'nt', 'nz', 'nl', 'ng','eng']
        # jieba.load_userdict('algorithm/userdict.txt')
        self.pseg=jieba.posseg

    def cut(self,s):
        seg_list = self.pseg.cut(s)
        words = []
        for word, flag in seg_list:
            if flag in self.fill and word not in self.stopwords:
                words.append(word)
        return words

jeibaUitl=JiebaUtil()