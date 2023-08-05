import os
import json
import argparse
from datetime import datetime, timedelta

from tqdm import tqdm
import isodate
import googleapiclient.discovery
import googleapiclient.errors

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils import timezone
from youtube_history.models import Playlist, Video, Category, Tag
import youtube_history

class Command(BaseCommand):

    #constants
    api_service_name = 'youtube'
    api_version = 'v3'
    youtube_url = 'https://youtu.be/'
    api_key = settings.API_KEY
    page_size_videos = 50
    page_size_comments = 100
    request_counter = 0
    next_list = False

    def get_playlist_items(self, youtube, playlist_id, page, max=50):
        try:
            request = youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=playlist_id,
                    maxResults=max,
                    pageToken=page
                )
            self.request_counter += 1
            return request.execute()
        except googleapiclient.errors.HttpError as err:
            if err.status_code == 403 and err.error_details[0]['reason'] == 'quotaExceeded':
                print(err.reason)
                return None
            else:
                print('Playlist {0} could not be retrieved! {1}'.format(playlist_id, err))
        return None

    def get_video_infos(self, youtube, video_ids, max=50):
        try:
            request = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=video_ids,
                    maxResults=max
                )
            self.request_counter += 1
            return request.execute()
        except googleapiclient.errors.HttpError as err:
            if err.status_code == 403 and err.error_details[0]['reason'] == 'quotaExceeded':
                print(err.reason)
                return None
            else:
                print('Infos for Videos {0} could not be retrieved! {1}'.format(video_ids, err))
        return None
        
    def get_category(self, youtube, category_id):

        try:
            existing_category = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            existing_category = None

        if(existing_category == None):

            try:
                request = youtube.videoCategories().list(
                    part="snippet",
                    id=category_id
                )
                self.request_counter += 1
                response = request.execute()
            except googleapiclient.errors.HttpError as err:
                if err.status_code == 403 and err.error_details[0]['reason'] == 'quotaExceeded':
                    print(err.reason)
                    return None
                else:
                    print('Category {0} could not be retrieved! {1}'.format(category_id, err))

            new_category = Category(
                id=category_id,
                title=response['items'][0]['snippet']['title']
            )

            try:
                new_category.save()
            except Exception as err:
                print('Category {0} could not be saved', category_id)

            return new_category
        
        else:

            return existing_category
    
    def get_comments(self, youtube, video_id, page, max=100):
        try:
            request = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=video_id,
                    maxResults=max,
                    pageToken=page
                )
            self.request_counter += 1
            return request.execute()
        except googleapiclient.errors.HttpError as err:
            if err.status_code == 403 and err.error_details[0]['reason'] == 'quotaExceeded':
                print(err.reason)
                return None
            elif err.status_code == 403 and err.error_details[0]['reason'] == 'commentsDisabled':
                print(err.reason)
                return None
            else:
                print('Comments for Video {0} could not be retrieved! {1}'.format(video_id, err))
        return None

    def get_top_comment(self, response):
        top_comment = None
        top_comment_likes = 0
        if(response != None):
            for c in response['items']:            
                comment_snippet = c['snippet']['topLevelComment']['snippet']
                if(comment_snippet['likeCount'] > 0 and comment_snippet['likeCount'] >= top_comment_likes):
                    top_comment_likes = comment_snippet['likeCount']
                    top_comment = comment_snippet
            return top_comment
        else:
            return None
    
    def get_attribute(self, dict, key):
        if key in dict:
            return dict[key]
        else:
            return None
        
    def save_videos(self, youtube, playlist, response_videos):

        latest_video = None
        try:
            if playlist != None:
                latest_video = Video.objects.filter(playlist__id=playlist.id).order_by('-published_at').values('published_at')
                video_count = latest_video.count()
        except ObjectDoesNotExist:
            latest_video = None

        for v in (pbarVideo := tqdm(response_videos['items'])):

            #reset
            top_comment = None
            page_token_comments = ''

            video_id = v['id']
            video_snippet = v['snippet']

            #check for latest video in database
            publish_date = datetime.strptime(video_snippet['publishedAt'], '%Y-%m-%dT%H:%M:%S%z')
            if(latest_video != None and video_count > 0 and latest_video[0]['published_at'] == publish_date):
                self.next_list = True
                break

            if playlist == None:
                playlist = Playlist.objects.get(id=Video.objects.get(id=video_id).playlist_id)
                if playlist == None:
                    print('Video does not belong to any available Playlist!')
                    return

            pbarVideo.set_description_str(video_snippet['title'] + ' [' + publish_date.strftime('%d.%m.%Y') + ']')
            
            #insert/update video
            video = Video(
                id=video_id,
                title=video_snippet['title'].replace(';', ''),
                published_at =  publish_date,
                duration = isodate.parse_duration(v['contentDetails']['duration']),
                view_count = self.get_attribute(v['statistics'], 'viewCount'),
                like_count = self.get_attribute(v['statistics'], 'likeCount'),
                comment_count = self.get_attribute(v['statistics'], 'commentCount'),
                thumbnail_url = video_snippet['thumbnails']['high']['url'],
                video_url = self.youtube_url + video_id
            )

            #get top comment
            response_comments = self.get_comments(youtube, video_id, page_token_comments, self.page_size_comments)
            if response_comments != None and "nextPageToken" in response_comments:
                page_token_comments = response_comments['nextPageToken']
                while (page_token_comments != ''):
                    top_comment = self.get_top_comment(response_comments)
                    if response_comments != None and "nextPageToken" in response_comments:
                        page_token_comments = response_comments['nextPageToken']
                        response_comments = self.get_comments(youtube, video_id, page_token_comments, self.page_size_comments)
                    else:
                        page_token_comments = ''
            else:
                top_comment = self.get_top_comment(response_comments)
                            
            #set top comment
            if(top_comment != None):
                video.top_comment_text = top_comment['textDisplay']
                video.top_comment_likes = top_comment['likeCount']
                video.top_comment_author = top_comment['authorDisplayName']

            #set playlist
            video.playlist = Playlist.objects.get(id=playlist.id)

            #set category
            video.category = self.get_category(youtube, video_snippet['categoryId'])

            #save video
            try:
                video.save()
            except Exception as err:
                print('Video {0} could not be saved! {1}'.format(video_id, err))
                continue

            #set tags
            tags = self.get_attribute(video_snippet, 'tags')
            if(tags != None):
                for t in tags:
                    try:
                        existing_tag = Tag.objects.get(name=t)
                    except ObjectDoesNotExist:
                        existing_tag = None

                    if(existing_tag == None):
                        new_tag = Tag(name=t)
                        try:
                            new_tag.save()
                        except Exception as err:
                            print('Tag {0} could not be saved', t)
                            continue
                        video.tag.add(new_tag)
                    else:
                        video.tag.add(existing_tag)

            try:
                playlist.request_count = self.request_counter
                playlist.save()
            except Exception as err:
                print('Playlist {0} could not be saved! {1}'.format(playlist.id, err))
        
    def add_arguments(self, parser):
        parser.add_argument("--initialize", nargs="+")
        parser.add_argument("--limit", nargs="+")
        parser.add_argument("--videos", nargs="+")
        parser.add_argument("--reset", nargs="+")

    def handle(self, *args, **options):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        youtube = googleapiclient.discovery.build(self.api_service_name, self.api_version, developerKey = self.api_key)

        #delete all tables
        if(options['reset'] and options['reset'][0] in ['True', 'true', '1']):
            Video.objects.all().delete()
            Playlist.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()

        #limit for last API call
        limit = 0
        if(options['limit']):
            limit = options['limit'][0]

        if(options['videos']):

            video_ids = options['videos'][0]
            response_videos = self.get_video_infos(youtube, video_ids, self.page_size_videos)
            self.save_videos(youtube, None, response_videos)

        else:

            #playlists from JSON
            playlists_json = None
            if(options['initialize']):
                json_file = options['initialize'][0]
                pth = os.path.dirname(youtube_history.__file__) + '\\management\\commands\\'
                with open(pth + '\\' + json_file) as f:
                    playlists_json = json.load(f)['playlists']

            #playlists from database
            try:
                playlists_database = Playlist.objects.filter(status='a').values('id', 'title')
            except ObjectDoesNotExist:
                playlists_database = None

            #save playlists from JSON
            if(playlists_json != None and playlists_database == None or playlists_database.count() == 0):          
                for p in playlists_json:
                    playlists_database = Playlist(
                        id=p['id'],
                        rank=p['rank'],
                        title=p['title'],
                        color=p['color'],
                        channel_id=p['channel_id'],
                        channel_title=p['channel_title']
                    )
                    playlists_database.save()
                playlists = playlists_json
            #load playlists from JSON
            elif(playlists_json != None and len(playlists_json) > 0):
                playlists = playlists_json
            #load playlists from database
            else:
                playlists = playlists_database

            #Playlists
            for p in playlists:

                #reset
                page_token_videos = ''
                self.next_list = False
                video_count = 0
                total_videos_diff = 0

                playlist_id = p['id']
                playlist = Playlist.objects.get(pk=playlist_id)

                #get last call
                if(playlist.last_api_call != None and playlist.last_api_call >= (timezone.now() - timedelta(days=limit))):
                    continue

                #get request count
                self.request_counter = playlist.request_count

                #get last token
                if(playlist.page_token != None):
                    page_token_videos = playlist.page_token

                #count videos in database
                try:
                    latest_video = Video.objects.filter(playlist__id=playlist_id).order_by('-published_at').values('published_at')
                    video_count = latest_video.count()
                except ObjectDoesNotExist:
                    latest_video = None

                #get total items
                response_playlist = self.get_playlist_items(youtube, playlist_id, page_token_videos, self.page_size_videos)
                if response_playlist == None:
                    continue

                total_videos = response_playlist['pageInfo']['totalResults']
                playlist.total_videos = total_videos
                total_videos_diff = total_videos - video_count

                print('Number of Videos in Database for Playlist ' + playlist.title + ': ' + str(video_count))

                #Videos per Playlist
                for i in (pbarPlaylist := tqdm(range(0, total_videos_diff, self.page_size_videos))):

                    video_number = video_count + (pbarPlaylist.last_print_n * self.page_size_videos)
                    pbarPlaylist.set_description_str(p['title'] + ' - ' + str(video_number) + '/' + str(total_videos) + ' Videos [' + str(playlist.request_count) + ' Requests]')

                    if page_token_videos != '':
                        response_playlist = self.get_playlist_items(youtube, playlist_id, page_token_videos, self.page_size_videos)

                    if response_playlist == None or self.next_list == True:
                        break

                    if "nextPageToken" in response_playlist:
                        page_token_videos = response_playlist['nextPageToken']
                        playlist.page_token = page_token_videos
                        try:
                            playlist.save()
                        except Exception as err:
                            print('Playlist {0} could not be saved! {1}'.format(playlist_id, err))

                    #get video ids and retrieve video infos
                    video_ids = ','.join([i['contentDetails']['videoId'] for i in response_playlist['items']])
                    response_videos = self.get_video_infos(youtube, video_ids, self.page_size_videos)
                    
                    #Videos
                    self.save_videos(youtube, playlist, response_videos)
    
                try:
                    playlist.last_api_call = timezone.now()
                    playlist.page_token = None
                    playlist.request_count = 0
                    playlist.save()
                except Exception as err:
                    print('Playlist {0} could not be saved! {1}'.format(playlist_id, err))
                    continue