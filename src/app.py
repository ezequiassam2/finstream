import logging

logging.basicConfig(level=logging.INFO)

def main():
    reader = ItemReader('ep747_resum.txt')
    processor = ItemProcessor()
    writer = ItemWriter('sqlite:///banco_dados.db')

    sections = reader.read_sections()
    for section in sections:
        df = processor.process(section)
        writer.write(df)

if __name__ == "__main__":
    main()
