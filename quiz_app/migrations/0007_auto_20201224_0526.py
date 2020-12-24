# Generated by Django 3.1.4 on 2020-12-24 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0006_student_studentquiztrack'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentquiztrack',
            name='Score',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='StudentQuesAnsTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_answer', models.IntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz_app.questions')),
            ],
        ),
    ]