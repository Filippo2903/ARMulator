var blockSelect = 0;
var selectLine = -1;

// Message bar
$("#message_bar").click(function () {
    $(this).slideToggle("normal", "easeInOutBack", function () {});
});

$("#assemble").click(function () {
    assemble();
});

// Change register tabs
$(".select_registers").click(function (e) {
    showTab(e.target.value);
});

$(document).ready(function () {
    // Change language of html elements if not default
    if (currentLang !== DEFAULT_LANG)
        for (const [key, value] of Object.entries(
            frontEndDictionary.htmlElements
        ))
            $(key).html(value);

    const $languageSelect = $("#language");

    $.each(allLanguages, function (code, label) {
        $("<option>").val(code).html(label).appendTo($languageSelect);
    });

    $(".register_row").click(function (e) {
        var mode = "";
        if (e.ctrlKey || e.metaKey) {
            $(this).toggleClass("reg_bkp_w");
        }
        if (e.shiftKey) {
            $(this).toggleClass("reg_bkp_r");
        }
        if (!(e.ctrlKey || e.metaKey || e.shiftKey)) {
            return;
        }

        if ($(this).hasClass("reg_bkp_w")) {
            mode = mode + "w";
        }
        if ($(this).hasClass("reg_bkp_r")) {
            mode = mode + "r";
        }

        sendData(["update", "bp_" + mode + "_" + $(this).attr("id")]);

        clearSelection();
    });

    function openConfigDialog() {
        $("#config_overlay").fadeIn(150, function () {
            $("#language option").each(function (_, option) {
                if (option.value === getLang()) {
                    option.selected = true;
                }
            });
            $("body").css("overflow", "hidden");
        });
    }

    function closeConfigDialog() {
        $("#config_overlay").fadeOut(150, function () {
            setLang($("#language").val());
            $("body").css("overflow", "");
        });
    }

    $("#config_overlay").on("click", function (e) {
        if (e.target.id === "config_overlay") {
            closeConfigDialog();
        }
    });

    function saveConfig() {
        setLang($("#language").val());
        closeConfigDialog();
    }

    $("#settings").on("click", openConfigDialog);
    $("#saveConfig").on("click", saveConfig);
    $("#closeConfig").on("click", closeConfigDialog);

    let sessionToDelete = null;

    function openDeleteDialog(index) {
        sessionToDelete = index;
        $("#delete_overlay").fadeIn(150, function () {
            $("body").css("overflow", "hidden");
        });
    }

    function closeDeleteDialog() {
        $("#delete_overlay").fadeOut(150, function () {
            $("body").css("overflow", "");
        });
    }

    $("#delete_overlay").on("click", function (e) {
        if (e.target.id === "delete_overlay") {
            closeDeleteDialog();
        }
    });

    $("#cancel-delete").on("click", function () {
        closeDeleteDialog();
    });

    $("#confirm-delete").on("click", function () {
        if (sessionToDelete !== null) {
            performDeleteSession(sessionToDelete);
            sessionToDelete = null;
        }
        closeDeleteDialog();
    });

    function closeMaxSessionDialog() {
        $("#max_sessions_overlay").fadeOut(150, function () {
            $("body").css("overflow", "");
        });
    }

    $("#max_sessions_overlay").on("click", function () {
        closeMaxSessionDialog();
    });

    $("#max_sessions_dialog").on("click", function (event) {
        event.stopPropagation(); // Evita che il click sul dialog chiuda l’overlay
    });

    $("#close-max-sessions").on("click", function () {
        closeMaxSessionDialog();
    });

    $(document).on("click", ".delete_session", function () {
        const index = parseInt($(this).data("session-index"));
        openDeleteDialog(index);
    });

    editor.setHighlightGutterLine(false);

    editor.on("guttermousedown", function (e) {
        var target = e.domEvent.target;
        if (target.className.indexOf("ace_gutter-cell") == -1) return;

        var row = e.getDocumentPosition().row;
        var index = $.inArray(row, asm_breakpoints);
        if (index >= 0) {
            asm_breakpoints.splice(index, 1);
            editor.session.clearBreakpoint(row);
        } else {
            asm_breakpoints.push(row);
            if ($("#assemble").text() == frontEndDictionary.start) {
                editor.session.setBreakpoint(row);
            }
        }

        if ($("#assemble").text() == frontEndDictionary.stop) {
            sendBreakpointsInstr();
        }

        blockSelect = blockSelect + 1;
        selectLine = row;
        setTimeout(function () {
            blockSelect = blockSelect - 1;
        }, 500);
    });

    editor.on("changeSelection", function (e) {
        var cur_row = editor.getCursorPosition()["row"];
        $(".mem_mousehighlight").removeClass("mem_mousehighlight");
        if (cur_row in line2addr) {
            mouse_highlight_mem = line2addr[cur_row];
        }
        updateMemoryBreakpointsView();

        if (blockSelect > 0) {
            editor.selection.setSelectionRange({
                start: {
                    row: selectLine,
                    column: selectLine,
                },
                end: {
                    row: selectLine,
                    column: selectLine,
                },
            });
        }
    });

    editor.on("change", function (e) {
        if (debug_marker !== null) {
            editor.session.removeMarker(debug_marker);
        }
        resetView();
        var end_row = e.end.row;
        var start_row = e.start.row;
        if (end_row != start_row) {
            editor.session.clearBreakpoints();
            for (var i = asm_breakpoints.length - 1; i >= 0; i--) {
                var row = asm_breakpoints[i];
                if (e.action == "insert") {
                    if (
                        row > start_row ||
                        (row == start_row && e.start.column == 0)
                    ) {
                        asm_breakpoints[i] = row + end_row - start_row;
                    }
                } else {
                    if (
                        (row > start_row ||
                            (row == start_row && e.start.column == 0)) &&
                        (row < end_row || (row == end_row && e.end.column > 0))
                    ) {
                        asm_breakpoints.splice(i, 1);
                    } else if (row > start_row) {
                        asm_breakpoints[i] = row + start_row - end_row;
                    }
                }
            }
            refreshBreakpoints();
        }
    });

    $("#interrupt_type").change(function () {
        if (document.getElementById("interrupt_active").checked) {
            sendData([
                "interrupt",
                true,
                $("#interrupt_type").val(),
                parseInt($("#interrupt_cycles").val()),
                parseInt($("#interrupt_cycles_first").val()),
            ]);
        }
    });

    $("#interrupt_active").change(function () {
        if (this.checked) {
            sendData([
                "interrupt",
                true,
                $("#interrupt_type").val(),
                parseInt($("#interrupt_cycles").val()),
                parseInt($("#interrupt_cycles_first").val()),
            ]);
        } else {
            sendData([
                "interrupt",
                false,
                $("#interrupt_type").val(),
                parseInt($("#interrupt_cycles").val()),
                parseInt($("#interrupt_cycles_first").val()),
            ]);
        }
    });

    $("input[type=text]:not(.session_name)").change(function () {
        var objid = $(this).attr("id");
        if (objid == "animate_speed") {
            return;
        }

        if (
            objid == "interrupt_active" ||
            objid == "interrupt_cycles" ||
            objid == "interrupt_cycles_first"
        ) {
            if (document.getElementById("interrupt_active").checked) {
                sendData([
                    "interrupt",
                    true,
                    $("#interrupt_type").val(),
                    parseInt($("#interrupt_cycles").val()),
                    parseInt($("#interrupt_cycles_first").val()),
                ]);
            }
            return;
        }

        target_val = $(this).val();

        if ($.inArray("formatted_value", this.classList) >= 0) {
            // Convert to hex if from another format
            format_ = $("#valueformat").val();
            if (format_ == "dec") {
                target_val = parseInt(target_val).toString(16);
            } else if (format_ == "decsign") {
                target_val = parseInt(target_val);
                if (target_val < 0) {
                    target_val = target_val + Math.pow(2, 32);
                }
                target_val = target_val.toString(16);
            } else if (format_ == "bin") {
                target_val = parseInt(target_val, 2).toString(16);
            } else if (format_ == "hex") {
                target_val = parseInt(target_val, 16).toString(16);
            }
        }

        if ("NaN" === target_val) {
            $(this).val("0");
            target_val = "0";
        }

        sendData(["update", $(this).attr("id"), target_val]);
    });

    $(".flag_btn").click(function () {
        if (!$("input", this).prop("disabled")) {
            sendData(["update", $(this).attr("name")]);
        }
    });

    // Help buttons
    $("#stepback").tooltipster({
        content: frontEndDictionary.stepback,
        position: "bottom",
    });
    $("#run").tooltipster({
        content: frontEndDictionary.run,
        position: "bottom",
    });
    $("#stepin").tooltipster({
        content: frontEndDictionary.stepin,
        position: "bottom",
    });
    $("#stepforward").tooltipster({
        content: frontEndDictionary.stepforward,
        position: "bottom",
    });
    $("#stepout").tooltipster({
        content: frontEndDictionary.stepout,
        position: "bottom",
    });

    var previous_format = "hex";
    $("#valueformat").change(function () {
        $(".formatted_value").each(function () {
            format_ = $("#valueformat").val();
            target_val = NaN;

            if (previous_format == "dec" || previous_format == "decsign") {
                target_val = parseInt($(this).val());
            } else if (previous_format == "bin") {
                target_val = parseInt($(this).val(), 2);
            } else if (previous_format == "hex") {
                target_val = parseInt($(this).val(), 16);
            }

            if (target_val < 0) {
                target_val = target_val + Math.pow(2, 32);
            }

            if (isNaN(target_val)) {
                return;
            }

            if (format_ == "dec") {
                $(this).val(target_val.toString());
            } else if (format_ == "decsign") {
                if (target_val > Math.pow(2, 31) - 1) {
                    target_val = target_val - Math.pow(2, 32);
                }
                $(this).val(target_val.toString());
            } else if (format_ == "bin") {
                $(this).val(target_val.toString(2));
            } else if (format_ == "hex") {
                $(this).val(formatHexUnsigned32Bits(target_val).slice(2));
            }
        });
        previous_format = $("#valueformat").val();
    });

    disableSim();
});
