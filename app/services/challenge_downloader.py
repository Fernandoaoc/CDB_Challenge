from app.services.challenge_runner import ChallengeRunner


class ChallengeDownloader:
    """Compat wrapper around the current challenge runner."""

    def __init__(self, headless: bool = True):
        self.runner = ChallengeRunner(headless=headless)

    def run(self):
        self.runner.execute()
        return {
            "result_message": self.runner.last_result_message,
            "screenshot_path": self.runner.last_screenshot_path,
        }

    def close(self):
        self.runner.close()
