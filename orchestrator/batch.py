import datetime
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import List, Callable, Optional, Dict

from core.utils.logger import get_logger
from core.utils.retry import retry
from etl.processor.data_processor import DataProcessor
from etl.reader.file_reader import FileReader
from etl.writer.db_writer import DBWriter

logger = get_logger(__name__)

class BatchOrchestrator:
    """
    Orquestrador de processamento em lote com paralelismo por seção usando arquitetura produtor-consumidor.

    Atributos:
        max_consumers (int): Número máximo de threads para processamento paralelo.
        progress (dict): Monitora o progresso de processamento de cada arquivo.
        lock (threading.Lock): Garante acesso thread-safe aos atributos compartilhados.
        task_queue (Queue): Fila de tarefas para consumidores.
        file_reader (FileReader): Leitor de arquivos.
        done (threading.Event): Sinaliza cancelamento.
        start_time (float): Marca o início do processamento.
        strategies (dict): Mapeia com base nas extensões dos arquivos as funções de processamento e leitura.
    """

    def __init__(self, max_consumers: int = 4):
        self.max_consumers = max_consumers
        self.progress: Dict[str, Dict[str, int]] = {}
        self.lock = threading.Lock()
        self.task_queue = Queue()
        self.file_reader = FileReader()
        self.done = threading.Event()
        self.start_time: Optional[float] = None
        self.strategies = {
            'txt': {'process': self.__process_txt_segment, 'reader': self.file_reader.read_txt},
            'json': {'process': self.__process_json_file, 'reader': self.file_reader.read_json}
        }

    def __get_strategy(self, file_path: str, run: str = 'process') -> Optional[Callable]:
        """
        Obtém a estratégia de processamento com base na extensão do arquivo.
        """
        file_type = file_path.split('.')[-1].lower()
        strategy = self.strategies.get(file_type, {})
        if not strategy:
            raise ValueError(f"Estratégia não encontrada para o arquivo {file_path}")
        return strategy.get(run)

    def __update_progress(self, file_path: str, total=0) -> None:
        """Atualiza o progresso de processamento de um arquivo.."""
        with self.lock:
            if self.progress.get(file_path) is None:
                self.progress[file_path] = {'total': total, 'processed': 0}
                logger.info(f"Start Progresso {file_path.split('/')[-1]}: {0}/{total} ({0:.1f}%)")
            self.progress[file_path]['processed'] += 1

    def __log_progress(self) -> None:
        """Loga o progresso atual em intervalos regulares."""
        while not self.done.is_set():
            time.sleep(5)
            with self.lock:
                for file_path, stats in self.progress.items():
                    total = stats['total']
                    processed = stats['processed']
                    percent = (processed / total * 100) if total > 0 else 0
                    logger.info(f"Progresso {file_path.split('/')[-1]}: {processed}/{total} ({percent:.1f}%)")

    def __process_txt_segment(self, content: dict, processor: DataProcessor, writer: DBWriter) -> None:
        """
        Processa um segmento de arquivo TXT.
        """
        processed_data = processor.process_report(content)
        if processed_data:
            writer.save_report(processed_data)

    def __process_json_file(self, content: dict, processor: DataProcessor, writer: DBWriter) -> None:
        """
        Processa um segmento de arquivo JSON.
        """
        processed_data = processor.process_transaction(content)
        if processed_data:
            writer.save_transaction(processed_data)

    @retry(max_attempts=3, delay=1)
    def __consumer(self, processor: DataProcessor, writer: DBWriter) -> None:
        """
        Consome tarefas da fila e processa cada seção com a estratégia apropriada.
        """
        while True:
            task = self.task_queue.get()
            if task is None:
                self.task_queue.task_done()
                break
            file_path, content, section_id = task
            try:
                self.__update_progress(file_path, content.get('total', 0))
                process = self.__get_strategy(file_path)
                process(content, processor, writer)
            except Exception as e:
                if not self.task_queue.empty():
                    logger.error(f"Falha ao processar seção {section_id} do arquivo {file_path}: {str(e)}")
            finally:
                self.task_queue.task_done()

    def __producer(self, files: List[str]) -> None:
        """
        Lê arquivos e coloca os dados na fila para serem processados pelos consumidores.
        """
        for file_path in files:
            if self.done.is_set():
                logger.info(f"Fim da importação do arquivo: {file_path}")
                break
            try:
                reader = self.__get_strategy(file_path, 'reader')
                logger.info(f"Importando arquivo: {file_path}")
                for content in reader(file_path):
                    self.task_queue.put((file_path, content, content.get("section_id", 0)))
            except Exception as e:
                logger.error(f"Falha ao ler {file_path}: {str(e)}")
                self.done.set()

    def __run_report_update(self, processor: DataProcessor, writer: DBWriter) -> None:
        """
        Atualiza registros que tem a seção nula e classifica as transações.
        """
        try:
            logger.info(f"Atualizando seções nulas...")
            amounts = writer.get_amounts_with_null_section(datetime.datetime.fromtimestamp(self.start_time))
            for amount in amounts:
                report_current = amount.report
                report_old = writer.get_report(report_current.report_id, report_current.reporting_for,
                                               report_current.page - 1)
                section = processor.process_last_section(report_old)
                if section:
                    writer.update_section(amount.id, section)
            logger.info(f"Classificando transações...")
            writer.update_transaction_class()
        except Exception as e:
            logger.error(f"Falha ao atualizar seções: {str(e)}")

    def run(self, files: List[str], processor: DataProcessor, writer: DBWriter) -> None:
        """
        Inicia o processamento dos arquivos em lote.
        """
        self.start_time = time.time()
        progress_thread = threading.Thread(target=self.__log_progress)
        progress_thread.start()

        try:
            with ThreadPoolExecutor(max_workers=self.max_consumers) as executor:
                # Inicia consumidores
                consumers = [executor.submit(self.__consumer, processor, writer) for _ in range(self.max_consumers)]

                # Inicia produtor em thread separada
                producer_thread = threading.Thread(target=self.__producer, args=(files,))
                producer_thread.start()
                producer_thread.join()

                # Sinaliza fim para consumidores
                for _ in range(self.max_consumers):
                    self.task_queue.put(None)

                # Aguarda conclusão da fila
                self.task_queue.join()
                self.__run_report_update(processor, writer)
                self.done.set()
                for future in consumers:
                    future.result()
        except Exception as e:
            logger.error(f"Erro crítico: {str(e)}")
            self.done.set()
        finally:
            progress_thread.join()
            logger.info(f"Tempo total: {time.time() - self.start_time:.2f}s")
