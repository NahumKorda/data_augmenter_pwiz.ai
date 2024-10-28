class Postprocessor:

    @classmethod
    def clean_csv(cls, text: str) -> str:
        text = text.strip()
        if text.startswith("```csv"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.replace("\"", "").strip()
        return text

    @classmethod
    def clean_list(cls, text: str) -> set[str]:
        retval = set()
        for phrase in text.split("\n"):
            phrase = phrase.strip()
            if phrase.startswith("-"):
                phrase = phrase[1:].strip()
            retval.add(phrase)
        return retval
