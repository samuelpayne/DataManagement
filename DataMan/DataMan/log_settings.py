LOGGING = {
	'version':1,
	'disable_existing_loggers': False,
	'formatters':{
		'large':{
			'format':'%(asctime)s  %(levelname)s  %(process)d  %(pathname)s  %(funcName)s  %(lineno)d  %(message)s  '
		},
		'tiny':{
			'format':'%(asctime)s  %(message)s  '
		}
	},
	'handlers':{
		'errors_file':{
			'level':'ERROR',
		       'class':'logging.handlers.TimedRotatingFileHandler',
			'when':'midnight',
			'interval':1,
			'filename':'logs/ErrorLoggers.log',
			'formatter':'large',
		},
		'info_file':{
			'level':'INFO',
		       'class':'logging.handlers.TimedRotatingFileHandler',
			'when':'midnight',
			'interval':1,
			'filename':'logs/InfoLoggers.log',
			'formatter':'large',
		},
		'debug_file':{
			'level':'DEBUG',
		       'class':'logging.handlers.TimedRotatingFileHandler',
			'when':'midnight',
			'interval':1,
			'filename':'logs/DebugLoggers.log',
			'formatter':'large',
		},
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': 'logs/django_request.log',
                'formatter':'large',
		},
	},
	'loggers':{
        '': {
            'handlers': ['errors_file'],
            'level': 'DEBUG',
            'propagate': True
        },
		'error_logger':{
			'handlers':['errors_file'],
			'level':'WARNING',
			'propagate':True,
		},
		'info_logger':{
			'handlers':['info_file'],
			'level':'INFO',
			'propagate':True,
		},
		'debug_logger':{
			'handlers':['debug_file'],
			'level':'DEBUG',
			'propagate':True,
		},
        'django.request': {
            'handlers': ['request_handler'],
		},
	},
}
