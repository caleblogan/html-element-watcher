from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from .models import WatchedElement
from .tasks import check_html_element_task
from config import celery_app


@login_required
def home(request):
    context = {
        'watched_elements': WatchedElement.objects.filter(user=request.user)
    }
    return render(request, 'watcher/home.html', context=context)


class WatchedElementDetailView(LoginRequiredMixin, generic.DetailView):
    model = WatchedElement

    def get_object(self, queryset=None):
        return get_object_or_404(WatchedElement, id=self.kwargs['pk'], user=self.request.user)


class WatchedElementCreateView(LoginRequiredMixin, generic.CreateView):
    model = WatchedElement
    fields = ['url', 'html_element', 'check_interval_hours', 'callback_url']
    template_name = 'watcher/watchedelement_create_form.html'
    success_url = reverse_lazy('watcher:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        task = check_html_element_task.delay(form.instance.id)
        form.instance.cur_task_id = task.id
        return super().form_valid(form)


class WatchedElementUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = WatchedElement
    fields = ['url', 'html_element', 'check_interval_hours', 'callback_url']
    template_name = 'watcher/watchedelement_create_form.html'
    success_url = reverse_lazy('watcher:home')

    def form_valid(self, form):
        celery_app.control.revoke(form.instance.cur_task_id)
        task = check_html_element_task.delay(form.instance.id)
        form.instance.cur_task_id = task.id
        return super().form_valid(form)


@csrf_exempt
def cb_test(request):
    print('cb info:', request.POST)
    return JsonResponse({'status': 'success'})
