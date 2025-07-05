import textwrap
from typing import TYPE_CHECKING, TypeVar, cast

from ._interfaces import BamlSourceGenerator
from ._model import (
    BamlClassModel,
    BamlEnumModel,
    BamlEnumValueModel,
    BamlFieldModel,
)

if TYPE_CHECKING:
    from baml_py.type_builder import TypeBuilder
T = TypeVar("T", bound="TypeBuilder")


class BamlModelToBamlSourceConverter(BamlSourceGenerator[T]):
    """Converts a list of BamlClassModel and BamlEnumModel objects into BAML source code."""

    def __init__(
        self, baml_models: list[BamlClassModel | BamlEnumModel], indent: str = "  "
    ):
        """
        Initializes the converter.

        Args:
            baml_models: A list of BAML models (classes and enums) to convert.
            indent: The string to use for indentation (e.g., "  " or "    ").

        """
        super().__init__(baml_models)
        self._indent = indent

    def _format_docstring(self, text: str | None, indent_level: int = 0) -> str:
        """Formats a description string into a BAML docstring."""
        if not text:
            return ""
        prefix = self._indent * indent_level + "/// "
        # Wrap text to a reasonable width, preserving paragraphs
        wrapped_lines = []
        for paragraph in text.split("\n\n"):
            lines = textwrap.wrap(
                paragraph.strip(),
                width=80 - len(prefix),  # Adjust width based on prefix length
                replace_whitespace=False,  # Keep existing newlines within paragraphs
                drop_whitespace=True,
                break_long_words=False,
                break_on_hyphens=False,
            )
            wrapped_lines.extend(lines)
            wrapped_lines.append("")  # Add blank line between paragraphs

        if wrapped_lines and not wrapped_lines[-1]:
            wrapped_lines.pop()  # Remove trailing blank line

        return "\n".join(prefix + line for line in wrapped_lines) + "\n"

    def _generate_field_baml(self, field: BamlFieldModel, indent_level: int) -> str:
        """Generates BAML source for a single class field."""
        parts = []

        indent_str = self._indent * indent_level
        base_line = (
            f"{indent_str}{field.name} {field.type_info.get_effective_type_str()}"
        )
        parts.append(base_line)

        attributes = []
        if field.alias:
            attributes.append(f'@alias("{field.alias}")')
        if field.skip:
            attributes.append("@skip")
        if field.description:  # Add if no docstring was generated
            attributes.append(f'@description(#"{field.description}"#)')  # Basic quoting

        if attributes:
            parts.append(" " + " ".join(attributes))

        return "".join(parts)

    def _generate_enum_value_baml(
        self, value: BamlEnumValueModel, indent_level: int
    ) -> str:
        """Generates BAML source for a single enum value."""
        parts = []
        docstring = self._format_docstring(value.description, indent_level)
        parts.append(docstring)

        indent_str = self._indent * indent_level
        base_line = f"{indent_str}{value.name}"
        parts.append(base_line)

        attributes = []
        if value.alias:
            attributes.append(f'@alias("{value.alias}")')
        if value.skip:
            attributes.append("@skip")
        # Field descriptions are typically handled by docstrings above the field.
        if value.description and not docstring:
            attributes.append(f'@description("{value.description}")')

        if attributes:
            parts.append(" " + " ".join(attributes))

        return "".join(parts)

    def _generate_class_baml(self, model: BamlClassModel) -> str:
        """Generates BAML source code for a BamlClassModel."""
        parts = []
        parts.append(self._format_docstring(model.description, indent_level=0))
        parts.append(f"class {model.name} {{\n")

        for prop in model.properties:
            parts.append(self._generate_field_baml(prop, indent_level=1))
            parts.append("\n")  # Add newline after each field + attributes

        # Add block-level attributes if any
        block_attributes = []
        if model.alias:
            block_attributes.append(f'@@alias("{model.alias}")')
        if model.is_dynamic:
            block_attributes.append("@@dynamic")
        if block_attributes:
            parts.append("\n")  # Add blank line before block attributes
            parts.extend([f"{self._indent}{attr}\n" for attr in block_attributes])

        parts.append("}\n")
        return "".join(parts)

    def _generate_enum_baml(self, model: BamlEnumModel) -> str:
        """Generates BAML source code for a BamlEnumModel."""
        parts = []
        parts.append(self._format_docstring(model.description, indent_level=0))
        parts.append(f"enum {model.name} {{\n")

        for value in model.values:
            parts.append(self._generate_enum_value_baml(value, indent_level=1))
            parts.append("\n")  # Add newline after each value + attributes

        # Add block-level attributes if any
        block_attributes = []
        if model.alias:
            block_attributes.append(f'@@alias("{model.alias}")')
        if model.is_dynamic:
            block_attributes.append("@@dynamic")
        if block_attributes:
            parts.append("\n")  # Add blank line before block attributes
            parts.extend([f"{self._indent}{attr}\n" for attr in block_attributes])

        parts.append("}\n")
        return "".join(parts)

    def generate(self) -> str:
        """
        Generates the BAML source code string from the provided models.

        Returns:
            A string containing the BAML source code.

        """
        baml_parts = []
        for model in self._baml_models:
            if isinstance(model, BamlClassModel):
                baml_parts.append(self._generate_class_baml(model))
            elif isinstance(model, BamlEnumModel):
                baml_parts.append(self._generate_enum_baml(model))
            else:
                raise TypeError(f"Unknown model type: {model.__class__.__name__} for {model}")

        # Join parts with double newlines for separation between definitions
        return "\n".join(baml_parts)

