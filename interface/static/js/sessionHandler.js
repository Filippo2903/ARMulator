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
$(document).on("click", ".delete_session", function () {
    const sessionId = parseInt($(this).data("session-index"));
    deleteSession(sessionId);
});

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

                if (savedEditor.current === sessionId) {
                    savedEditor.current = Math.max(sessionId - 1, 0);
                } else if (savedEditor.current > sessionId) {
                    savedEditor.current -= 1;
                }

                editor.setValue(savedEditor.data[savedEditor.current].code, -1);
            }

            localStorage.setItem(
                LOCAL_STORAGE_KEY,
                JSON.stringify(savedEditor)
            );
            updateSessionPanel();

            if (savedEditor.data.length === 0) {
                createNewSession();
            }
        }
    }
}

// Binding per nuova sessione
$(document).on("click", "#session_new", createNewSession);

function createNewSession() {
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || {
        defaultEditor: editor.getValue(),
        current: null,
        data: [],
    };

    if (savedEditor.data.length >= 10) {
        alert("Max number of sessions reached");
        return;
    }

    if (savedEditor.current !== null) {
        saveCurrentEditor();
        savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));

        // Aggiunge alla fine
        savedEditor.data.push({
            name: "New Session",
            code: editor.getValue(),
        });

        // Imposta l'indice corrente sull'ultimo elemento
        savedEditor.current = savedEditor.data.length - 1;
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
$("#sessions").keydown(function (e) {
    if (e.keyCode === 13) return false;
});

$(document).on("keydown", ".session_name", function (e) {
    var $this = $(this);
    var text = $this.text();

    // Se l'utente preme backspace e il testo ha solo un carattere, blocca l'azione
    if (e.key === "Backspace" && text.length === 1) {
        e.preventDefault();
    }
});

$(document).on("input", ".session_name", function () {
    var $this = $(this);
    var newName = $this.text().trim();

    if (!newName) {
        newName = "New Session";
        $this.text(newName);
    }

    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));

    if (savedEditor.current !== null) {
        savedEditor.data[savedEditor.current].name = newName;
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedEditor));
    }
});

// Funzione per salvare l'editor corrente
function saveCurrentEditor(forceNewName = false) {
    var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || {
        defaultEditor: editor.getValue(),
        current: null,
        data: [],
    };

    var name = $("#selected .session_name").html();
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
    var content = $("#sessions");
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
            var message = `<div ${selectedProperty} class="session_item">
            <div class="session_name" ${editable}>${data.name}</div>
            <button class="delete_session" data-session-index="${i}">X</button>
            </div>`;

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
