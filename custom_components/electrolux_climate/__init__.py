# Copyright 2022 DotEfekts (original author)
# Copyright 2024 jnctech (modifications)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""The Electrolux Control integration."""
import base64

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from homeassistant.const import CONF_HOST, CONF_TIMEOUT, CONF_NAME, CONF_MAC
from homeassistant.components.climate.const import ATTR_MAX_TEMP, ATTR_MIN_TEMP

from broadlink import DEFAULT_TIMEOUT

from .const import PLATFORMS, DEFAULT_MIN, DEFAULT_MAX

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

# Example migration function
async def async_migrate_entry(hass, config_entry: ConfigEntry):
    if config_entry.version == 1:

        config_entry.version = 2

        if "ip" in config_entry.data:
            new = {**config_entry.data}

            new[CONF_NAME] = config_entry.title
            config_entry.title = "ELECTROLUX_OEM"

            new[CONF_HOST] = config_entry.data["ip"]
            new[CONF_MAC] = base64.b64decode(config_entry.data["mac"]).hex()
            new[CONF_TIMEOUT] = DEFAULT_TIMEOUT
            new[ATTR_MIN_TEMP] = DEFAULT_MIN
            new[ATTR_MAX_TEMP] = DEFAULT_MAX

            hass.config_entries.async_update_entry(config_entry, data=new)
    # if config_entry.version == 2:

    #     config_entry.version = 3
    #     new = {**config_entry.data}

    #     hass.config_entries.async_update_entry(config_entry, unique_id=new[CONF_MAC], data=new)
    return True