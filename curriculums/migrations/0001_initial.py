# Generated by Django 2.2.5 on 2019-09-17 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0002_course_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('attachment_url', models.CharField(max_length=100)),
                ('file_type', models.CharField(max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
            options={
                'db_table': 'curriculums',
            },
        ),
    ]
