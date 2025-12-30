document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("cmdForm");
    const input = document.getElementById("cmd");   // <-- richtig!
    const output = document.getElementById("output");
    const button = document.getElementById("runBtn");

    // -----------------------------
    //  Befehlshistorie
    // -----------------------------
    let history = [];
    let historyIndex = -1;

    input.addEventListener("keydown", (e) => {
        if (e.key === "ArrowUp") {
            e.preventDefault();
            if (historyIndex > 0) {
                historyIndex--;
                input.value = history[historyIndex];
            } else if (historyIndex === -1 && history.length > 0) {
                historyIndex = history.length - 1;
                input.value = history[historyIndex];
            }
        }

        if (e.key === "ArrowDown") {
            e.preventDefault();
            if (historyIndex < history.length - 1) {
                historyIndex++;
                input.value = history[historyIndex];
            } else {
                historyIndex = -1;
                input.value = "";
            }
        }
    });

    // -----------------------------
    //  Formular absenden
    // -----------------------------
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const cmd = input.value.trim();
        if (!cmd) return;

        // Eingabefeld leeren
        input.value = "";

        // History speichern
        history.push(cmd);
        historyIndex = -1;

        // UI sperren
        output.textContent = "";
        button.disabled = true;
        button.textContent = "Läuft...";

        // SSE starten
        const evtSource = new EventSource("/stream?command=" + encodeURIComponent(cmd));

        evtSource.onmessage = function (event) {
            if (event.data === "[END]") {
                evtSource.close();
                button.disabled = false;
                button.textContent = "Ausführen";
                return;
            }

            const div = document.createElement("div");
            div.textContent = event.data;
            output.appendChild(div);
            output.scrollTop = output.scrollHeight;
        };

        evtSource.onerror = function () {
            const div = document.createElement("div");
            div.textContent = "Verbindung unterbrochen.";
            output.appendChild(div);
            output.scrollTop = output.scrollHeight;

            evtSource.close();
            button.disabled = false;
            button.textContent = "Ausführen";
        };
    });
});
