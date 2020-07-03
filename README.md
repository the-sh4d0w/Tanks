# Tanks
A tank battle game inspired by [Tanks from Wii Play](https://en.wikipedia.org/wiki/Wii_Play#Tanks!).
Ein Panzerkampfspiel, das von [Panzerkiste aus Wii Play](https://de.wikipedia.org/wiki/Wii_Play#Inhalt) inspiriert ist.

## Eigene Level erstellen
Dies ist Level 1. Er ist als JSON-Datei gespeichert.
```json
{
    "spawn": [
        380,
        200
    ],
    "enemies": [
        {
            "color": "red",
            "spawn": [
                10,
                170
            ]
        }
    ],
    "walls": [
        {
            "type": "I_x",
            "position": [
                360,
                180
            ]
        },
        {
            "type": "I_x",
            "position": [
                400,
                180
            ]
        },
        {
            "type": "I_y",
            "position": [
                360,
                190
            ]
        },
        {
            "type": "I_y",
            "position": [
                430,
                190
            ]
        }
    ]
}
```
Das ``object`` enthält drei Elemente: "spawn", der Startpunkt des Spielers, "enemies", eine Liste aller Gegner, und "walls", eine Liste aller Wände.
"spawn" ist ein ``array`` mit einer x-Koordinate und einer y-Koordinate (Das Feld ist immer 800x400 groß).

"entities" ist ein ``array`` mit ``collections``, die die Gegner darstellen. Jede ``collection`` enthält einen ``string`` mit einer Farbe (es gibt die Farben 'red', 'green' und 'yellow') und einen ``array`` mit einer x-Koordinate und einer y-Koordinate.

"walls" ist ein ``array`` mit ``collections``, die die Wände darstellen. Jede ``collection`` enthält einen ``string`` mit einem Wandtyp (es gibt die Wände 'I_x' und 'I_y') und einen ``array`` mit einer x-Koordinate und einer y-Koordinate.

## Einstellungen
Dies sind die Standardeinstellungen. Sie sind als JSON-Datei gespeichert.
```json
{
    "fps": 60,
    "speed": 2,
    "firerate": 10,
    "detection_range": 200,
    "attack_range": 110,
    "speeds": {
        "red": 1,
        "yellow": 2,
        "green": 1
    },
    "firerates": {
        "red": 10,
        "yellow": 13,
        "green": 5
    }
}
´´´
"fps" stellt die frames per second also die Bilder pro Sekunde dar. Bitte nicht verändern.
"speed" ist die Geschwindigkeit des Spielers. Je höher, desto schneller.
"firerate" ist die Feuerrate. je niedriger, desto schneller.