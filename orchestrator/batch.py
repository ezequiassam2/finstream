import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from core.utils.logger import get_logger
from core.utils.retry import retry
from etl.reader.file_reader import FileReader

logger = get_logger(__name__)


class BatchOrchestrator:
    def __init__(self, max_consumers: int = 1):
        self.max_consumers = max_consumers
        self.task_queue = Queue(maxsize=1000)  # Fila limitada para evitar estouro de memória
        self.file_reader = FileReader()
        self.strategies = {
            'txt': {'process': self._process_txt_segment, 'reader': self.file_reader.read_txt},
            'json': {'process': self._process_json_file, 'reader': self.file_reader.read_json}
        }

    def _get_strategy(self, file_path: str, run='process'):
        file_type = file_path.split('.')[-1].lower()
        return self.strategies.get(file_type).get(run)

    def _process_txt_segment(self, data, processor, writer, section_count):
        processed_data = processor.process_report(data, section_count)
        if processed_data:
            writer.save_report(processed_data)

    def _process_json_file(self, data, processor, writer, section_count):
        processed_data = processor.process_transaction(data, section_count)
        if processed_data:
            writer.save_transaction(processed_data)

    @retry(max_attempts=3, delay=1)
    def _consumer(self, processor, writer):
        while True:
            task = self.task_queue.get()
            if task is None:  # Sinal para encerrar
                self.task_queue.task_done()
                break
            file_path, data,  section_count = task
            try:
                strategy = self._get_strategy(file_path)
                strategy(data, processor, writer, section_count)
            except Exception as e:
                logger.error(f"Falha ao processar segmento {section_count} do arquivo {file_path}: {str(e)}")
            finally:
                self.task_queue.task_done()

    def _producer(self, files: list):
        for file_path in files:
            try:
                reader = self._get_strategy(file_path, 'reader')
                section_count = 0
                logger.info(f"Lendo arquivo: {file_path}")
                for data in reader(file_path):
                    section_count+=1
                    self.task_queue.put((file_path, data, section_count))
            except Exception as e:
                logger.error(f"Falha ao ler {file_path}: {str(e)}")

    def run(self, files: list, processor, writer):
        # Inicia consumidores
        with ThreadPoolExecutor(max_workers=self.max_consumers) as executor:
            consumers = [
                executor.submit(self._consumer, processor, writer)
                for _ in range(self.max_consumers)
            ]

            # Inicia produtor em thread separada
            producer_thread = threading.Thread(target=self._producer, args=(files,))
            producer_thread.start()
            producer_thread.join()  # Espera o produtor terminar

            # Sinaliza fim para consumidores
            for _ in range(self.max_consumers):
                self.task_queue.put(None)

            # Espera todos os consumidores finalizarem
            self.task_queue.join()
            for future in consumers:
                future.result()
