from django.template import loader
from django.http import HttpResponse

from wavepool.models import NewsPost
from wavepool.code_exercise_defs import code_exercise_defs, code_review_defs, code_design_defs
from django.conf import settings


def front_page(request):
    """ View for the site's front page
        Returns all available newsposts, formatted like:
            cover_story: the newsposts with is_cover_story = True
            top_stories: the 3 most recent newsposts that are not cover story
            archive: the rest of the newsposts, sorted by most recent
    """
    template = loader.get_template('wavepool/frontpage.html')
    # filter the NewsPost objects to find the one that is the cover story
    cover_story = NewsPost.objects.all().filter(is_cover_story=True)
    # filter the NewsPost objects that aren't the cover story and slice the most recent three out
    top_stories = NewsPost.objects.all().filter(is_cover_story=False).order_by('publish_date')[:3]
    # filter the next NewsPost objects that aren't the cover story and aren't the most recent three
    other_stories = NewsPost.objects.all().filter(is_cover_story=False).order_by('publish_date')[3:]

    context = {
        'cover_story': cover_story,
        'top_stories': top_stories,
        'archive': other_stories,
    }

    return HttpResponse(template.render(context, request))


def newspost_detail(request, newspost_id=None):
    template = loader.get_template('wavepool/newspost.html')
    # get the correct newspost by doing something like NewsPost.objects.get(id=newspost_id)
    newspost = NewsPost.objects.order_by('?').first()
    context = {
        'newspost': newspost
    }

    return HttpResponse(template.render(context, request))


def instructions(request):
    template = loader.get_template('wavepool/instructions.html')

    context = {
        'code_exercise_defs': code_exercise_defs,
        'code_design_defs': code_design_defs,
        'code_review_defs': code_review_defs,
        'show_senior_exercises': settings.SENIOR_USER,
    }
    return HttpResponse(template.render(context, request))
