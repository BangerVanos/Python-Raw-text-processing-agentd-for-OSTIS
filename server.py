import argparse
from sc_kpm import ScServer
from modules.raw_text_processing_module.raw_text_processing_module import RawTextProcessingModule
from modules.raw_text_processing_module import raw_text_processing_configs as cf

from sc_kpm.utils import create_link, get_link_content_data
from sc_kpm.utils.action_utils import (
    create_action_answer,
    execute_agent,
    finish_action_with_status,
    get_action_answer,
    get_action_arguments,
)
import logging

SC_SERVER_PROTOCOL = "protocol"
SC_SERVER_HOST = "host"
SC_SERVER_PORT = "port"

SC_SERVER_PROTOCOL_DEFAULT = "ws"
SC_SERVER_HOST_DEFAULT = "localhost"
SC_SERVER_PORT_DEFAULT = "8090"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="[%d-%b-%y %H:%M:%S]"
)


def main(args: dict):
    server = ScServer(
        f"{args[SC_SERVER_PROTOCOL]}://{args[SC_SERVER_HOST]}:{args[SC_SERVER_PORT]}/ws_json")

    with server.connect():        
        modules = [
            RawTextProcessingModule(),
        ]
        server.add_modules(modules[0])
        with server.register_modules():
            # question, is_successful = execute_agent(
            # arguments={
            #     create_link('apple color red; apple liked by human; apple place of growth tree', ScLinkContentType.STRING): False,                
            # },
            # concepts=[CommonIdentifiers.QUESTION, cf.NON_OFFICIAL_API_AGENT_ACTION],
            # wait_time=1,
            # )            
            server.serve()    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--protocol', type=str, dest=SC_SERVER_PROTOCOL, default=SC_SERVER_PROTOCOL_DEFAULT, help="Sc-server protocol")
    parser.add_argument(
        '--host', type=str, dest=SC_SERVER_HOST, default=SC_SERVER_HOST_DEFAULT, help="Sc-server host")
    parser.add_argument(
        '--port', type=int, dest=SC_SERVER_PORT, default=SC_SERVER_PORT_DEFAULT, help="Sc-server port")
    args = parser.parse_args()

    main(vars(args))
