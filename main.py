import os

from dotenv import load_dotenv

from core.utils.logger import get_logger
from etl.processor.data_processor import DataProcessor
from etl.writer.db_writer import DBWriter
from orchestrator.batch import BatchOrchestrator

load_dotenv()
logger = get_logger(__name__)

def main():
    processor = DataProcessor()
    writer = DBWriter(os.environ.get('DATABASE_URL'))
    orchestrator = BatchOrchestrator()

    base_dir = os.path.dirname(__file__)
    relative_path = "data/raw/EP747/EP747_20240705.TXT"
    file_path = os.path.join(base_dir, relative_path)

    files = [file_path]
    # files = [os.path.join(base_dir, "data/raw/EP747/VSS-600/VSS-600.TXT")]
    # files = [os.path.join(base_dir, "data/raw/VISA_CLEARING/VISA_TRANSACTIONAL_CLEARING_20240705_01.json")]
    orchestrator.run(files, processor, writer)

if __name__ == "__main__":
    main()
