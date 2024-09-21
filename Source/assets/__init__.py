from . import (
    rbxl,
    mesh,
)

import util.resource
import urllib3
import os


def resolve_asset_id(id_str: str | None) -> int | None:
    #print("resolve",id_str)
    if not id_str:
        return None
    try:
        return int(id_str)
    except ValueError:
        return None


def resolve_asset_version_id(id_str: str | None) -> int | None:
    # Don't assume this is true for production Roblox:
    # RFD treats 'asset version ids' the same way as just plain 'version ids'.
    return resolve_asset_id(id_str)


def get_asset_path(aid: int) -> str:
    return util.resource.retr_full_path(util.resource.dir_type.ASSET, f'{aid:011d}')


def load_online_asset(asset_id: int) -> bytes | None:
    for key in {'id'}:
        url = f'https://assetdelivery.roblox.com/v1/asset/?{key}={asset_id}'
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        if response.status == 200:
            break
    else:
        return

    data = response.data
    data = rbxl.parse(data)
    data = mesh.parse(data)

    return data


def load_asset(asset_id: int) -> bytes | None:
    '''
    Loads cached asset by ID, else load from online.
    '''
    path = get_asset_path(asset_id)
    cached = os.path.isfile(path)

    if cached:
        with open(path, 'rb') as f:
            return f.read()
  #  print(asset_id)
   # if asset_id == 4409479779:
  #      print("load")
    online_data = load_online_asset(asset_id)
    if not online_data:
        return

    with open(path, 'wb') as f:
        f.write(online_data)

    return online_data
