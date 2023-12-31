from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list import ListView
from youtube_history.models import Video, Playlist, Sorting
from datetime import datetime, date, timedelta
import json
import logging

logger = logging.getLogger(__name__)

@csrf_protect
def index(request):

    #SELECTED DATE
    selected_date_str = request.POST.get('datepicker')
    if(selected_date_str != None):
        logger.info('Selected Date: ' + selected_date_str)
    else:
        logger.info('Selected Date: None')
    if(selected_date_str == '' or selected_date_str == None):
        selected_date = datetime.now()
        selected_date_str = datetime.now().strftime('%d.%m.%Y')
    else:
        if(len(selected_date_str) <= 5):
            selected_date_str = datetime.now().strftime('%d.%m.%Y')
        selected_date = datetime.strptime(selected_date_str, '%d.%m.%Y')

    #Videos by Date
    videos = Video.objects.filter(
        duration__gt = timedelta(minutes=1),
        published_at__year__lte = selected_date.year,
        published_at__month = selected_date.month,
        published_at__day = selected_date.day,
    )

    #All Playlists
    '''
    all_playlists = Playlist.objects.filter(
        id__in = [v.playlist.id for v in videos]
    ).values()
    '''
    all_playlists = Playlist.objects.all().values()

    #FILTER
    checked_playlist_ids = request.POST.getlist('playlist')
    if(checked_playlist_ids == [] or checked_playlist_ids == None):
        logger.info('Filter: None')
        if('playlist' in request.session):
            checked_playlist_ids = request.session['playlist']
        else:
            checked_playlist_ids = [p['id'] for p in all_playlists]
    else:
        logger.info('Filter:\n' + '\n'.join(checked_playlist_ids))
        request.session['playlist'] = checked_playlist_ids
    checked_playlists = Playlist.objects.filter(
        id__in = checked_playlist_ids
    ).values()
    
    #Videos by Checked Playlist
    videos = videos.filter(playlist__in = checked_playlist_ids)

    #Count Videos per Checked Playlist
    checked_playlists_extended = []
    for p in checked_playlists:
        video_count = len(videos.filter(playlist_id = p['id']))
        if(video_count > 0):
            checked_playlists_extended.append({
                'Playlist': p,
                'Count': video_count
            })

    #SORTING
    selected_sorting_item = request.POST.get('sorting')       
    if(selected_sorting_item == '' or selected_sorting_item == None):
        logger.info('Sorting: None')
        if('sorting' in request.session):
            selected_sorting_item = request.session['sorting']
        else:
            selected_sorting_item = 'default'
    else:
        logger.info('Sorting: ' + selected_sorting_item)
        request.session['sorting'] = selected_sorting_item
    all_sorting_items = Sorting.objects.values()

    if(selected_sorting_item == 'default'):
        videos = videos.order_by(
            'playlist__rank', 
            '-published_at__year', 
            'published_at__hour', 
            'published_at__minute', 
            'title')
    else:
        ascending_obj = all_sorting_items.filter(column_name = selected_sorting_item).values('ascending')[0]
        order_by_column = ''
        if(ascending_obj['ascending'] == False):
            order_by_column = '-'
        order_by_column += selected_sorting_item
        videos = videos.order_by(order_by_column)

    context = { 
        'selected_date_str': selected_date_str,
        'videos': videos,
        'all_playlists': all_playlists,
        'checked_playlists': checked_playlists,
        'checked_playlists_extended': checked_playlists_extended,
        'checked_playlist_ids': checked_playlist_ids,
        'sorting': {
            'selected': selected_sorting_item, 
            'all': all_sorting_items
        }
    }
    
    response = render(request, 'index.html', context)
    return response

def privacy(request):
    return render(request, 'privacy.html')