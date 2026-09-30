from .models import SiteSettings

def site_settings(request):
    try:
        settings_obj = SiteSettings.load()
    except Exception:
        settings_obj = None

    unread_notifications = 0
    if request.user.is_authenticated:
        unread_notifications = request.user.notifications.filter(is_read=False).count()

    return {
        'site_settings': settings_obj,
        'unread_notifications_count': unread_notifications,
    }
