class ParagraphStore:
    def __init__(self, paragraph_id) -> None:
        self.id = paragraph_id
        self.sentences = []
    def add_sentence(self, sentence):
        self.sentences.append(sentence)

class EmbeddingMatch:
    def __init__(self, document_id) -> None:
        # an id can be tosl-2022-77031_39_9
        # convert it to tosl-2022-77031 (as 39 is the paragraph and 9 is the sentence)
        self.id = document_id.split("_")[0]
        self.paragraphs = {}
    
    def add_paragraph(self, paragraph_number):
        paragraph = ParagraphStore(paragraph_number)
        self.paragraphs[paragraph_number] = paragraph

    def add_to_paragraph(self, paragraph_number, sentence_number, score, text, related=False):
        if paragraph_number not in self.paragraphs:
            self.add_paragraph(paragraph_number)
        paragraph = self.paragraphs[paragraph_number]
        # check if text has already been added to the paragraph
        if text not in [s["text"] for s in paragraph.sentences]:
            paragraph.add_sentence({"id": sentence_number, "score": score, "text": text, "is_related": related})

    def add_paragraphs_and_sentences(self, paras, sents, score, text, related=False):
        for p in paras:
            for s in sents:
                self.add_to_paragraph(p, s, score, text, related)
