import pytube
from pytube import YouTube
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset("kinetics-600")


def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


if __name__ == '__main__':
    YouTube('https://youtu.be/ocXx2Kw9x0U').streams.first().download(filename='filename')


