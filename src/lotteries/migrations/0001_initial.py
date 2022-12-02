# Generated by Django 3.1.4 on 2022-12-02 17:45

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LotteryGame',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('numbers', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(db_index=True), default=list, size=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('winning_game', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lottery_games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]