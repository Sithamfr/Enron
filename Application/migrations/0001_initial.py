# Generated by Django 2.1.5 on 2019-05-07 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='adresses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employe', models.IntegerField()),
                ('adresse', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='destinataires',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('en_tant_que', models.CharField(max_length=3)),
                ('desti', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_enron.adresses')),
            ],
        ),
        migrations.CreateModel(
            name='employes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=20)),
                ('prenom', models.CharField(max_length=20)),
                ('login', models.CharField(max_length=20, unique=True)),
                ('poste', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='mails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('objet', models.CharField(default='', max_length=400)),
                ('corps', models.TextField()),
                ('discu', models.PositiveIntegerField(default=0)),
                ('expe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_enron.adresses')),
            ],
        ),
        migrations.CreateModel(
            name='references',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dossier', models.CharField(default='', max_length=200)),
                ('id_original', models.CharField(default='', max_length=60)),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_enron.mails')),
            ],
        ),
        migrations.AddField(
            model_name='destinataires',
            name='mail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_enron.mails'),
        ),
    ]