$(document).ready(function() {
    function prePopulateAdvancedForm(queryVariables) { 
	for (var i = 0; i < queryVariables.length; i++) {
	    var current = queryVariables[i];
	    var fieldList = current.split("=");
	    var fieldName = fieldList[0];
	    var fieldValue = fieldList[1];
	    if (fieldValue === "none") {
		console.log(fieldName);
	    } else if (fieldValue.length === 0) {
		console.log(fieldName)
	    } else {
		var findingString = "#" + fieldName
		if (fieldName == 'composer-query') {
		  addlString = findingString + " option[value='" + fieldValue + "']"
		  $(addlString).prop('selected', true);
		} else if (fieldName == "item-type-query")  {
		  addlString = findingString + " option[value='" + fieldValue + "']"
		  $(addlString).prop('selected', true);
		} else {
		 $(findingString).val(fieldValue);
		}
	    }
	}
    }

    $("#show-advanced-search").click(function() {
	$("#simple-search").hide();
	$("#show-advanced-search").hide()
	$("#advanced-search").show();
	$("#show-simple-search").show();
    })

    $("#show-simple-search").click(function() {
	$("#advanced-search").hide();
	$("#simple-search").show();
	$("#show-simple-search").hide()
	$("#show-advanced-search").show();
    })
    var query = window.location.search;
    var simple_search_form = $("#simple-search");
    var advanced_search_form = $("#advanced-search");
    if (query !== "") {
    	var vars = query.split("?")[1].split("&");
    	firstVar = vars[0];
	firstVarProperty = firstVar.split("=")[0];
	if (firstVarProperty == 'query') {
	    advanced_search_form.hide();	
	    $("[id='query']").val(firstVar.split("=")[1]);
	} else {
	    simple_search_form.hide();
	    prePopulateAdvancedForm(vars)

	}
    } else {
	advanced_search_form.hide();
	$("#show-simple-search").hide();
    }
})
