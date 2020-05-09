# Copy paste the script in `python manage.py shell`
import json
from blog.models import Post


def bulk_post(file_name):
    with open(file_name, 'r') as fp:
        posts_json = json.load(fp)
        for p in posts_json:
            post = Post(title=p['title'], content=p['content'], author_id=p['author'])
            post.save()

bulk_post('scripts/posts.json')