from pathlib import Path

block_cipher = None
base_path = Path('.').absolute()

a = Analysis(
    ['src/main.py'],
    pathex=[str(base_path)],
    binaries=[],
    datas=[
        (str(base_path / 'data'), 'data'),
    ],
    hiddenimports=[
        'tensorflow',
        'cv2',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='handsup-backend',
    debug=False,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='handsup-backend',
)