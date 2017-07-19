from .base import DEBUG

if DEBUG == True:
	from .local import *
else:
	from .production import *