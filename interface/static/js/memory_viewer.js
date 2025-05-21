var editableGrid = null;
var mouse_highlight_mem = [];

function highlightMemoryCells(addresses, className, parseAsHex = false) {
  addresses.forEach(addr => {
    const tofind = formatHexUnsigned32Bits(addr).slice(0, 9) + "0";
    const tableRow = $("#memoryview td")
      .filter((_, td) => $(td).text() === tofind)
      .closest("tr");

    if (tableRow.length === 0) return;

    const col = parseAsHex ? parseInt(addr, 16) % 16 : addr % 16;
    $(".editablegrid-c" + col, tableRow).addClass(className);
  });
}


function updateMemoryBreakpointsView() {
  highlightMemoryCells(mem_highlights_r, "highlightRead");
  highlightMemoryCells(mem_highlights_w, "highlightWrite");
  highlightMemoryCells(mem_breakpoints_r, "mem_r", true);
  highlightMemoryCells(mem_breakpoints_w, "mem_w", true);
  highlightMemoryCells(mem_breakpoints_rw, "mem_rw", true);
  highlightMemoryCells(mem_breakpoints_e, "mem_e", true);
  highlightMemoryCells(mem_breakpoints_instr, "mem_instr");
  highlightMemoryCells(mouse_highlight_mem, "mem_mousehighlight");
}


function changeMemoryViewPage() {
    refresh_mem_paginator = true;
    var target = $("#jump_memory").val();
    target_memaddr = target;
    var page = Math.floor(parseInt(target) / (16 * 20));
    editableGrid.setPageIndex(page);
}

function resetMemoryViewer() {
    refresh_mem_paginator = true;

    const metadata = [
        { name: "ch", label: "addr", datatype: "string", editable: false },
        ...Array.from({ length: 16 }, (_, i) => ({
            name: "c" + i,
            label: i.toString(16).toUpperCase().padStart(2, "0"),
            datatype: "string",
            editable: true,
        })),
    ];

    const data = Array.from({ length: 20 }, (_, i) => {
        const values = { ch: formatHexUnsigned32Bits(i * 16) };
        for (let j = 0; j < 16; j++) values["c" + j] = "--";
        return { id: i, values };
    });

    editableGrid = new EditableGrid("DemoGridJsData", {
        modelChanged(row, col, oldValue, newValue, rowref) {
            if (oldValue === "--") {
                editableGrid.setValueAt(row, col, "--", true);
                return;
            }

            if (newValue.length > 2) {
                newValue = newValue.slice(0, 2);
                editableGrid.setValueAt(row, col, newValue, true);
            }

            const addr = parseInt($("td:first", rowref).text(), 16) + (col - 1);
            sendData(["memchange", addr, newValue]);
        },
        enableSort: false,
        pageSize: 20,
        tableRendered() {
            this.updatePaginator();
            updateMemoryBreakpointsView();
        },
    });

    editableGrid.load({ metadata, data });
    editableGrid.renderGrid("memoryview", "testgrid");

    updateMemoryBreakpointsView();
}

function cellClick(e) {
    var suffix = null;
    for (var i = 0; i < e.target.classList.length; i++) {
        if (e.target.classList[i].slice(0, 14) == "editablegrid-c") {
            suffix = e.target.classList[i].slice(-2);
        }
    }
    if (suffix == null) {
        return;
    }
    if (suffix[0] == "c") {
        suffix = suffix.slice(-1);
    }
    suffix = parseInt(suffix).toString(16);
    if (suffix != "NaN") {
        var addr =
            $("td:first", $(e.target).closest("tr")).text().slice(0, 9) +
            suffix;
        if (e.shiftKey) {
            sendData(["breakpointsmem", addr, "r"]);
        }
        if (e.ctrlKey || e.metaKey) {
            sendData(["breakpointsmem", addr, "w"]);
        }
        if (e.altKey) {
            sendData(["breakpointsmem", addr, "e"]);
        }
    }
}

var refresh_mem_paginator = true;
var target_memaddr = null;

$(document).ready(function () {
    EditableGrid.prototype.updatePaginator = function () {
        if (refresh_mem_paginator) {
            refresh_mem_paginator = false;

            var paginator = $("#paginator").empty();
            var nbPages = this.getPageCount();

            // "first" link
            var link = $("<a>").html(
                '<i class="fa-solid fa-backward-step"></i>'
            );
            if (!this.canGoBack())
                link.css({ opacity: 0.4, filter: "alpha(opacity=40)" });
            else
                link.css("cursor", "pointer").click(function (event) {
                    refresh_mem_paginator = true;
                    editableGrid.firstPage();
                });
            paginator.append(link);

            // "prev" link
            link = $("<a>").html(
                '<i class="fa-solid fa-play" style="transform: rotate(180deg)"></i>'
            );
            if (!this.canGoBack())
                link.css({ opacity: 0.4, filter: "alpha(opacity=40)" });
            else
                link.css("cursor", "pointer").click(function (event) {
                    refresh_mem_paginator = true;
                    editableGrid.prevPage();
                });
            paginator.append(link);

            var mem_begin = $(".editablegrid-ch:eq(1)").text();
            if (target_memaddr !== null) {
                mem_begin = target_memaddr;
            }
            paginator.append(
                '<input id="jump_memory" type="text" value="' +
                    mem_begin +
                    '"/><input id="jump_memory_go" type="submit" value="Go">'
            );
            target_memaddr = null;

            $("#jump_memory").keyup(function (e) {
                if (e.keyCode == 13) {
                    changeMemoryViewPage();
                }
            });
            $("#jump_memory_go").click(changeMemoryViewPage);

            // "next" link
            link = $("<a>").html('<i class="fa-solid fa-play"></i>');
            if (!this.canGoForward())
                link.css({ opacity: 0.4, filter: "alpha(opacity=40)" });
            else
                link.css("cursor", "pointer").click(function (event) {
                    refresh_mem_paginator = true;
                    editableGrid.nextPage();
                });
            paginator.append(link);

            // "last" link
            link = $("<a>").html('<i class="fa-solid fa-forward-step"></i>');
            if (!this.canGoForward())
                link.css({ opacity: 0.4, filter: "alpha(opacity=40)" });
            else
                link.css("cursor", "pointer").click(function (event) {
                    refresh_mem_paginator = true;
                    editableGrid.lastPage();
                });
            paginator.append(link);
        }
    };

    $("#memoryview").click(cellClick);
    resetMemoryViewer();
});
