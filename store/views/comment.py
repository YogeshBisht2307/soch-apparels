from django.shortcuts import redirect
from store.models import Comment, Cloth
from django.views.generic.base import View
from django.http import HttpResponse, response
from django.core.handlers.wsgi import WSGIRequest



class CommentView(View):
    def post(self, request: WSGIRequest) -> response.HttpResponseRedirect:
        comment = request.POST.get('comment')
        cloth: Cloth = Cloth.objects.get(cloth_slug=request.POST.get('cloth_slug'))
        if comment != "" and len(comment) > 4:
            user = request.user
            comments = Comment()
            comments.comment = comment
            comments.user = user
            comments.cloth = cloth
            comments.save()

        return redirect(request.POST.get('return_url'))
