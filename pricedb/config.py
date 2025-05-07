import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class PriceDbConfig:
    def __init__(self):
        self.config_path = self._get_config_path()
        self.config_data = self._load_config()

    def _get_config_path(self) -> Path:
        """Get the path to the configuration file."""
        config_dir = None
        
        # Check for XDG_CONFIG_HOME environment variable
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            config_dir = Path(xdg_config) / "pricedb"
        else:
            # Default to platform-specific config directory
            home = Path.home()
            if os.name == "posix":  # Linux/Mac
                config_dir = home / ".config" / "pricedb"
            elif os.name == "nt":  # Windows
                config_dir = home / "AppData" / "Roaming" / "pricedb" / "config"
        
        if not config_dir:
            raise RuntimeError("Could not determine configuration directory")
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "pricedb.yaml"

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not self.config_path.exists():
            return {}
        
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f) or {}

    def save_config(self):
        """Save configuration to file."""
        with open(self.config_path, "w") as f:
            yaml.dump(self.config_data, f)

    @property
    def prices_path(self) -> Optional[str]:
        return self.config_data.get("prices_path")

    @prices_path.setter
    def prices_path(self, value: str):
        self.config_data["prices_path"] = value
        self.save_config()

    def get_value(self, key: str) -> Any:
        return self.config_data.get(key)

    def set_value(self, key: str, value: Any):
        self.config_data[key] = value
        self.save_config()
