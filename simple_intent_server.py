#!/usr/bin/env python3

import argparse
import asyncio

from intent_handler_hermes import IntentHandlerHermesMqtt

import paho.mqtt.client as mqtt
import rhasspyhermes.cli as hermes_cli

from global_configuration import GlobalConfiguration

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--configuration",
        help="full path to configuration file",
    )

    parser.add_argument(
        "--rhasspy-profile-dir",
        help="full path to rhasspy profile directory",
    )

    hermes_cli.add_hermes_args(parser)
    args = parser.parse_args()
    hermes_cli.setup_logging(args)

    global_configuration = GlobalConfiguration(
                               rhasspy_profile_dir=args.rhasspy_profile_dir
                           )

    global_configuration.load()

    val = global_configuration.get_rhasspy_profile_value("mqtt.host")
    if val and args.host == "localhost":
        args.host = val
    
    ext_mqtt = global_configuration.get_rhasspy_profile_value("mqtt.enabled") == "true"
    if not ext_mqtt:
        if args.port == 1883:
            args.port = 12183
    else:
        val = global_configuration.get_rhasspy_profile_value("mqtt.port")
        if val and args.port == 1883:
            args.port = int(val)

    client = mqtt.Client()
    hermes = IntentHandlerHermesMqtt(
                client,
                global_configuration=global_configuration,
                site_ids=args.site_id
             )
    hermes_cli.connect(client, args)
    client.loop_start()

    try:
        asyncio.run(hermes.handle_messages_async())
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()


main()