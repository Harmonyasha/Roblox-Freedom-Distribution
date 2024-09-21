from web_server._logic import web_server_handler, server_path
import urllib.parse
import re


@server_path("/game/players/([0-9]+)/", regex=True)
@server_path("/.127.0.0.1/game/players/([0-9]+)/", regex=True)
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    self.send_json({"ChatFilter": "blacklist"})
    return True


@server_path("/moderation/v2/filtertext")
def _(self: web_server_handler) -> bool:

    # Manually parsing here since `self.query` isn't automatically populated prior.
    field_data = str(self.read_content(), encoding='utf-8')
    self.query = dict(urllib.parse.parse_qsl(field_data))

    orig_text = self.query.get('text', None)
    if not orig_text:
        return False


    self.send_json({
        "success": True,
        "message": orig_text,
        "data": {
            "AgeUnder13": orig_text,
            "Age13OrOver": orig_text,
        },
    })
    return True
