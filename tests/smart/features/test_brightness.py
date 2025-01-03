import pytest

from kasa.iot import IotDevice
from kasa.smart import SmartDevice

from ...conftest import dimmable_iot, get_parent_and_child_modules, parametrize

brightness = parametrize("brightness smart", component_filter="brightness")


@brightness
async def test_brightness_component(dev: SmartDevice):
    """Test brightness feature."""
    brightness = next(get_parent_and_child_modules(dev, "Brightness"))
    assert brightness
    assert isinstance(dev, SmartDevice)
    assert "brightness" in dev._components

    # Test getting the value
    feature = brightness._device.features["brightness"]
    assert isinstance(feature.value, int)
    assert feature.value > 1
    assert feature.value <= 100

    # Test setting the value
    await feature.set_value(10)
    await dev.update()
    assert feature.value == 10

    with pytest.raises(ValueError, match="out of range"):
        await feature.set_value(feature.minimum_value - 10)

    with pytest.raises(ValueError, match="out of range"):
        await feature.set_value(feature.maximum_value + 10)


@dimmable_iot
async def test_brightness_dimmable(dev: IotDevice):
    """Test brightness feature."""
    assert isinstance(dev, IotDevice)
    assert "brightness" in dev.sys_info or bool(dev.sys_info["is_dimmable"])

    # Test getting the value
    feature = dev.features["brightness"]
    assert isinstance(feature.value, int)
    assert feature.value > 0
    assert feature.value <= 100

    # Test setting the value
    await feature.set_value(10)
    await dev.update()
    assert feature.value == 10

    with pytest.raises(ValueError, match="out of range"):
        await feature.set_value(feature.minimum_value - 10)

    with pytest.raises(ValueError, match="out of range"):
        await feature.set_value(feature.maximum_value + 10)
