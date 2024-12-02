from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter

class User(AbstractUser):
        # address, address_detail, postcode 추가
    address = models.CharField(max_length=100)
    address_detail = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)



class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """ 
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        # address, address_detail, postcode 추가

        address = data.get("address")
        address_detail = data.get("address_detail")
        postcode = data.get("postcode")
        
        
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
            
        if address:
            user_field(user, "address", address)
        if address_detail:
            user_field(user, "address_detail", address_detail)
        if postcode:
            user_field(user, "postcode", postcode)

        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user
