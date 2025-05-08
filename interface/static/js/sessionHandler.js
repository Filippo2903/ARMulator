// Timer per salvare automaticamente l'editor ogni 60 secondi
var saveEditorTimer = window.setInterval(onTimer, 60000);

// Inizializza l'editor con una sessione valida o crea una nuova
(function initializeEditor() {
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || {
        defaultEditor: editor.getValue(),
        current: null,
        data: [],
    };

    if (!Array.isArray(savedEditor.data) || savedEditor.data.length === 0) {
        createNewSession();
    } else if (
        savedEditor.current !== null &&
        savedEditor.data[savedEditor.current]
    ) {
        editor.setValue(savedEditor.data[savedEditor.current].code, -1);
    } else {
        savedEditor.current = 0;
        editor.setValue(savedEditor.data[0].code, -1);
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedEditor));
    }

    updateSessionPanel();
})();

// Bind per eliminare una sessione
$(document).on("click", ".delete_button", function () {
    const sessionId = parseInt($(this).data("session-index"));
    deleteSession(sessionId);
});

// Gestisci la cancellazione di una sessione
function deleteSession(sessionId) {
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));

    if (savedEditor.current !== null) {
        var message = "Are you sure you want to delete this session?";

        if (confirm(message)) {
            if (savedEditor.data.length === 1) {
                editor.setValue(savedEditor.defaultEditor, -1);
                savedEditor.current = null;
                savedEditor.data = [];
            } else {
                saveCurrentEditor();
                savedEditor = JSON.parse(
                    localStorage.getItem(LOCAL_STORAGE_KEY)
                );
                savedEditor.data.splice(sessionId, 1);
                savedEditor.current =
                    savedEditor.current === sessionId ? 0 : sessionId;
                editor.setValue(savedEditor.data[0].code, -1);
            }

            localStorage.setItem(
                LOCAL_STORAGE_KEY,
                JSON.stringify(savedEditor)
            );

            updateSessionPanel();

            if (savedEditor["data"].length === 0) {
                createNewSession();
            }
        }
    }
}

// Binding per nuova sessione
$(document).on("click", "#session_new", createNewSession);

// Gestisci la creazione di una nuova sessione
function createNewSession() {
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || {
        defaultEditor: editor.getValue(),
        current: null,
        data: [],
    };

    if (savedEditor.current !== null) {
        saveCurrentEditor();
        savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
        savedEditor.data.unshift({
            name: "New Session",
            code: editor.getValue(),
        });
        savedEditor.current = 0;
    } else {
        savedEditor.current = 0;
        savedEditor.data = [
            {
                name: "New Session",
                code: editor.getValue(),
            },
        ];
    }

    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedEditor));
    editor.setValue(savedEditor.defaultEditor, -1);
    saveCurrentEditor(true);
    updateSessionPanel();
}

// Previene l'inserimento di nuove righe nel pannello delle sessioni
$("#session_content").keydown(function (e) {
    if (e.keyCode === 13) return false;
});

// Salva il nome nel localStorage quando viene cambiato
$(document).on("input", "#session_name", function () {
    var newName = $(this).text().trim(); // Ottieni il nuovo nome (senza spazi prima e dopo)
    if (!newName) {
        newName = "New Session"; // Imposta un nome predefinito se il campo è vuoto
    }

    // Ottieni la sessione attualmente selezionata
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));

    if (savedEditor.current !== null) {
        // Aggiorna il nome della sessione nel salvataggio
        savedEditor.data[savedEditor.current].name = newName;
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedEditor)); // Salva nel localStorage
    }
});

// Funzione per salvare l'editor corrente
function saveCurrentEditor(forceNewName = false) {
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || {
        defaultEditor: editor.getValue(),
        current: null,
        data: [],
    };

    var name = $("#selected #session_name").html();
    if (!name || forceNewName) {
        name = "New Session";
    }

    var data = {
        code: editor.getValue(),
        name: name,
    };

    if (
        typeof savedEditor.current === "number" &&
        Array.isArray(savedEditor.data)
    ) {
        savedEditor.data[savedEditor.current] = data;
    } else {
        savedEditor.current = 0;
        savedEditor.data = [data];
    }

    if (!savedEditor.defaultEditor) {
        savedEditor.defaultEditor = editor.getValue();
    }

    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedEditor));
}

// Funzione per ottenere la data o l'ora della sessione
function getDateOrHour(p_date) {
    var today = new Date();
    var dateToCompare = new Date(0);
    if (
        today.setDate(today.getDate() - 1) <
        dateToCompare.setUTCMilliseconds(p_date)
    ) {
        return dateToCompare.toTimeString().split(" ")[0];
    } else {
        return (
            dateToCompare.getDate() +
            "/" +
            (dateToCompare.getMonth() + 1) +
            "/" +
            dateToCompare.getFullYear()
        );
    }
}

// Funzione per aggiornare il pannello delle sessioni
function updateSessionPanel() {
    var content = $("#session_content");
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    content.html("");
    if (savedEditor.current !== null) {
        var current = savedEditor.current;

        for (let i = 0; i < savedEditor.data.length; i++) {
            var data = savedEditor.data[i];

            var selectedProperty = 'onclick="restoreSession(' + i + ')"';
            var editable = "";
            if (current === i) {
                selectedProperty = 'id="selected"';
                editable = 'contenteditable="true"';
            }
            var message =
                "<div " +
                selectedProperty +
                ' class="session_item">' +
                '<div id="session_id">' +
                (i + 1) +
                "</div>" +
                '<div class="session_item_right">' +
                '<div id="session_name" ' +
                editable +
                ">" +
                data.name +
                `</div><div><button class="delete_button" data-session-index="${i}">Delete</button></div>` +
                "</div></div>";

            content.append(message);
        }
    }
}

// Funzione per il timer di salvataggio automatico
function onTimer() {
    var defaultEditor = JSON.parse(
        localStorage.getItem(LOCAL_STORAGE_KEY)
    ).defaultEditor;
    var currentEditor = editor.getValue();
    if (defaultEditor !== currentEditor) {
        saveCurrentEditor();
        updateSessionPanel();
    }
}

// Funzione per ripristinare una sessione selezionata
function restoreSession(selected) {
    saveCurrentEditor();
    console.log("Restoring session:", selected);
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    editor.setValue(savedEditor.data[selected].code, -1);
    savedEditor.current = selected;
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedEditor));
    updateSessionPanel();
}

// Salvataggio finale dell'editor prima della chiusura della finestra
window.onbeforeunload = function () {
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    var defaultEditor = savedEditor.defaultEditor;
    var currentEditor = editor.getValue();
    if (defaultEditor !== currentEditor) {
        saveCurrentEditor();
    }
};
