from django.views import View
from django.shortcuts import render


class IndexView(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)