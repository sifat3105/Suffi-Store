from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a regular user after validating email and normalizing it.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)  # Hashes the password automatically
        user.save(using=self._db)
        return user
    def create_staffuser(self, email, password=None):
        user = self.create_user(email,
                password=password
        )
        user.is_staff = True
        user.save(using=self._db)
        
        return user
    def create_superuser(self, email, password=None):
        user = self.create_user(email,
                password=password
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        
        return user