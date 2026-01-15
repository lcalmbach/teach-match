from school_management.models import CustomUser

CustomUser.objects.create_superuser(
    email='lukas.calmbach@bs.ch',
    password='password',
    first_name='Lukas',
    last_name='Calmbach'
)