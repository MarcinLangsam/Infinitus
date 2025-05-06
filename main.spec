import os
import sys

# Wyczyść sys.path, aby zapobiec problemom z nieprawidłowymi ścieżkami
sys.path = [p for p in sys.path if p and isinstance(p, str) and os.path.exists(p)]

# Określ folder projektu
project_dir = os.getcwd()

# Zasoby projektu
datas = [
    (os.path.join(project_dir, 'mymain.kv'), '.'),
    (os.path.join(project_dir, 'graphics'), 'graphics'),
    (os.path.join(project_dir, 'status_list.txt'), '.'),
    (os.path.join(project_dir, 'skill_list.txt'), '.'),
    (os.path.join(project_dir, 'save_game.txt'), '.'),
    (os.path.join(project_dir, 'items_list.txt'), '.'),
    (os.path.join(project_dir, 'enemy_skill_list.txt'), '.'),
    (os.path.join(project_dir, 'weapon_anim.atlas'), '.'),
    (os.path.join(project_dir, 'enemy_anim.atlas'), '.'),
    (os.path.join(project_dir, 'character_anim.atlas'), '.')
]

# Binaria (pozostawiamy puste, ponieważ Kivy automatycznie dołącza potrzebne DLL-e)
binaries = []

# Ręczne określenie kluczowych modułów Kivy
hiddenimports = [
    'kivy',
    'kivy.app',
    'kivy.uix.label',
    'kivy.uix.button',
    'kivy.uix.image',
    'kivy.uix.screen',
    'kivy.uix.screenmanager',
    'kivy.uix.boxlayout',
    'kivy.uix.gridlayout',
    'kivy.uix.scrollview',
    'kivy.uix.progressbar',
    'kivy.core.window',
    'kivy.core.audio',
    'kivy.core.image',
    'kivy.graphics',
    'kivy.clock',
    'kivy.event',
    'kivy.properties',
    'kivy.lang',
    'kivy.animation',
    'kivy.uix.widget',
    'kivy.uix.behaviors',
    'kivy.uix.popup',
    'kivy.uix.textinput',
    'kivy.uix.dropdown',
    'kivy.uix.spinner',
    'kivy.uix.recycleview',
    'kivy.uix.tabbedpanel',
    'kivy.network.urlrequest',
    'kivy.storage.jsonstore'
]

# Konfiguracja analizy
a = Analysis(
    ['main.py'],
    pathex=[project_dir],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Tworzenie pliku PYZ
pyz = PYZ(a.pure)

# Tworzenie pliku EXE w trybie --onedir
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Zbieranie wszystkich plików w folderze (tryb --onedir)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)