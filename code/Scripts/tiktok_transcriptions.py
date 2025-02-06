import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable

import requests


def group_by(lst: list, key_extractor: Callable):
    d = defaultdict(list)
    for item in lst:
        d[key_extractor(item)].append(item)
    return d


def get_transcripts_for_tiktok_video(video_id: str, transcripts_dir: Path):
    video_url = f"https://www.tiktok.com/@unknown/video/{video_id}"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"
    headers = {
        "User-Agent": user_agent,
        "Referer": "https://www.tiktok.com/",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1"
    }

    print(f"Fetching video URL: {video_url}")
    try:
        response = requests.get(video_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching video URL: {e}")
        return

    html_content = response.text

    # Extracting the JSON object from the HTML file
    json_match = re.search(r'(?<="__DEFAULT_SCOPE__":)[^<]*', html_content)
    if not json_match:
        print("JSON data not found in the HTML content.")
        return

    json_data = json.loads(json_match.group(0).strip()[:-1])  # manually removing last character
    transcripts_infos = json_data["webapp.video-detail"]["itemInfo"]["itemStruct"]["video"]["subtitleInfos"]

    language_code_priority = [
        "eng-US",
        "fra-FR",
        "deu-DE",
        "spa-ES",
    ]
    subtitle_infos_by_format = group_by(transcripts_infos, lambda info: info["Format"])
    for subtitle_format, infos_list in subtitle_infos_by_format.items():
        sorted_transcripts_infos_list = sorted(transcripts_infos,
                                               key=lambda info: language_code_priority.index(
                                                   info["LanguageCodeName"]) if
                                               info["LanguageCodeName"] in language_code_priority else math.inf)
        transcripts_info = sorted_transcripts_infos_list[0]
        url = transcripts_info["Url"]
        language = transcripts_info["LanguageCodeName"]
        source = transcripts_info["Source"]

        suffix = "vtt" if subtitle_format == "webvtt" else "json" if subtitle_format == "creator_caption" else None

        filename = f"{video_id}_{subtitle_format}_{language}_{source}"
        if suffix:
            filename += f".{suffix}"
        try:
            file_response = requests.get(url, headers=headers)
            file_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to download transcripts for video {video_id}, language {language}: {e}")
            continue

        video_dir = transcripts_dir / video_id
        video_dir.mkdir(exist_ok=True)
        with open(video_dir / filename, "wb+") as f:
            f.write(file_response.content)
            print(f"Saved file: {video_dir / filename}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 tiktok_transcriptions.py <video_id> <output_dir>")
        sys.exit(1)

    video_id = sys.argv[1]
    transcripts_dir = Path(sys.argv[2])
    get_transcripts_for_tiktok_video(video_id, transcripts_dir)
