from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_account_already_exists_mail(self, *args, **kwargs):
        """
        We don't need this feature ever. Nobody wants it. I swear.
        """
        pass
