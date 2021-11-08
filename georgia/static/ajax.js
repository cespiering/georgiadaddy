
// CHANGE DROPDOWN SELECTORS
function showOptions(evt) {
    evt.preventDefault();
  
    //url is flask route endpoint
    const url = '/branch.json';
    //formData is branch value : All, E, J, L
    const formData = {branch: $('#branch').val()};
    //sends info to flask, gets back a response
    $.get(url, formData, (response) => {
      for (const id in response["hide"]) {
        $(`${id}`).hide();
      };
      for (const id in response["n_values"]) {
        $(`${id}`).val("None");
      };
      for (const id in response["show"]) {
        $(`${id}`).show();
      };
    });
  }    
    // TODO: request weather with that URL and show the forecast in #weather-info
  
    
  $('#branch').on('change', showOptions);
  