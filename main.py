import time
import datetime
import csv
import pickle
from json import JSONDecodeError
from dataclasses import dataclass
from tqdm import tqdm
from configuration import OpenAIConfiguration
from postprocessor import Postprocessor
from prompter import OpenAIPrompter
from templates import OPENAI_MESSAGES, OPENAI_MASK


@dataclass
class Phrases:
    original: str
    rephrases: set[str]

    def get_rephrases(self) -> list[list[str]]:
        return [[self.original, rephrase] for rephrase in self.rephrases]


def rephrase(phrase: str) -> set[str] | None:
    try:
        response = prompter.prompt(OPENAI_MESSAGES, OPENAI_MASK, phrase)
        return Postprocessor.clean_list(response)
    except JSONDecodeError:
        return None


if __name__ == '__main__':

    config = OpenAIConfiguration()
    config.load("/Users/nahumkorda/code/resources/pwiz/openai_config.yml")

    prompter = OpenAIPrompter(config)

    start = time.time()

    output_for_pickling = list()
    output_for_csv = list()
    with open("/Users/nahumkorda/code/resources/pwiz/test.txt", "r") as input_file:
        lines = input_file.readlines()
        for i, line in tqdm(enumerate(lines), total=len(lines)):
            line = line.strip()
            phrases = rephrase(line)
            if phrases is not None:
                rephrases = Phrases(original=line, rephrases=phrases)
                output_for_pickling.append(rephrases)
                output_for_csv.extend(rephrases.get_rephrases())

    end = time.time()
    diff = end - start
    print("Augmentation completed in " + str(datetime.timedelta(seconds=diff)))
    print(f"Total {len(output_for_pickling)} original phrases resulting in {len(output_for_csv)} data points.")

    with open("/Users/nahumkorda/code/resources/pwiz/positive_train_data.pkl", "wb") as output_file:
        pickle.dump(output_for_pickling, output_file)

    with open ("/Users/nahumkorda/code/resources/pwiz/positive_train_data.csv", "w", newline='') as output_file:
        write = csv.writer(output_file)
        write.writerows(output_for_csv)

