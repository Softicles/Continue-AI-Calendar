from allauth.socialaccount.models import SocialToken, SocialApp
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from allauth.socialaccount.signals import social_account_added, social_account_updated, pre_social_login
import logging

logger = logging.getLogger(__name__)

@receiver(social_account_added)
def fetch_and_log_token(sender, request, sociallogin, **kwargs):
    account = sociallogin.account
    logger.debug(f"social_account_added triggered for account: {account}")
    
    try:
        token = SocialToken.objects.get(account=account)
        logger.debug(f" Token found: {token.token}")
    except SocialToken.DoesNotExist:
        logger.error(f" No token found for account: {account}")


@receiver(user_logged_in)
def user_logged_in_receiver(request, user, **kwargs):
    print(f"User logged in: {user}")

@receiver(social_account_added)
def social_account_added_receiver(request, sociallogin, **kwargs):
    print("Social account added:", sociallogin.account)

@receiver(social_account_updated)
def social_account_updated_receiver(request, sociallogin, **kwargs):
    print("Social account updated:", sociallogin.account)

@receiver(pre_social_login)
def log_sociallogin_token(sender, request, sociallogin, **kwargs):
    print("SOCIALLOGIN DATA:")
    print("Token:", getattr(sociallogin.token, 'token', None))
    print("Token secret:", getattr(sociallogin.token, 'token_secret', None))
    
    # Avoid accessing .user directly
    if hasattr(sociallogin, 'account'):
        print("Provider:", sociallogin.account.provider)
        print("UID:", sociallogin.account.uid)
        