from batch_orchestrator import BatchJob

def main():
    files_to_process = [
        '/Users/ezequias.ferreira/Projects/_opt.exec/finstream/data/raw/EP747/EP747_20240705.TXT',
        # Adicione mais arquivos conforme necessário
    ]

    # Cria uma instância do batch job
    batch_job = BatchJob()

    # Inicia o processamento
    batch_job.run_job(files_to_process)

if __name__ == "__main__":
    main()