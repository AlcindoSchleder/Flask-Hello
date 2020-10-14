/**
 * Manipulação dos eventos da página principal
 *
 * @version    1.0.0
 * @author     Alcindo Schleder <alcindo.schleder@amcom.com.br>
 *
 */

var IndexEvents = function () {

    var documentEvents = function () {
    };

    return {
        //main function to initiate the module
        init: function () {
            documentEvents();
        },
    };

}();

$(document).ready(function() {
    IndexEvents.init(); // starting home page events
});
