-- SQLite
SELECT 
    id,
    published_at,
    modified_on,
    title
FROM youtube_history_video
WHERE playlist_id = 'UUQvTDmHza8erxZqDkjQ4bQQ'
ORDER BY published_at DESC;