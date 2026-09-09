from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LoginCase:
    name: str
    username: str
    password: str


def invalid_login_cases() -> tuple[LoginCase, ...]:
    return (
        LoginCase("empty credentials", "", ""),
        LoginCase("whitespace credentials", "   ", "   "),
        LoginCase("overlong username", "a" * 256, "Password123"),
        LoginCase("unicode username", "estudiante-ñ", "Password123"),
        LoginCase("sql-shaped username", "' OR '1'='1", "Password123"),
        LoginCase("xss-shaped username", "<script>alert(1)</script>", "Password123"),
    )