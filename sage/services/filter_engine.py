"""Filter engine for subsetting personas based on filter expressions."""

import re
from typing import Any, Callable


class FilterEngine:
    """Apply filters to subset personas."""

    # Comparison operators mapping
    OPERATORS: dict[str, Callable[[Any, Any], bool]] = {
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
        "!=": lambda a, b: a != b,
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        "=": lambda a, b: a == b,
    }

    def apply_filters(
        self,
        personas: list[dict[str, Any]],
        filters: list[str],
    ) -> tuple[list[dict[str, Any]], list[bool]]:
        """
        Apply filters to personas.

        Supports filter expressions like:
        - "age>=30" - numeric comparison
        - "gender=F" - string equality
        - "income!=low" - string inequality
        - "region in [North,South,West]" - membership check

        Args:
            personas: List of persona dictionaries
            filters: List of filter expressions

        Returns:
            filtered_personas: List of personas matching all filters
            match_flags: Boolean list indicating which personas matched
        """
        if not filters:
            return personas, [True] * len(personas)

        match_flags = []
        filtered = []

        for persona in personas:
            matches = all(self._evaluate_filter(persona, f) for f in filters)
            match_flags.append(matches)
            if matches:
                filtered.append(persona)

        return filtered, match_flags

    def _evaluate_filter(self, persona: dict[str, Any], filter_expr: str) -> bool:
        """
        Evaluate a single filter expression against a persona.

        Args:
            persona: Persona dictionary
            filter_expr: Filter expression string

        Returns:
            True if persona matches the filter, False otherwise
        """
        # Handle 'in' operator: field in [val1,val2,val3]
        in_match = re.match(r"(\w+)\s+in\s+\[([^\]]+)\]", filter_expr)
        if in_match:
            field = in_match.group(1)
            values = [v.strip() for v in in_match.group(2).split(",")]
            persona_value = persona.get(field)
            return str(persona_value) in values

        # Handle 'not in' operator: field not in [val1,val2,val3]
        not_in_match = re.match(r"(\w+)\s+not\s+in\s+\[([^\]]+)\]", filter_expr)
        if not_in_match:
            field = not_in_match.group(1)
            values = [v.strip() for v in not_in_match.group(2).split(",")]
            persona_value = persona.get(field)
            return str(persona_value) not in values

        # Handle comparison operators (must check longer ones first)
        for op in [">=", "<=", "!=", ">", "<", "="]:
            if op in filter_expr:
                parts = filter_expr.split(op, 1)
                if len(parts) != 2:
                    continue

                field = parts[0].strip()
                value = parts[1].strip()

                persona_value = persona.get(field)
                if persona_value is None:
                    return False

                # Try numeric comparison first
                try:
                    numeric_persona_value = float(persona_value)
                    numeric_value = float(value)
                    return self.OPERATORS[op](numeric_persona_value, numeric_value)
                except (ValueError, TypeError):
                    # Fall back to string comparison
                    return self.OPERATORS[op](str(persona_value), value)

        raise ValueError(f"Invalid filter expression: {filter_expr}")

    def validate_filters(self, filters: list[str]) -> list[str]:
        """
        Validate filter expressions.

        Args:
            filters: List of filter expressions

        Returns:
            List of validation errors (empty if all valid)
        """
        errors = []
        for i, f in enumerate(filters):
            try:
                # Try to parse the filter
                # Check for 'in' operator
                if " in [" in f or " not in [" in f:
                    if not re.match(r"(\w+)\s+(not\s+)?in\s+\[([^\]]+)\]", f):
                        errors.append(f"Filter {i}: Invalid 'in' expression: {f}")
                    continue

                # Check for comparison operators
                has_operator = False
                for op in [">=", "<=", "!=", ">", "<", "="]:
                    if op in f:
                        has_operator = True
                        parts = f.split(op, 1)
                        if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
                            errors.append(f"Filter {i}: Invalid comparison: {f}")
                        break

                if not has_operator:
                    errors.append(f"Filter {i}: No valid operator found: {f}")

            except Exception as e:
                errors.append(f"Filter {i}: {str(e)}")

        return errors
