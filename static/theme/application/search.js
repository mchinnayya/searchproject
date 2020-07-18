// Class definition
var KTSelect2 = function () {
  var base_url = window.location.origin;

  // Private functions
  var select2_remote = function () {
    $('.kt_select2').select2({
      placeholder: "--------------"
    });

    function formatRepo(repo) {
      // console.log('i am calling');
      console.log(repo);
      if (repo.loading) return repo.text;
      if (repo.loading) return repo.text;
      var markup = "<div class='select2-result-repository clearfix'>" +
        "<div class='select2-result-repository__meta'>" +
        "<div class='select2-result-repository__title'>" + repo.text + "</div>";
      markup += "</div>";
      return markup;
    }

    function formatRepoSelection(repo) {
      $('#text_search_input').val(repo.id);
      return repo.text;
    }

    $("#emergency_details_search").select2({
      placeholder: "Search emergency details",
      allowClear: true,
      ajax: {
        url: base_url + "/emergency-details-search",
        type: "GET",
        delay: 250,
        data: function (params) {
          return {
            q: params.term, // search term
            page: params.page
          };
        },
        processResults: function (data, params) {
          // parse the results into the format expected by Select2
          // since we are using custom formatting functions we do not need to
          // alter the remote JSON data, except to indicate that infinite
          // scrolling can be used
          params.page = params.page || 1;

          return {
            results: $.map(data, function (obj) {
              return {
                id: obj.id,
                result: obj,
                text: "Name: " + obj.fields.emergency_name  + " ( Code: " + obj.fields.emergency_code + " )"
              };
            })
          };
        },
        cache: false
      },
      escapeMarkup: function (markup) {
        return markup;
      }, // let our custom formatter work
      minimumInputLength: 2,
      templateResult: formatRepo, // omitted for brevity, see the source of this page
      templateSelection: formatRepoSelection // omitted for brevity, see the source of this page
    });
  }
  // Public functions
  return {
    init: function () {
      select2_remote();
    }
  };
}();

// Initialization
jQuery(document).ready(function () {
  KTSelect2.init();
});