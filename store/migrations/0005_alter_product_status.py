# Generated by Django 5.0.4 on 2024-07-17 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('待上架', '待上架'), ('上架中', '上架中'), ('刪除', '刪除')], default='上架中', max_length=50),
        ),
    ]
