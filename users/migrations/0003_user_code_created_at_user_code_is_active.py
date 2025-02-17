# Generated by Django 5.1.3 on 2025-02-02 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="code_created_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="время создания кода"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="code_is_active",
            field=models.BooleanField(default=False, verbose_name="активность кода"),
        ),
    ]