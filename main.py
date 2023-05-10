import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import (
    ItemEnterEvent,
    KeywordQueryEvent,
    PreferencesEvent,
)
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import json
import os
from fuzzywuzzy import process


class NerdFontsExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(PreferencesEvent, OnLoad())
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.nerdfonts_icons = []
        self.nerdfonts_names = []


class ItemEnterEventListener(EventListener):
    def on_event(self, event: ItemEnterEvent, extension: NerdFontsExtension):
        cmd = 'echo -e "{}"| xclip -selection clipboard'.format(
            event.get_data())
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)


class KeywordQueryEventListener(EventListener):
    def on_event(self, event: KeywordQueryEvent, extension: NerdFontsExtension):
        items = []
        filterd = []
        filterd = filter(extension.nerdfonts_names, event.get_argument())
        for i in filterd:
            idx = extension.nerdfonts_names.index(i)
            j = extension.nerdfonts_icons[idx]
            items.append(
                ExtensionResultItem(
                    icon="img/nerd-fonts-character-logo-md.png",
                    name=j["icon"],
                    description=j["name"],
                    on_enter=ExtensionCustomAction(
                        data=j["icon"],
                        keep_app_open=False,
                    ),
                )
            )

        return RenderResultListAction(items)


class OnLoad(EventListener):
    def on_event(self, event, extension: NerdFontsExtension):
        current_path = os.path.dirname(os.path.abspath(__file__))
        json_open = open(current_path + "/nerdfonts.json")
        extension.nerdfonts_icons = json.load(json_open)
        extension.nerdfonts_names = [r["name"]
                                     for r in extension.nerdfonts_icons]
        return super().on_event(event, extension)


def filter(names, query):
    if query == None:
        return names[:10]
    res = process.extract(query, names, limit=10)
    return [r[0] for r in res]


if __name__ == "__main__":
    NerdFontsExtension().run()
