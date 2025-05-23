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

function performDeleteSession(sessionId) {
  var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));

  if (savedEditor.current !== null) {
    if (savedEditor.data.length === 1) {
      editor.setValue(savedEditor.defaultEditor, -1);
      savedEditor.current = null;
      savedEditor.data = [];
    } else {
      saveCurrentEditor();
      savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
      savedEditor.data.splice(sessionId, 1);

      if (savedEditor.current === sessionId) {
        savedEditor.current = Math.max(sessionId - 1, 0);
      } else if (savedEditor.current > sessionId) {
        savedEditor.current -= 1;
      }

      editor.setValue(savedEditor.data[savedEditor.current].code, -1);
    }

    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedEditor));
    updateSessionPanel();

    if (savedEditor.data.length === 0) {
      createNewSession();
    }
  }
}

$(document).on("click", "#new_session", createNewSession);

function openMaxSessionDialog() {
  $("#max_sessions_overlay").fadeIn(150, function () {
    $("body").css("overflow", "hidden");
  });
}

function createNewSession() {
  var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || {
    defaultEditor: editor.getValue(),
    current: null,
    data: [],
  };

  if (savedEditor.data.length >= 10) {
    openMaxSessionDialog();
    return;
  }

  if (savedEditor.current !== null) {
    saveCurrentEditor();
    savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));

    savedEditor.data.push({
      name: frontEndDictionary.newSession,
      code: editor.getValue(),
    });

    savedEditor.current = savedEditor.data.length - 1;
  } else {
    savedEditor.current = 0;
    savedEditor.data = [
      {
        name: frontEndDictionary.newSession,
        code: editor.getValue(),
      },
    ];
  }

  localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedEditor));
  editor.setValue(savedEditor.defaultEditor, -1);
  saveCurrentEditor(true);
  updateSessionPanel();
}

function saveSessionName($input) {
  var newName = $input.val().trim();
  var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
  if (savedEditor.current !== null) {
    savedEditor.data[savedEditor.current].name = newName;
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedEditor));
  }
}

$(document).on("input", ".session_name", function () {
  saveSessionName($(this));
});

$(document).on("blur", ".session_name", function () {
  var $this = $(this);
  var text = $this.val().trim();

  if (text === "") {
    var $container = $this.closest(".session_item");
    var index = $container.find(".delete_session").data("session-index");
    $this.val(frontEndDictionary.session + " " + (index + 1));
  }

  saveSessionName($this);
});

// Funzione per salvare l'editor corrente
function saveCurrentEditor(forceNewName = false) {
  var savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || {
    defaultEditor: editor.getValue(),
    current: null,
    data: [],
  };

  var name = $("#selected .session_name").val();
  if (!name || forceNewName) {
    name = frontEndDictionary.newSession;
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

// Funzione per aggiornare il pannello delle sessioni
function updateSessionPanel() {
  const content = $("#sessions");
  const savedEditor = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));

  const newSessionBtn = $("#new_session").detach();
  content.empty();

  if (savedEditor.current !== null) {
    const current = savedEditor.current;

    for (let i = 0; i < savedEditor.data.length; i++) {
      const data = savedEditor.data[i];

      const message = `<div ${
        current === i ? 'id="selected"' : `onclick="restoreSession(${i})"`
      } class="session_item">
                <div class="session_name_wrapper">
                    <input name="session_name" type="text" class="session_name" value="${
                      data.name
                    }">
                </div>
                <i class="delete_session fa-solid fa-xmark fa-2x" data-session-index="${i}"></i>
            </div>`;

      content.append(message);
    }
  }

  content.append(newSessionBtn);
}

// Funzione per il timer di salvataggio automatico
function onTimer() {
  var defaultEditor = JSON.parse(
    localStorage.getItem(LOCAL_STORAGE_KEY),
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
