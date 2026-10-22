from cs2esp.features.feature_registry import build_enabled_features


def test_only_enabled_features_built():
    cfg = {
        "features": {
            "esp": {"enabled": True},
            "aimbot": {"enabled": False},
            "radar": {"enabled": True},
        }
    }
    names = {f.name for f in build_enabled_features(cfg)}
    assert names == {"esp", "radar"}


def test_empty_config():
    assert build_enabled_features({}) == []
</br>