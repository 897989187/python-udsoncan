from PyInstaller.utils.hooks import collect_submodules, collect_data_files
hiddenimports = collect_submodules('my_module')
datas = collect_data_files('my_module')