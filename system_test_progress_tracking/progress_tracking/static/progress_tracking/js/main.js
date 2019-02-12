
/**
 * get paginator div (used by putPaginator function)
 * @param  {Number} totalPages
 * @param  {Number} pageSize
 * @param  {Number} pageNumber
 * @param  {Boolean} hasPrevious
 * @param  {Number} previousPageNumber
 * @param  {Number} hasNext
 * @param  {Boolean} nextPageNumber
 */
function getPaginatorDiv(totalPages, pageSize, pageNumber,
                         hasPrevious, previousPageNumber,
                         hasNext, nextPageNumber) {

    let paginatorDiv = $( document.createElement('div') );
    
    if (totalPages > 1) {
        if (hasPrevious == true) {
            paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='" + 1 + "' data-page-size='" + pageSize + "' href='?page=1&page_size=" + pageSize + "'>First</a>");
            paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='" + previousPageNumber + "' data-page-size='" + pageSize + "' href='?page=" + previousPageNumber + "&page_size=" + pageSize + "'>Previous</a>");
        }

        for (let i = 1; i <= totalPages; i++) {
            if (i == pageNumber) {
                paginatorDiv.append("<a class='btn btn-info mb-4 mx-1' data-page='" + i + "' data-page-size='" + pageSize + "' href='?page=" + i + "&page_size=" + pageSize + "'>" + i + "</a>");
            } else if ((i > (pageNumber - 3)) && (i < (pageNumber + 3))) {
                paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='" + i + "' data-page-size='" + pageSize + "' href='?page=" + i + "&page_size=" + pageSize + "'>" + i + "</a>");
            }

        }

        if (hasNext == true) {
            paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='" + nextPageNumber + "' data-page-size='" + pageSize + "' href='?page=" + nextPageNumber + "&page_size=" + pageSize + "'>Next</a>");
            paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='" + totalPages + "' data-page-size='" + pageSize + "' href='?page=" + totalPages + "&page_size=" + pageSize + "'>Last</a>");
        }
    }
        
    paginatorDiv.append("<div class='dropdown d-inline mb-4 mx-1 float-right'>" +
        "<button class='btn btn-outline-info dropdown-toggle' type='button' id='dropdownMenuButton' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
            "Items per page: " + pageSize +
        "</button>" +
        "<div class='dropdown-menu' aria-labelledby='dropdownMenuButton'>" +
            "<a class='dropdown-item' data-page='1' data-page-size='10' href='#'>10</a>" +
            "<a class='dropdown-item' data-page='1' data-page-size='40' href='#'>40</a>" +
            "<a class='dropdown-item' data-page='1' data-page-size='100' href='#'>100</a>" +
        "</div>" +
    "</div>");

    return paginatorDiv;
}


/**
 * put paginator to given element
 * @param  {String} paginatorTarget    element where paginator will be put.
 * @param  {String} fetchDataFunction  data received from django rest endpoint
 * @param  {String} data               data received from django rest endpoint
 *                                     shall contain following properties:
 *                                        total_pages
 *                                        page_size
 *                                        page_number
 *                                        has_previous
 *                                        previous_page_number
 *                                        has_next
 *                                        next_page_number
 */
function putPaginator(paginatorTarget, fetchDataFunction, data, cookieName) {
    paginatorTarget.html("");
    let paginatorDiv = getPaginatorDiv(data.total_pages, data.page_size, data.page_number,
        data.has_previous, data.previous_page_number, data.has_next, data.next_page_number);
    paginatorTarget.html(paginatorDiv);

    paginatorTarget.find( "a" ).click(function( event ) {
        event.preventDefault();
        let elem = $(this);
        let page = elem.data('page');
        let pageSize = elem.data('pageSize');
        if (cookieName != undefined) {
            console.log("test");
            Cookies.set(Cookies.set(cookieName, pageSize, { expires: 31 }));
        }
        fetchDataFunction(page, pageSize);
    });
}


function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'), sParameterName, i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
}


/**
 * Fills info modal with script details.
 * Filled modal has is located by selectors:
 *           - "#infoModalLabel"
 *           - "#infoModal .modal-body"
 *
 * @param  {data} data  data from which modal will be filled.
 *     it has to contain properties:
 *           - script  - code of python script
 *           - file_name
 *           - file_path
 *           - timestamp_start
 *           - timestamp_stop
 */
function fillInfoModal(data) {
    let infoModalLabel = $("#infoModalLabel");
    let infoModalBody = $("#infoModal .modal-body");
    let script = data.script;
    script = "<pre><code>" + script + "</code></pre>";
    infoModalLabel.text(data.file_name);
    let html = "<div>" +
            "<p>file name: " + data.file_name + "</p>" +
            "<p>file path: <small>" + data.file_path + "</small></p>" +
            "<p>start: " + data.timestamp_start + "</p>" +
            "<p>stop: " + data.timestamp_stop + "</p>" +
            "<p>script: </p>" + script;
    infoModalBody.html(html);
    let codes = document.querySelectorAll('code');
    [].forEach.call(codes, function (block) {
        hljs.highlightBlock(block)
    });
}



function fillPageWithData(data) {
    console.log("fillPageWithData");
    let machineName = data.machine_name;
    let masterScenario = data.last_master_scenario;
    let timestampStart = masterScenario.timestamp_start;
    let startedAgo = masterScenario.started_ago;
    let timestampStop = masterScenario.timestamp_stop;
    let finishedAgo = masterScenario.finished_ago;
    let duration = masterScenario.duration;
    let status = masterScenario.status;
    let testsCount = masterScenario.tests_count;
    let scenariosCount = masterScenario.scenarios_count;
    let testsStatistics = masterScenario.tests_statistics;
    let scenarios = masterScenario.scenarios;

    // fill first paragraph
    let firstParagraph = $("#firstParagraph");
    if ((finishedAgo != null) && (timestampStop != null)) {
        finishedAgo = finishedAgo + " ago";
    } else {
        finishedAgo = "";
        timestampStop = "-";
        duration = "-";
    }

    firstParagraph.html(
        "Started: <span >" + timestampStart + "</span> <small>" + startedAgo + " ago</small>" +
        "<span class='mx-3 badge bg-ts-" + status + "'>" + status + "</span>" +
        "<button class='btn btn-info btn-sm info-button' data-toggle='modal' title='Info' data-target='#infoModal' data-model-name='master_scenario' data-model-id='" + masterScenario.pk + "'><span class='fas fa-info'></span></button>");

    firstParagraph.append(
        "<br>" +
        "Finished: " + timestampStop + " <small>" + finishedAgo + " </small>" +
        "<br>" +
        "Execution time: " + duration);

    // fill table-statistics
    let tableStatistics = $("#tableStatistics");
    $.each(testsStatistics, function(key, value) {
        tableStatistics.find("#ts-" + key).text(value);
    });
    tableStatistics.find("#ts-testsCount").text(testsCount);
    tableStatistics.find("#ts-scenariosCount").text(scenariosCount);

    // fill tests table
    let tableScenariosTests = $("#tableScenarioTests");
    let tableBody = tableScenariosTests.find("tbody");
    tableBody.html("");
    $.each(scenarios, function(index, scenario) {
        let tests = scenario.tests;
        tableBody.append(
            "<tr>" +
            "<th colspan='3' class='bg-steel-light align-middle'>" + scenario.file_name + "</th>" +
            "<td class='align-middle text-center bg-steel-light' style='width: 10%'>" +
            "<button class='btn btn-info btn-xs info-button' data-toggle='modal' title='Info' data-target='#infoModal' data-model-name='scenario' data-model-id='" + scenario.pk + "'><span class='fas fa-info xs'></span></button>" +
            "</td>" +
            "</tr>");

        $.each(tests, function (index, test) {
            let additionalStyle = "";
            if ((test.status == "running") || (test.status == "waiting")) {
                additionalStyle = "progress-bar-striped progress-bar-animated";
            }

            tableBody.append(
                "<tr>" +
                "<td class='align-middle' style='width: 10%'>" + index + "</td>" +
                "<td class='align-middle' style='width: 40%'>" + test.file_name + "</td>" +
                "<td class='align-middle' style='width: 40%'>" +
                    "<div class='progress' style='height: 38px;'>" +
                        "<div class='progress-bar bg-ts-" + test.status + " " + additionalStyle + "' role='progressbar' aria-valuenow='100' aria-valuemin='0' aria-valuemax='100' style='width: 100%'>" + test.status + "</div>" +
                    "</div>" +
                "</td>" +
                "</td>" +
                "<td class='align-middle text-center' style='width: 10%'>" +
                    "<button class='btn btn-info btn-xs info-button' data-toggle='modal' title='Info' data-target='#infoModal' data-model-name='test' data-model-id='" + test.pk + "'><span class='fas fa-info xs'></span></button>" +
                "</td>" +
                "</tr>")
        })
    })
}


function assingInfoButton() {
    $("button.info-button").click(function () {
        let modelId = $(this).data("modelId");
        let modelName = $(this).data("modelName");

        $.ajax({
            url: "/tm_api/" + modelName + "/" + modelId,
            method: "GET",
            success: function (data) {
                fillInfoModal(data);
            },
            error: function (data) {
                console.log("error");
                console.log(data);
            }
        });
    })
}



$( document ).ready(function() {
    console.log("main.js loaded");
});
