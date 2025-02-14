from batch_orchestrator import BatchJob

def main():
    files_to_process = [
        'path/to/file1.txt',
        'path/to/file2.txt'
        # Adicione mais arquivos conforme necessário
    ]

    # Cria uma instância do batch job
    batch_job = BatchJob('/Users/ezequias.ferreira/Projects/_opt.exec/finstream/data/raw/EP747/EP747_20240705.TXT')

    # Inicia o processamento
    batch_job.run_job()

if __name__ == "__main__":
    main()
