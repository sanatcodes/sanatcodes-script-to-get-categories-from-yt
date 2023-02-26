"""Worker to extract Ireland Trending YouTube Video Statistics."""
import logging
from datetime import datetime
from pathlib import Path
from time import time

import pandas as pd
import pytz
import requests
import json

from common.utils import save_to_csv
from yt_id import config, YouTube
from yt_id.logger import setup_logging

_LOGGER = logging.getLogger("main")


def main():

    _LOGGER.info("Start retrieving Irealnd youtube trending videos")
    now = datetime.now(tz=pytz.utc)
    dataset_version = datetime.now(tz=pytz.timezone("GMT"))
    dataset_version = dataset_version.strftime("%Y%m%d.%H%M")

    youtube = YouTube(
        url=config.URL,
        api_key=config.API_KEY
    )
    start = time()
    videos = youtube.get_trendings()
    end = time()
    _LOGGER.debug("Done retrieving raw video data in %.3fs",
                  (end - start))

    df_videos = pd.DataFrame([
        video.to_dict(trending_time=now)
        for video in videos
    ])
    _LOGGER.info("Got total %d trending videos", df_videos.shape[0])

    filename = Path(config.DATADIR) / f"trending_{dataset_version}.csv"
    # save_to_csv(df_videos, filename.as_posix())
    # df_saved = pd.read_csv(filename)
    # _LOGGER.info("Done saving %d trending videos (%s). Total videos: %d",
    #              df_videos.shape[0], filename, df_saved.shape[0])

    # manuipulate data
    df_videos['trending_time'] = pd.to_datetime(
        df_videos['trending_time']).dt.date
    df_videos['view'] = pd.to_numeric(df_videos['view'])
    df_videos['like'] = pd.to_numeric(df_videos['like'], errors='coerce')
    df_videos = df_videos.dropna(subset=['like'])
    df_videos['like'] = df_videos['like'].astype(int)
    df_videos['comment'] = pd.to_numeric(df_videos['comment'], errors='coerce')
    df_videos['comment'] = df_videos['comment'].fillna(0)
    df_videos['comment'] = df_videos['comment'].astype(int)
    test = df_videos.groupby(['trending_time', 'category_id'])[
        'view', 'like', 'comment'].sum().reset_index()
    test['videos'] = df_videos.groupby(
        ['trending_time', 'category_id']).size().reset_index(name='videos')['videos']
    test['trending_date'] = pd.to_datetime(test['trending_time'])
    test.drop(['trending_time'], axis=1, inplace=True)
    # ---- changing date to year week and month -----
    # test['year'] = test['trending_date'].dt.year
    # test['month'] = test['trending_date'].dt.month
    # test['day'] = test['trending_date'].dt.day
    # test['day_of_week'] = test['trending_date'].dt.dayofweek
    # test.drop(['trending_date'], axis=1, inplace=True)

    test = test.reindex(columns=[
                        "trending_date", "category_id", "view", "like", "comment", "videos"])
    # test.reset_index(inplace=True, drop=True)
    test.columns = ["trending_date", "category_id", "views", "likes",
                    "comment_count", "videos"]

    test["trending_date"] = test["trending_date"].astype(str)
    # send data to mondo db
    data = test.to_dict(orient='records')
    json_data = json.dumps(data)
    print('what data looks like:', json_data)
    payload = json.loads(json_data)
    response = requests.post(
        'http://127.0.0.1:8000/category', json=payload)
    print(response.status_code)
    print(response.json())

    # save to csv
    save_to_csv(test, filename.as_posix())
    df_saved = pd.read_csv(filename)
    _LOGGER.info("Done saving %d trending videos (%s). Total videos: %d",
                 df_videos.shape[0], filename, df_saved.shape[0])


if __name__ == "__main__":
    setup_logging(config.LOG_LEVEL)
    main()
