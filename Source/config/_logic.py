import data_transfer
import util.resource
import util.versions
import storage
import tomli


class base_type:
    def __init__(self, path: str) -> None:
        '''
        Reads the game configuration data from a file and serialises it.
        '''
        print("Game data serialising...")
        self.config_path = util.resource.retr_config_full_path(path)
        with open(self.config_path, 'rb') as f:
            self.data_dict: dict = tomli.load(f)

        self.data_transferer = data_transfer.transferer()
        print("Game data serialised")
