# settings/darkmode-context-processor.py
def dark_mode_preference(request):
    dark_mode = request.session.get('dark_mode', False)
    return {'dark_mode': dark_mode}
