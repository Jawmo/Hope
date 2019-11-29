import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # add additional fields in here

    first_name = models.CharField(max_length=30)
    char_name = models.CharField(max_length=50, blank=True)
    uuid_id = models.CharField(default=uuid.uuid4, editable=True, max_length=50)

    def __str__(self):
        return self.email

class Players(models.Model):

    unique_id = models.CharField(max_length=10, primary_key=True)
    uuid_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50, blank=True)
    entity_type = models.CharField(max_length=500, blank=False)
    description = models.CharField(max_length=999)
    gender = models.CharField(max_length=30)
    race = models.CharField(max_length=30)
    vitals = models.CharField(max_length=999, blank=True)
    core_attributes = models.CharField(max_length=999, blank=True)
    player_state = models.CharField(max_length=30, default="logged_out")
    conditions = models.CharField(default="{'stance': 'standing'}", max_length=255)
    stow_loc = models.CharField(max_length=100, blank=True)
    location = models.UUIDField(blank=True)


    def __str__(self):
        return self.description['name']

class Rooms(models.Model):
    # add additional fields in here
    unique_id = models.CharField(max_length=10, primary_key=True)
    uuid_id = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=150)
    name = models.CharField(max_length=999)
    description = models.CharField(max_length=999)
    exits = models.CharField(max_length=100)
    region = models.CharField(max_length=30, blank=True)
    zone = models.CharField(max_length=50, blank=True)
    elevation = models.CharField(max_length=30, blank=True)
    effects = models.CharField(max_length=500, blank=True)
    owner = models.CharField(max_length=30, blank=True)
    ship_id = models.CharField(max_length=36, blank=True)
    coordinates = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name, self.description

class Npcs(models.Model):
    # add additional fields in here
    unique_id = models.CharField(max_length=10, primary_key=True)
    uuid_id = models.CharField(max_length=50)
    join_table = models.CharField(max_length=50)
    description = models.CharField(max_length=999, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    race = models.CharField(max_length=30, blank=True)
    vitals = models.CharField(max_length=999, blank=True)
    core_attributes = models.CharField(default="{}", max_length=255, blank=True)
    npc_state = models.CharField(max_length=50, blank=True)
    conditions = models.CharField(max_length=500, blank=True)
    credit = models.CharField(max_length=50)
    supply = models.CharField(max_length=255, blank=True)
    demand = models.CharField(max_length=255, blank=True)
    home_loc = models.CharField(max_length=255, blank=True)
    demeanor = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50)


    def __str__(self):
        return self.description

class Items(models.Model):
    # add additional fields in here
    unique_id = models.CharField(max_length=10, primary_key=True)
    uuid_id = models.CharField(max_length=50)
    description = models.CharField(max_length=999)
    keyword = models.CharField(max_length=30)
    attributes = models.CharField(max_length=999, blank=True)
    dynamic_stats = models.CharField(max_length=30)
    room_target = models.CharField(max_length=30, blank=True)
    is_open = models.BooleanField(default=True)
    location = models.CharField(max_length=50)
    location_body = models.CharField(max_length=999, blank=True)
    owner = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.description

class Orgs(models.Model):
    # add additional fields in here
    unique_id = models.CharField(max_length=10, primary_key=True)
    uuid_id = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    org_desc = models.CharField(max_length=255, blank=True)
    supply = models.CharField(max_length=255, blank=True)
    demand = models.CharField(max_length=255, blank=True)
    home = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Wiki(models.Model):
    # add additional fields in here
    unique_id = models.CharField(max_length=10, primary_key=True)
    base_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255, blank=True)
    content = models.CharField(max_length=999, blank=True)
    usage = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

class News(models.Model):
    # add additional fields in here
    unique_id = models.CharField(max_length=999, primary_key=True)
    post_title = models.CharField(max_length=999, blank=True)
    post_date = models.DateField(max_length=999, blank=True)
    post_author = models.CharField(max_length=999, blank=True)
    post_content = models.TextField(max_length=999, blank=True)

    def __str__(self):
        return self.unique_id