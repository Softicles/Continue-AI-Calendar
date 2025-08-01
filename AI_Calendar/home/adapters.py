from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialToken, SocialApp

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_token(self, request, sociallogin):
        token_data = getattr(sociallogin, 'token', None)
        account = getattr(sociallogin, 'account', None)

        if not token_data or not account:
            print("Adapter: token or account not found.")
            return

        try:
            if account.user_id is None:
                account.user = sociallogin.user
                
            # Save accounts if not saved
            if account.pk is None:
                account.save()
            
            app = SocialApp.objects.get(provider=account.provider)
            token, created = SocialToken.objects.get_or_create(
                account=account,
                app=app,
                defaults={
                    'token': token_data.token,
                    'token_secret': token_data.token_secret
                }
            )
            if not created:
                token.token = token_data.token
                token.token_secret = token_data.token_secret
                token.save()
                print("Adapter: Token updated.")
            else:
                print("Adapter: Token created.")
        except Exception as e:
            print("Adapter error saving token:", e)

    def pre_social_login(self, request, sociallogin):
        super().pre_social_login(request, sociallogin)
        self.save_token(request, sociallogin)
        
    def save_user_info(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # Extract user info
        extra_data = sociallogin.account.extra_data
        user.first_name = extra_data.get('given_name', '')
        user.last_name = extra_data.get('family_name', '')

        return user


