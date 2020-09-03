
# rhasspy-simple-intent

simple intent hander/intent dispatcher for rhasspy.

Intent handlers (somewhat like simple skills) can be "pluged-in" (copied in) into the intents folder and will receive the event as a Python Dict just like a custom command handler in rhasspy would do.

Included are some Home Assistant intents, where you can switch on/off lights, get temperature values, control your media players and activte scenes. Also includes are some misc intents. The interesting thing is, that the entities are described in the senteces. This looks like so:

<details>
<summary>Example Sentences are in German (click to expand)</summary>
<p>

```
[misc-GetTime]
wie spät

[misc-Compliment]
mach (schatz){who} ein kompliment

[homeassistant-GetTemperature]
wie ist die temperatur (aussen | draussen) (:){entity_id:sensor.mebus_3001_temp}

[homeassistant-ChangeLightState]
schalte ($lights) ($on-off-states)
licht (  (an){state:on} | (ein){state:on} ) (:){entity_id:light.living_colors_wohnzimmer}
licht (:){state:on} (:){entity_id:light.living_colors_wohnzimmer}
licht (aus){state:off} (:){entity_id:light.living_colors_wohnzimmer light.beleuchtung_lichterschlauch light.beleuchtung_pflanzen}

[homeassistant-ActivateScene]
alles [im wohnzimmer] aus (:){entity_id:scene.wohnzimmer_aus}

[homeassistant-ControlMediaPlayer]
schalte den fernseher (:){entity_id:media_player.tv_wohnzimmer} (an | ein | aus){state} (:){action:turn_on_off}
fernseher (:){entity_id:media_player.tv_wohnzimmer} ($on-off-states) (:){action:turn_on_off}
film (pause | stop){action} (:){entity_id:media_player.mediacenter_wohnzimmer} 
film (weiter){action:play} (:){entity_id:media_player.mediacenter_wohnzimmer} 
```

</p>
</details>

## Requirements

  

* Python 3.7

* Rhasspy 2.5

  

## Installation

```bash

$ git clone https://github.com/mk-81/rhasspy-simple-intent.git

$ cd rhasspy-simple-intent

$ python3 -m venv .

$ source bin/activate

$ pip install aiohttp

$ pip install paho-mqtt

$ pip install rhasspy-hermes

$ deactivate

$ chmod u+x simple_intent_server.py

```

  

## Running

```bash

$ bin/rhasspy-remote-http-hermes --rhasspy-profile-dir=<location of your rhasspy profile.json>

```
The program will try to extract all relevant information from your profile.json. Elsewise, you have to pass the MQTT connection information via url params


### Connection to home assistant
Make sure, you have entered the Home Assistant URL in your rhasspy profile json or maintain a HomeAssistantConfig.json file fith the following structure in your rhasspy profile dir
  
{
	"url" : "< HA URL >",
	"authorizationToken" : < HA authorization token >"
}

Why running as an service instead of a custom command script?
* A custom handler does not interfere with other handlers (custom scripts or home assistant).
* No need to adjust your cosutom command script to handle new intents.
* Faster - I found that the python interpreter needs about half a second to start.


## Structure
|--- rhasspy-simple-intent            # this is actually in the github project
     |--- services                    # location for all services (e.g. home assistant interface)
            |--- home_assistant       # home assistant service module
      |--- internts                   # location for all intent modules
            |---  BaseIntentHandler   # base class for intent handler inheritance
            |--- ...                  # place for all other intent handlers - name = intent name

## TODO
propably a whole lot... at least:
* homeassistant services
	* [ ] sensor interface
	* [ ] enchance light interface
		* [ ] change color 
		* [ ] change intensity
* [ ] i18n (languages...)
* [ ] setup and install scripts
