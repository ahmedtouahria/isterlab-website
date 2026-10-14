from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('chatbot', '0002_category_message_response_delete_inquiry'),
        ('landing', '0008_contactpartner_country_contactpartner_cv_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='blogs',
            field=models.ManyToManyField(blank=True, related_name='blogs', to='landing.blog'),
        ),
    ]
