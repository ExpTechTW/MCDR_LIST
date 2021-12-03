from mcdreforged.api.all import *
import re
import json
import math
from typing import NamedTuple


class Position(NamedTuple):
    x: float
    y: float
    z: float


f = open('C:/Users/whes1/Desktop/server/plugins/list.json', 'r')
line = f.read()
Json = json.loads(line)

PLUGIN_METADATA = {
    'id': 'LIST_whes1015',
    'version': '1.0.0',
    'name': 'LIST'
}


def process_coordinate(text: str) -> Position:
    data = text[1:-1].replace('d', '').split(', ')
    data = [(x + 'E0').split('E') for x in data]
    assert len(data) == 3
    return Position(*[float(e[0]) * 10 ** int(e[1]) for e in data])


def on_info(server: PluginServerInterface, info: Info):
    if info.is_player and info.content == '!!list':
        LIST = server.rcon_query('list').split(' ')
        LIST.remove('There')
        LIST.remove('are')
        LIST.remove('of')
        LIST.remove('a')
        LIST.remove('max')
        LIST.remove('players')
        LIST.remove('online:')
        LIST.remove('of')
        times=0
        newlist=[]
        for i in range(len(LIST)):
            if LIST[i].isdigit()==False:
                position = process_coordinate(re.search(r'\[.*]', server.rcon_query('data get entity {} Pos'.format(LIST[i].replace(',','')))).group())
                Json[LIST[i]+'X'] = position.x
                Json[LIST[i]+'Y'] = position.y
                Json[LIST[i]+'Z'] = position.z
                times=times+1
                newlist.append(LIST[i])
        f = open('C:/Users/whes1/Desktop/server/plugins/list.json', 'w')
        f.write(json.dumps(Json))
        f.close()
        for i in range(times):
            server.tell(info.player,newlist[i])
            server.tell(info.player,"X "+str(Json[newlist[i]+'X'])+" Y "+str(Json[newlist[i]+'Y'])+" Z "+str(Json[newlist[i]+'Z']))

def on_load(server, old):
    server.register_help_message('!!cam', '切換自由視角')
