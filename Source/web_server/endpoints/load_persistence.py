from web_server._logic import web_server_handler, server_path
import urllib.parse
import itertools


@server_path('/persistence/set')  # Usually expects POST.
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/datastoreservice.py#L92
    '''
    form_content = str(self.read_content(), encoding='utf-8')
    form_data = dict(urllib.parse.parse_qsl(form_content))
    database = self.server.database.persistence

    # TODO: implement sorted data stores.
    data_type = self.query.get('type', None)

    scope = self.query.get(
        'scope',
        'global',
    )

    target = self.query.get(
        'target',
        None,
    )
    if not target:
        return False

    key = self.query.get(
        'key',
        None,
    )
    if not key:
        return False

    value = form_data.get(
        'value',
        None,
    )

    database.set(scope, target, key, value)
    self.send_json({"data": value})
    return True


@server_path('/persistence/getv2')  # Usually expects POST.
@server_path('/persistence/getV2')  # Usually expects POST.
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/datastoreservice.py#L162
    '''
    form_content = str(self.read_content(), encoding='utf-8')
    form_data = dict(urllib.parse.parse_qsl(form_content))
    database = self.server.database.persistence

    return_data = []
    for starting_count in itertools.count(0):
        prefix = "qkeys[%d]" % starting_count
        scope = form_data.get(
            f"{prefix}.scope",
            'global',
        )

        target = form_data.get(
            f"{prefix}.target",
            None,
        )
        if not target:
            break

        key = form_data.get(
            f"{prefix}.key",
            None,
        )
        if not key:
            break

        value = database.get(scope, target, key)
        return_data.append({
            "Value": value,
            "Scope": scope,
            "Key": key,
            "Target": target,
        })

    # TODO: implement sorted data stores.
    data_type = self.query.get('type', None)

    if starting_count == 0:
        self.send_json({"data": [], "message": "No data being requested"})
        return True

    self.send_json({"data": return_data})
    return True
