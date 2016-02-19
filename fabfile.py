import os


def validate():
    validate_cloudformation_files()


def validate_cloudformation_files():
    import boto3
    client = boto3.client('cloudformation')
    
    current_dir = os.path.dirname(__file__)
    cloudformation_dir = os.path.join(current_dir, 'cloudformation')
    cloudformation_files = []
    for (dirpath, dirnames, filenames) in os.walk(cloudformation_dir):
        cloudformation_files = [f for f in filenames if f.endswith('.json')]
        break
    
    for filename in cloudformation_files:
        print 'validating', filename
        file_path = os.path.join(cloudformation_dir, filename)
        template_body = open(file_path).read()
        client.validate_template(TemplateBody=template_body)
        
        
def sync_cassandra():
    from cassandra.cqlengine.management import sync_table, create_keyspace
    from benchmark.feeds import UserFeed, TimelineFeed
    create_keyspace('stream_framework', 'SimpleStrategy', 3)
    for feed_class in [UserFeed, TimelineFeed]:
        timeline = feed_class.get_timeline_storage()
        sync_table(timeline.model)