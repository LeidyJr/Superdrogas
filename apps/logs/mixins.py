from .models import LogApp

class LoggerFormMixin(object):
    def form_valid(self, form):
        logger = LogApp()
        try:
        	self.object = form.save(commit=False)
        except Exception:
        	pass
        logger.log(self.request, ("%s:%s")%(self.mensaje_log, self.object.id), "POST")
        return super(LoggerFormMixin, self).form_valid(form)

class LoggerGetMixin(object):
    def get(self, request, *args, **kwargs):
        logger = LogApp()
        logger.log(request, ("%s-%s:%s")%(self.mensaje_log, self.model.__name__, self.object.id), "GET")
        return super(LoggerGetMixin, self).get(request, *args, **kwargs)