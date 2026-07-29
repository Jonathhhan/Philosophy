# Kapitel 8: Algorithmus

## 1. Vom Programm zum bedingten Übergang

Ein Programm ordnet mögliche Anschlüsse vor. Es gliedert, welche Fortsetzungen zugänglich, relevant oder naheliegend werden, ohne als Programm bereits die Weise jedes einzelnen Übergangs festzulegen. Manche Vorordnungen gehen jedoch weiter. Sie unterscheiden Bedingungen und verbinden sie mit einer Weise des Weitergehens, die in vergleichbaren Fällen erneut vollzogen werden kann.

Ein Schnitt kann etwa durch eine bereits gebildete Sequenz vorgeordnet werden, ohne dass daraus hervorgeht, an welcher Stelle er gesetzt werden soll. Wird dagegen festgelegt, bei jedem erkannten Taktschlag zum nächsten Bild überzugehen, ist nicht nur ein Feld möglicher Anschlüsse vorgeordnet. Eine Bedingung und ein Übergang sind so miteinander verbunden, dass dieselbe Übergangsordnung wiederholt angewendet werden kann.

Diese besondere Ordnung untersucht der Begriff des Algorithmus. Er bezeichnet weder eine besonders starke Form des Programms noch jedes geordnete Geschehen. Seine Eigenfunktion liegt in der wiederholbaren Ordnung bedingter Übergänge.

## 2. Algorithmus

Der Algorithmus wird häufig mit Computerprogrammen, mathematischen Verfahren oder eindeutigen Wenn-dann-Anweisungen verbunden. Diese Zusammenhänge sind wichtig, bestimmen aber nicht allein die Reichweite des Begriffs. Algorithmische Ordnungen können notiert und von Maschinen ausgeführt werden. Sie können ebenso einen handwerklichen oder künstlerischen Vollzug anleiten, ohne in digitalem Code vorzuliegen.

> Algorithmus ist die wiederholbare Ordnung bedingter Übergänge.

„Ordnung“ bezeichnet hier nicht das einzelne Übergangsereignis, sondern dessen Bedingungs-Übergangs-Relation. Ein Übergang ist algorithmisch bestimmt, sofern er seinen Stellenwert in einem Zusammenhang erhält, der Bedingungen unterscheidet und Weisen des Weitergehens miteinander verknüpft. Ob dafür bereits eine einzelne bedingte Anweisung genügt oder mehrere Schritte beziehungsweise Verzweigungen erforderlich sind, folgt noch nicht aus der Definition.

„Bedingt“ bedeutet, dass der Übergang nicht bloß zeitlich auf etwas anderes folgt. Innerhalb der algorithmischen Ordnung muss ein Unterschied gelten, von dem abhängt, welcher Übergang vollzogen wird. Die Bedingung kann sich auf eine Eingabe, einen erreichten Zustand, ein gemessenes Merkmal oder das Ergebnis einer vorausgegangenen Operation beziehen.

„Übergang“ bezeichnet die geordnete Beziehung, in der unter einer solchen Bedingung eine Operation ausgeführt, ein anderer Zustand erreicht oder eine Ausgabe erzeugt wird. Der Algorithmus ist weder die Bedingung noch die einzelne Operation. Er ist die Ordnung ihrer bedingten Verknüpfung.

Die Definition verlangt bislang weder, dass diese Ordnung vollständig ausgeschrieben ist, noch dass sie nach endlich vielen Schritten endet oder einen bestimmten Ergebniszustand erreicht. Solche Merkmale gehören zu vielen klassischen Algorithmusbegriffen. Sie dürfen hier nicht ohne Entscheidung ergänzt werden.

TODO: Autor entscheiden, ob Explizierbarkeit, Endlichkeit und Terminierung notwendige Merkmale des Algorithmus sein sollen und ob bereits ein einzelner wiederholbarer bedingter Übergang als Algorithmus genügt. Bis dahin werden diese Eigenschaften als mögliche Formen algorithmischer Ordnung, nicht als Bestandteile der verbindlichen Definition behandelt.

## 3. Wiederholbarkeit und Ausführung

Wiederholbarkeit bedeutet nicht, dass ein vollständiges Ereignis identisch zurückkehrt. Zwei Ausführungen unterscheiden sich mindestens durch ihre zeitliche Stellung. Sie können außerdem anderes Material bearbeiten, auf verschiedenen technischen Trägern stattfinden und unterschiedliche Nebenfolgen haben.

Wiederholt wird die Ordnung einer Bedingungs-Übergangs-Relation. Situationen werden in bestimmten Hinsichten als vergleichbar behandelt; an die so unterschiedenen Bedingungen wird dieselbe Weise des Weitergehens gebunden. Ein Verfahren, das jede Audiodatei nach derselben Ordnung in ein anderes Format überführt, kann trotz verschiedener Dateien und Ausgaben denselben Algorithmus ausführen.

Wiederholbarkeit ist deshalb eine Eigenschaft der Ordnung, nicht die Behauptung, dass sie faktisch schon mehrfach ausgeführt wurde. Ein entworfener Algorithmus kann wiederholbar sein, obwohl er erst einmal oder noch gar nicht ausgeführt wurde. Ebenso beweist die mehrfache Wiederkehr eines Ergebnisses für sich genommen keinen Algorithmus. Sie könnte durch andere Prozesse entstanden sein.

Algorithmus, Darstellung, Ausführung und Ergebnis sind zu unterscheiden. Eine Notation oder ein Quelltext kann eine algorithmische Ordnung darstellen. Eine Ausführung aktualisiert diese Ordnung unter konkreten Bedingungen. Das Ergebnis ist ein hervorgebrachter Zustand, eine Ausgabe oder eine Folge. Verschiedene Darstellungen und technische Implementierungen können möglicherweise denselben Algorithmus realisieren; derselbe Algorithmus kann bei verschiedenen Eingaben unterschiedliche Ergebnisse hervorbringen.

Eine algorithmische Ordnung kann beschrieben oder notiert sein, ohne in einem konkreten Zusammenhang bereits wirksam zu werden. Programm ist definitionsgemäß eine wirksame Vorordnung möglicher Anschlüsse. Nach dem in Kapitel 7 vorgeschlagenen Relationsgebrauch wirkt ein Algorithmus programmatisch, sofern seine Übergangsordnung tatsächliche Aktualisierungen vorordnet. Unabhängig von diesem Vorschlag bleiben die Definitionen verschieden: Programm hebt die Wirksamkeit einer Vorordnung hervor, Algorithmus die Wiederholbarkeit bedingter Übergänge.

TODO: Autor präzisieren, wodurch derselbe Algorithmus über verschiedene Beschreibungen, Implementierungen und Ausführungen hinweg identisch bleibt. Strukturelle Gleichheit der Übergänge, praktische Austauschbarkeit und identische Notation sind nicht ohne Weiteres dasselbe.

## 4. Determination, Wahrscheinlichkeit und Unvorhersagbarkeit

Wiederholbarkeit darf nicht mit einem stets identischen Ergebnis gleichgesetzt werden. Bei einer deterministischen Übergangsordnung ist unter denselben algorithmisch relevanten Bedingungen genau ein weiterer Übergang bestimmt. Auch ein solcher Verlauf kann praktisch unvorhersagbar bleiben, wenn seine Berechnung zu komplex ist oder die Ausgangsbedingungen nicht vollständig bekannt sind.

Sofern stochastische Übergangsordnungen unter den Algorithmusbegriff fallen, verbinden sie Bedingungen mit einer Wahrscheinlichkeitsverteilung und einem stochastischen Auswahl- oder Abtastverfahren. Unter vergleichbaren Bedingungen kann ein anderer konkreter Übergang eintreten. Wiederholt wird dann nicht das Ergebnis, sondern die Wahrscheinlichkeits- und Auswahlordnung, nach der es hervorgebracht wird.

Die Markov-Experimente der Masterarbeit bilden den genealogischen Anlass für diese Erweiterung. Der jeweils vorausgegangene Zustand oder eine Folge früherer Zustände bildet die Bedingung, von der die Wahrscheinlichkeiten möglicher Folgezustände abhängen. Bei jeder Generierung können andere Tonfolgen entstehen, während die Übergangsmatrix und die Weise der Auswahl bestehen bleiben.[^ma-markov]

Ein früheres Ergebnis kann innerhalb eines Algorithmus erneut als Bedingung oder Eingabe bearbeitet werden. Eine solche Rückführung verändert nicht notwendig die Übergangsordnung selbst. Auch wenn vorgesehene Regeln Parameter anpassen oder frühere Zustände speichern, bleibt die Veränderung algorithmisch geordnet, sofern die Weise dieser Anpassung bereits zur wiederholbaren Ordnung gehört.

Unvorhersagbarkeit betrifft das Wissen über einen Verlauf. Algorithmische Bestimmtheit betrifft die Ordnung, nach der Übergänge hervorgebracht werden. Ein zufälliges oder überraschendes Ergebnis ist deshalb nicht allein aufgrund seiner Unvorhersagbarkeit improvisiert. Entscheidend bleibt, ob die relevante Übergangsordnung bereits vorliegt oder ob ein Anschluss in der besonderen Situation formbildend bestimmt werden muss.

TODO: Autor bestätigen, ob stochastische und nichtdeterministische Verfahren ausdrücklich unter den Algorithmusbegriff fallen, sofern ihre Wahrscheinlichkeits-, Auswahl- oder Zulässigkeitsordnung wiederholbar bestimmt ist. Die Quellen tragen diese Erweiterung genealogisch, die verbindliche Definition legt sie aber noch nicht ausdrücklich fest.

## 5. Regel, Muster und bloße Regelmäßigkeit

Eine Regel kann erlaubte, verbotene oder vorgesehene Vollzüge unterscheiden, ohne bereits eine Übergangsordnung zu bilden. Algorithmisch wird eine Regelbeziehung dort, wo Bedingungen so mit Operationen verknüpft werden, dass die Weise des Übergangs wiederholt angewendet werden kann. Eine einzelne Regel kann Teil eines Algorithmus sein; nicht jede Regel ist deshalb selbst ein Algorithmus.

Auch ein Plan kann algorithmische Schritte enthalten, ist aber nicht mit ihnen identisch. Ein Plan nimmt einen Verlauf oder ein Ziel vorweg. Ein Algorithmus kann Übergänge ordnen, ohne den Zweck seiner Anwendung oder einen gewünschten Endzustand darzustellen. Umgekehrt kann ein Plan Ziele benennen, ohne anzugeben, wie unter veränderten Bedingungen weiter zu verfahren ist.

Eine Routine bezeichnet eine eingeübte Weise des Vollzugs. Sie kann eine algorithmische Ordnung realisieren, ohne dass die ausführende Person jeden Übergang ausdrücklich formuliert. Sie kann ebenso flexibel auf situative Unterschiede reagieren, die in keiner wiederholbaren Übergangsordnung erfasst sind. Aus der Regelmäßigkeit eines eingeübten Handelns folgt deshalb noch nicht, dass sein gesamter Vollzug algorithmisch ist.

Dasselbe gilt für sichtbare Muster und Sequenzen. Eine regelmäßig erscheinende Bildfolge kann situativ montiert worden sein, ohne dass eine vorgeordnete Übergangsordnung sie hervorgebracht hat. Umgekehrt kann ein Algorithmus Ergebnisse erzeugen, in denen kein einfaches Muster erkennbar ist. Das Muster liegt in der Gestalt eines Ergebnisses; der Algorithmus in der Ordnung seiner möglichen Hervorbringung.

Auch bloße Kausalität genügt nicht. Ein Material kann altern, ein Stromausfall eine Maschine unterbrechen und ein Gegenstand unter bestimmten physikalischen Bedingungen fallen. Solche Vorgänge können regelmäßig beschrieben werden. Ohne einen eigenen Nachweis werden sie damit nicht zu Algorithmen. Der gestuft offene Anschlussbegriff verbietet es, jede regelmäßige Naturfolge als algorithmische Ordnung zu behandeln.

Ein Algorithmus ist auch nicht allein aufgrund seiner Mehrschrittigkeit eine Organisation. Er ordnet bedingte Übergänge; Organisation koordiniert mehrere Anschlussbedingungen in einem Zusammenhang. Ein Verfahren kann innerhalb einer Organisation eingesetzt werden, ohne mit ihr identisch zu sein.

## 6. Bedingung, Kategorie und Anwendung

Ein Algorithmus kann nur an Unterschieden operieren, die innerhalb seiner Ordnung als Bedingungen bearbeitbar sind. Dazu müssen Eigenschaften gemessen, bezeichnet, kategorisiert oder auf andere Weise so dargestellt werden, dass von ihnen ein Übergang abhängig gemacht werden kann. Ein algorithmisch relevanter Zustand ist deshalb nicht die vollständige Wirklichkeit einer Situation. Er ist eine unter bestimmten Gesichtspunkten unterschiedene Konfiguration.

Die Feststellung einer Bedingung kann selbst technisch geordnet sein. Ein Messwert überschreitet einen Grenzwert, ein Zeichen stimmt mit einer gespeicherten Folge überein oder eine Eingabe gehört nach vorgegebenen Merkmalen zu einer Kategorie. Sie kann jedoch auch eine fallbezogene Bestimmung verlangen. Ob eine Äußerung ironisch, eine Einstellung spannungsreich oder eine Situation einer bekannten Regel vergleichbar ist, ergibt sich nicht notwendig aus der Übergangsordnung, die nach dieser Feststellung angewendet wird.

Ein Teilvollzug kann daher nach erfolgter Klassifikation algorithmisch geordnet sein, obwohl die Klassifikation selbst auf situierte Wahrnehmung und eingeübtes Können angewiesen bleibt. Wird auch sie durch ein weiteres Verfahren geordnet, verschiebt sich die Frage auf dessen Eingaben, Messungen und Kategorien. Daraus folgt nicht, dass algorithmische Klassifikation prinzipiell unvollständig sein muss. Es folgt nur, dass jeweils ausgewiesen werden muss, welche Unterschiede die Ordnung bearbeitet und welche Bedingungen ihrer Anwendung vorausliegen.

Die korrekte Ausführung eines Algorithmus entscheidet deshalb noch nicht, ob seine Kategorien den untersuchten Zusammenhang hinreichend erfassen oder ob seine Anwendung dort angebracht ist. Diese Fragen gehören zur späteren Beurteilung. Für den Algorithmusbegriff genügt hier die analytische Trennung zwischen der internen Ordnung eines Übergangs und den Bedingungen, unter denen ein Fall ihr zugeordnet wird.

TODO: Autor entscheiden, ob die Erkennung beziehungsweise fallbezogene Bestimmung der Bedingung selbst vollständig zur algorithmischen Ordnung gehören muss. Die vorliegende Ebenenanalyse lässt algorithmische Übergänge auch dort zu, wo ihre Anwendung von einem nicht algorithmisch bestimmten Klassifikationsschritt abhängt.

## 7. Algorithmische Montage und Improvisation

Die früheren Montagearbeiten verwenden Algorithmus, Programm, Struktur und Notation noch nicht in der heute verbindlichen Trennung. Die Masterarbeit bezeichnet den Algorithmus zunächst als vorher festgelegte Entscheidungsfolge oder Spielregel und setzt ihn zeitweise mit einem ausgeführten Programm in Beziehung.[^ma-frueher-algorithmus] Der gegenwärtige Begriff übernimmt diese Taxonomie nicht. Er entwickelt aus ihr die wiederholbare Ordnung bedingter Übergänge als eigenständige Bestimmung.

Zugleich zeigt die historische Untersuchung algorithmischer Filmkomposition, dass eine solche Ordnung nicht an Computer gebunden ist. Notationen und Schemata konnten filmische Übergänge vorordnen, die anschließend von Menschen am Schneidetisch ausgeführt wurden. Die Masterarbeit beschreibt außerdem, wie sich improvisatorische Tätigkeit bei generativen Verfahren von der unmittelbaren Montage in die Entwicklung und Veränderung des Verfahrens verschieben kann.[^ma-film]

Algorithmus und Improvisation sind damit keine vollständigen Gegensätze. Ein Montageprozess kann algorithmische Teilvollzüge enthalten und an anderen Stellen eine situative Formbestimmung verlangen. Ein Verfahren kann vorsehen, dass bei einem erkannten Merkmal eine bestimmte Aufnahmegruppe durchsucht wird; welche Merkmale überhaupt relevant sind oder wie mit einem unerwarteten Ergebnis weitergearbeitet wird, kann außerhalb dieser Übergangsordnung bestimmt werden.

Der Montage-Automat macht diese Ebenen praktisch untersuchbar. Er ordnet filmisches Material anhand ausgewählter Untertitelmerkmale, Ähnlichkeiten und Gewichtungen. Dadurch kann er assoziative Folgen erzeugen. Zugleich zeigt das Experiment, dass die erzeugten Beziehungen davon abhängen, welche Merkmale als Daten bereitgestellt und wie sie kategorisiert wurden. Bildhandlung, Klang, Körperhaltung und weitere Eigenschaften blieben in der untersuchten Fassung unberücksichtigt.[^ma-automat]

Diese Beobachtung beweist keine prinzipielle Grenze jeder Algorithmisierung von Montage. Sie zeigt genauer, welche Beziehungen die gewählte Übergangsordnung erfassen konnte und welche der konkrete Versuch nicht bearbeitete. Montage dient hier als epistemisches Modell, weil die Übersetzung von Material in Bedingungen, Kategorien und Übergänge praktisch vollzogen und an ihren Ergebnissen verglichen werden kann.

Technische Operationen können dabei algorithmisch geordnet sein, ohne dass Maschinen deshalb verstehen, entscheiden oder improvisieren. In hybriden Vollzügen wählen Menschen Kategorien, konfigurieren Verfahren, führen technische Operationen aus und schließen an deren Ergebnisse an. Ob rein technische Zustandsübergänge selbst Anschlüsse im vollen Sinn des Buches bilden, bedarf gemäß dem gestuft offenen Geltungsbereich eines eigenen Nachweises.

TODO: Den Status rein technischer Übergänge als Anschlüsse offenhalten. Bis zu einem eigenen Nachweis bezeichnet „algorithmischer Anschluss“ nur einen menschlichen oder hybriden Vollzug, in dem eine algorithmische Übergangsordnung für Anschlussmöglichkeiten wirksam wird.

## 8. Vom Übergang zum Zusammenhang

Die Ausführung eines Algorithmus kann Elemente auswählen, Operationen vollziehen und Folgen erzeugen. Damit ist noch nicht erklärt, wie mehrere Elemente, Übergänge und Relationen so angeordnet werden, dass ein bestimmter Zusammenhang möglicher und aktualisierter Anschlüsse entsteht.

Eine algorithmisch erzeugte Folge kann durchaus komponiert sein oder zum Bestandteil einer Komposition werden. Aus ihrer algorithmischen Hervorbringung allein folgt jedoch noch nicht, wie ihre Teile einander bestimmen, welche Beziehungen erhalten werden und welche Gestalt der Zusammenhang gewinnt.

Der Algorithmus hebt die wiederholbare Ordnung bedingter Übergänge hervor. Die nächste Frage richtet sich auf die Anordnung mehrerer solcher Übergänge und ihrer Elemente zu einem Zusammenhang.

Diese Frage führt zum Komponieren.

[^ma-frueher-algorithmus]: Jonathan Frank, *Algorithmische Komposition in der Filmmontage oder wie ich darüber denke*, 2. Aufl. (2020), gedruckte S. 13–15 und 150–152.
[^ma-film]: Ebd., gedruckte S. 20–24 und 150–152.
[^ma-markov]: Ebd., gedruckte S. 38–44.
[^ma-automat]: Ebd., gedruckte S. 51, 58–59 und 92–93.
