from web_server._logic import web_server_handler, server_path
import assets


@server_path("/asset")
@server_path("/asset/")
@server_path("/v1/asset")
@server_path("/v1/asset/")
@server_path("/.127.0.0.1/asset/")
def _(self: web_server_handler) -> bool:
    asset_id = next(
        (
            i for i in [
                assets.resolve_asset_id(
                    self.query.get('id', None),
                ),
                assets.resolve_asset_version_id(
                    self.query.get('assetversionid', None),
                ),
            ]
            if i != None),
        None
    )

    if not asset_id:
      #  print('not asset parser',asset_id)
        return False
    asset = assets.load_asset(asset_id)
    if not asset:
       # print('not asset request',asset_id)
        return False
    
  
    self.send_data(asset)
    return True
