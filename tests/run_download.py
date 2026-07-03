from app.services.challenge_downloader import ChallengeDownloader

downloader = ChallengeDownloader()

try:
    print(downloader.run())
finally:
    downloader.close()
