
/**
 * Changes the text of the article textarea to the given
 * button category
 * @param  {element} button The html button to get the
 * category name from
 * @param  {string} jsonStaticPath The string with the
 * path to the json file with the article samples
 */
function changeArticleText(button, jsonStaticPath){

    const articleTextElement = document.getElementById("article-text");
    const articleCategory = button.innerHTML;

    /* Read the json file using jQuery */
    $.getJSON(jsonStaticPath)
        .done(function (data) {
            /* .trim is necessary to remove any spaces from the name */
            const categoryName = $.trim(articleCategory.toLowerCase());
            /* Change the textarea value */
            articleTextElement.value = data[categoryName];
    });
}