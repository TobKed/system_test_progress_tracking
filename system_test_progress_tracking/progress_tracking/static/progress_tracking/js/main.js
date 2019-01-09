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
            "<a class='dropdown-item' data-page='1' data-page-size='2' href='#'>2</a>" +
            "<a class='dropdown-item' data-page='1' data-page-size='4' href='#'>4</a>" +
            "<a class='dropdown-item' data-page='1' data-page-size='6' href='#'>6</a>" +
        "</div>" +
    "</div>");




    return paginatorDiv;
}


$( document ).ready(function() {
    console.log("pagination test");

});
