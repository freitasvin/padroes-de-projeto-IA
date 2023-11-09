from threading import Thread
from tqdm import tqdm
import pandas as pd

class Correcter:
    def __init__(self, corrections):
        self.corrections = corrections
    def correct(self, text):
        for incorrect, correct in self.corrections.items():
            text = text.replace(incorrect, correct)
        return text
corrections = {
    'primeirra': 'primeira',
    'testo': 'texto',
    'ero': 'erro',
    'assim': 'asim',
    'eh': 'é',
}

# Carregando o DataFrame a partir do arquivo CSV
df = pd.read_csv('teste.csv')

# Criando uma instância de Correcter
correcter = Correcter(corrections)

# Simple Factory Pattern
def create_thread(index, texts):
    return Thread(target=correct_and_save, args=(index, texts))

def correct_and_save(index, texts):
    corrected_texts = [correcter.correct(text) for text in tqdm(texts, disable=get_disable_strategy(index))]
    corrected_persuade_sample_df = pd.DataFrame({'corrected_text': corrected_texts})
    corrected_persuade_sample_df.to_csv(f'corrected_persuade_{index}.csv', index=False)

# Strategy Pattern
def get_disable_strategy(index):
    return True if index != 1 else False

num_threads = 4
text_per_thread = len(df['full_text']) // num_threads

# Criação de threads usando a fábrica
threads = [create_thread(i + 1, df['full_text'][i * text_per_thread:(i + 1) * text_per_thread]) for i in range(num_threads)]

# Inicialização e espera das threads
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
