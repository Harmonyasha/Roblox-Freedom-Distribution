import urllib.request
import util.resource
import util.versions
import util.const
import py7zr
import io


def get_remote_link(roblox_version: util.versions.roblox, bin_type: util.resource.bin_subtype) -> str:
    return util.const.GIT_LINK_FORMAT % (
        util.const.GIT_RELEASE_VERSION,
        roblox_version.name,
        bin_type.value,
    )


def download_binary(roblox_version: util.versions.roblox, bin_type: util.resource.bin_subtype) -> None:
    link = "https://github.com/Windows81/Roblox-Filtering-Disabled/releases/download/2024-06-12T0810Z/v463.Player.7z"
    res = urllib.request.urlopen(link).read()
    full_dir = util.resource.retr_roblox_full_path(roblox_version,  bin_type)
    py7zr.unpack_7zarchive(io.BytesIO(res), full_dir)
