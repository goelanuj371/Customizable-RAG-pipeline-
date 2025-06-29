import os
import shutil

def run_setup():
    current_dir = os.getcwd()
    config_dest = os.path.join(current_dir, "config.yaml")

    if os.path.exists(config_dest):
        print("✅ config.yaml already exists in this directory.")
        return

    # Locate the default config inside the package directory
    default_config_path = os.path.join(current_dir, "customrag", "config", "default_config.yaml")

    if not os.path.exists(default_config_path):
        print(f"❌ Default config not found at {default_config_path}")
        return

    try:
        shutil.copy(default_config_path, config_dest)
        print("✅ config.yaml generated successfully!")
        print("🛠️  Please open it and fill in your provider, model, and API key.")
    except Exception as e:
        print("❌ Error copying config file:", e)

if __name__ == "__main__":
    run_setup()
