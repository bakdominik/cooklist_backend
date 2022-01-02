# Generated by Django 3.2.5 on 2022-01-02 16:58

import cooklist_api.recipes.enums
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measure_type', models.CharField(choices=[('G', 'g'), ('ML', 'ml'), ('PCS', 'pcs'), ('GLASS', 'glass'), ('SPOON', 'spoon'), ('TEASPOON', 'teaspoon')], default='G', max_length=50)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('preparation_time', models.DurationField()),
                ('servings', models.IntegerField()),
                ('public', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('utensils', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None)),
                ('type', enumfields.fields.EnumIntegerField(enum=cooklist_api.recipes.enums.RecipeType)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authored_recipes', to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(blank=True, related_name='recipes', to='recipes.Ingredient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScheduledRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('meal_type', enumfields.fields.EnumIntegerField(enum=cooklist_api.recipes.enums.MealType)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedule', to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ingredient',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ingredients', to='recipes.product'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipes.recipe'),
        ),
        migrations.CreateModel(
            name='RecipeStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='recipes.recipe')),
            ],
            options={
                'unique_together': {('recipe', 'step_number')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='ingredient',
            unique_together={('recipe', 'product', 'measure_type', 'amount')},
        ),
    ]
