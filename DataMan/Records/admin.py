from django.contrib import admin
from Records.models import *

# Register your models here.

admin.site.register(Sample)
admin.site.register(Experiment)
admin.site.register(Dataset)
admin.site.register(InstrumentSetting)
admin.site.register(Instrument)
admin.site.register(ExperimentalDesign)
admin.site.register(Protocol)
admin.site.register(fileStatusOption)

admin.site.register(FileRead)