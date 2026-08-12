from dataclasses import dataclass

from plc_test.core.tag import Tag
from plc_test.core.tag_mapping import TagMapping


@dataclass(frozen=True)
class AllenBradleyTagMapping(TagMapping):
    controller_tag: str

    def get_address(self) -> str:
        return self.controller_tag
