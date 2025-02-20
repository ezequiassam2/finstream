import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import List, Callable, Any, Optional, Dict

from core.utils.logger import get_logger
from core.utils.retry import retry
from etl.reader.file_reader import FileReader

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
        self.progress: Dict[str, Dict[str, int]] = {}  # {file_path: {'total': X, 'processed': Y}}
        self.lock = threading.Lock()
        self.task_queue = Queue()
        self.file_reader = FileReader()
        self.done = threading.Event()
        self.start_time: Optional[float] = None
        self.strategies = {
            'txt': {'process': self._process_txt_segment, 'reader': self.file_reader.read_txt},
            'json': {'process': self._process_json_file, 'reader': self.file_reader.read_json}
        }

    def _get_strategy(self, file_path: str, run: str = 'process') -> Optional[Callable]:
        """
        Obtém a estratégia de processamento com base na extensão do arquivo.
        """
        file_type = file_path.split('.')[-1].lower()
        strategy = self.strategies.get(file_type, {})
        if not strategy:
            raise ValueError(f"Estratégia não encontrada para o arquivo {file_path}")
        return strategy.get(run)

    def _process_txt_segment(self, data: str, processor: Any, writer: Any, section_count: int) -> None:
        """
        Processa um segmento de arquivo txt.
        """
        processed_data = processor.process_report(data, section_count)
        if processed_data:
            writer.save_report(processed_data)

    def _process_json_file(self, data: dict, processor: Any, writer: Any, section_count: int) -> None:
        """
        Processa um segmento de arquivo json.
        """
        processed_data = processor.process_transaction(data, section_count)
        if processed_data:
            writer.save_transaction(processed_data)

    @retry(max_attempts=3, delay=1)
    def _consumer(self, processor: Any, writer: Any) -> None:
        """
        Consome tarefas da fila e processa cada uma com a estratégia apropriada.
        """
        while True:
            task = self.task_queue.get()
            if task is None:  # Sinal para encerrar
                self.task_queue.task_done()
                break
            file_path, data, section_count = task
            try:
                strategy = self._get_strategy(file_path)
                strategy(data, processor, writer, section_count)
            except Exception as e:
                logger.error(f"Falha ao processar segmento {section_count} do arquivo {file_path}: {str(e)}")
            finally:
                self.task_queue.task_done()

    def _producer(self, files: List[str]) -> None:
        """
        Lê arquivos e coloca os dados na fila para serem processados pelos consumidores.
        """
        for file_path in files:
            try:
                reader = self._get_strategy(file_path, 'reader')
                section_count = 0
                logger.info(f"Importando arquivo: {file_path}")
                for data in reader(file_path):
                    section_count += 1
                    self.task_queue.put((file_path, data, section_count))
                logger.info(f"Fim da importação do arquivo: {file_path}")
            except Exception as e:
                logger.error(f"Falha ao ler {file_path}: {str(e)}")

    def run(self, files: List[str], processor: Any, writer: Any) -> None:
        """
        Inicia o processamento dos arquivos.
        """
        # Inicia consumidores
        with ThreadPoolExecutor(max_workers=self.max_consumers) as executor:
            consumers = [executor.submit(self._consumer, processor, writer) for _ in range(self.max_consumers)]

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