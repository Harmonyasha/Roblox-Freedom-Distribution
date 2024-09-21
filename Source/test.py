import os
path = os.getcwd().replace("\\Source","")+"./AssetCache"
files = [f for f in os.listdir(path)]
for f in files:
    if f.endswith(".rbxm"):
        file_without_extension = f.replace(".rbxm", "")
        if file_without_extension in files:
            os.remove(os.path.join(path, file_without_extension))
        os.rename(os.path.join(path, f), os.path.join(path, file_without_extension))
