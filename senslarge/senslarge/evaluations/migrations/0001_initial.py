# Generated by Django 2.0.4 on 2019-05-19 14:07

from django.conf import settings
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
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie_text', models.TextField(blank=True, max_length=200, verbose_name='Texte')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('choice_text', models.TextField(blank=True, verbose_name='Texte')),
                ('valorisation', models.CharField(choices=[('0', '0'), ('+1', '+1'), ('+2', '+2'), ('+3', '+3'), ('-1', '-1'), ('-2', '-2'), ('-3', '-3')], default=0, max_length=2, verbose_name='Valorisation')),
                ('categorie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='choixcategories', to='evaluations.Categorie', verbose_name='Catégorie')),
            ],
            options={
                'ordering': ('question', 'order'),
            },
        ),
        migrations.CreateModel(
            name='ChoiceUtilisateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur_entier', models.IntegerField(default=0)),
                ('reference_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choiceusers', to='evaluations.Choice')),
                ('reference_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Formulaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200, verbose_name='Titre')),
                ('introduction', models.TextField(verbose_name='Introduction')),
                ('type_form', models.CharField(choices=[('PONDERATION', 'Ponderation'), ('SELECTION', 'Selection'), ('SELECTION_VALORISATION', 'Selection and Valorisation')], max_length=26, verbose_name='Type')),
                ('nb_points', models.IntegerField(default=0, help_text='À répartir entre les choix', verbose_name='Nombre de points')),
                ('typegraphe', models.CharField(choices=[('radar', 'radar'), ('barres', 'barres')], max_length=7, verbose_name='Graphique')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('question_text', models.TextField(verbose_name='Texte')),
                ('formulaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='evaluations.Formulaire', verbose_name='Formulaire')),
            ],
            options={
                'ordering': ('formulaire', 'order'),
            },
        ),
        migrations.CreateModel(
            name='TicketFormulaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('formul', models.ManyToManyField(related_name='tickets', to='evaluations.Formulaire')),
                ('users_lien', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='formulaires', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='evaluations.Question', verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='categorie',
            name='formulaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='evaluations.Formulaire', verbose_name='Formulaire'),
        ),
    ]
