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

Eine Ordnung ist nur insofern algorithmisch, als ihre relevanten Bedingungen, Operationen und deren Übergangsrelation prinzipiell hinreichend angegeben oder rekonstruiert werden können. Diese Spezifizierbarkeit verhindert, dass jede Routine oder nachträglich beobachtete Regelmäßigkeit als Algorithmus gilt. Sie verlangt jedoch weder eine vollständige schriftliche Notation noch ein bewusstes Wissen der Ausführenden.

Endlichkeit und Terminierung sind keine notwendigen Merkmale des hier verwendeten Algorithmusbegriffs. Rekursive, interaktive oder fortlaufende Verfahren können algorithmisch geordnet sein, ohne einen endgültigen Ergebniszustand zu erreichen. Auch eine einzelne bedingte Übergangsrelation kann eine algorithmische Ordnung bilden, sofern ihre Weise des Weitergehens unter vergleichbaren Bedingungen erneut angewendet werden kann.

## 3. Wiederholbarkeit und Ausführung

Wiederholbarkeit bedeutet nicht, dass ein vollständiges Ereignis identisch zurückkehrt. Zwei Ausführungen unterscheiden sich mindestens durch ihre zeitliche Stellung. Sie können außerdem anderes Material bearbeiten, auf verschiedenen technischen Trägern stattfinden und unterschiedliche Nebenfolgen haben.

Wiederholt wird die Ordnung einer Bedingungs-Übergangs-Relation. Situationen werden in bestimmten Hinsichten als vergleichbar behandelt; an die so unterschiedenen Bedingungen wird dieselbe Weise des Weitergehens gebunden. Ein Verfahren, das jede Audiodatei nach derselben Ordnung in ein anderes Format überführt, kann trotz verschiedener Dateien und Ausgaben denselben Algorithmus ausführen.

Wiederholbarkeit ist deshalb eine Eigenschaft der Ordnung, nicht die Behauptung, dass sie faktisch schon mehrfach ausgeführt wurde. Ein entworfener Algorithmus kann wiederholbar sein, obwohl er erst einmal oder noch gar nicht ausgeführt wurde. Ebenso beweist die mehrfache Wiederkehr eines Ergebnisses für sich genommen keinen Algorithmus. Sie könnte durch andere Prozesse entstanden sein.

Algorithmus, Darstellung, Ausführung und Ergebnis sind zu unterscheiden. Eine Notation oder ein Quelltext kann eine algorithmische Ordnung darstellen. Eine Ausführung aktualisiert diese Ordnung unter konkreten Bedingungen. Das Ergebnis ist ein hervorgebrachter Zustand, eine Ausgabe oder eine Folge. Verschiedene Darstellungen und technische Implementierungen können möglicherweise denselben Algorithmus realisieren; derselbe Algorithmus kann bei verschiedenen Eingaben unterschiedliche Ergebnisse hervorbringen.

Eine algorithmische Ordnung kann beschrieben oder notiert sein, ohne in einem konkreten Zusammenhang bereits wirksam zu werden. Programm ist definitionsgemäß eine wirksame Vorordnung möglicher Anschlüsse. Ein Algorithmus wirkt programmatisch, sofern seine Übergangsordnung tatsächliche Aktualisierungen vorordnet. Die Definitionen bleiben verschieden: Programm hebt die Wirksamkeit einer Vorordnung hervor, Algorithmus die Wiederholbarkeit bedingter Übergänge.

Die Identität eines Algorithmus liegt nicht in einem identischen Zeichenbestand, einem bestimmten materiellen Träger oder der Gleichheit einzelner Ausführungen. Sie liegt in der strukturerhaltenden Gleichheit seiner spezifizierten Ordnung bedingter Übergänge auf einer ausgewiesenen Analyseebene.

Verschiedene Darstellungen und Implementierungen realisieren denselben Algorithmus, wenn ihre relevanten Zustände, Bedingungen, Operationswirkungen und Übergangsrelationen strukturerhaltend aufeinander bezogen werden können. Bei stochastischen Verfahren muss außerdem die bedingte Wahrscheinlichkeits- und Auswahlordnung erhalten bleiben, nicht die konkrete Folge gezogener Werte.

Welche Unterschiede als algorithmisch relevant und welche als implementierungsintern gelten, muss für den jeweiligen Vergleich ausgewiesen werden. Eine andere Notation, Programmiersprache oder technische Zerlegung kann dieselbe Übergangsordnung darstellen. Gleiche Ein- und Ausgaben, dieselbe praktische Aufgabe oder Austauschbarkeit in einem begrenzten Zusammenhang genügen dagegen nicht für Identität, wenn die Weise des Weitergehens verschieden geordnet ist.

Materielle Unterschiede verändern den Algorithmus, wenn sie seine relevante Übergangsordnung verändern. Numerische Präzision, Zeit- oder Speichergrenzen, Datenrepräsentation, Sensorik und vorgesehene Fehlerpfade können deshalb zur algorithmischen Ordnung gehören. Bleiben deren Unterschiede ohne Einfluss auf die relevanten Bedingungen und Übergänge, gehören sie zur Implementierung oder konkreten Ausführung. Derselbe Algorithmus kann dadurch materiell verschieden realisiert und zugleich unterschiedlich programmatisch wirksam werden.

## 4. Determination, Wahrscheinlichkeit und Unvorhersagbarkeit

Wiederholbarkeit darf nicht mit einem stets identischen Ergebnis gleichgesetzt werden. Bei einer deterministischen Übergangsordnung ist unter denselben algorithmisch relevanten Bedingungen genau ein weiterer Übergang bestimmt. Auch ein solcher Verlauf kann praktisch unvorhersagbar bleiben, wenn seine Berechnung zu komplex ist oder die Ausgangsbedingungen nicht vollständig bekannt sind.

Stochastische Übergangsordnungen fallen unter den Algorithmusbegriff, sofern sie Bedingungen mit einer bestimmten Wahrscheinlichkeitsverteilung und einem wiederholbaren Auswahl- oder Abtastverfahren verbinden. Unter vergleichbaren Bedingungen kann ein anderer konkreter Übergang eintreten. Wiederholt wird dann nicht das Ergebnis, sondern die Wahrscheinlichkeits- und Auswahlordnung, nach der es hervorgebracht wird.

Die Markov-Experimente der Masterarbeit bilden den genealogischen Anlass für diese Erweiterung. Der jeweils vorausgegangene Zustand oder eine Folge früherer Zustände bildet die Bedingung, von der die Wahrscheinlichkeiten möglicher Folgezustände abhängen. Bei jeder Generierung können andere Tonfolgen entstehen, während die Übergangsmatrix und die Weise der Auswahl bestehen bleiben.[^ma-markov]

Ein früheres Ergebnis kann innerhalb eines Algorithmus erneut als Bedingung oder Eingabe bearbeitet werden. Eine solche Rückführung verändert nicht notwendig die Übergangsordnung selbst. Auch wenn vorgesehene Regeln Parameter anpassen oder frühere Zustände speichern, bleibt die Veränderung algorithmisch geordnet, sofern die Weise dieser Anpassung bereits zur wiederholbaren Ordnung gehört.

Unvorhersagbarkeit betrifft das Wissen über einen Verlauf. Algorithmische Bestimmtheit betrifft die Ordnung, nach der Übergänge hervorgebracht werden. Ein zufälliges oder überraschendes Ergebnis ist deshalb nicht allein aufgrund seiner Unvorhersagbarkeit improvisiert. Entscheidend bleibt, ob die relevante Übergangsordnung bereits vorliegt oder ob ein Anschluss in der besonderen Situation formbildend bestimmt werden muss.

Eine nichtdeterministische Ordnung ist davon zu unterscheiden. Bestimmt sie nur eine Menge zulässiger Übergänge, ohne die Weise ihrer Auswahl zu ordnen, bildet sie eine Regel oder Einschränkung, aber noch keinen vollständigen Algorithmus des nächsten Übergangs. Algorithmisch wird auch dieser Vollzug erst, wenn eine wiederholbare Ausführungsordnung bestimmt, wie aus den zulässigen Übergängen weitergegangen wird.

## 5. Regel, Routine und Muster

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

Die Erkennung einer Bedingung gehört insoweit zum Algorithmus, als ihre Prüfung oder Klassifikation selbst durch eine wiederholbare Übergangsordnung bestimmt wird. Andernfalls bildet sie eine externe Anwendungsbedingung des algorithmischen Teilvollzugs. Ein menschlich klassifizierter Fall kann daher einen algorithmischen Übergang auslösen, ohne dass die situierte Klassifikation selbst algorithmisch wird.

## 7. Algorithmische Montage und Improvisation

Die früheren Montagearbeiten verwenden Algorithmus, Programm, Struktur und Notation noch nicht in der heute verbindlichen Trennung. Die Masterarbeit bezeichnet den Algorithmus zunächst als vorher festgelegte Entscheidungsfolge oder Spielregel und setzt ihn zeitweise mit einem ausgeführten Programm in Beziehung.[^ma-frueher-algorithmus] Der gegenwärtige Begriff übernimmt diese Taxonomie nicht. Er entwickelt aus ihr die wiederholbare Ordnung bedingter Übergänge als eigenständige Bestimmung.

Zugleich zeigt die historische Untersuchung algorithmischer Filmkomposition, dass eine solche Ordnung nicht an Computer gebunden ist. Notationen und Schemata konnten filmische Übergänge vorordnen, die anschließend von Menschen am Schneidetisch ausgeführt wurden. Die Masterarbeit beschreibt außerdem, wie sich improvisatorische Tätigkeit bei generativen Verfahren von der unmittelbaren Montage in die Entwicklung und Veränderung des Verfahrens verschieben kann.[^ma-film]

Algorithmus und Improvisation sind damit keine vollständigen Gegensätze. Ein Montageprozess kann algorithmische Teilvollzüge enthalten und an anderen Stellen eine situative Formbestimmung verlangen. Ein Verfahren kann vorsehen, dass bei einem erkannten Merkmal eine bestimmte Aufnahmegruppe durchsucht wird; welche Merkmale überhaupt relevant sind oder wie mit einem unerwarteten Ergebnis weitergearbeitet wird, kann außerhalb dieser Übergangsordnung bestimmt werden.

Der Montage-Automat macht diese Ebenen praktisch untersuchbar. Das Gutachten zur Masterarbeit bezeichnet ihn als Denkmodell eines subjektiven `if–then–else`.[^gutachten-automat] Im dokumentierten `Alphaville`-Versuch bildeten Untertitel zugleich das Lern- und das zuzuordnende Material. Häufige Wörter wurden als Stoppwörter zurückgestellt, andere nach ihrer angenommenen Bedeutung für die Verkettung gewichtet. Damit war nicht bloß festgelegt, dass ähnliche Texte aufeinander folgen sollten. Es war geordnet, welche Texteigenschaften als Bedingungen gelten und wie stark sie die Auswahl eines Übergangs beeinflussen.[^ma-automat]

Für das Buch lässt sich daran untersuchen, wie situierte Montageurteile in Kategorien, Bedingungen und Übergänge übersetzt werden. Die Ausführung konnte assoziative Folgen erzeugen; eine berechnete Geschichte oder ein erkennbarer Strukturtransfer entstand in der untersuchten Fassung nicht. Bildhandlung, Klang, Körperhaltung und weitere Eigenschaften blieben außerhalb ihrer Datenordnung. Das Ergebnis verweist daher nicht auf eine unüberwindliche Grenze des Algorithmischen, sondern auf die bestimmte Reichweite dieses Algorithmus: Er bearbeitete genau die Unterschiede, die durch Kategorien, Gewichte und Datenrepräsentation für seine Übergänge spezifiziert waren.

Diese Beobachtung beweist keine prinzipielle Grenze jeder Algorithmisierung von Montage. Sie zeigt genauer, welche Beziehungen die gewählte Übergangsordnung erfassen konnte und welche der konkrete Versuch nicht bearbeitete. Der Werkzeugbau und die diagrammatische Darstellung gehören dabei zur Erkenntnispraxis: Sie machen Kategorien, Bedingungen und Übergänge sichtbar, veränderbar und an erzeugten Folgen vergleichbar.[^ma-werkzeug-algorithmus] Montage dient hier als epistemisches Modell, weil die Übersetzung von Material in eine Übergangsordnung praktisch vollzogen und geprüft werden kann.

Technische Operationen können dabei algorithmisch geordnet sein, ohne dass Maschinen deshalb verstehen, entscheiden oder improvisieren. In hybriden Vollzügen wählen Menschen Kategorien, konfigurieren Verfahren, führen technische Operationen aus und schließen an deren Ergebnisse an. Bis zu einem eigenen Nachweis für rein technische Anschlussvollzüge bezeichnet „algorithmischer Anschluss“ deshalb nur einen menschlichen oder hybriden Vollzug, in dem eine algorithmische Übergangsordnung für Anschlussmöglichkeiten wirksam wird.

## 8. Vom Übergang zum Zusammenhang

Die Ausführung eines Algorithmus kann Elemente auswählen, Operationen vollziehen und Folgen erzeugen. Damit ist noch nicht erklärt, wie mehrere Elemente, Übergänge und Relationen so angeordnet werden, dass ein bestimmter Zusammenhang möglicher und aktualisierter Anschlüsse entsteht.

Eine algorithmisch erzeugte Folge kann durchaus komponiert sein oder zum Bestandteil einer Komposition werden. Aus ihrer algorithmischen Hervorbringung allein folgt jedoch noch nicht, wie ihre Teile einander bestimmen, welche Beziehungen erhalten werden und welche Gestalt der Zusammenhang gewinnt.

Der Algorithmus hebt die wiederholbare Ordnung bedingter Übergänge hervor. Die nächste Frage richtet sich auf die Anordnung mehrerer solcher Übergänge und ihrer Elemente zu einem Zusammenhang.

Diese Frage führt zum Komponieren.

[^ma-frueher-algorithmus]: Jonathan Frank, *Algorithmische Komposition in der Filmmontage oder wie ich darüber denke*, 2. Aufl. (2020), gedruckte S. 13–15 und 150–152.
[^ma-film]: Ebd., gedruckte S. 20–24 und 150–152.
[^ma-markov]: Ebd., gedruckte S. 38–44.
[^ma-automat]: Ebd., gedruckte S. 51, 58–59 und 92–93.
[^ma-werkzeug-algorithmus]: Ebd., gedruckte S. 37, 51–58 und 141–149.
[^gutachten-automat]: Gutachten zu Jonathan Frank, *Algorithmische Komposition in der Filmmontage oder wie ich darüber denke*, S. 2–3.
