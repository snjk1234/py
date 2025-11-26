# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

# Collect all necessary data and metadata
datas = []
datas += copy_metadata('streamlit')
datas += copy_metadata('altair')
datas += copy_metadata('pandas')
datas += copy_metadata('pillow')
datas += copy_metadata('validators')
datas += copy_metadata('importlib_metadata')
datas += collect_data_files('streamlit')
datas += collect_data_files('altair')

# Add project files
datas += [
    ('utils', 'utils'),
    ('credentials.json', '.'),
]

# Collect hidden imports
hiddenimports = []
hiddenimports += collect_submodules('streamlit')
hiddenimports += collect_submodules('altair')
hiddenimports += [
    'pandas',
    'gspread',
    'oauth2client',
    'openpyxl',
    'xlsxwriter',
    'plotly',
    'click',
    'validators',
    'watchdog',
    'tornado',
    'importlib_metadata',
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='نظام_عمولة_المشرفين',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # يمكنك إضافة أيقونة هنا
)
