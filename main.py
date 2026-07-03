import argparse

from app.services.challenge_runner import ChallengeRunner


def main():
    parser = argparse.ArgumentParser(description="Executar automação do desafio CDB")
    parser.add_argument(
        "--visible",
        action="store_true",
        help="Executar o navegador em modo visível (padrão é headless)",
    )
    args = parser.parse_args()

    runner = ChallengeRunner(headless=not args.visible)

    try:
        runner.execute()
    except Exception as exc:
        print(f"Erro: {exc}")
    finally:
        runner.close()


if __name__ == "__main__":
    main()