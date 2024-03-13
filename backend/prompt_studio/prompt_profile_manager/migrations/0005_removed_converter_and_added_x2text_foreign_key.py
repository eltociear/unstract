# Generated by Django 4.2.1 on 2024-02-23 11:10

import json

import django.db.models.deletion
from cryptography.fernet import Fernet
from django.conf import settings
from django.db import connection, migrations, models


def fill_with_default_x2text(apps, schema):
    ProfileManager = apps.get_model("prompt_profile_manager", "ProfileManager")
    AdapterInstance = apps.get_model("adapter_processor", "AdapterInstance")

    encryption_secret: str = settings.ENCRYPTION_KEY
    f: Fernet = Fernet(encryption_secret.encode("utf-8"))
    metadata = {
        "url": "http://unstract-unstructured-io:8000/general/v0/general"
    }
    json_string = json.dumps(metadata)
    metadata_b = f.encrypt(json_string.encode("utf-8"))

    adapter_instance = AdapterInstance(
        adapter_name="DefaultX2text",
        adapter_id="unstructuredcommunity|eeed506f-1875-457f-9101-846fc7115676",
        adapter_type="X2TEXT",
        adapter_metadata_b=metadata_b,
    )
    adapter_instance.save()
    ProfileManager.objects.filter(x2text__isnull=True).update(
        x2text=adapter_instance
    )


def reversal_x2text(*args):
    """Reversal is NOOP since x2text is simply dropped during reverse."""


def disable_triggers(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute(
            "ALTER TABLE adapter_adapterinstance DISABLE TRIGGER ALL;"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("adapter_processor", "0004_alter_adapterinstance_adapter_type"),
        (
            "prompt_profile_manager",
            "0004_rename_retrival_strategy_profilemanager_retrieval_strategy",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profilemanager",
            name="pdf_to_text_converters",
        ),
        migrations.RunPython(
            disable_triggers, reverse_code=migrations.RunPython.noop
        ),
        migrations.AddField(
            model_name="profilemanager",
            name="x2text",
            field=models.ForeignKey(
                db_comment="Field to store the X2Text Adapter chosen by the user",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="profile_manager_x2text",
                to="adapter_processor.adapterinstance",
            ),
        ),        
    ]
