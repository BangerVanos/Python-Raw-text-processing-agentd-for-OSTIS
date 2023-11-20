"""This is agent which uses non-official API
of LLMs. You can choose used model in configs
by changing NON_OFFICIAL_API_DEFAULT_MODEL parameter"""


import g4f
from sc_client.constants.common import ScEventType
from sc_client.models import ScAddr, ScLinkContentType, ScTemplate

from sc_kpm.identifiers import QuestionStatus
from sc_kpm.sc_keynodes import Idtf
from sc_kpm.sc_result import ScResult
from sc_kpm.utils.action_utils import (
    get_action_arguments,
    finish_action_with_status,
    create_action_answer
)
from sc_kpm.utils import (
    get_link_content_data,
    create_link
)
from sc_kpm import ScAgentClassic

from . import raw_text_processing_configs as cf
from .interfaces import IGetCleanText
from requests import HTTPError
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="[%d-%b-%y %H:%M:%S]"
)


class NonOfficialAPITextProcessor(ScAgentClassic, IGetCleanText):
    def __init__(self) -> None:                     
        super().__init__(cf.NON_OFFICIAL_API_AGENT_ACTION)               

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:                       
        self.logger.info('Non-official API raw text processor began to run...')        
        raw_text_node = get_action_arguments(action_element, 1)[0]
        if not raw_text_node:
            self.logger.error('Error: could not find raw text sc-link to process')
            return ScResult.ERROR_INVALID_PARAMS
        raw_text = get_link_content_data(raw_text_node)
        if not isinstance(raw_text, str):
            self.logger.error(f'Error: your raw text must be string type, but text of yours is {type(raw_text)}')
            return ScResult.ERROR_INVALID_TYPE
        try:
            clean_text = self._get_clean_text(raw_text, 'lang_en')
            answer_link = create_link(clean_text, ScLinkContentType.STRING)
        except HTTPError as err:
            self.logger.error(f'Error: {err}.\nThis error is on non-official API\'s side.')
            return ScResult.ERROR
        print(clean_text)
        create_action_answer(action_element, answer_link)
        self.logger.info('Successfully processed the text using non-official API! Wery well!')
        finish_action_with_status(action_element, True)
        return ScResult.OK
    
    def _get_clean_text(self, raw_text: str, language: str) -> str:
        """Method applies raw text describing structure from KB and language, which is string
        containing text like lang_YOUR_LANGUAGE_CODE (which is different representation for languages in
        OSTIS KBs). For example, english language will be lang_en. For text processing non-official
        LLM api is used. You can configure used model in raw_text_processing_configs file"""

        messages = [{'role': 'user', 'content': cf.PROMPTS[language].format(raw_text)}]
        response = g4f.ChatCompletion.create(
            model=cf.NON_OFFICIAL_API_DEFAULT_MODEL,
            messages=messages,
            temperature=0
        )
        self.logger.info(f'Successfully cleaned text for you\n:{response}')
        return response    
