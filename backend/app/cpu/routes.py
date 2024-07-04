from app.cpu import views

def setup_routes(app):
    app.router.add_view("/api/cpu_loads", views.ListCPULoadView)
    app.router.add_view("/api/cpu_load_last_hour", views.GetCPULoadLastHourView)
    app.router.add_view("/api/cpu_load_per_minute", views.GetCPULoadLastHourPerMinuteView)

