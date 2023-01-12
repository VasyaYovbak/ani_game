from connection import session
from parsers.attack_on_titan.database.download import download_attack_on_titan_data
from parsers.bleach.database.download import download_bleach_data
from parsers.demon_slayer.database.download import download_demon_slayer_data
from parsers.dragon_ball.database.download import download_dragon_ball_data
from parsers.fairy_tail.database.download import download_fairy_tail_data
from parsers.hunter.database.download import download_hunter_data
from parsers.jojo.database.download import download_jojo_data
from parsers.my_hero_academia.database.download import download_my_hero_academia_data
from parsers.naruto.database.download import download_naruto_data
from parsers.one_piece.database.download import download_one_piece_data
from parsers.one_punch.database.download import download_one_punch_data

"""Run this file in case you need to fulfill Character table with all parsed data"""

download_one_punch_data(session=session)
download_one_piece_data(session=session)
download_jojo_data(session=session)
download_hunter_data(session=session)
download_dragon_ball_data(session=session)
download_bleach_data(session=session)
download_demon_slayer_data(session=session)
download_attack_on_titan_data(session=session)
download_my_hero_academia_data(session=session)
download_fairy_tail_data(session=session)
download_naruto_data(session=session)
