import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from processor.item_processor import ItemProcessor
from src.reader.item_reader import ItemReader
from writer.item_writer import ItemWriter


class BatchJob:
    def __init__(self):
        self.processor = ItemProcessor()
        self.writer = ItemWriter()

    def __process_content(self, content):
        processed = self.processor.process(content)
        if processed:
            self.writer.save(processed)

    def __run_step(self, file_path):
        reader = ItemReader(file_path)
        # for content in reader.read():
        #     self.__process_content(content)
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.__process_content, content) for content in reader.read()]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Erro ao processar conteúdo {e}")

    def run_job(self, files):
        # for file_path in files:
        #     self.__run_step(file_path)
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.__run_step, file_path)
                for file_path in files
            ]

            for future in as_completed(futures):
                try:
                    future.result()  # Captura e trata exceções de execução
                except Exception as e:
                    logging.error(f"Erro ao processar arquivo {e}")
