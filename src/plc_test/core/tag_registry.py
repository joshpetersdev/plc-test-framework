from .exceptions import TagNotFoundError
from .plc_vendor import PLCVendor
from .tag import Tag
from .tag_mapping import TagMapping


class TagRegistry:
    """Registry of logical PLC tags and vendor-specific mappings."""

    def __init__(self) -> None:
        self._tags: dict[str, Tag] = {}
        self._mappings: dict[str, dict[PLCVendor, TagMapping]] = {}

    def register_tag(self, tag: Tag) -> None:
        """Register a logical PLC tag."""

        if tag.name in self._tags:
            raise ValueError(
                f"Tag '{tag.name}' is already registered."
            )

        self._tags[tag.name] = tag
        self._mappings[tag.name] = {}

    def register_mapping(
        self,
        tag_name: str,
        vendor: PLCVendor,
        mapping: TagMapping,
    ) -> None:
        """Register a vendor-specific mapping for a tag."""

        if tag_name not in self._tags:
            raise TagNotFoundError(
                f"Tag '{tag_name}' is not registered."
            )

        if mapping.tag.name != tag_name:
            raise ValueError(
                f"Mapping tag '{mapping.tag.name}' does not match "
                f"tag '{tag_name}'."
            )

        if vendor in self._mappings[tag_name]:
            raise ValueError(
                f"A mapping for vendor '{vendor.value}' already "
                f"exists for tag '{tag_name}'."
            )

        self._mappings[tag_name][vendor] = mapping

    def get_tag(self, tag_name: str) -> Tag:
        """Return a logical tag."""

        try:
            return self._tags[tag_name]
        except KeyError as exc:
            raise TagNotFoundError(
                f"Tag '{tag_name}' is not registered."
            ) from exc

    def get_mapping(
        self,
        tag_name: str,
        vendor: PLCVendor,
    ) -> TagMapping:
        """Return the mapping for a tag and PLC vendor."""

        if tag_name not in self._tags:
            raise TagNotFoundError(
                f"Tag '{tag_name}' is not registered."
            )

        try:
            return self._mappings[tag_name][vendor]
        except KeyError as exc:
            raise TagNotFoundError(
                f"No mapping for vendor '{vendor.value}' exists "
                f"for tag '{tag_name}'."
            ) from exc

    def contains(self, tag_name: str) -> bool:
        """Return True if a tag is registered."""

        return tag_name in self._tags

    def has_mapping(
        self,
        tag_name: str,
        vendor: PLCVendor,
    ) -> bool:
        """Return True if a vendor-specific mapping exists."""

        if tag_name not in self._tags:
            return False

        return vendor in self._mappings[tag_name]

    def remove_tag(self, tag_name: str) -> None:
        """Remove a tag and all of its mappings."""

        if tag_name not in self._tags:
            raise TagNotFoundError(
                f"Tag '{tag_name}' is not registered."
            )

        del self._tags[tag_name]
        del self._mappings[tag_name]

    def clear(self) -> None:
        """Remove all tags and mappings."""

        self._tags.clear()
        self._mappings.clear()

    def __len__(self) -> int:
        """Return the number of registered tags."""

        return len(self._tags)
