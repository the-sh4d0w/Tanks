# Tanks
A tank battle game inspired by Tanks from Wii Play.
Ein Panzerkampfspiel (?), das von Panzerkiste aus Wii Play inspiriert ist.

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
´´´
Das ``object`` enthält drei Elemente: "spawn", der Startpunkt des Spielers, "enemies", eine Liste aller Gegner, und "walls", eine Liste aller Wände.
"spawn" ist ein ``array`` mit einer x-Koordinate und einer y-Koordinate (Das Feld ist immer 800x400 groß).

"entities" ist ein ``array`` mit ``collections``, die die Gegner darstellen. Jede ``collection`` enthält einen ``string`` mit einer Farbe (es gibt die Farben 'red', 'green' und 'yellow') und einen ``array`` mit einer x-Koordinate und einer y-Koordinate.

"walls" ist ein ``array`` mit ``collections``, die die Wände darstellen. Jede ``collection`` enthält einen ``string`` mit einem Wandtyp (es gibt die Wände 'I_x' und 'I_y') und einen ``array`` mit einer x-Koordinate und einer y-Koordinate.