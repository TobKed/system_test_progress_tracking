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

    if (hasPrevious == true) {
        paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='"+ 1 + "' data-page-size='" + pageSize + "' href='?page=1&page_size=" + pageSize + "'>First</a>");
        paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='"+ previousPageNumber + "' data-page-size='" + pageSize + "' href='?page=" + previousPageNumber + "&page_size=" + pageSize + "'>Previous</a>");
    }

    for (let i = 1; i <= totalPages; i++) {
        if (i == pageNumber) {
            paginatorDiv.append("<a class='btn btn-info mb-4 mx-1' data-page='"+ i + "' data-page-size='" + pageSize + "' href='?page=" + i + "&page_size=" + pageSize + "'>" + i + "</a>");
        } else if ( (i > (pageNumber-3)) && (i < (pageNumber+3)) ) {
            paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='"+ i + "' data-page-size='"+ pageSize + "' href='?page=" + i + "&page_size=" + pageSize + "'>" + i + "</a>");
        }

    }

    if (hasNext == true) {
        paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='"+ nextPageNumber + "' data-page-size='"+ pageSize + "' href='?page=" + nextPageNumber + "&page_size=" + pageSize + "'>Next</a>");
        paginatorDiv.append("<a class='btn btn-outline-info mb-4 mx-1' data-page='"+ totalPages + "' data-page-size='"+ pageSize + "' href='?page=" + totalPages     + "&page_size=" + pageSize + "'>Last</a>");
    }

    return paginatorDiv;
}


$( document ).ready(function() {
    console.log("pagination test");

});
