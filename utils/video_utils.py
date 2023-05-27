from datetime import timedelta
import json
import os
import subprocess

import youtube_dl
from youtube_dl.utils import (DownloadError, ExtractorError)


def download_video(url, start, dur, output):
    output_tmp = os.path.join("/tmp", os.path.basename(output))
    try:
        # From https://stackoverflow.com/questions/57131049/is-it-possible-to-download-a-specific-part-of-a-file
        with youtube_dl.YoutubeDL({'format': 'best'}) as ydl:
            result = ydl.extract_info(url, download=True)
            video = result['entries'][0] if 'entries' in result else result

        url = video['url']
        if start < 5:
            offset = start
        else:
            offset = 5
        start -= offset
        offset_dur = dur + offset
        start_str = str(timedelta(seconds=start))
        dur_str = str(timedelta(seconds=offset_dur))

        cmd = ['ffmpeg', '-i', url, '-ss', start_str, '-t', dur_str, '-c:v',
               'copy', '-c:a', 'copy', output_tmp]
        subprocess.call(cmd)

        start_str_2 = str(timedelta(seconds=offset))
        dur_str_2 = str(timedelta(seconds=dur))

        cmd = ['ffmpeg', '-i', output_tmp, '-ss', start_str_2, '-t', dur_str_2, output]
        subprocess.call(cmd)
        return True

    except (DownloadError, ExtractorError) as e:
        print("Failed to download %s" % output)
        return False


def set_up_videos():
    with open("./kinetics400/test.json", "r") as f:
        test_data = json.load(f)

    target_classes = [
        'springboard diving',
        'surfing water',
        'swimming backstroke',
        'swimming breast stroke',
        'swimming butterfly stroke',
    ]
    data_dir = "./videos"
    max_samples = 5

    classes_count = {c: 0 for c in target_classes}

    for fn, data in test_data.items():
        label = data["annotations"]["label"]
        segment = data["annotations"]["segment"]
        url = data["url"]
        dur = data["duration"]
        if label in classes_count and classes_count[label] < max_samples:
            c_dir = os.path.join(data_dir, label)
            if not os.path.exists(c_dir):
                os.makedirs(c_dir)

            start = segment[0]
            output = os.path.join(c_dir, "%s_%s.mp4" % (label.replace(" ", "_"), fn))

            results = True
            if not os.path.exists(output):
                result = download_video(url, start, dur, output)
            if result:
                classes_count[label] += 1

    print("Finished downloading videos!")
