from passguard.policy import PasswordPolicy
from passguard.rules.length import MinLengthRule
from passguard.rules.character import UppercaseRule, DigitRule
from passguard import PasswordValidator

from asyncio.log import logger
from typing import Any

import email_validator

class AuthService:
    
    @staticmethod
    async def password_policy():
        policy = PasswordPolicy()
        policy.add_rule(MinLengthRule(min_length=12))
        policy.add_rule(UppercaseRule(severity="HIGH"))
        policy.add_rule(DigitRule(severity="HIGH"))

        return policy

    @staticmethod
    async def password_validator(password):
        policy = await AuthService.password_policy()

        validator = PasswordValidator(policy=policy)

        result = validator.evaluate(password=password)
        if result.valid():
            logger.info(f"Result: {result.to_dict()}", exc_info=True)
            return True
        return False

    @staticmethod
    async def passwordmismatch(password: str, confirm_password: str):
        if password is None or confirm_password is None:
            return False
        
        if password.strip() != confirm_password.strip():
            return False
        return True

    @staticmethod
    async def validate_email(email: str) -> tuple[bool, str | None]:
        try:
            valid_email = email_validator.validate_email(email, check_deliverability=True)
        except email_validator.EmailNotValidError as e:
            return False, email
        return True, valid_email.normalized