
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
function putPaginator(paginatorTarget, fetchDataFunction, data) {
    paginatorTarget.html("");
    let paginatorDiv = getPaginatorDiv(data.total_pages, data.page_size, data.page_number,
        data.has_previous, data.previous_page_number, data.has_next, data.next_page_number);
    paginatorTarget.html(paginatorDiv);

    paginatorTarget.find( "a" ).click(function( event ) {
        event.preventDefault();
        let elem = $(this);
        let page = elem.data('page');
        let pageSize = elem.data('pageSize');
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


$( document ).ready(function() {
    console.log("main.js loaded");
});
