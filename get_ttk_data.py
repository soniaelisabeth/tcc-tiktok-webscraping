import os
import logging
from TikTokApi import TikTokApi
import pandas as pd
import asyncio

ms_token = os.environ.get(
    "ms_token",
    'lLgrWjRo3eGMYTpUs8lIaqW7CvJWaSt3jsTSAoQpFx3HXmuAaaYH_9OBf-8kWXdZKGr5fcxJH_j7lAo1F4O1H59ZUZ97d4NtBBJ7_lRTuIEJjzDSDSBLzu7rICFpbYMhh8fQcod3iIaXEMwcW6lxE_acsqA='
    ) # get your own ms_token from your cookies on tiktok.com

cookies = [{
    "csrf_session_id": "805d56b42ffc51648c0ca488a2b7b4be",
    "csrfToken": "KDKGvviP-es9kBw1EfDq-fJX_sNwGUowqFrM",
    "s_v_web_id": "verify_lwsmpsr7_QJwPU5yv_OIND_4Z6q_AkW0_nOUQbHzfTw9Q",
    "tt_csrf_token": "Lswx6jw9-hUbnMzrUjoJiY_MTq-_9Ady4TTc",
    "perf_feed_cache": "{%22expireTimestamp%22:1717527600000%2C%22itemIds%22:[%227354043957338295585%22%2C%227375899510532328709%22%2C%227370074401351421190%22]}",
    "sessionid": "4273013a2913f3e14319fdcea433e02b"
}]

logging.basicConfig(filename='tiktok_data.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def trending_videos():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False, cookies=cookies)
        logging.info('Sessao de Scraping inicializada com sucesso.')

        video_data_list = []

        async for video in api.trending.videos(count=20):
            video_contents = video.as_dict.get('contents', {})
            video_description = video_contents[0].get('desc', '') if video_contents else ''
            hashtags = [hashtag.name for hashtag in video.hashtags]

            current_video_data = {
                'id': video.id,
                'creator': video.author.username,
                'hashtags': ', '.join(hashtags),
                'description': video_description
            }
            video_data_list.append(current_video_data)

            logging.info(f'Dados do video coletados: {current_video_data}')
        
        df = pd.DataFrame(video_data_list)
        df.to_csv('tiktok_data.csv', index=False, mode='a', header=not os.path.exists('tiktok_data.csv'))
        logging.info('Todos os dados dos videos coletados e salvos.')

if __name__ == "__main__":
    asyncio.run(trending_videos())