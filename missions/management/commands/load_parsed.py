import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

from django.core.management import BaseCommand, CommandError

from missions.models import *


class Command(BaseCommand):
    help = "Loads data from json dump"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        filepath = options.get("file", "")
        path = Path(filepath)
        if not path.exists():
            raise CommandError(f"Invalid file: {filepath}")

        with open(filepath, encoding="utf-8") as file:
            data = json.load(file)

        # Mission
        mission, _ = Mission.objects.get_or_create(
            title=data["title"], number=data["number"]
        )

        # Objectives
        Objective(
            title="Основная задача", text=data["main_task"], mission=mission
        ).save()

        for k, v in data["tasks"].items():
            objective = Objective(
                title=k[3:].strip().rstrip("."),
                text=v["text"],
                mission=mission,
                type=ObjectiveType.SECONDARY,
            )
            objective.save()

            for timg in v["images"]:
                img = ObjectiveImage(objective=objective)
                img.save()

                file = open(
                    os.path.abspath(
                        os.path.join(
                            "C:/users/tinytengu/desktop/mgsvimages",
                            os.path.basename(timg),
                        )
                    ),
                    "rb",
                )

                img.image.save(os.path.basename(timg), file, True)

                file.close()

        # Facts
        for ftext in data["facts"]:
            fact = Fact(text=ftext, mission=mission)
            fact.save()

        # Dialogs
        for (title, text) in data["dialogs"]:
            match = re.search(r"^(.+?):\s(.*)$", text)
            if not match:
                print(f"No character for '{title}'")
                character = Character.objects.first()
            else:
                character, created = Character.objects.get_or_create(
                    name=match.group(1)
                )
                if created:
                    print(f"Created character '{character.name}'")
                text = match.group(2).strip()

            dlg = Dialog(title=title, text=text, mission=mission, character=character)
            dlg.save()
