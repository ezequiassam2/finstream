from reader.item_reader import TxtReader, JsonReader


class ReportFactory:

    @staticmethod
    def get_reader(file_path: str, file_type: str) -> TxtReader | JsonReader:
        if file_type == 'txt':
            return TxtReader(file_path)
        elif file_type == 'json':
            return JsonReader(file_path)
        else:
            raise ValueError(f"Leitor não encontrado para o tipo de arquivo: {file_type}")
