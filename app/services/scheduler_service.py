import math
import time
from typing import Awaitable, Callable, Dict, List
from collections import defaultdict
from app.services import weight_strategy
from app.enum.action_type import ActionType
from app.models import db_w2v_mapper
from app.util.weight_aging import exponential_decay_weight
from app.repositories.action_log_repository import ActionLogRepository
from app.repositories.user_weight_repository import UserWeightRepository

async def resize_weight(
    action_log_repo: ActionLogRepository,
    user_weight_repo: UserWeightRepository,
    get_genres_by_content_id_func: Callable[[int], Awaitable[List[str]]]
):
    all_logs = await action_log_repo.find_all_order_by_user_id()
    grouped_logs = group_logs_by_user_id(all_logs)

    for user_id, logs in grouped_logs.items():
        genre_dict = defaultdict(int)
        for log in logs:
            try:
                action_type = ActionType[log['action']]
            except KeyError:
                continue

            value = int(log['value'])
            weight = weight_strategy.convert_to_weight(action_type, value)
            weight = exponential_decay_weight(weight, log['timestamp'])

            content_id = log['contentId']
            genres = await get_genres_by_content_id_func(content_id)
            for genre in genres:
                translated = db_w2v_mapper.translate_genre(genre)
                if translated:
                    genre_dict[translated] += weight

        for genre_name, weight in genre_dict.items():
            await user_weight_repo.reset_weight(user_id, genre_name, weight)

    print("✅ 가중치 재계산 완료")
    return

def calc_resized_weight(timestamp : int, weight : float):
  current_timestamp_ms = int(time.time() * 1000)  # 현재 시간 (밀리초)
  delta_ms = current_timestamp_ms - timestamp
  delta_days = delta_ms / (1000 * 60 * 60 * 24)  # 하루 단위 경과 시간

  resized_weight = weight * math.exp(-1 * delta_days)
  return resized_weight

def group_logs_by_user_id(logs: List[Dict]) -> Dict[int, List[Dict]]:
    grouped = defaultdict(list)
    for log in logs:
        user_id = log["userId"]
        grouped[user_id].append(log)
    return dict(grouped)