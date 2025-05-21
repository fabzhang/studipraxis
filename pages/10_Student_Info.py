import streamlit as st

st.set_page_config(
    page_title="Informationen für Studierende - studiPraxis",
    page_icon="🧑‍🎓"
)

st.markdown("""
<div style='margin-top:1em; margin-bottom:1em;'>
<h3 style='color:#15396b;'>Was bedeutet es, Werkstudent zu sein?</h3>
<p>Werkstudent*innen sind Studierende, die neben ihrem Studium bei einem Arbeitgeber unter bestimmten Voraussetzungen beschäftigt sind. Die wichtigste Voraussetzung ist, dass dein Schwerpunkt auf deinem Studium bleibt. Dies wird sichergestellt, indem deine Arbeitszeit grundsätzlich auf <b>20 Stunden pro Woche</b> begrenzt ist.</p>
<p>Es gibt jedoch Ausnahmen, die wir weiter unten erklären.</p>
<h4>Welche Voraussetzungen musst du mitbringen?</h4>
<p>Die maximale Anzahl Semester in denen du als Werkstudent*in arbeiten darfst beträgt 25. Außerdem darfst du dich nicht in einem Urlaubssemester befinden.</p>
<h4>Wie ist die Arbeitszeit geregelt?</h4>
<p>Als Werkstudent*in gilt grundsätzlich ein wöchentliches Limit von 20 Arbeitsstunden.</p>
<p>Du darfst diese Grenze jedoch <b>in bis zu 26 Wochen pro Jahr überschreiten</b>, wenn:</p>
<ul>
    <li>die Mehrarbeit abends, nachts, am Wochenende oder in den Semesterferien erfolgt,</li>
    <li>der Zeitraum im Voraus bekannt ist,</li>
    <li>und innerhalb eines Zeitjahres die 26-Wochen-Grenze eingehalten wird.</li>
</ul>
<h4>Warum ein Werkstudentenjob über Studipraxis?</h4>
<ol>
    <li><b>Praxiserfahrung sammeln – Werde fit für deinen Berufsstart</b>
        <ul>
            <li>Sicherer Umgang mit Patient*innen</li>
            <li>Basisfertigkeiten wie Blutabnahmen, Infusionen legen, Anamnesegespräche führen</li>
            <li>Assistenz im OP und bei Untersuchungen</li>
            <li>Mitarbeit im Stations- und Praxisbetrieb</li>
            <li>Verständnis für Teamabläufe in Kliniken und Praxen entwickeln</li>
        </ul>
        <p>Diese Erfahrungen geben dir Sicherheit im späteren Berufsleben und verschaffen dir einen klaren Vorteil bei Bewerbungen für Famulaturen, Hospitationen oder deine Assistenzarztstelle – und natürlich für dein PJ, falls dort keine zentrale Bewerbung erfolgt.</p>
    </li>
    <li><b>Geld verdienen – Studiere sorgenfreier</b>
        <ul>
            <li>Faire Vergütung durch tarifnahe oder marktgerechte Stundenlöhne</li>
            <li>Flexible Arbeitszeiten, angepasst an dein Studium</li>
            <li>Keine Nebenjobs mehr außerhalb deines Fachgebiets</li>
            <li>Attraktiver Status für Arbeitgeber durch reduzierte Sozialabgaben</li>
        </ul>
        <p>Du arbeitest nicht nur sinnvoll nebenbei, sondern baust aktiv an deiner Zukunft.</p>
    </li>
    <li><b>Krankenversicherung – Sicher abgesichert</b>
        <ul>
            <li><b>Unter 25 Jahre:</b> Möglichst weiterhin familienversichert, wenn dein Einkommen unter der Geringfügigkeitsgrenze (556 €/Monat, 2025) bleibt</li>
            <li><b>Über der Geringfügigkeitsgrenze:</b> Günstige werkstudentische Versicherung bei einer Krankenkasse deiner Wahl</li>
            <li>Reduzierte Abgaben: Keine Beiträge zur Kranken-, Pflege- oder Arbeitslosenversicherung, nur Rentenbeiträge</li>
            <li>Fester Beitragssatz: Dein Krankenkassenbeitrag bleibt unabhängig von deinem Einkommen konstant</li>
            <li>Freie Wahl zwischen gesetzlicher und (freiwilliger) privater Krankenversicherung</li>
            <li>Ab deinem 30. Lebensjahr darfst du zwar weiter als Werkstudent*in arbeiten, musst dich aber Eigenständig im Regeltarif krankenversichern</li>
        </ul>
        <p>So bist du auch finanziell bestens abgesichert – und kannst dich voll auf dein Studium konzentrieren.</p>
    </li>
    <li><b>Netzwerk aufbauen – Kontakte für deine medizinische Karriere</b>
        <ul>
            <li>Knüpfe früh Kontakte zu Ärzt:innen, Praxisinhaber:innen und Klinikleitungen</li>
            <li>Sichere dir Empfehlungsschreiben und Kontakte für später</li>
            <li>Stärke dein berufliches Profil durch positive praktische Erfahrungen</li>
        </ul>
        <p>Ein gutes Netzwerk öffnet dir viele Wege für deine Karriere.</p>
    </li>
    <li><b>Spaß haben – Medizin erleben, bevor es richtig losgeht</b>
        <ul>
            <li>Setze dein Wissen in der Praxis um</li>
            <li>Erlebe Teamarbeit und echte Erfolge im Alltag</li>
            <li>Motiviere dich durch Erfahrungen, die dich durch Prüfungszeiten tragen</li>
        </ul>
    </li>
</ol>
<p style='font-weight:bold; color:#15396b;'>Medizin erleben statt nur lernen – das ist Studipraxis.</p>
</div>
""", unsafe_allow_html=True)

# Add a button to go back to the student page
if st.button("Zurück zur Startseite", use_container_width=True):
    st.switch_page("pages/1_Student.py") 