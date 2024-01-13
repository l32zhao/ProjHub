from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

# @receiver(post_save, sender=Profile)    # #the @a_new_decorator is just a short way of saying: a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
# def profileUpdated(sender, instance, created, **kwargs):
#     print('Profile Saved!')
#     print('Instance:', instance)
#     print('Created:', created)


# Triggle when instance's signal happen
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance                     # user = User()
        profile = Profile.objects.create(
            user=user,                      # profile.user = user
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        print(profile)
    

def deleteUser(sender, instance, **kwargs):
    user = instance.user                    # user = profile.user
    user.delete()
    print('Deleting user...')

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created == False:    # Avoid recursion
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
        
post_save.connect(createProfile, sender=User)   # Set Model of Profile as Sender
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)