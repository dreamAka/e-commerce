"""
Custom template filters for price formatting.
Formats numbers with dot separators: 1200000 → 1.200.000
"""
from django import template

register = template.Library()


@register.filter(name='price_format')
def price_format(value):
    """
    Formats a number with dot (.) as thousands separator.
    Example: 1200000 → 1.200.000
    """
    try:
        # Convert to integer (remove decimals for price display)
        num = int(float(value))
        # Format with dots as thousands separator
        formatted = f'{num:,}'.replace(',', '.')
        return formatted
    except (ValueError, TypeError):
        return value
