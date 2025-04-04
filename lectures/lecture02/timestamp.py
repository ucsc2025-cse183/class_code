from datetime import datetime, timezone
now = datetime.now(timezone.utc)
timestamp = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
