"""
Utility functions used across the Password Tool project.
"""

def validate_length(length: int) -> bool:
    """
    Validate password length.

    Args:
        length (int): Desired password length.

    Returns:
        bool: True if valid length, else False.
    """
    return 6 <= length <= 64
