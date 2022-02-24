# snake
Ein künstlich intelligentes Snake-Programm als Projekt meiner vorwissenschaftlichen Arbeit (VWA)

Es wurde Python 3.9.10 verwendet.
Die Programmbibliotheken torch, numpy, pygame und matplotlib sind erforderlich.

- environment.py beinhaltet das Umfeld Snake, nimmt eine Aktion als Eingabe, gibt Wahrnehmungen sowie eine Belohnung zurück und zeichnet das Spiel auf den Bildschirm.
- network.py beinhaltet das künstliche neuronale Netz, nimmt ein Array in größe der Wahrnehmungen an und gibt eine Aktion als Integer zurück.
- agent.py beinhaltet den Lernalgorithmus, interagiert mit environment.py sowie network.py um die Gewichte des Netzwerks anzupassen, diese werden zusätzlich abgespeichert.
- main.py setzt agent.py in eine Trainingsschleife, weiters wird ein Graph Score/Spiele auf den Bildschirm gezeichnet. In der Datei können Spielfeldgröße und Geschwindigkeit eingestellt werden.

Zum Starten des Programms:
> python main.py

snake.py beinhaltet ein normales, tastengesteuertes Snake-spiel, welches man zum Vergleich selbst spielen kann. Zum Starten:
> python snake.py
