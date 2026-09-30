import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jpt_holidays.settings')
application = get_wsgi_application()
app = application

# Auto-initialize database for Vercel ephemeral container
if os.getenv('VERCEL') or 'VERCEL' in os.environ:
    try:
        from django.core.management import call_command
        db_file = '/tmp/db.sqlite3'
        if not os.path.exists(db_file) or os.path.getsize(db_file) == 0:
            call_command('migrate', interactive=False)
            try:
                call_command('seed_data')
            except Exception as e:
                print("Auto-seed error:", e)
    except Exception as err:
        print("Auto-migrate error:", err)


