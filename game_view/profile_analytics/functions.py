import json

from azure.cosmos.exceptions import CosmosResourceNotFoundError
from game_view.profile_analytics.config import date_now, container


def get_primary_key(date, user_id):
    return f"{date} {user_id}"


def print_profile_analytics_db(container=container):
    query = "SELECT * FROM AniGame"
    params = [dict(name="@user_id")]

    items = container.query_items(
        query=query, parameters=params, enable_cross_partition_query=True
    )

    for item in items:
        print(json.dumps(item, indent=True))


def find_item(item_id, container=container):
    try:
        return container.read_item(item=item_id, partition_key=item_id)
    except CosmosResourceNotFoundError:
        return None


def create_analytics_item(user):
    date = date_now
    user_id = user.id
    games_played_today = 0
    data = {
        "id": get_primary_key(date, user_id),
        "user_id": user_id,
        "number_of_games": games_played_today,
        "rating": user.rating,
        "date": str(date),
    }
    return data


def update_profile_analytics(looser, winner, container=container):
    date = date_now
    looser_primary_key, winner_primary_key = get_primary_key(date, looser.id), get_primary_key(date, winner.id)
    looser_item = find_item(looser_primary_key)
    winner_item = find_item(winner_primary_key)
    items = [(looser_item, looser), (winner_item, winner)]

    for (item, user) in items:
        if item is None:
            # print(f"Created {user.id} {item}")
            analytic_item = create_analytics_item(user)
            container.create_item(analytic_item)
        else:
            item['rating'] = user.rating
            item['number_of_games'] = item['number_of_games'] + 1
            # print(f"Updated {user.id}")
            container.upsert_item(body=item)


print_profile_analytics_db()
