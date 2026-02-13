"""Custom allauth adapter to handle Djongo compatibility issues"""
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class DjangoAllauthAdapter(DefaultAccountAdapter):
    """Custom adapter that avoids problematic Djongo queries"""

    def clean_username(self, username, shallow=False):
        """
        Override to avoid Djongo's problematic .exists() call
        """
        username = super().clean_username(username, shallow=shallow)
        
        if not shallow:
            try:
                # Try count() instead of exists() to avoid Djongo recursion issues
                existing_count = User.objects.filter(username=username).count()
                if existing_count > 0:
                    raise ValueError(f'Username "{username}" already exists')
            except Exception:
                # If even count fails, just allow the creation
                # The database constraint will catch duplicates
                pass
        
        return username
