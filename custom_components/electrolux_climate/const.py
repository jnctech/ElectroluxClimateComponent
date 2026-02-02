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

"""Constants for the Electrolux Climate integration."""

from datetime import timedelta
from homeassistant.const import Platform

DOMAIN = "electrolux_climate"

FAN_QUIET = "quiet"
FAN_TURBO = "turbo"

MIN_TEMP = 0
DEFAULT_MIN = 17
MAX_TEMP = 40
DEFAULT_MAX = 30

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SWITCH]
SCAN_INTERVAL = timedelta(seconds=5)