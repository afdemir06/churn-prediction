import os
import joblib
import json

def get_next_version(directory="models"):
    current_dir=os.path.dirname(os.path.abspath(__file__))
    base_dir=os.path.dirname(current_dir)
    os.makedirs(f"{base_dir}/{directory}",exist_ok=True)
    MODELS_PATH=os.path.join(base_dir,directory)

    files=[f for f in os.listdir(MODELS_PATH) if f.endswith(".joblib")]
    if not files:
        return 1

    versions=[int(f.split("_v")[1].split(".")[0]) for f in files]
    return max(versions)+1

def save_model(pipeline,feature_names):
    version=get_next_version()
    file_name=f"models/model_v{version}.joblib"
    metadata_file_name=f"models/model_v{version}_metadata.json"
    joblib.dump(pipeline,file_name)
    metadata={
        "features":feature_names,
        "version":f"v{version}"
    }
    with open(metadata_file_name,"w") as f:
        json.dump(metadata,f,indent=4)
    return version