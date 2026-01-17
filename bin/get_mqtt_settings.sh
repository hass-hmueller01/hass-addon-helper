#!/usr/bin/with-contenv bashio
# ==============================================================================
# Get MQTT Settings Script
# This script retrieves MQTT broker settings either from Home Assistant add-on
# configuration or from a user-provided mqtt_config.py file for non-Home Assistant
# environments.
# Holger Mueller, Alexandre-io - MIT License 2025-2026
# v001 2025-06-30 hmueller01 Initial version migrated from homeassistant-vcontrol addon (Alexandre-io)
# v002 2026-01-17 hmueller01 Added non-HA environment support
# ==============================================================================

if [ -d /usr/lib/bashio ]; then
    # Check if user has provided MQTT configuration
    if bashio::config.has_value 'mqtt_host' \
        && bashio::config.has_value 'mqtt_port' \
        && bashio::config.has_value 'mqtt_user' \
        && bashio::config.has_value 'mqtt_password'; then

        # Use configured MQTT settings
        export MQTT_HOST=$(bashio::config 'mqtt_host')
        export MQTT_PORT=$(bashio::config 'mqtt_port')
        export MQTT_USER=$(bashio::config 'mqtt_user')
        export MQTT_PASSWORD=$(bashio::config 'mqtt_password')
        bashio::log.info "Using configured MQTT Host: $MQTT_HOST:$MQTT_PORT"

    # If no user configuration is found, check if internal MQTT service is available
    elif bashio::services.available "mqtt"; then

        # Use internal MQTT service settings
        export MQTT_HOST=$(bashio::services mqtt "host")
        export MQTT_PORT=$(bashio::services mqtt "port")
        export MQTT_USER=$(bashio::services mqtt "username")
        export MQTT_PASSWORD=$(bashio::services mqtt "password")
        bashio::log.info "Using internal MQTT Host: $MQTT_HOST:$MQTT_PORT"

    # Exit if neither user-provided nor internal MQTT configuration is available
    else
        bashio::exit.nok "No MQTT broker configured and no internal MQTT service available"
    fi

# This is for non-Home Assistant environments, try to parse user mqtt_config.py file
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    source <($SCRIPT_DIR/parse_mqtt_config.py)
    if [[ -z "$MQTT_HOST" || -z "$MQTT_PORT" ]]; then
        echo "No MQTT broker configured"
    else
        echo "Using mqtt_config.py configured MQTT Host: $MQTT_HOST:$MQTT_PORT"
    fi
fi
