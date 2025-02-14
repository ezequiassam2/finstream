from concurrent.futures import ThreadPoolExecutor

from factory.report_factory import ReportFactory
from processor.item_processor import ItemProcessor
from writer.item_writer import ItemWriter


class BatchJob:
    def __init__(self, file_path, file_type='txt'):
        self.file_path = file_path
        self.reader = ReportFactory.get_reader(file_path, file_type)
        self.processor = ItemProcessor()
        self.writer = ItemWriter()

    def run_step(self):
        # Leitura, Processamento e Escrita
        for content in self.reader.read():
            processed = self.processor.process(content)
            if processed:
                self.writer.write(processed)

    def run_job(self):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self.run_step)
            try:
                future.result()
            except Exception as e:
                print(f"Erro ao processar arquivo: {e}")
