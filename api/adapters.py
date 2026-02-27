from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Check a session variable or query param sent from Flutter 
        # to decide if they are a TAILOR or CUSTOMER
        role = request.GET.get('role', 'CUSTOMER') 
        user.role = role
        user.save()
        return user